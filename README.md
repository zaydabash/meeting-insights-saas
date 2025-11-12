# Meeting Insights SaaS

```
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║                    MEETING INSIGHTS SAAS                              ║
║                                                                       ║
║     Production-ready B2B platform for meeting intelligence            ║
║                                                                       ║
║     Swift iOS • FastAPI • React • PostgreSQL • Redis                  ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

A production-ready B2B SaaS platform for capturing, transcribing, and extracting insights from meetings. Built with Swift iOS, FastAPI, and React.

---

## Table of Contents

```
┌─────────────────────────────────────────────────────────────────────┐
│  [Architecture]  [Features]  [Quick Start]  [API Docs]  [Deploy]  │
└─────────────────────────────────────────────────────────────────────┘
```

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────┐
│ Meeting Insights Platform │
└─────────────────────────────────────────────────┘
│
┌─────────────────┼─────────────────┐
│ │ │
┌───────▼──────┐ ┌───────▼──────┐ ┌───────▼──────┐
│ iOS App │ │ Admin Web │ │ API Gateway │
│ (SwiftUI) │ │ (React) │ │ (Nginx) │
└───────┬──────┘ └───────┬──────┘ └───────┬──────┘
│ │ │
└─────────────────┼─────────────────┘
│
┌─────────▼─────────┐
│ FastAPI Backend │
│ (Python 3.11) │
└─────────┬─────────┘
│
┌─────────────────────────────┼─────────────────────────────┐
│ │ │
┌───────▼────────┐ ┌────────▼────────┐ ┌───────▼────────┐
│ PostgreSQL │ │ Redis │ │ Celery Worker │
│ (Database) │ │ (Cache/Queue) │ │ (Async Jobs) │
└─────────────────┘ └────────────────┘ └────────────────┘
│
┌───────▼────────┐
│ MinIO │
│ (S3 Storage) │
└─────────────────┘
```

### Data Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│ Meeting Processing Flow │
└─────────────────────────────────────────────────────────────────────┘

1. Capture
┌─────────┐
│ iOS App │ ──► Upload Audio ──► ┌──────────┐
└─────────┘ │ API │
└────┬─────┘
│
2. Storage │
┌──────────┐ │
│ MinIO │ ◄─── Store Audio ───────┘
└──────────┘

3. Processing
┌──────────┐ ┌──────────────┐
│ API │ ──► Queue Job ──────────►│ Worker │
└──────────┘ └──────┬───────┘
│
4. Transcription │
┌──────────┐ │
│ Whisper │ ◄─── Transcribe Audio ─────────┘
└────┬─────┘
│
5. NLP Extraction
┌──────────────┐
│ LLM Provider │ ◄─── Extract Insights ─────┐
│ (OpenAI/ │ │
│ Anthropic/ │ │
│ Mock) │ │
└──────┬───────┘ │
│ │
6. Storage │
┌──────────┐ │
│PostgreSQL│ ◄─── Save Insights ────────────┘
└──────────┘

7. Real-time Updates
┌──────────┐ ┌──────────┐ ┌──────────┐
│ Worker │ ────►│ Redis │ ────►│ WebSocket│ ────► iOS/Admin
└──────────┘ └──────────┘ └──────────┘
```

### Component Interaction

```
┌──────────────────────────────────────────────────────────────────┐
│ Request Flow Example │
└──────────────────────────────────────────────────────────────────┘

