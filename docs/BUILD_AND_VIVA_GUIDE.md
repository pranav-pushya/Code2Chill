# Code2Chill — Living Build Documentation and Viva Guide

**Last updated:** 16 November 2026  
**Current stage:** Research and planning, with an existing standalone prototype.  
**Policy:** Update this guide after every task or independently completed step.

## 1. Purpose

This guide explains what has been built, how it works, why choices were made, and how results were verified. It supports viva preparation and future handover.

Use [WEBSITE_ROADMAP.md](../WEBSITE_ROADMAP.md) for planned phases and steps. Use this guide for actual implementation explanations and evidence.

For viva preparation, read the current status, study the relevant feature flow, review tradeoffs and limitations, and practice the questions in your own words. Demonstrate only functionality that actually exists.

### Status vocabulary

| Status | Meaning |
| --- | --- |
| Planned | A proposal; not implemented |
| Existing, source-reviewed | Files were inspected; runtime behavior may be unverified |
| Implemented, unverified | Code exists but relevant checks have not run or passed |
| Verified | Recorded checks passed; assurance is limited to their scope |
| Partial / blocked | Work is incomplete; explain what remains and why |
| Superseded | Replaced by a later decision but retained as history |

## 2. Project Overview

Code2Chill needs a public club website and an interface for authorized leads to maintain its content. Planned features include events, projects, a team roster, recruitment, and administration.

The assignment requires a Python full-stack website with dynamic data. The proposed interpretation is a Python backend with a React browser interface. Confirm any assessment rule requiring Python-rendered templates before scaffolding.

The owner confirmed Lakshay Kalra as president and Jiya Arora as vice-president. Other roster entries, event details, and publication statistics still need appropriate confirmation.

### What dynamic data means

Club records will be stored in a database and returned through the backend. Administrators will update them without editing frontend source code. Animation alone does not make the content dynamic: a moving card with a hardcoded event is still static data.

## 3. Current Implementation Status

| Area | State | Evidence / limitation |
| --- | --- | --- |
| Roadmap | Written | Eleven phases with steps and completion criteria |
| Content register | Created and verified | [Register](CONTENT_REGISTER.md) records evidence, checks, asset availability, and open content gaps |
| Brand assets | Existing, inspected | Two 745 × 740 PNG logo variants |
| Website prototype | Existing, source-reviewed | `extra.html`; no live-browser validation during initial review |
| Ink theme effect | Existing, source-reviewed | WebGL2, html2canvas, and GSAP logic |
| React/Vite scaffold | Planned | No application scaffold created |
| Python API | Planned | No FastAPI implementation created |
| Database and migrations | Planned | No models or migrations created |
| Registration and recruitment | Planned | Prototype buttons do not save submissions |
| Authentication and dashboard | Planned | Not implemented |
| Automated tests and CI | Planned | No application test suite or CI setup |
| Deployment | Planned | No deployment created during this work |

**Accurate current viva statement:** “I have reviewed the supplied prototype and assets, documented the implementation phases, and established a build log. The production frontend, Python API, and database are still to be implemented.”

## 4. Repository Map

| File | Purpose |
| --- | --- |
| [README.md](../README.md) | Project entry point |
| [WEBSITE_ROADMAP.md](../WEBSITE_ROADMAP.md) | Planned implementation and completion checklist |
| [CODE2CHILL_WEBSITE_MASTER.md](../CODE2CHILL_WEBSITE_MASTER.md) | Earlier specification; reconcile proposals and unsupported claims |
| [bluprint.pdf](../bluprint.pdf) | Earlier ten-page blueprint |
| [download.svg](../download.svg) | Proposed architecture diagram |
| [download2.svg](../download2.svg) | Proposed recruitment sequence |
| [extra.html](../extra.html) | Standalone prototype |
| [Code2Chill.png](../Code2Chill.png) | Background logo |
| [Code2Chill_transparent.png](../Code2Chill_transparent.png) | Transparent logo |
| [GEMINI.md](../GEMINI.md) | Existing project rules |
| [AGENTS.md](../AGENTS.md) | Contributor/agent instructions and documentation policy |
| [CONTENT_REGISTER.md](CONTENT_REGISTER.md) | Phase 1 evidence, ownership, publication readiness, and asset inventory |
| This guide | Current build explanation, decisions, verification, and task history |

## 5. Existing Prototype — How It Works

### Page structure

The single HTML file contains markup, CSS, and JavaScript. It includes navigation, a hero, decorative terminal, ecosystem cards, sample event, team roster, recruitment calls to action, and footer. External resources supply fonts and libraries. A logo is embedded directly in the HTML as image data.

