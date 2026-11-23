<p align="center">
  <img src="docs/design/brand/club-mark-480.webp" alt="Code2Chill Logo" width="160" />
</p>

<h1 align="center">Code2Chill (C2C)</h1>

<p align="center">
  <strong>Where Serious Code Meets Chill Vibes</strong><br />
  Official Student Technical Club &bull; Chitkara University
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat&logo=python&logoColor=white" alt="Python 3.13+" />
  <img src="https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/PostgreSQL-17-4169E1?style=flat&logo=postgresql&logoColor=white" alt="PostgreSQL 17" />
  <img src="https://img.shields.io/badge/React-19-61DAFB?style=flat&logo=react&logoColor=black" alt="React 19" />
  <img src="https://img.shields.io/badge/TypeScript-5.9-3178C6?style=flat&logo=typescript&logoColor=white" alt="TypeScript" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-4.0-06B6D4?style=flat&logo=tailwindcss&logoColor=white" alt="Tailwind CSS" />
  <img src="https://img.shields.io/badge/Vite-8.0-646CFF?style=flat&logo=vite&logoColor=white" alt="Vite" />
</p>

---

## 🎧 Overview

**Code2Chill (C2C)** is an active, student-led technical community under the **Office of Student Life at Chitkara University**. We bridge intense, industry-grade software engineering with an inclusive, relaxed community culture. 

No toxic hustle culture—just curious builders collaborating through hands-on hackathons, open-source projects, and peer-to-peer mentorship.

This repository houses the **dynamic Python full-stack club portal**, featuring an asynchronous FastAPI REST backend, a persistent relational PostgreSQL database, and an editorial, high-performance React client interface.

---

## ✨ Key Capabilities

* **Dynamic Event Hub**: Real-time discovery for upcoming hackathons, coding sprints, and historical archives (*DOMination*, *Byte The Vibe*).
* **Official University Handoff**: Pragmatic registration flow integrating seamlessly with Chitkara University's official student portal.
* **Open Source Showcase**: Highlights real, member-built projects (such as *NEXUS* emotion detection and *ChronoAtlas*).
* **Verified Team Hierarchy**: Dynamic roster management for club leadership and domain heads.
* **Campus Event Programme Aesthetic**: An original, high-contrast visual design system built with self-hosted typography (*Barlow Condensed* & *DM Sans*) and WCAG-compliant accessibility focus rings.

---

## 🏛️ System Architecture

```text
CLIENT (Browser)                 BACKEND GATEWAY (FastAPI)           PERSISTENCE
┌──────────────────┐            ┌──────────────────────────┐       ┌─────────────────┐
│ React 19 SPA     │            │ SlowAPI (Rate Limiter)   │       │ PostgreSQL 17   │
│ - Vite & TS      │ HTTP JSON  │           │              │       │ (Async Engine)  │
│ - Tailwind CSS   │───────────▶│ Pydantic v2 Validation   │       │                 │
│ - Route Router   │◀───────────│           │              │       │ - Members       │
│ - Service Status │            │ FastAPI APIRouter (/api) │       │ - Events        │
└──────────────────┘            │           │              │ Async │ - Projects      │
                                │ SQLAlchemy 2.0 AsyncPool ├──────▶│ - Applications  │
                                └──────────────────────────┘       └─────────────────┘
```

---

## 📁 Repository Structure

