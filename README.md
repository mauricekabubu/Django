# Django Projects 🐍⚡

> A progressive collection of Django projects — from fundamentals and traditional server-rendered applications to production-ready APIs, distributed systems, and AI-powered applications.

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![REST API](https://img.shields.io/badge/REST%20API-FF6B35?style=for-the-badge)
![OAuth](https://img.shields.io/badge/OAuth-4285F4?style=for-the-badge)

## 🚀 About

This repository is my **Django engineering journey**, organized as a progression from beginner-level applications to increasingly complex systems.

Rather than treating Django as a collection of tutorials, each project is built to explore a specific layer of modern web engineering:

```text
Django Fundamentals
        ↓
Server-Side Applications
        ↓
Authentication & Authorization
        ↓
Database Architecture
        ↓
REST APIs
        ↓
PostgreSQL
        ↓
Caching & Background Jobs
        ↓
Async & Real-Time Systems
        ↓
Production Architecture
        ↓
AI-Powered Applications
```

The goal is not simply to build applications that work.

The goal is to understand **why they work, how they scale, how they fail, and how to architect them properly.**

---

# 🧭 Project Roadmap

Projects are intentionally organized from **simple → intermediate → advanced → complex**.

| # | Project | Level | Focus |
|---|---|---|---|
| 01 | 📚 Bookshelf | Beginner → Intermediate | Django fundamentals, authentication, OAuth, sessions |
| 02 | 📝 Blog Platform | Intermediate | Models, relationships, permissions, content management |
| 03 | 🛒 E-Commerce Platform | Intermediate | Transactions, carts, orders, payments |
| 04 | 🎓 School Management System | Advanced | Complex domain architecture, RBAC, APIs, reporting |
| 05 | 💬 Real-Time Application | Advanced | WebSockets, Channels, async communication |
| 06 | 🤖 AI-Powered Platform | Advanced → Complex | LLMs, agents, tools, memory, automation |
| 07 | ⚙️ Distributed Django System | Complex | Microservices, queues, caching, observability |

> Projects may be added, redesigned, or replaced as the architecture evolves.

---

# 📚 01 — Bookshelf

The first major project in the repository is a **Bookshelf web application**.

It started from Django fundamentals but has evolved beyond a basic CRUD application.

### Current concepts

- Django project/app architecture
- Models and database relationships
- Django ORM
- URL routing
- Function/class-based views
- Templates
- Static files
- Media uploads
- Sessions
- Authentication
- Authorization
- OAuth authentication
- Admin interface
- Form handling
- Testing

### Architecture

```text
Browser
   │
   ▼
Django URLs
   │
   ▼
Views
   │
   ├── Authentication
   ├── Books
   └── Application Logic
   │
   ▼
Django ORM
   │
   ▼
Database
```

The Bookshelf project represents the transition from **learning Django syntax** to understanding Django as a web application framework.

---

# 🧱 Engineering Principles

Every project in this repository is built around progressively stronger engineering principles.

### Separation of concerns

Applications should have clear boundaries between:

```text
Presentation
    ↓
Application Logic
    ↓
Domain Logic
    ↓
Data Access
    ↓
Infrastructure
```

### Security first

Authentication is only one part of application security.

Projects progressively explore:

- Authentication
- Authorization
- RBAC
- CSRF protection
- CORS
- Secure sessions
- OAuth 2.0
- Secrets management
- Input validation
- Rate limiting
- Secure API design

### Database engineering

As complexity increases, projects move from basic ORM usage toward:

- PostgreSQL
- Foreign keys
- Constraints
- Transactions
- Indexing
- Query optimization
- Aggregations
- Database migrations
- Connection pooling

### API architecture

Later projects transition from traditional server-rendered applications toward API-driven systems:

```text
Frontend
   │
   │ HTTP / JSON
   ▼
Django REST API
   │
   ├── Authentication
   ├── Business Logic
   ├── Validation
   └── Permissions
   │
   ▼
PostgreSQL
```

---

# ⚡ Advanced Stack

As the repository progresses, technologies are introduced according to the problems they solve.

### Backend

- Python
- Django
- Django REST Framework
- Django Channels
- Celery
- Redis

### Databases

- PostgreSQL
- SQLite for lightweight development/testing

### Authentication

- Django Authentication
- Sessions
- OAuth 2.0
- Token-based authentication
- JWT where appropriate

### Infrastructure

- Docker
- Nginx
- Linux
- CI/CD
- Cloud deployment

### APIs & Communication

- REST
- WebSockets
- JSON
- HTTP
- Webhooks

### AI Systems

Advanced projects may incorporate:

- Large Language Models
- AI agents
- Tool calling
- Retrieval systems
- Vector databases
- Conversation memory
- Autonomous workflows
- Database-aware agents

---

# 🤖 AI + Django

One of the later goals of this repository is exploring Django as the backend infrastructure for **AI-powered systems**.

Instead of treating AI as a simple chatbot endpoint:

```text
User → LLM → Response
```

the architecture can evolve toward:

```text
                    ┌───────────────┐
                    │      LLM      │
                    └───────┬───────┘
                            │
                      Tool Calling
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
          Database        Email        Reports
              │             │             │
              └─────────────┼─────────────┘
                            ▼
                       Django API
                            │
                            ▼
                           User
```

This explores the intersection of:

**Web Engineering × Backend Systems × AI Automation**

---

# 🧪 Testing

Testing becomes increasingly important as project complexity grows.

The repository explores:

- Unit tests
- Integration tests
- API tests
- Authentication tests
- Database tests
- Permission tests
- Regression testing

The objective is to move from:

> "It works on my machine."

to:

> "The system has automated evidence that it works."

---

# 🐳 Deployment & Infrastructure

Later projects will progressively introduce production infrastructure.

```text
                    Internet
                       │
                       ▼
                    Nginx
                       │
                       ▼
                 Django / ASGI
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      PostgreSQL     Redis        Celery
          │                         │
          │                         ▼
          │                    Background Jobs
          │
          ▼
       Persistent Data
```

Deployment concepts include:

- Environment variables
- Docker
- Reverse proxies
- WSGI / ASGI
- PostgreSQL
- Redis
- Background workers
- Logging
- Monitoring
- CI/CD
- Cloud hosting

---

# 📈 Learning Progression

The repository intentionally follows an increasing complexity curve.

### 🟢 Beginner

Learn Django itself.

```text
Models
Views
URLs
Templates
Forms
Admin
ORM
Static Files
```

### 🟡 Intermediate

Build complete web applications.

```text
Authentication
OAuth
Permissions
Relationships
PostgreSQL
REST APIs
Testing
```

### 🟠 Advanced

Solve real engineering problems.

```text
Caching
Background Tasks
Redis
Celery
WebSockets
Async Django
API Architecture
Security
Docker
```

### 🔴 Complex

Build systems rather than pages.

```text
Distributed Systems
AI Agents
Tool Calling
Event-Driven Architecture
Observability
Scalability
Fault Tolerance
Cloud Infrastructure
```

---

# 🗂️ Repository Structure

Each major application is kept isolated so that projects can evolve independently.

```text
django-projects/
│
├── 01-bookshelf/
│   ├── manage.py
│   ├── config/
│   ├── books/
│   ├── templates/
│   ├── static/
│   ├── media/
│   ├── requirements.txt
│   └── README.md
│
├── 02-blog/
│   └── ...
│
├── 03-ecommerce/
│   └── ...
│
├── 04-school-management/
│   └── ...
│
└── 05-ai-platform/
    └── ...
```

Each project is effectively its own Django environment while sharing the same repository as a **Django engineering laboratory**.

---

# 🎯 Purpose

This repository exists to document a progression:

> **From writing Django applications to engineering backend systems.**

The projects are not designed purely to demonstrate how many technologies can be used.

Each technology should answer a real engineering question:

- Why PostgreSQL instead of SQLite?
- When should Redis be introduced?
- When does Celery become necessary?
- Why use ASGI?
- When are WebSockets justified?
- How should authentication be designed?
- How should APIs be structured?
- How do background jobs interact with the database?
- How can AI safely interact with application data?
- What happens when the system starts scaling?

---

# 🛠️ Development Philosophy

```text
Build
  ↓
Break
  ↓
Debug
  ↓
Understand
  ↓
Refactor
  ↓
Test
  ↓
Deploy
  ↓
Scale
```

Every failure is part of the engineering process.

The objective is not to avoid complexity.

It is to **earn the ability to handle it.**

---

# 📌 Status

🚧 **Actively evolving**

This repository will continue growing as new Django concepts, architectures, and technologies are explored.

The projects are intentionally developed in stages, so the repository represents an evolving record of Django and backend engineering experience.

---

# 👨‍💻 Author

**Maurice Kabubu**

Backend-focused developer exploring:

```text
Python
Django
APIs
PostgreSQL
Cloud
DevOps
AI Automation
Distributed Systems
```

> **From MVP to Global.**