### Theme transition flow

This explanation comes from source inspection, not a successful runtime test.

1. The theme button or `T` shortcut requests a theme change.
2. The script determines the source and destination themes.
3. html2canvas captures the theme appearances into canvases.
4. WebGL uploads the snapshots as textures.
5. A fragment shader blends their pixels along a procedural ink-shaped boundary.
6. The live page switches theme beneath the overlay.
7. The overlay disappears after the transition.

The source provides fallback paths when snapshots or the renderer are unavailable. A settings panel changes parameters such as duration and tendril reach.

### Known limitations

- `#about`, `#events`, and `#projects` links have no matching targets.
- Club action buttons do not implement registration or application workflows.
- There are no backend requests, database records, or authentication.
- Desktop navigation disappears on smaller screens without a replacement menu.
- Reduced-motion support and persisted theme preference are absent from the reviewed source.
- Full-page snapshots introduce memory and rendering costs.
- Snapshot validity depends on dimensions; content changes of the same size can leave stale snapshots.

### Viva questions

**Does the prototype satisfy the dynamic-data requirement?**  
No. It has interactive presentation, but club content is hardcoded. The full application must retrieve and persist records through the Python backend.

**What does the shader do?**  
It calculates how pixels from two page snapshots blend to produce an ink-like boundary. It is a visual effect, separate from business logic.

**Why separate the production application into modules?**  
Shared UI, multiple workflows, backend rules, and data models have different responsibilities. Separating them improves maintainability and makes focused testing possible.

## 6. Proposed Architecture — Not Yet Implemented

```text
Student / administrator
          |
          v
React browser interface
          | HTTP + JSON
          v
FastAPI routes
          | Validation, authorization, business rules
          v
SQLAlchemy database access
          |
          v
PostgreSQL

Media files -> persistent object storage
Media metadata -> database
Schema revisions -> Alembic migrations
```

| Component | Planned responsibility | Rationale |
| --- | --- | --- |
| React + TypeScript | Browser interface and state | Reusable components and explicit types |
| Vite | Development and build tooling | Dedicated frontend build workflow |
| Tailwind CSS | Shared styling rules | Consistent visual implementation |
| FastAPI | Python API and backend coordination | Validation integration and generated API documentation |
| Pydantic | Request/response contracts | Structured validation and errors |
| SQLAlchemy | Database queries and model mapping | Structured persistence layer |
| PostgreSQL | Persistent relational records | Relationships, constraints, and transactions |
| Alembic | Schema revisions | Repeatable, reviewable database changes |
| Object storage | Persistent media | Media remains available across app deployments |

These choices are proposals, not installed dependencies. Record actual versions and commands when scaffolding happens.

### Proposed registration flow

If this website owns registration:

1. Student submits the form.
2. Backend validates input and checks the event and registration window.
3. Business logic prevents duplicates and enforces capacity transactionally.
4. Database stores the registration.
5. Backend returns a safe confirmation response.
6. Frontend displays confirmation; authorized administrators review the record.

If the university portal owns registration, implement an external handoff and document that boundary. Do not claim external registrations are stored locally.

## 7. Decision Register

| ID | Decision / question | Status | Reason / follow-up |
| --- | --- | --- | --- |
| DEC-001 | Treat prototype as reference, not final design | Agreed direction | Owner expects substantial improvement |
| DEC-002 | Use both existing logos according to context | Confirmed | Preserve originals and choose by contrast/placement |
| DEC-003 | Python backend with dynamic records | Confirmed requirement | Assignment requirement |
| DEC-004 | React + FastAPI + PostgreSQL | Proposed | Confirm assessment interpretation before scaffolding |
| DEC-005 | Local versus university registration | Open | Determines ownership and workflow scope |
| DEC-006 | Administrator session strategy | Open | Specify storage, expiry, logout, and relevant request protections |
| DEC-007 | Production ink transition | Open | Requires performance/accessibility evaluation |
| DEC-008 | Update documentation after every task/step | Confirmed | Accurate viva preparation and handover |

When replacing a decision, record the reason and affected implementation. Retain the old entry as superseded.

## 8. Verification Register