Client API Gateway Backend
│ │ │
│── POST /meetings/upload ──►│ │
│ │───► FastAPI │
│ │ Router │
│ │ │──► Validate
│ │ │──► Upload to S3
│ │ │──► Create Meeting
│ │ │──► Queue Job
│ │◄─── Response │
│◄─── 201 Created ───────────│ │
│ │ │
│ │ │──► Worker picks job
│ │ │──► Transcribe
│ │ │──► Extract Insights
│ │ │──► Save to DB
│ │ │──► Emit WebSocket
│ │ │
│◄─── WebSocket Update ──────│◄──────────────────────│
```

## Features

### Core Capabilities

```
╔═══════════════════════════════════════════════════════════════════════╗
║                         FEATURE MATRIX                                 ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  ┌─────────────────────┬─────────────────────────────────────────┐ ║
║  │ Audio Capture       │ [✓] iOS Recording                        │ ║
║  │                     │ [✓] Background Upload                    │ ║
║  │                     │ [✓] Resume/Retry                         │ ║
║  ├─────────────────────┼─────────────────────────────────────────┤ ║
║  │ Transcription       │ [✓] Real-time Streaming                  │ ║
║  │                     │ [✓] Server-side Whisper                 │ ║
║  │                     │ [✓] On-device Fallback                  │ ║
║  ├─────────────────────┼─────────────────────────────────────────┤ ║
║  │ NLP Extraction      │ [✓] Action Items                        │ ║
║  │                     │ [✓] Decisions                           │ ║
║  │                     │ [✓] Sentiment Analysis                 │ ║
║  │                     │ [✓] Meeting Summary                    │ ║
║  │                     │ [✓] Topic Detection                    │ ║
║  ├─────────────────────┼─────────────────────────────────────────┤ ║
║  │ Security & Privacy  │ [✓] PII Redaction                       │ ║
║  │                     │ [✓] Reversible Vault                    │ ║
║  │                     │ [✓] JWT Authentication                 │ ║
║  │                     │ [✓] Multi-tenant Isolation             │ ║
║  ├─────────────────────┼─────────────────────────────────────────┤ ║
║  │ Analytics           │ [✓] Usage Metering                     │ ║
║  │                     │ [✓] Cost Tracking                      │ ║
║  │                     │ [✓] Provider Performance               │ ║
║  ├─────────────────────┼─────────────────────────────────────────┤ ║
║  │ Integrations        │ [✓] Slack Notifications                 │ ║
║  │                     │ [✓] Jira Task Creation                 │ ║
║  │                     │ [✓] Calendar Linking                   │ ║
║  └─────────────────────┴─────────────────────────────────────────┘ ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Admin Web App

```
╔═══════════════════════════════════════════════════════════════════════╗
║                      ADMIN DASHBOARD                                  ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │  DASHBOARD METRICS                                               │ ║
║  ├─────────────────────────────────────────────────────────────────┤ ║
║  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │ ║
║  │  │ Meetings     │  │ Open Tasks   │  │ Cost         │         │ ║
║  │  │ 12 / month   │  │ 8            │  │ $45.20       │         │ ║
║  │  └──────────────┘  └──────────────┘  └──────────────┘         │ ║
║  │  ┌──────────────┐                                              │ ║
║  │  │ Usage        │                                              │ ║
║  │  │ 120 min      │                                              │ ║
║  │  └──────────────┘                                              │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │  MEETINGS BROWSER                                                │ ║
║  ├─────────────────────────────────────────────────────────────────┤ ║
║  │  [Q4 Planning Meeting]    [Processed]    [2024-01-15]          │ ║
║  │  [Team Standup]           [Processed]    [2024-01-14]          │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │  TASK KANBAN                                                     │ ║
║  ├─────────────────────────────────────────────────────────────────┤ ║
║  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │ ║
║  │  │ OPEN         │  │ IN PROGRESS   │  │ DONE         │         │ ║
║  │  │ ────────────  │  │ ────────────  │  │ ──────────── │         │ ║
║  │  │ • Task 1     │  │ • Task 3     │  │ • Task 5     │         │ ║
║  │  │ • Task 2     │  │ • Task 4     │  │              │         │ ║
║  │  │              │  │              │  │              │         │ ║
║  │  │ [5 tasks]    │  │ [2 tasks]    │  │ [1 task]     │         │ ║
║  │  └──────────────┘  └──────────────┘  └──────────────┘         │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
║  Navigation: [Users] | [Usage & Costs] | [Settings]                 ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### iOS App Features

```
╔═══════════════════════════════════════════════════════════════════════╗
║                      iOS APP STRUCTURE                                 ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │  RECORDING INTERFACE                                              │ ║
║  ├─────────────────────────────────────────────────────────────────┤ ║
║  │  ┌───────────────────────────────────────────────────────────┐  │ ║
║  │  │  [REC] Recording... 00:05:23                              │  │ ║
║  │  │  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │  │ ║
║  │  │  Waveform: ▁▂▃▅▆▇█▇▆▅▃▂▁▁▂▃▅▆▇█▇▆▅▃▂▁                  │  │ ║
║  │  │  [Pause]  [Stop]  [Resume]                                │  │ ║
║  │  └───────────────────────────────────────────────────────────┘  │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │  LIVE TRANSCRIPT                                                  │ ║
║  ├─────────────────────────────────────────────────────────────────┤ ║
║  │  ┌───────────────────────────────────────────────────────────┐  │ ║
║  │  │  Speaker 1: We need to finalize the budget...            │  │ ║
║  │  │  Speaker 2: I'll have it ready by Friday.                │  │ ║
║  │  │                                                           │  │ ║
║  │  │  [NEW INSIGHT] Action Item: Finalize budget             │  │ ║
║  │  │  Owner: John | Due: 2024-01-20                            │  │ ║
║  │  └───────────────────────────────────────────────────────────┘  │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
║  Navigation: [Meeting List] | [Search] | [Settings]                   ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## Quick Start

