<div align="center">

# 🔬 ShodhAI

### *Autonomous AI Research Report Generation Platform*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-Stateful_AI-FF6B35?style=for-the-badge)](https://langchain-ai.github.io/langgraph/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Azure](https://img.shields.io/badge/Azure-Deployable-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)](https://azure.microsoft.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

**ShodhAI** (शोध = *Research* in Hindi) is a full-stack AI platform that autonomously generates comprehensive, publication-ready research reports on any topic — powered by multi-agent orchestration, real-time web research, and human-in-the-loop refinement.

[Features](#-key-features) · [Architecture](#-system-architecture) · [Demo](#-how-it-works) · [Setup](#-getting-started) · [Deployment](#-deployment)

</div>

---

## 🎯 The Problem

Researching a topic deeply takes hours — reading multiple sources, cross-referencing information, synthesizing insights, and structuring everything into a coherent report. Traditional tools just assist with search; they don't actually *think*, *analyze*, or *write* for you.

## 💡 The Solution

**ShodhAI** automates the entire research lifecycle. It doesn't just search — it deploys a team of AI analyst personas that each approach the topic from a different angle, conduct structured interviews backed by real-time web data, and collaboratively produce a multi-section research report with proper citations. The result is a downloadable, publication-ready document in DOCX or PDF format.

---

## ✨ Key Features

### 🤖 Multi-Agent Research Pipeline
- Dynamically generates **diverse AI analyst personas** (technical, ethical, business, policy, etc.) tailored to each topic
- Each analyst independently conducts a structured interview with an AI expert, asking probing questions from their unique perspective
- Parallel execution ensures comprehensive coverage of the topic

### 🌐 Real-Time Web Research
- Integrated with **Tavily Search API** for real-time web data retrieval
- AI agents autonomously formulate search queries based on interview context
- Sources are cited and traceable throughout the final report

### 🧠 LangGraph-Powered Orchestration
- Built on **LangGraph** — a stateful, graph-based AI workflow engine
- Complex DAG (Directed Acyclic Graph) with conditional edges, parallel branches, and interrupt points
- Full state persistence with checkpointing for resumable workflows

### 👤 Human-in-the-Loop Refinement
- After AI generates analyst personas, the user can provide **real-time feedback** to refine perspectives
- Interrupt-resume architecture allows the pipeline to pause, accept input, and continue seamlessly
- Iterative refinement until the user is satisfied with the research direction

### 📄 Multi-Format Export
- Reports automatically exported as both **DOCX** and **PDF**
- Structured with proper headings, sections, introduction, conclusion, and source citations
- Smart text wrapping, centered layout, and page management for PDF output

### 🔐 User Authentication System
- Secure **signup/login** with bcrypt password hashing
- Session-based authentication with cookie management
- SQLAlchemy ORM with SQLite for user data persistence

### 🎨 Clean Web Interface
- Responsive **FastAPI + Jinja2** web UI with glassmorphism-inspired design
- Real-time loading spinners during report generation
- Password visibility toggle, form validation, and download buttons
- Gradient backgrounds with smooth fade-in animations

### 📊 Structured Logging & Error Handling
- **Structlog** JSON-based structured logging (console + file)
- Custom exception hierarchy with full traceback capture
- Timestamped log files for audit trails

### 🐳 Production-Ready Infrastructure
- Multi-stage **Dockerfile** for optimized container images
- **Jenkinsfile** CI/CD pipeline for automated testing and deployment
- **Azure Container Apps** deployment with secrets management
- Health check endpoint for container orchestration

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        ShodhAI Platform                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐    ┌──────────────┐    ┌───────────────────────┐ │
│  │  Web UI   │───▸│  FastAPI      │───▸│  Report Service       │ │
│  │ (Jinja2)  │    │  Routes       │    │  (Orchestrator)       │ │
│  └──────────┘    └──────────────┘    └───────────┬───────────┘ │
│                                                   │             │
│                            ┌──────────────────────▼──────────┐ │
│                            │     LangGraph Workflow Engine     │ │
│                            │                                  │ │
│  ┌─────────────────────────┼──────────────────────────────┐  │ │
│  │                         │                              │  │ │
│  │  ┌──────────────┐  ┌───▼──────────┐  ┌────────────┐  │  │ │
│  │  │ Create       │  │  Human       │  │ Initiate   │  │  │ │
│  │  │ Analysts     │─▸│  Feedback    │─▸│ Interviews │  │  │ │
│  │  └──────────────┘  │  (Interrupt) │  └─────┬──────┘  │  │ │
│  │                    └──────────────┘        │         │  │ │
│  │                                    ┌───────┼───────┐ │  │ │
│  │                                    │       │       │ │  │ │
│  │                              ┌─────▼─┐ ┌──▼──┐ ┌──▼─┐│  │ │
│  │                              │Analyst│ │Ana. │ │Ana.││  │ │
│  │                              │  #1   │ │ #2  │ │ #3 ││  │ │
│  │                              └───┬───┘ └──┬──┘ └──┬─┘│  │ │
│  │                                  │        │       │  │  │ │
│  │                    ┌─────────────▼────────▼───────▼┐ │  │ │
│  │                    │  Interview Sub-Graph (each)    │ │  │ │
│  │                    │                               │ │  │ │
│  │                    │  Ask Question ──▸ Web Search   │ │  │ │
│  │                    │       │              │         │ │  │ │
│  │                    │       ◂── Generate Answer ◂──  │ │  │ │
│  │                    │       │                        │ │  │ │
│  │                    │  Save Interview ──▸ Write      │ │  │ │
│  │                    │                    Section     │ │  │ │
│  │                    └───────────────────────┬───────┘ │  │ │
│  │                                            │         │  │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────▼───────┐ │  │ │
│  │  │ Write        │  │ Write        │  │ Write      │ │  │ │
│  │  │ Introduction │  │ Conclusion   │  │ Report     │ │  │ │
│  │  └──────┬───────┘  └──────┬───────┘  └────┬───────┘ │  │ │
│  │         │                 │               │         │  │ │
│  │         └─────────────────┼───────────────┘         │  │ │
│  │                           │                         │  │ │
│  │                    ┌──────▼───────┐                  │  │ │
│  │                    │  Finalize    │                  │  │ │
│  │                    │  Report      │                  │  │ │
│  │                    └──────┬───────┘                  │  │ │
│  │                           │                         │  │ │
│  └───────────────────────────┼─────────────────────────┘  │ │
│                              │                            │ │
│                    ┌─────────▼──────────┐                 │ │
│                    │  Export Engine      │                 │ │
│                    │  DOCX + PDF         │                 │ │
│                    └────────────────────┘                  │ │
│                                                           │ │
└───────────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────────┐ │
│  │ SQLAlchemy  │  │ Structlog    │  │ Tavily Web Search   │ │
│  │ User Auth   │  │ JSON Logger  │  │ Real-time Data      │ │
│  └────────────┘  └──────────────┘  └─────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 How It Works

```
User enters topic    AI creates 3+ analyst     User reviews &        Each analyst conducts
 "Impact of LLMs"  ──▸  personas with unique  ──▸  provides feedback  ──▸  independent interview
                        perspectives               on analysts            backed by web search
                                                                              │
    ┌─────────────────────────────────────────────────────────────────────────┘
    │
    ▼
Sections compiled    Introduction & conclusion     Final report         Download as
into unified body ◂── generated in parallel    ◂── assembled with  ──▸  DOCX + PDF
                                                    citations
```

**Step 1:** User submits a research topic through the web dashboard

**Step 2:** The system generates 3+ AI analyst personas, each with a unique affiliation, role, and research focus (e.g., a technical researcher, an ethics analyst, a business strategist)

**Step 3:** User can review the analysts and provide feedback to refine their perspectives (human-in-the-loop)

**Step 4:** Each analyst independently interviews an AI expert — asking follow-up questions, performing web searches via Tavily, and gathering cited information

**Step 5:** Each analyst writes a report section from their interview findings

**Step 6:** The system compiles all sections, generates an introduction and conclusion in parallel, and assembles the final report

**Step 7:** The completed report is exported as both DOCX and PDF, ready for download

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **AI Orchestration** | LangGraph | Stateful multi-agent workflow with checkpointing |
| **LLM Providers** | OpenAI GPT-4o / Google Gemini / Groq | Flexible multi-provider LLM support |
| **Web Search** | Tavily API | Real-time web research with source attribution |
| **Backend** | FastAPI + Uvicorn | High-performance async API server |
| **Frontend** | Jinja2 + Vanilla CSS + JS | Server-rendered responsive web UI |
| **Database** | SQLAlchemy + SQLite | User authentication & session management |
| **Security** | bcrypt + Passlib | Password hashing & verification |
| **Document Export** | python-docx + ReportLab | DOCX and PDF report generation |
| **Logging** | Structlog | JSON-structured logging with file persistence |
| **Containerization** | Docker (multi-stage) | Optimized production container images |
| **CI/CD** | Jenkins | Automated build, test, and deployment pipeline |
| **Cloud** | Azure Container Apps | Scalable serverless container deployment |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- API keys for at least one LLM provider
- Tavily API key for web search

### Installation

```bash
# Clone the repository
git clone https://github.com/jaiswal-naman/ShodhAI.git
cd ShodhAI

# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate        # Windows
# source venv/bin/activate     # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Configuration

```bash
# Copy the environment template
cp .env.copy .env
```

Edit `.env` with your API keys:

```env
GROQ_API_KEY=your_groq_key_here
GOOGLE_API_KEY=your_google_key_here
OPENAI_API_KEY=your_openai_key_here
TAVILY_API_KEY=your_tavily_key_here
LLM_PROVIDER=openai    # Options: openai, google, groq
```

### Run

```bash
uvicorn research_and_analyst.api.main:app --reload
```

Visit **http://localhost:8000** → Sign up → Enter a topic → Get your AI-generated report!

---

## 🐳 Deployment

### Docker

```bash
docker build -t shodhai .
docker run -p 8000:8000 --env-file .env shodhai
```

### Azure Container Apps

```bash
# 1. Setup infrastructure
./setup-app-infrastructure.sh

# 2. Build and push Docker image
./build-and-push-docker-image.sh

# 3. Deploy via Jenkins pipeline (or manually)
```

---

## 📁 Project Structure

```
ShodhAI/
├── research_and_analyst/              # Core application package
│   ├── api/
│   │   ├── main.py                    # FastAPI app initialization & CORS
│   │   ├── routes/report_routes.py    # Auth + report generation endpoints
│   │   ├── services/report_service.py # Business logic & workflow orchestration
│   │   └── templates/                 # Jinja2 HTML templates (4 pages)
│   ├── workflows/
│   │   ├── report_generator_workflow.py  # Main LangGraph DAG (7 nodes)
│   │   └── interview_workflow.py         # Interview sub-graph (5 nodes)
│   ├── schemas/models.py              # Pydantic models & TypedDict states
│   ├── config/configuration.yaml      # Multi-provider LLM configuration
│   ├── utils/
│   │   ├── model_loader.py            # Dynamic LLM/embedding factory
│   │   └── config_loader.py           # YAML config with env override
│   ├── prompt_lib/prompt_locator.py   # 6 Jinja2 prompt templates
│   ├── database/db_config.py          # SQLAlchemy models & auth helpers
│   ├── logger/                        # Structlog JSON logger
│   └── exception/                     # Custom exception with traceback
├── static/css/styles.css              # UI styling
├── Dockerfile                         # Multi-stage production build
├── Dockerfile.jenkins                 # Jenkins CI server image
├── Jenkinsfile                        # Full CI/CD pipeline
├── azure-deploy-jenkins.sh            # Jenkins Azure deployment
├── setup-app-infrastructure.sh        # Azure infra provisioning
└── build-and-push-docker-image.sh     # Docker build & ACR push
```

---

## 🔮 Future Roadmap

- [ ] RAG integration for document-based research (PDF/URL upload)
- [ ] Streaming response for real-time report generation progress
- [ ] Multi-language report generation
- [ ] Research history dashboard with saved reports
- [ ] Collaborative research sessions with multiple users
- [ ] Advanced analytics on research quality and source diversity

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ by [Naman Jaiswal](https://github.com/jaiswal-naman)**

*ShodhAI — Because research should be intelligent, autonomous, and effortless.*

</div>