| ID | Check | Result | Scope |
| --- | --- | --- | --- |
| VER-001 | Repository and source inventory | Initial materials identified | Read-only inspection |
| VER-002 | Render and inspect ten PDF pages | Blueprint reviewed | Document inspection |
| VER-003 | Logo dimensions and transparency | Both 745 × 740; alpha channel in transparent version | Does not prove quality at every display size |
| VER-004 | Prototype source and anchors | Missing targets and unimplemented workflows identified | No live-browser test |
| VER-005 | Roadmap phase/criterion checks | Eleven phases and criteria present | Markdown structure check |
| VER-006 | Python checks of documentation readability, relative links, section/task counts, and maintenance references | Passed: four files readable, local links resolve, twelve guide sections and four historical task entries present | Documentation-only checks; no application tests run |
| VER-009 | Phase 1.1 pass 1, Python checks and `git diff --check` | All 23 rows had unique IDs, complete fields, valid statuses and dates, and resolvable local links. Both PNG dimensions, the transparent logo's alpha channel, and the Phase 1 checkbox state matched the register. | Repository and document structure |
| VER-010 | Phase 1.1 pass 2, source and publication review | Cross-checked the two leadership titles against the owner-confirmed roadmap, the club and event claims against indexed LinkedIn evidence, and portal capability against the university's indexed portal page. | Direct retrieval of the LinkedIn pages, Instagram profile, and club-specific portal page did not succeed. Unsupported claims remain open. |

Append actual checks, commands or procedures, results, and limitations. “Code reviewed” is not equivalent to “runtime tested.”

## 9. Viva Answer Foundations

These explain concepts and planned behavior, not claims of completed implementation.

**What problem does this project solve?**  
It helps students discover club activity and lets authorized leads maintain content and manage submissions.

**Why is a backend necessary?**  
It enforces rules and permissions and coordinates persistent data. A browser cannot be trusted to enforce those rules on its own.

**What is an API?**  
A defined interface for requesting or submitting data. An endpoint specifies a route, method, input contract, and response.

**Authentication versus authorization?**  
Authentication identifies the user. Authorization determines what that user can do. Logging in does not automatically grant every permission.

**Why validate on frontend and backend?**  
Frontend validation gives immediate feedback. Backend validation is authoritative because requests can bypass the interface.

**What does an ORM do?**  
It maps records and provides structured query tools. Developers still need to understand constraints, transactions, relationships, and query behavior.

**Why use migrations?**  
They make schema changes repeatable and reviewable. They do not guarantee zero data loss; testing and backups remain necessary.

**What is a transaction?**  
A group of database operations that commit together or roll back. Capacity-sensitive workflows also need appropriate locking or atomic operations to prevent concurrent overbooking.

**Does async always make code faster?**  
No. It helps overlap I/O waiting. It does not automatically accelerate CPU-heavy work, and blocking operations can still stall execution.

**Is CORS authentication?**  
No. It controls browser cross-origin access behavior. It does not replace permissions or input validation.

**How will you prove that data is dynamic?**  
Once implemented, change a published record through the dashboard, show the public update without editing frontend code, and demonstrate persistence after restarting the backend.

**Why consider FastAPI?**  
The proposed system uses a separate frontend and Python API. Validation integration and generated documentation fit that architecture. Avoid unsupported claims that other frameworks cannot support asynchronous work.

**How will you prove the system works?**  
Demonstrate complete journeys and run focused tests for validation, permissions, persistence, duplicates, deadlines, and capacity. Report only checks that actually ran.

## 10. Chronological Task Log

These entries summarize work visible in this conversation. The prototype and earlier specifications predate these tasks; their authorship and creation dates are not inferred.

### TASK-001 — Repository review

- **Date:** 16 November 2026.
- **Status:** Review completed; runtime validation not performed.
- **Objective:** Understand supplied materials before planning implementation.
- **Work:** Inspected all nine initial files, prototype source, logos, SVGs, and rendered PDF pages.
- **Result:** Identified a planning-stage repository without a production application scaffold.
- **Validation:** VER-001 through VER-004.
- **Limitation:** No live-browser validation of the prototype.
- **Viva takeaway:** Distinguish existing prototype behavior from planned production features.

### TASK-002 — Research and phased planning

- **Date:** 16 November 2026.
- **Status:** Plan produced; source extraction partial.
- **Objective:** Connect club needs and the assignment to concrete implementation phases.
- **Work:** Attempted supplied URLs and fallbacks; reviewed indexed club LinkedIn content; developed eleven phases.
- **Result:** Identified confirmed leadership, provisional content, and proposed architecture.
- **Limitation:** Supplied club and design-reference pages were not retrievable. Their current designs are not verified.
- **Viva takeaway:** Explain which facts are confirmed and which require further verification.

### TASK-003 — Markdown roadmap