### Prerequisites

```
╔═══════════════════════════════════════════════════════════════════════╗
║                      REQUIRED TOOLS                                   ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  ┌──────────────────────────────┬─────────────────────────────────┐ ║
║  │ Tool                          │ Version                          │ ║
║  ├──────────────────────────────┼─────────────────────────────────┤ ║
║  │ Docker & Docker Compose        │ v20.10+                          │ ║
║  │ Python                        │ v3.11+                           │ ║
║  │ Node.js                       │ v20+                             │ ║
║  │ PostgreSQL (optional)         │ v15+ (if not using Docker)       │ ║
║  │ Redis (optional)              │ v7+ (if not using Docker)        │ ║
║  └──────────────────────────────┴─────────────────────────────────┘ ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Local Development

#### Step 1: Clone and Setup

```bash
git clone https://github.com/zaydabash/meeting-insights-saas.git
cd meeting-insights-saas
make setup
```

#### Step 2: Start All Services

```bash
make dev
```

This starts the complete stack:

```
╔═══════════════════════════════════════════════════════════════════════╗
║                      RUNNING SERVICES                                  ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  ┌──────────────────────┬──────────────────┬──────────────────────┐  ║
║  │ Service              │ Port             │ Purpose              │  ║
║  ├──────────────────────┼──────────────────┼──────────────────────┤  ║
║  │ PostgreSQL           │ localhost:5432   │ Database             │  ║
║  │ Redis                │ localhost:6379   │ Cache/Queue          │  ║
║  │ MinIO API            │ localhost:9000   │ S3 Storage           │  ║
║  │ MinIO Console        │ localhost:9001   │ Storage UI           │  ║
║  │ FastAPI              │ localhost:8000   │ Backend API          │  ║
║  │ React Admin          │ localhost:5173   │ Admin Web App        │  ║
║  │ Nginx                │ localhost:80     │ Reverse Proxy        │  ║
║  └──────────────────────┴──────────────────┴──────────────────────┘  ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

#### Step 3: Initialize Database

```bash
# Run migrations
make migrate

# Seed with demo data
make seed
```

#### Step 4: Access Services

```
╔═══════════════════════════════════════════════════════════════════════╗
║                      SERVICE URLs                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  ┌──────────────────────────┬──────────────────────────────────────┐ ║
║  │ Service                   │ URL                                  │ ║
║  ├──────────────────────────┼──────────────────────────────────────┤ ║
║  │ Admin Dashboard           │ http://localhost:5173                 │ ║
║  │ API Documentation        │ http://localhost:8000/docs            │ ║
║  │ API Base URL              │ http://localhost:8000/api/v1           │ ║
║  │ MinIO Console             │ http://localhost:9001                  │ ║
║  │                          │ (minioadmin / minioadmin)             │ ║
║  └──────────────────────────┴──────────────────────────────────────┘ ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Demo Credentials

After seeding the database:

```
╔═══════════════════════════════════════════════════════════════════════╗
║                      DEMO ACCOUNTS                                    ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │  ADMIN ACCOUNT                                                   │ ║
║  ├─────────────────────────────────────────────────────────────────┤ ║
║  │  Email:    admin@demo.com                                       │ ║
║  │  Password: demo123                                               │ ║
║  │  Role:     Administrator                                         │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │  MEMBER ACCOUNT                                                  │ ║
║  ├─────────────────────────────────────────────────────────────────┤ ║
║  │  Email:    member@demo.com                                       │ ║
║  │  Password: demo123                                               │ ║
║  │  Role:     Member                                                │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## Environment Variables

See `.env.example` for all configuration options. Key variables:

```bash
# Database
DB_URL=postgresql+psycopg://postgres:postgres@db:5432/meeting_insights

# LLM Provider (mock, openai, anthropic)
LLM_PROVIDER=mock
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here

# Redaction
REDACTION_ENABLED=true

# Integrations
SLACK_BOT_TOKEN=your-token
JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email
JIRA_API_TOKEN=your-token
```