```text
Code2Chill/
├── backend/                  # Python 3.13+ FastAPI ASGI application
│   ├── app/                  # Application core, database engine, and routers
│   ├── tests/                # Automated pytest test suites
│   ├── compose.yaml          # Local PostgreSQL 17 container orchestration
│   ├── pyproject.toml        # uv / PEP 621 dependency management
│   └── uv.lock               # Deterministic Python dependency lock
├── frontend/                 # React 19 + TypeScript + Vite + Tailwind CSS
│   ├── src/                  # Component tree, router, and page styles
│   ├── package.json          # npm scripts and dependencies
│   ├── vite.config.ts        # Vite build configuration
│   └── biome.json            # Biome formatting and linting configuration
├── docs/                     # Living documentation, design system & planning
│   ├── BUILD_GUIDE.md        # Living build guide & technical viva preparation
│   ├── DEVELOPMENT.md        # Local environment & developer setup guide
│   ├── CONTENT_REGISTER.md   # Verified club facts, events, and asset inventory
│   ├── LAUNCH_SCOPE.md       # Scope boundaries, registration, and recruitment rules
│   ├── PAGES_AND_JOURNEYS.md # 9 route specs, user flows, and error resilience
│   ├── VISUAL_IDENTITY.md    # Design system, tokens, and logo placement matrix
│   ├── WIREFRAMES.md         # Responsive desktop and mobile wireframes
│   ├── AGENTS.md             # Contributor instructions and documentation policy
│   ├── planning/             # Historical planning specifications and blueprints
│   └── design/               # Standalone HTML page previews & offline web assets
│       ├── brand/            # Responsive WebP marks, icons, and favicon
│       ├── fonts/            # Self-hosted Barlow Condensed & DM Sans
│       ├── index.html        # Verified Home design preview
│       └── domination.html   # Verified Event Detail design preview
├── Expriments/               # Isolated prototype experiments
├── .gitignore                # Environment and dependency exclusion rules
├── README.md                 # Project entry point
└── WEBSITE_ROADMAP.md        # 11-phase implementation roadmap
```

---

## 🛠️ Local Development & Setup

For step-by-step local developer setup, Docker container commands, and backend/frontend startup instructions, please refer to the **[Local Development Guide](docs/DEVELOPMENT.md)**.

---

## 📖 Living Documentation Suite

The project enforces continuous living documentation updated across all development phases:

| Document | Focus & Purpose |
| :--- | :--- |
| **[Implementation Roadmap](WEBSITE_ROADMAP.md)** | 11-phase master execution plan with strict completion criteria. |
| **[Living Build Guide](docs/BUILD_GUIDE.md)** | Chronological task history (`TASK-001`+), verification logs, and viva defense answers. |
| **[Local Development Guide](docs/DEVELOPMENT.md)** | Prerequisites, local PostgreSQL container, FastAPI startup, and Vite client execution. |
| **[Content Register](docs/CONTENT_REGISTER.md)** | Verified club facts, leadership roster, past events, and media provenance. |
| **[Launch Scope & Rules](docs/LAUNCH_SCOPE.md)** | MVP feature boundaries, university registration handoff, and recruitment rules. |
| **[Pages & User Journeys](docs/PAGES_AND_JOURNEYS.md)** | Route specifications, interaction flows, and system resilience states. |
| **[Visual Identity System](docs/VISUAL_IDENTITY.md)** | Tokens, typography scales, contrast checks, and brand export rules. |
| **[Wireframe Specifications](docs/WIREFRAMES.md)** | Responsive desktop and mobile wireframes with realistic content lengths. |

---

## 👥 Club Leadership & Core Team

| Name | Role | Domain |
| :--- | :--- | :--- |
| **Lakshay Kalra** | Club Leader / President | Executive |
| **Jiya Arora** | Vice-President | Executive |
| **Samanyu Thakur** | Technical Head | Technical Domain |
| **Bhupinder Singh** | Technical Head | Technical Domain |
| **Tamanna Kakkar** | Content Head | Editorial & Content |
| **Ayush Sharma** | Content Head | Editorial & Content |
| **Jashan Bhalla** | Social Media Head | Media & Branding |
| **Muskan Dhanda** | Promotion Head | Public Relations |
| **Divyana Garg** | Core Member | Operations |
| **Hunar Mehndiratta** | Core Member | Tech & Operations |

---

## 🌐 Community & Connect

* **Instagram**: [@code2chill](https://www.instagram.com/code2chill/)
* **University Listing**: [Chitkara University &bull; Code2Chill](https://chitkarau.life/clubs/code2chill)
* **LinkedIn**: [Code2Chill on LinkedIn](https://www.linkedin.com/company/code2chill)