- **Date:** 16 November 2026.
- **Status:** Created and structurally checked.
- **File:** [WEBSITE_ROADMAP.md](../WEBSITE_ROADMAP.md).
- **Work:** Added step checkboxes, deliverables, completion criteria, and a demonstration sequence.
- **Validation:** File exists; all eleven phase/criterion entries present.
- **Limitation:** Written steps do not constitute completed implementation.
- **Viva takeaway:** Connect implementation phases to demonstrable outcomes.

### TASK-004 — Living documentation workflow

- **Date:** 16 November 2026.
- **Status:** Documentation created and structurally verified.
- **Objective:** Keep detailed build explanations and viva preparation updated after every task/step.
- **Files:** This guide, [AGENTS.md](../AGENTS.md), [GEMINI.md](../GEMINI.md), and [README.md](../README.md).
- **Work:** Added current status, prototype explanation, proposed architecture, decisions, validation evidence, viva questions, and task history. Added update instructions and navigation links.
- **Reason:** Keep documentation tied to actual evidence and avoid presenting proposed features as completed work.
- **Attempt note:** An initial combined patch failed because README context did not match. No files were changed by that failed patch; the patch was split and retried.
- **Validation:** VER-006 passed. A Python check verified file readability, local link targets, twelve guide sections, four task entries, and references in the instruction/navigation files.
- **Limitation:** Instructions govern future work; they are not a background service detecting arbitrary manual edits. Manual contributors must follow the update policy too.
- **Viva takeaway:** Explain what changed, how it works, why it was chosen, and what was checked.


### TASK-006 — Create the content register

- **Date:** 19 November 2026.
- **Roadmap step:** Phase 1.1.
- **Status:** Register completed and verified in two passes.
- **Objective:** Establish one place to track which club facts and assets have evidence and who can fill the gaps.
- **Changes and files:** Created [CONTENT_REGISTER.md](CONTENT_REGISTER.md), checked off 1.1 in the [roadmap](../WEBSITE_ROADMAP.md#phase-1--establish-content-and-scope), and recorded the register and verification here.
- **How it works:** Each entry has a stable ID, source or accountable owner, verification status, check date, and follow-up. The register covers identity, events, projects, registration, recruitment, and assets.
- **Why this approach:** Source status controls what can feed public copy. Item-level follow-ups let later steps request the missing material without relying on sample figures or draft roster entries.
- **Validation:** VER-009 checked the register structure and repository assets. VER-010 reviewed the claims and source limitations.
- **Delivery notes:** A separate staging patch isolates Phase 1.1 from the existing Phase 3 edits. The first staging attempt could not read the sandbox-local patch, so the retry uses a workspace copy. GitHub remote discovery in the restricted shell failed with a resolver error.
- **Limitations / remaining work:** The register contains explicit gaps for the roster, domains, contact details, event material, projects, and workflow rules.
- **Viva Q&A:** **Why record a check date for a missing value?** It identifies when the gap was last reviewed and who can resolve it. **What can you publish from an event recap?** The claims the source supports. Dates, winners, and photographs need their own evidence and permissions.

## 11. Template for Every Future Task or Step

Use the next task ID and actual date. For multi-step work, document independently completed steps as they finish.

For each roadmap step, complete two verification passes and record the evidence. Commit and push the verified step as requested by the project owner before starting the next step.

```markdown
### TASK-NNN — Task title

- **Date:** Actual date.
- **Roadmap step:** Phase and step ID, or not applicable.
- **Status:** Verified / implemented-unverified / partial / blocked / documentation-only.
- **Objective:** Problem or requested behavior.
- **Changes and files:** Actual changes, with relative repository links.
- **How it works:** Plain-language data or control flow.
- **Why this approach:** Rationale, alternatives, and meaningful tradeoffs.
- **Validation:** Actual commands/procedures, results, and scope.
- **Limitations / remaining work:** Known gaps, failures, and dependencies.
- **Viva Q&A:** Implementation-specific questions and concise answers.
```

Also update current status, relevant feature explanations, decision records, verification evidence, and roadmap checkboxes as appropriate. Add feature-specific sections as implementation grows.

## 12. Documentation Review Checklist

- Current status matches actual files and behavior.
- Every task or independently completed step has a dated entry.
- Planned and implemented features are distinguished.
- Rationale and relevant tradeoffs are explained.
- Actual verification and limitations are recorded.
- Viva answers reflect the implementation.
- Roadmap boxes are checked only for completed work.
- Documentation contains no credentials or private submission records.