## API Endpoints

### Endpoint Map

```
╔═══════════════════════════════════════════════════════════════════════╗
║                      API STRUCTURE                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  /api/v1/                                                             ║
║  │                                                                    ║
║  ├── auth/                                                            ║
║  │   ├── POST   /register      Register org + user                   ║
║  │   ├── POST   /login         Authenticate                          ║
║  │   └── GET    /me            Current user info                      ║
║  │                                                                    ║
║  ├── meetings/                                                        ║
║  │   ├── POST   /upload        Upload audio file                     ║
║  │   ├── POST   /text          Create from transcript                ║
║  │   ├── GET    /              List (with filters)                   ║
║  │   ├── GET    /{id}          Get details                           ║
║  │   ├── POST   /{id}/process  Queue processing                      ║
║  │   └── WS     /{id}/stream   Real-time updates                     ║
║  │                                                                    ║
║  ├── nlp/                                                            ║
║  │   ├── POST   /extract       Extract insights                      ║
║  │   ├── POST   /redact        Redact PII                            ║
║  │   └── GET    /providers     List LLM providers                    ║
║  │                                                                    ║
║  ├── tasks/                                                           ║
║  │   ├── POST   /              Create task                            ║
║  │   ├── PATCH  /{id}          Update task                           ║
║  │   └── GET    /              List tasks                            ║
║  │                                                                    ║
║  ├── integrations/                                                    ║
║  │   ├── POST   /slack/post     Post to Slack channel                 ║
║  │   └── POST   /jira/create    Create Jira issues                   ║
║  │                                                                    ║
║  └── admin/                                                           ║
║      ├── GET    /org/users      List org users                        ║
║      ├── POST   /org/users      Invite user                           ║
║      ├── GET    /usage          Usage statistics                       ║
║      └── GET    /costs          Cost breakdown                        ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Request/Response Examples

#### Authentication Flow

```
┌─────────┐ ┌─────────┐
│ Client │ │ API │
└────┬────┘ └────┬────┘
│ │
│ POST /auth/register │
│ {org_name, email, password} │
├─────────────────────────────────────────────►
│ │
│ │──► Create Org
│ │──► Create User
│ │──► Generate JWT
│ │
│ 201 Created │
│ {token, user, org} │
◄──────────────────────────────────────────────┤
│ │
│ Store token in localStorage/Keychain │
│ │
```

#### Meeting Processing Flow

```
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ Client │ │ API │ │ Worker │ │ DB │
└────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘
│ │ │ │
│ Upload │ │ │
├───────────► │ │
│ │ │ │
│ │──► Store │ │
│ │──► Create │ │
│ │──► Queue │ │
│ │ │ │
│ 201 Created│ │ │
◄────────────┤ │ │
│ │ │ │
│ │ │──► Pick │
│ │ │──► Process│
│ │ │ │──► Save
│ │ │ │
│ │◄────────────┤ │
│ │ Results │ │
│ │ │ │
│ WebSocket │ │ │
◄────────────┤ │ │
│ Updates │ │ │
│ │ │ │
```

## Project Structure

```
meeting-insights-saas/
│
├── apps/
│ ├── api/ # FastAPI Backend
│ │ ├── app/
│ │ │ ├── api/ # API routers & endpoints
│ │ │ │ ├── v1/ # v1 API routes
│ │ │ │ └── websocket/ # WebSocket handlers
│ │ │ ├── core/ # Core config & utilities
│ │ │ │ ├── config.py # Settings
│ │ │ │ ├── database.py# DB connection
│ │ │ │ └── security.py# Auth & encryption
│ │ │ ├── models/ # SQLAlchemy ORM models
│ │ │ ├── schemas/ # Pydantic request/response
│ │ │ ├── services/ # Business logic layer
│ │ │ │ ├── nlp_provider.py
│ │ │ │ ├── redaction.py
│ │ │ │ └── storage.py
│ │ │ └── workers/ # Celery async tasks
│ │ ├── alembic/ # Database migrations
│ │ └── scripts/ # Utility scripts
│ │
│ ├── admin/ # React Admin Web App
│ │ ├── src/
│ │ │ ├── pages/ # Page components
│ │ │ │ ├── Dashboard.tsx
│ │ │ │ ├── Meetings.tsx
│ │ │ │ ├── Tasks.tsx
│ │ │ │ └── ...
│ │ │ ├── components/ # Reusable components
│ │ │ ├── hooks/ # Custom React hooks
│ │ │ └── lib/ # Utilities & API client
│ │ └── package.json
│ │
│ └── ios/ # Swift iOS App
│ └── MeetingInsights/
│ ├── Views/ # SwiftUI views
│ ├── ViewModels/ # MVVM view models
│ ├── Services/ # API & recording services
│ └── Models/ # Data models
│
├── infra/
│ ├── docker-compose.yml # Local dev stack
│ └── nginx/ # Reverse proxy config
│ └── nginx.conf
│
├── scripts/ # Utility scripts
│ └── eval_fixtures/ # Test data
│
├── .github/
│ └── workflows/ # CI/CD pipelines
│ ├── ci.yml # Tests & linting
│ └── docker.yml # Docker builds
│
├── README.md # This file
├── Makefile # Common commands
└── .gitignore # Git ignore rules
```

### Code Organization

```
┌─────────────────────────────────────────────────────────────┐
│ Layer Architecture │
├─────────────────────────────────────────────────────────────┤
│ │
│ Presentation Layer │
│ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ │
│ │ iOS App │ │ Admin Web │ │ API Docs │ │
│ └──────┬───────┘ └──────┬──────┘ └──────┬──────┘ │
│ │ │ │ │
│ ───────┴──────────────────┴─────────────────┴─────── │
│ │
│ API Layer │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ FastAPI Routers (Auth, Meetings, NLP, Tasks, etc.) │ │
│ └──────────────────────┬──────────────────────────────┘ │
│ │ │
│ Business Logic Layer │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Services (NLP, Redaction, Storage, Usage) │ │
│ └──────────────────────┬──────────────────────────────┘ │
│ │ │
│ Data Layer │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Models (SQLAlchemy) │ Storage (S3/MinIO) │ │
│ └──────────────────────┬──────────────────────────────┘ │
│ │ │
│ ───────────────────────┴─────────────────────────────── │
│ │
│ Infrastructure │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ PostgreSQL │ Redis │ MinIO │ Celery Workers │ │
│ └─────────────────────────────────────────────────────┘ │
│ │
└─────────────────────────────────────────────────────────────┘
```

## Development

### Backend (FastAPI)

```bash
cd apps/api
python -m venv venv
source venv/bin/activate # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Run server
uvicorn app.main:app --reload
```

### Admin (React)

```bash
cd apps/admin
npm install
npm run dev
```

### Running Tests

```bash
# API tests
cd apps/api
pytest

