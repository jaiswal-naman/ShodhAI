# 🔬 ShodhAI — Autonomous Research Report Generator

**ShodhAI** (शोध = Research in Hindi) is an AI-powered platform that autonomously generates comprehensive research reports on any topic. It leverages multiple AI analyst personas that conduct interviews, perform web research, and collaboratively produce structured, downloadable reports.

## ✨ Features

- **Multi-Analyst Architecture** — Generates diverse analyst personas (e.g., technical, ethical, business) to cover different angles of a topic
- **LangGraph-Powered Workflow** — Stateful, multi-step pipeline with human-in-the-loop feedback
- **Web Research Integration** — Tavily-powered search for real-time web data gathering
- **Human Feedback Loop** — Review and refine AI-generated analyst perspectives before report generation
- **Multi-Format Export** — Download reports as DOCX or PDF
- **User Authentication** — Secure signup/login with bcrypt password hashing
- **Structured Logging** — JSON-based structured logging with Structlog
- **Docker & CI/CD Ready** — Dockerfile, Jenkinsfile, and Azure deployment scripts included

## 🏗️ Architecture

```
ShodhAI/
├── research_and_analyst/          # Core application package
│   ├── api/                       # FastAPI server, routes, templates
│   ├── workflows/                 # LangGraph report generation pipeline
│   ├── schemas/                   # Pydantic models & state definitions
│   ├── config/                    # YAML-based LLM provider configs
│   ├── utils/                     # Model & config loaders
│   ├── prompt_lib/                # Jinja2 prompt templates
│   ├── database/                  # SQLAlchemy user auth
│   ├── logger/                    # Structlog custom logger
│   └── exception/                 # Custom exception handling
├── static/                        # CSS assets
├── generated_report/              # Output reports (auto-generated)
└── Dockerfile                     # Container deployment
```

## 🔄 How It Works

1. **User submits a topic** via the web dashboard
2. **AI creates analyst personas** tailored to the topic
3. **Human reviews** and optionally provides feedback on the analysts
4. **Each analyst conducts an interview** with an AI expert, backed by web research
5. **Sections are compiled** into introduction, body, and conclusion
6. **Final report** is assembled and exported as DOCX + PDF

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- API keys for at least one LLM provider (OpenAI / Google Gemini / Groq)
- Tavily API key for web search

### Setup

```bash
# Clone the repo
git clone https://github.com/jaiswal-naman/ShodhAI.git
cd ShodhAI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: .\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.copy .env
# Edit .env and add your API keys
```

### Run

```bash
uvicorn research_and_analyst.api.main:app --reload
```

Visit `http://localhost:8000` to access the dashboard.

## ⚙️ Configuration

### Environment Variables (`.env`)

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Groq API key (for DeepSeek/Llama models) |
| `GOOGLE_API_KEY` | Google API key (for Gemini models) |
| `OPENAI_API_KEY` | OpenAI API key (for GPT models) |
| `TAVILY_API_KEY` | Tavily API key (for web search) |
| `LLM_PROVIDER` | Which provider to use: `openai`, `google`, or `groq` (default: `openai`) |

### LLM Provider Config (`research_and_analyst/config/configuration.yaml`)

Supports multiple providers:
- **Groq**: `deepseek-r1-distill-llama-70b`
- **Google**: `gemini-2.0-flash`
- **OpenAI**: `gpt-4o`

## 🐳 Docker

```bash
docker build -t shodhai .
docker run -p 8000:8000 --env-file .env shodhai
```

## 📄 License

MIT License

## 👤 Author

**Naman Jaiswal** — [GitHub](https://github.com/jaiswal-naman)