import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi.responses import FileResponse, StreamingResponse

try:
    from azure.storage.blob import BlobServiceClient
except Exception:  # pragma: no cover - local dependency may be absent before install
    BlobServiceClient = None


URL_PATTERN = re.compile(r"https?://[^\s)<>\"]+")


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _file_size(path: str | None) -> int:
    if not path or not os.path.exists(path):
        return 0
    return os.path.getsize(path)


def extract_sources(report_text: str) -> list[str]:
    seen = set()
    sources = []
    for match in URL_PATTERN.findall(report_text or ""):
        source = match.rstrip(".,;:")
        if source not in seen:
            sources.append(source)
            seen.add(source)
    return sources


def merge_sources(*source_lists: list[str] | None) -> list[str]:
    seen = set()
    merged = []
    for source_list in source_lists:
        for source in source_list or []:
            cleaned = source.strip().rstrip(".,;:") if source else ""
            if cleaned and cleaned not in seen:
                merged.append(cleaned)
                seen.add(cleaned)
    return merged


class ReportArchive:
    def __init__(self):
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.container_name = os.getenv("AZURE_STORAGE_CONTAINER", "reports")
        self.local_root = Path(os.getcwd()) / "generated_report"
        self._container = None

    @property
    def enabled(self) -> bool:
        return bool(self.connection_string and BlobServiceClient)

    def _container_client(self):
        if not self.enabled:
            return None
        if self._container is None:
            service = BlobServiceClient.from_connection_string(self.connection_string)
            self._container = service.get_container_client(self.container_name)
            if not self._container.exists():
                self._container.create_container()
        return self._container

    def store_report(
        self,
        *,
        topic: str,
        username: str | None,
        final_report: str,
        docx_path: str,
        pdf_path: str,
        sources: list[str] | None = None,
    ) -> dict[str, Any]:
        sources = merge_sources(sources, extract_sources(final_report))
        report_id = Path(docx_path).stem
        metadata = {
            "id": report_id,
            "topic": topic,
            "username": username,
            "created_at": _utc_now(),
            "docx_file": Path(docx_path).name,
            "pdf_file": Path(pdf_path).name,
            "docx_size": _file_size(docx_path),
            "pdf_size": _file_size(pdf_path),
            "sources": sources,
            "source_count": len(sources),
            "preview": final_report,
        }

        container = self._container_client()
        if not container:
            return metadata

        prefix = f"reports/{report_id}"
        self._upload_file(container, f"{prefix}/{metadata['docx_file']}", docx_path)
        self._upload_file(container, f"{prefix}/{metadata['pdf_file']}", pdf_path)
        container.upload_blob(
            f"{prefix}/metadata.json",
            json.dumps(metadata, ensure_ascii=False, indent=2),
            overwrite=True,
            content_type="application/json",
        )
        return metadata

    def _upload_file(self, container, blob_name: str, path: str):
        with open(path, "rb") as handle:
            container.upload_blob(blob_name, handle, overwrite=True)

    def list_reports(self, *, username: str | None = None, limit: int = 6) -> list[dict[str, Any]]:
        container = self._container_client()
        reports = self._list_blob_reports(container, username) if container else self._list_local_reports(username)
        return sorted(reports, key=lambda item: item.get("created_at", ""), reverse=True)[:limit]

    def _list_blob_reports(self, container, username: str | None) -> list[dict[str, Any]]:
        reports = []
        for blob in container.list_blobs(name_starts_with="reports/"):
            if not blob.name.endswith("/metadata.json"):
                continue
            data = container.download_blob(blob.name).readall()
            item = json.loads(data.decode("utf-8"))
            if username and item.get("username") not in (None, username):
                continue
            reports.append(item)
        return reports

    def _list_local_reports(self, username: str | None) -> list[dict[str, Any]]:
        reports = []
        if not self.local_root.exists():
            return reports

        for folder in self.local_root.iterdir():
            if not folder.is_dir():
                continue
            docx = next(folder.glob("*.docx"), None)
            pdf = next(folder.glob("*.pdf"), None)
            if not docx or not pdf:
                continue
            reports.append(
                {
                    "id": folder.name,
                    "topic": folder.name.replace("_", " "),
                    "username": username,
                    "created_at": datetime.fromtimestamp(folder.stat().st_mtime, timezone.utc).isoformat(),
                    "docx_file": docx.name,
                    "pdf_file": pdf.name,
                    "docx_size": _file_size(str(docx)),
                    "pdf_size": _file_size(str(pdf)),
                    "sources": [],
                    "source_count": 0,
                    "preview": "",
                }
            )
        return reports

    def download_file(self, file_name: str):
        local_file = self._find_local_file(file_name)
        if local_file:
            return FileResponse(path=str(local_file), filename=file_name, media_type="application/octet-stream")

        container = self._container_client()
        if not container:
            return None

        for blob in container.list_blobs(name_starts_with="reports/"):
            if blob.name.endswith(f"/{file_name}"):
                stream = container.download_blob(blob.name)
                return StreamingResponse(
                    stream.chunks(),
                    media_type="application/octet-stream",
                    headers={"Content-Disposition": f'attachment; filename="{file_name}"'},
                )
        return None

    def _find_local_file(self, file_name: str) -> Path | None:
        if not self.local_root.exists():
            return None
        for path in self.local_root.rglob(file_name):
            if path.is_file():
                return path
        return None