# Admin tests
cd apps/admin
npm test

# All tests
make test
```

## LLM Providers

The system supports multiple LLM providers with automatic routing:

```
╔═══════════════════════════════════════════════════════════════════════╗
║                    PROVIDER COMPARISON                                 ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  ┌──────────────┬──────────────────────┬───────────────────────────┐ ║
║  │ Provider     │ Model                │ Use Case                  │ ║
║  ├──────────────┼──────────────────────┼───────────────────────────┤ ║
║  │ Mock         │ Deterministic        │ Local Dev & Testing       │ ║
║  │              │ (Free)               │                           │ ║
║  ├──────────────┼──────────────────────┼───────────────────────────┤ ║
║  │ OpenAI       │ GPT-4 Turbo          │ Production (Fast)        │ ║
║  │              │ ~$0.01/1K tokens     │                           │ ║
║  ├──────────────┼──────────────────────┼───────────────────────────┤ ║
║  │ Anthropic    │ Claude 3 Opus        │ Production (Quality)      │ ║
║  │              │ ~$0.015/1K tokens     │                           │ ║
║  └──────────────┴──────────────────────┴───────────────────────────┘ ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Provider Selection

```bash
# Use Mock (default - no API key needed)
LLM_PROVIDER=mock

# Use OpenAI
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...

# Use Anthropic
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sk-ant-...
```

### Cost Tracking

```
╔═══════════════════════════════════════════════════════════════════════╗
║                    COST ESTIMATION                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  Each meeting processing automatically tracks:                        ║
║                                                                       ║
║  [*] Input tokens consumed                                            ║
║  [*] Output tokens generated                                          ║
║  [*] Estimated cost per provider                                      ║
║  [*] Latency metrics                                                  ║
║                                                                       ║
║  View costs in Admin → Usage & Costs                                  ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## Redaction

PII redaction is enabled by default. Detects:
- Email addresses
- Phone numbers
- Credit card numbers
- SSNs

Redacted values are stored in a vault with reversible tokens for admin access.

## Integrations

### Slack
1. Create Slack app and bot token
2. Set `SLACK_BOT_TOKEN` environment variable
3. Use `POST /api/v1/integrations/slack/post` endpoint

### Jira
1. Generate API token from Jira account settings
2. Set `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`
3. Use `POST /api/v1/integrations/jira/create` endpoint

## Deployment

### Docker Compose (Production)

1. Update `.env` with production values
2. Set strong `JWT_SECRET`
3. Configure real S3 credentials
4. Run: `docker-compose -f infra/docker-compose.yml up -d`

### Kubernetes (Optional)

Helm charts and Terraform configs can be added for cloud deployment.

## Roadmap

```
╔═══════════════════════════════════════════════════════════════════════╗
║                    FEATURE ROADMAP                                     ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │  Phase 1: MVP (Current)                                         │ ║
║  ├─────────────────────────────────────────────────────────────────┤ ║
║  │  [✓] Core meeting capture & processing                          │ ║
║  │  [✓] Basic NLP extraction                                        │ ║
║  │  [✓] Admin dashboard                                             │ ║
║  │  [✓] Slack/Jira integrations                                     │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │  Phase 2: Enterprise Features                                    │ ║
║  ├─────────────────────────────────────────────────────────────────┤ ║
║  │  [ ] SSO (OIDC/SAML)                                            │ ║
║  │  [ ] SCIM user provisioning                                      │ ║
║  │  [ ] Advanced RBAC                                              │ ║
║  │  [ ] Calendar integrations                                       │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │  Phase 3: Advanced AI                                           │ ║
║  ├─────────────────────────────────────────────────────────────────┤ ║
║  │  [ ] RAG over documents                                          │ ║
║  │  [ ] Multi-language support                                      │ ║
║  │  [ ] Advanced diarization                                        │ ║
║  │  [ ] Eval harness                                                │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │  Phase 4: Scale                                                  │ ║
║  ├─────────────────────────────────────────────────────────────────┤ ║
║  │  [ ] Kubernetes deployment                                       │ ║
║  │  [ ] Multi-region support                                        │ ║
║  │  [ ] Advanced analytics                                          │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## Technology Stack

```
╔═══════════════════════════════════════════════════════════════════════╗
║                    TECH STACK                                          ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │  FRONTEND                                                        │ ║
║  ├─────────────────────────────────────────────────────────────────┤ ║
║  │  React 18      │  TypeScript  │  Tailwind CSS                  │ ║
║  │  Vite          │  TanStack    │  React Router                  │ ║
║  │  Query         │  Recharts    │  Lucide Icons                  │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │  BACKEND                                                         │ ║
║  ├─────────────────────────────────────────────────────────────────┤ ║
║  │  FastAPI       │  SQLAlchemy  │  Pydantic                       │ ║
║  │  Celery        │  Redis       │  Alembic                        │ ║
║  │  Boto3 (S3)    │  WebSockets  │  JWT Auth                       │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │  AI/ML                                                          │ ║
║  ├─────────────────────────────────────────────────────────────────┤ ║
║  │  OpenAI API    │  Anthropic   │  Whisper (ASR)                 │ ║
║  │  Custom NLP    │  Redaction   │  Fuzzy Matching                │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
║  ┌─────────────────────────────────────────────────────────────────┐ ║
║  │  INFRASTRUCTURE                                                 │ ║
║  ├─────────────────────────────────────────────────────────────────┤ ║
║  │  Docker        │  Docker      │  Nginx                          │ ║
║  │  Compose       │  PostgreSQL  │  MinIO (S3)                     │ ║
║  │  Redis         │  GitHub      │  Actions (CI/CD)               │ ║
║  └─────────────────────────────────────────────────────────────────┘ ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Please open an issue or submit a PR.

## Support

For issues and questions:
- Open a [GitHub Issue](https://github.com/zaydabash/meeting-insights-saas/issues)
- Check the [API Documentation](http://localhost:8000/docs) when running locally
- Join our community discussions

---

<div align="center">

**Built for better meeting insights**

[Back to Top](#meeting-insights-saas)

</div>

