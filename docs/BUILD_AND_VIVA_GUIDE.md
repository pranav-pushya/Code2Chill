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
| Phase 1 launch scope | Defined and verified | [Launch scope](LAUNCH_SCOPE.md) describes the essential release, university registration, recruitment defaults, and open decisions |
| Phase 2 pages and journeys | Defined and verified | [Page plan](PAGES_AND_JOURNEYS.md) and [wireframes](WIREFRAMES.md) specify actions, states, and recovery paths |
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

**Accurate current viva statement:** “I verified the available club content, defined the first release, and mapped its public and administrator journeys. Desktop and mobile wireframes show the planned content and actions. The production frontend, Python API, and database are planned.”

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
| [LAUNCH_SCOPE.md](LAUNCH_SCOPE.md) | Launch workflow decisions and the boundaries of local data handling |
| [PAGES_AND_JOURNEYS.md](PAGES_AND_JOURNEYS.md) | Planned routes, navigation, and user journeys |
| [WIREFRAMES.md](WIREFRAMES.md) | Desktop and mobile layout sketches using verified club copy |
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

### Planned launch registration

The launch uses the university portal for event sign-ups. Code2Chill will publish event details, show the latest verified registration state, and link to the approved university event page when open. The portal handles student records and confirmation. See the [event registration decision](LAUNCH_SCOPE.md#event-registration).

If a future release takes ownership of registration, the proposed local flow is:

1. Student submits the form.
2. Backend validates input and checks the event and registration window.
3. Business logic prevents duplicates and enforces capacity transactionally.
4. Database stores the registration.
5. Backend returns a safe confirmation response.
6. Frontend displays confirmation; authorized administrators review the record.

## 7. Decision Register

| ID | Decision / question | Status | Reason / follow-up |
| --- | --- | --- | --- |
| DEC-001 | Treat prototype as reference, not final design | Agreed direction | Owner expects substantial improvement |
| DEC-002 | Use both existing logos according to context | Confirmed | Preserve originals and choose by contrast/placement |
| DEC-003 | Python backend with dynamic records | Confirmed requirement | Assignment requirement |
| DEC-004 | React + FastAPI + PostgreSQL | Proposed | Confirm assessment interpretation before scaffolding |
| DEC-005 | Local versus university registration | Superseded by DEC-011 | The launch uses an external handoff |
| DEC-006 | Administrator session strategy | Open | Specify storage, expiry, logout, and relevant request protections |
| DEC-007 | Production ink transition | Open | Requires performance/accessibility evaluation |
| DEC-008 | Update documentation after every task/step | Confirmed | Accurate viva preparation and handover |
| DEC-011 | Use the university portal for launch event sign-ups | Selected for launch | One system holds registration records. The organizer confirms each event link and state. |
| DEC-012 | Show an announcement while no recruitment cycle is approved | Selected for launch | Keeps the Join page usable while the club confirms actual dates, domains, eligibility, application route, and reviewers. |
| DEC-013 | Use the first-release scope as the baseline for route and workflow planning | Selected for launch | The site can demonstrate dynamic content publication with verified records and official links. Deferred features and open decisions have owners or follow-up phases. |

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
| VER-011 | Phase 1.2 preliminary source and reachability check | Checked the club's indexed profile, public role evidence, and the supplied portal and social URLs. Direct requests returned generic HTML for Instagram and the university route, and HTTP 403 for LinkedIn. | The browser connection timed out. Chrome reported active user input during the fallback. The approved roster, domain list, and official contact route still require confirmation. |
| VER-012 | Phase 1.2 preliminary document check | Python checked status labels across all 12 identity rows, relative links, the unchecked 1.2 box, and that the Git index was empty. `git diff --check` passed. | This check covered the research notes and repository state. Final verification depends on the approved identity details. |
| VER-013 | Phase 1.2 final pass 1, university and owner evidence | Two anonymous Chrome renders exposed the public club page. A Python comparison matched all ten roster entries, four domain labels, the public links, and the visible membership interest action to the register. | The executive titles use owner confirmation. The check did not submit a membership request. |
| VER-014 | Phase 1.2 final pass 2, publication and repository review | Checked document links, evidence labels, unfilled contact details, the Phase 1 checkbox sequence, and the staged change scope. `git diff --cached --check` passed. | The general enquiries address and the behavior behind the membership interest action remain open. |
| VER-015 | Phase 1.3 pass 1, event source cross-check | Rendered both university event pages in Chrome. Python compared their dates, venue, topic details, and publication flags to the register. Confirmed the upcoming state and the On Fire recap separately. | Both event schedules showed zero duration. Byte The Vibe also had conflicting times. |
| VER-016 | Phase 1.3 pass 2, publication and repository review | Checked evidence links, asset and results statuses, checkbox order, and the staged files with Python and `git diff --cached --check`. | Official placement lists, event media reuse, and some event details remain open. |
| VER-017 | Phase 1.4 pass 1, project provenance and link check | Read public contributor accounts and GitHub API metadata and README. The NEXUS demo returned HTTP 200 with the expected title. Python matched credits, repository URLs, and attribution against the register. | Demo interaction, camera and mic behavior, and media rights remain unverified. |
| VER-018 | Phase 1.4 pass 2, publication and repository review | Checked evidence links, distinct project and starter records, missing-asset status, checklist sequence, and the staged scope. `git diff --cached --check` passed. | ChronoAtlas links and approved screenshots remain open. |
| VER-019 | Phase 1.5 pass 1, registration design check | Used the observed university event pages to review open, closed, full, ended, and pending scenarios. Python checked the state table, event references, and system of record. | Design verification. Live submission remains untested. |
| VER-020 | Phase 1.5 pass 2, documentation and repository review | Checked the roadmap, verification and decision IDs, relative links, staged files, and `git diff --cached --check`. | No application implementation or portal integration was exercised. |
| VER-021 | Phase 1.6 pass 1, recruitment rules and boundary review | Matched the university's interest action and checked documented cycle settings and form fields. A Python walkthrough with demonstration settings checked five cases from unconfigured through the closing instant. | Design walkthrough. No form or real applicant data was used. |
| VER-022 | Phase 1.6 pass 2, documentation and repository review | Checked the recruitment default, missing official settings, cross-document links, checklist sequence, and staged scope. `git diff --cached --check` passed. | Reviewers, dates, and other actual cycle settings are still to be provided. |
| VER-023 | Phase 1.7 pass 1, scope and deliverables review | Python checked the essential, deferred, and open sections against the register, the portal decision, the recruitment default, and all seven Phase 1 items. | Scope review covers design commitments and open dependencies. |
| VER-024 | Phase 1.7 pass 2, repository and sequence review | Checked all Phase 1 task records and verification references, local links and anchors, staged scope, and `git diff --cached --check`. | Application development and testing are later phases. |
| VER-025 | Phase 1 audit and correction pass 1, evidence and behavior | GitHub reported the Phase 1 tip. Rendered the club and two event records, found all ten named roster entries and an empty upcoming list, and confirmed both public project repositories and the NEXUS demo response. Compared the corrected roadmap to the portal and recruitment decisions. | Indexed club social evidence and the university's Instagram link support attribution. Live submissions and third-party demo interactions were outside the check. |
| VER-026 | Phase 1 correction pass 2, staged document review | Checked the corrected roadmap, dated content observation, local links and anchors, and exact staged scope. `git diff --cached --check` passed. | Repository and planning verification. |
| VER-027 | Phase 2.1 pass 1, route walkthrough | Compared the route table and sitemap, matched named route examples to the content register, and walked through navigation and missing-content paths. | Route design. No router is implemented. |
| VER-028 | Phase 2.1 pass 2, repository review | Verified the route plan and roadmap links, checkbox sequence, task record, and staged scope. `git diff --cached --check` passed. | Document validation. |
| VER-029 | Phase 2.2 pass 1, event journey walkthrough | Checked list entry, archive and shared links, registration conditions, missing details, error recovery, and the external handoff against the Phase 1 rules. | Planned journey only. |
| VER-030 | Phase 2.2 pass 2, repository review | Checked the staged diagram references, repository links, checklist sequence, and task record. `git diff --cached --check` passed. | No booking was attempted. |
| VER-031 | Phase 2.3 pass 1, recruitment walkthrough | Checked inactive, scheduled, external, local, invalid, retry, saved, and closed paths against the cycle rules and graph. | No active cycle or application service is available in the project. |
| VER-032 | Phase 2.3 pass 2, repository review | Verified staged links, roadmap sequence, task log, and the launch versus conditional route distinction. `git diff --cached --check` passed. | Document validation. |
| VER-033 | Phase 2.4 pass 1, administrator walkthrough | Checked the content and reviewer branches, protected preview, session recovery, stale drafts, publish feedback, and ownership of submissions. | Planned permission checks and editor behavior. |
| VER-034 | Phase 2.4 pass 2, repository review | Verified staged links, the admin route plan, task log, and roadmap sequence. `git diff --cached --check` passed. | No sign-in service or dashboard was exercised. |
| VER-035 | Phase 2.5 pass 1, state coverage and precedence | Checked 21 state definitions against the event, recruitment, and administrator journeys. Walked through success, failure, empty, status, and access recovery. | Design review. Accessibility behaviors still need implementation and browser testing. |
| VER-036 | Phase 2.5 pass 2, repository review | Verified staged links, checklist order, task log, and exact change scope. `git diff --cached --check` passed. | Document validation. |
| VER-037 | Phase 2.6 pass 1, layout and content review | Inspected the rendered text layout and checked 28 desktop and mobile panels for consistent widths, planned routes, readable wrapping, and source-backed examples. | Low-fidelity diagrams. Browser breakpoints and accessibility still need implementation checks. |
| VER-038 | Phase 2.6 pass 2, repository review | Verified staged links, the wireframe file, task log, and checklist order. `git diff --cached --check` passed. | Document validation. |
| VER-039 | Phase 2.7 pass 1, action and journey audit | Checked public and private page actions against the sitemap, wireframe controls, interface states, and Phase 1 ownership boundaries. | Planned actions. Runtime routing and submission tests are later phases. |
| VER-040 | Phase 2.7 pass 2, final Phase 2 repository review | Verified staged links, all seven Phase 2 completion markers, verification records, and changed files. `git diff --cached --check` passed. | Document validation. |
| VER-041 | Phase 1 and 2 audit, correction pass 1 | Checked the 14 completed roadmap items, 29 content records, both logos, the live GitHub branch, and the corrected event and recruitment scenarios. The university pages, project repositories, NEXUS demo, and Instagram endpoint returned HTTP 200. | The LinkedIn profile returned HTTP 403 to the direct request. Public indexing still showed the club profile. The audit used no live applications or bookings. |
| VER-042 | Phase 1 and 2 audit, correction pass 2 | Chrome rendered all three diagrams to SVG with Mermaid 11.12.0. Checked staged links, 14 wireframe pairs, 36 control labels, the 22 interface states, and `git diff --cached --check`. | Planning and diagram validation. The website implementation still needs runtime tests. |

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
- **Delivery notes:** A separate staging patch isolated Phase 1.1 from the existing Phase 3 edits. The first staging attempt could not read the sandbox-local patch, so the retry used a workspace copy. Restricted-shell remote discovery failed with a resolver error. The subsequent push succeeded and updated `origin/main` to `486c059`.
- **Limitations / remaining work:** The register contains explicit gaps for the roster, domains, contact details, event material, projects, and workflow rules.
- **Viva Q&A:** **Why record a check date for a missing value?** It identifies when the gap was last reviewed and who can resolve it. **What can you publish from an event recap?** The claims the source supports. Dates, winners, and photographs need their own evidence and permissions.

### TASK-007 — Consolidate club identity

- **Date:** 19 November 2026.
- **Roadmap step:** Phase 1.2.
- **Status:** Partial at the time. Completed in TASK-008 after the owner supplied the links.
- **Objective:** Consolidate launch-ready identity copy, leadership, domains, official links, and a public contact route.
- **Changes and files:** Updated [the identity section of the content register](CONTENT_REGISTER.md#club-identity-and-contacts) with short copy, public evidence for role leads, and link-check results. Recorded the research in this guide.
- **How it works:** The confirmed description and titles have their own rows. Member profiles and accounts with conflicting affiliations remain leads until club leadership confirms current titles and publication scope.
- **Why this approach:** A role in an individual profile may reflect one project or a previous term. A server response confirms the server answered. The club record or profile must still identify Code2Chill before its link is ready for public use.
- **Validation:** VER-011 records the evidence and direct link checks. VER-012 checks that the register and roadmap reflect the open items. Final verification awaits the owner-approved details.
- **Limitations / remaining work:** Confirm the full roster, domain names, official Instagram and university club URLs, and the public contact route, or obtain approval to omit unavailable items. Step 1.2 remains open.
- **Viva Q&A:** **Why do you need to confirm individual role titles with the club?** Public profiles may disagree or describe different periods. The club can confirm the current titles to publish. **What did HTTP 200 verify?** The server returned a page, whose contents still need to establish the expected club identity.

### TASK-008 — Verify the club identity against the university listing

- **Date:** 19 November 2026.
- **Roadmap step:** Phase 1.2.
- **Status:** Identity inventory completed with explicit contact gaps.
- **Objective:** Replace provisional role and link leads with the club's published identity, using the two URLs the owner supplied.
- **Changes and files:** Updated the [content register](CONTENT_REGISTER.md#club-identity-and-contacts) with launch copy, ten roster entries, four domain labels, confirmed URLs, and the university membership interest path. Checked off 1.2 in the [roadmap](../WEBSITE_ROADMAP.md#phase-1--establish-content-and-scope).
- **How it works:** The university page supplies the club description and public roster. The register preserves the role shown by the university alongside the project-owner titles for president and vice-president. It uses the clean Instagram URL that also appears on the university page.
- **Why this approach:** The university listing resolves earlier conflicts from individual profiles. The social links and membership interest path give students somewhere to find the club while the general enquiries address remains unknown.
- **Validation:** VER-013 checked the published facts and source labels. VER-014 checked the commit contents and correct treatment of missing details.
- **Limitations / remaining work:** The in-app browser connection timed out, so the page was inspected with anonymous Chrome rendering. A general club email, faculty liaison, approved photos, and terms of office remain open. Available recruitment domains may vary by cycle. The interest action's sign-in and submission behavior remain untested.
- **Viva Q&A:** **Why show two sources for the executive titles?** The university shows Club Leader and Core Member. The owner confirmed the more specific president and vice-president titles for club copy. **How did you resolve the disputed Content Head title?** The club's university listing gives Ayush Sharma that title directly.

### TASK-009 — Collect event material

- **Date:** 19 November 2026.
- **Roadmap step:** Phase 1.3.
- **Status:** Public event inventory collected and verified. Results and media gaps tracked.
- **Objective:** Build a sourced event archive and identify missing material for event detail pages.
- **Changes and files:** Updated the [content register](CONTENT_REGISTER.md#events-and-projects) with two university event records, an On Fire recap, a dated upcoming status check, and leads for placements and event images. Updated the [roadmap](../WEBSITE_ROADMAP.md#phase-1--establish-content-and-scope).
- **How it works:** The university event pages supply dates, venue, and summaries. The media lead's recap establishes On Fire as a past club event. Each unresolved time, placement, or asset has an owner or source lead in the register.
- **Why this approach:** The schedule fields show zero duration on both university event pages, and one conflicts with the event recap. Date-level archive copy remains useful while event leads verify times. Published images still need credits and reuse permission for the new site.
- **Validation:** VER-015 checked the event facts and conflicting fields. VER-016 checked the staged documentation, links, and roadmap sequence.
- **Limitations / remaining work:** Event leads must confirm exact times where relevant, official placements, On Fire's date and venue, and which posters and photographs the site may use. The upcoming event list reflects the day it was checked.
- **Viva Q&A:** **How can both registration figures and attendance figures be accurate?** Registrations count sign-ups. Attendance counts who took part. Give each figure its own label and source. **What happens when an official event page gives different times?** Publish the verified date and keep the time open until the event lead resolves the discrepancy.

### TASK-010 — Collect project material

- **Date:** 19 November 2026.
- **Roadmap step:** Phase 1.4.
- **Status:** Project inventory verified with missing links and assets tracked.
- **Objective:** Find attributable Code2Chill event projects and verify the links and materials that could support a showcase.
- **Changes and files:** Added NEXUS, ChronoAtlas, and the DOMination starter repository to the [content register](CONTENT_REGISTER.md#events-and-projects). Recorded missing screenshots in the asset inventory and checked off 1.4 in the [roadmap](../WEBSITE_ROADMAP.md#phase-1--establish-content-and-scope).
- **How it works:** NEXUS uses the contributors' account and README for description and credits. Its GitHub metadata points to the demo. ChronoAtlas relies on the contributor's recap, with its links left open. The starter is recorded as an event resource with attribution from NEXUS.
- **Why this approach:** A challenge entry belongs to the team that built it. Linking to the authors' project lets the site show the outcome of the club's event while giving the team credit and preserving the starter's attribution.
- **Validation:** VER-017 checked the evidence and demo response. VER-018 checked publication statuses, repository links, and staged scope.
- **Limitations / remaining work:** The contributor's shortened link returned HTTP 403. GitHub metadata provided the direct demo link. The starter README returned HTTP 404, so its role comes from the downstream README. ChronoAtlas needs a repository and demo link, and both projects need approved screenshots before assets can be published.
- **Viva Q&A:** **How did you verify that the demo belongs to NEXUS?** The public repository's homepage points to the deployment, which returned the same project title as the README. **Why credit the starter separately?** The starter gave participants a starting point. The NEXUS contributors created the project built on it.

### TASK-011 — Decide event registration ownership

- **Date:** 19 November 2026.
- **Roadmap step:** Phase 1.5.
- **Status:** Launch design selected and verified in documentation.
- **Objective:** Give each event one registration system and define what Code2Chill shows students.
- **Changes and files:** Wrote the [registration rules](LAUNCH_SCOPE.md#event-registration), updated REG-02 in the [content register](CONTENT_REGISTER.md#registration-and-recruitment), and aligned the [roadmap](../WEBSITE_ROADMAP.md) and guide with the decision.
- **How it works:** Code2Chill will store and publish event content, a registration status, and an official destination if available. Open events link to a verified university page. Closed, full, ended, and unconfirmed events display the corresponding status. The portal handles bookings and confirmation.
- **Why this approach:** The university already displays event registration through its existing portal. A handoff keeps sign-ups and capacity in one place. For the viva, use an event publication and handoff to demonstrate the website's dynamic content.
- **Validation:** VER-019 checked the launch behavior against event states and the available source evidence. VER-020 checked the commit contents and related documentation.
- **Limitations / remaining work:** No live registration or portal data integration was tested. The organizer still confirms each event's destination and availability. A local sign-up feature would require a future ownership decision.
- **Viva Q&A:** **Where is a registration saved?** The university portal owns the launch sign-up. Code2Chill stores the event and official link. **How do you show dynamic data in the viva?** Publish an event in the dashboard and show the saved content update on the public page, then demonstrate the external handoff.

### TASK-012 — Define recruitment rules

- **Date:** 19 November 2026.
- **Roadmap step:** Phase 1.6.
- **Status:** Recruitment design verified. The default is an announcement until the club supplies a cycle.
- **Objective:** Define what students see, what a later application needs, and who is responsible for review.
- **Changes and files:** Added [recruitment rules](LAUNCH_SCOPE.md#recruitment), kept the missing actual cycle settings visible in the [content register](CONTENT_REGISTER.md#registration-and-recruitment), and updated the [roadmap](../WEBSITE_ROADMAP.md#phase-1--establish-content-and-scope).
- **How it works:** Define a cycle with a start, close, available domains, eligibility, reviewers, and one application route. The planned form asks for a name, university email, and domain, with an optional motivation or portfolio. Public behavior moves from announcement to scheduled, open, and closed as configuration and time allow.
- **Why this approach:** Published club domains can change availability across cycles. A cycle makes the opening times, eligibility, and reviewer assignments explicit. The university membership interest link remains useful while application details are pending.
- **Validation:** VER-021 walked through the planned rules and checked both time boundaries using demonstration values. VER-022 checked the staged documents and roadmap state.
- **Limitations / remaining work:** The club still needs to supply a real cycle, including dates, eligibility, enabled domains, reviewers, and the approved application route. Form handling and reviewer access controls are planned for Phase 8.
- **Viva Q&A:** **What is the difference between membership interest and an application?** The university listing has a general interest action. A domain application belongs to a configured recruitment cycle with rules and reviewers. **What happens at the exact closing time?** The local form must reject it because the closing instant is outside the open window.

### TASK-013 — Set the launch scope and close Phase 1

- **Date:** 19 November 2026.
- **Roadmap step:** Phase 1.7 and Phase 1 completion review.
- **Status:** Phase 1 planning and content verification complete. Later-phase implementation is planned.
- **Objective:** Give the first release a defined set of features and record where later choices or missing club material affect launch.
- **Changes and files:** Added essentials, deferrals, and open decisions to the [launch scope](LAUNCH_SCOPE.md#first-public-release). Linked each Phase 1 deliverable from the [roadmap](../WEBSITE_ROADMAP.md#phase-1--establish-content-and-scope) and updated this guide's status and decision register.
- **How it works:** The first release uses the [content register](CONTENT_REGISTER.md), the university registration handoff, and recruitment's announcement state. An authenticated content editor and persistent event publication form the planned viva workflow. The scope table identifies a responsible role or phase for each open item.
- **Why this approach:** Students can find club information and verified event links even when there is no current event or recruitment cycle. The site can demonstrate dynamic content independently of private registration data held by the university.
- **Validation:** VER-023 checked scope against the Phase 1 deliverables. VER-024 checked the staged documentation, evidence links, and completion sequence.
- **Limitations / remaining work:** Club leads still need to supply the general contact address, some event details, approved images, and live recruitment settings. Later phases will choose the rendering approach, authentication, and hosting against the assessment and implementation requirements.
- **Viva Q&A:** **What does Phase 1 prove?** The launch has a sourced content inventory and explicit workflow rules, with missing data identified. **What proves the website is dynamic in the finished demo?** An administrator's saved event update must appear publicly and persist when the backend restarts.

### TASK-014 — Audit and correct Phase 1 deliverables

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 1 follow-up before Phase 2.
- **Status:** Seven original deliverables checked. Roadmap inconsistencies corrected and verified twice.
- **Objective:** Verify the pushed commits, source evidence, and agreement between the roadmap and the launch rules.
- **Changes and files:** Corrected the [roadmap](../WEBSITE_ROADMAP.md) to reflect the confirmed event dates, the university registration handoff, and the recruitment announcement default. Updated the dated upcoming-events observation in the [content register](CONTENT_REGISTER.md#events-and-projects).
- **How it works:** The planned demo verifies that Code2Chill's published event content and destination persist. The university owns the registration. Recruitment follows the announcement path until the club approves a cycle.
- **Why this approach:** Old summary and demo language pointed to work that the launch decision had already assigned to the university or made conditional. Aligning it before the route work prevents those assumptions from reaching the interface.
- **Validation:** VER-025 checked the live GitHub tip, 29 evidence rows, ten roster entries, both logos, university records, project sources, and planned behavior. VER-026 checked the staged correction and repository links.
- **Limitations / remaining work:** Live booking, membership interest submission, and project interactions remain untested. Club-owned content and recruitment decisions still open in [launch scope](LAUNCH_SCOPE.md#open-decisions-and-content-gaps) remain explicitly recorded.
- **Viva Q&A:** **What should survive a restart in the public-launch demo?** The published event content, registration state, and approved destination. **What does the external handoff prove?** Code2Chill can direct students to the right university event without owning the booking workflow.

### TASK-015 — Define public routes

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 2.1.
- **Status:** Nine public routes planned and verified.
- **Objective:** Give each first-release public page a stable address and a way to reach it.
- **Changes and files:** Created the [public sitemap](PAGES_AND_JOURNEYS.md#public-sitemap) and linked it from the [roadmap](../WEBSITE_ROADMAP.md#phase-2--define-pages-and-user-journeys).
- **How it works:** The route table and tree show the public pages, the two detail patterns, direct entry, and recovery paths. The header and footer share navigation across public pages.
- **Why this approach:** Dedicated list and detail URLs support shared links and let visitors recover from a missing item. The plan is usable with either frontend rendering approach still under consideration.
- **Validation:** VER-027 checked route coverage and examples against the content register. VER-028 checked staged documentation and step order.
- **Limitations / remaining work:** The site router, data loading, and visual navigation are planned. Journeys and screen states are specified in later Phase 2 steps.
- **Viva Q&A:** **What is a slug?** It is the unique readable identifier for a published item within its content type. **What happens if an event slug is unknown?** The site shows a not-found state with a link back to Events.

### TASK-016 — Map event discovery and registration

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 2.2.
- **Status:** Event journey planned and verified.
- **Objective:** Show how students find current and past events, read details, and reach official sign-up.
- **Changes and files:** Added the [event journey](PAGES_AND_JOURNEYS.md#event-discovery-and-registration) and updated Step 2.2 in the [roadmap](../WEBSITE_ROADMAP.md#phase-2--define-pages-and-user-journeys).
- **How it works:** The flow has list and shared-link entry points. It checks registration status and a verified event destination before exposing the handoff. Closed, full, ended, pending, missing, and error conditions have clear outcomes.
- **Why this approach:** Students can still explore the archive when the schedule is empty. The official university handoff keeps ticket availability and confirmations with the owner of the booking workflow.
- **Validation:** VER-029 walked the event cases against the launch scope. The first assertion expected eleven links in the diagram. Manual review found twelve, including both shared-URL outcomes, and the corrected assertion passed. VER-030 reviewed the staged documentation and sequence.
- **Limitations / remaining work:** These are planned routes and actions. A live portal sign-up and browser Back behavior will need testing when Code2Chill has a working frontend.
- **Viva Q&A:** **Why can a published event omit a registration button?** Publication makes its information visible. The button requires an open registration state and a verified official destination.

### TASK-017 — Map the recruitment journey

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 2.3.
- **Status:** Recruitment paths planned and verified.
- **Objective:** Give students a useful Join page before recruitment opens and a clear path during an approved cycle.
- **Changes and files:** Added the [recruitment journey](PAGES_AND_JOURNEYS.md#recruitment-journey) and checked off Step 2.3 in the [roadmap](../WEBSITE_ROADMAP.md#phase-2--define-pages-and-user-journeys).
- **How it works:** Join shows the announcement or the published cycle state. An open cycle points to one approved external or local route. The planned local flow handles domain selection, validation, uncertain responses, successful save, and closure.
- **Why this approach:** Students can express general membership interest while the club configures recruitment. Server checks at submission protect the approved window and duplicate rule even when a form was open earlier.
- **Validation:** VER-031 walked the state outcomes and checked the diagram against Phase 1. VER-032 checked the staged plan and current roadmap status.
- **Limitations / remaining work:** The club must supply a real cycle. The local form, email ownership check, and reviewer workflow still need implementation.
- **Viva Q&A:** **Can an open tab submit after the closing instant?** The backend verifies the deadline when it receives the request. The planned form shows the closed state if the window has ended.

### TASK-018 — Map administration and publishing

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 2.4.
- **Status:** Administrator workflow planned and verified.
- **Objective:** Define how staff manage drafts and publish content, and where authorized local reviewers handle applications.
- **Changes and files:** Added the [administrator journey](PAGES_AND_JOURNEYS.md#administrator-journey) and checked off Step 2.4 in the [roadmap](../WEBSITE_ROADMAP.md#phase-2--define-pages-and-user-journeys).
- **How it works:** Staff sign in, open a permitted area, save a draft, preview it behind authentication, and publish it explicitly. Reviewer permissions are scoped to assigned local cycles. Failed publication and expired sessions have recovery paths.
- **Why this approach:** Drafts can be edited without changing public content. Checking permission and the saved version on the server protects both drafts and the published result.
- **Validation:** VER-033 walked through administrator and reviewer cases. VER-034 checked documentation and step sequence in the staged files.
- **Limitations / remaining work:** Authentication, permission checks, draft versions, editor screens, and application review remain implementation work.
- **Viva Q&A:** **Why protect the preview path?** A draft can contain unfinished material. Access to it follows the same authorization check as the editor.

### TASK-019 — Specify interface states and recovery

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 2.5.
- **Status:** Twenty-one interface states planned and verified.
- **Objective:** Define what the interface says and what students or staff can do as data and workflow conditions change.
- **Changes and files:** Added the [interface state matrix](PAGES_AND_JOURNEYS.md#interface-states) and checked off Step 2.5 in the [roadmap](../WEBSITE_ROADMAP.md#phase-2--define-pages-and-user-journeys).
- **How it works:** The matrix ties each condition to a visible message and an available action. A load failure takes priority over an empty result. An ended event takes priority over an older registration state.
- **Why this approach:** Accurate status copy helps users recover. Text and keyboard feedback communicate the outcome without relying on color alone.
- **Validation:** VER-035 checked coverage and state precedence against the planned journeys. VER-036 checked the staged plan and linked records.
- **Limitations / remaining work:** These messages and behaviors still need UI components, server responses, and browser accessibility testing.
- **Viva Q&A:** **Why distinguish a failed request from an empty list?** The server may have records even when the request fails. A retry addresses the failure, while an empty result can direct visitors to other content.

### TASK-020 — Create desktop and mobile wireframes

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 2.6.
- **Status:** Fourteen desktop and mobile wireframe pairs planned and verified.
- **Objective:** Show how verified content and the planned workflows fit on wide and narrow pages.
- **Changes and files:** Added [WIREFRAMES.md](WIREFRAMES.md), linked it from the [page plan](PAGES_AND_JOURNEYS.md#wireframes), and checked off Step 2.6 in the [roadmap](../WEBSITE_ROADMAP.md#phase-2--define-pages-and-user-journeys).
- **How it works:** Each wireframe pairs a desktop arrangement with a single-column mobile reading order. Public examples use a real event date and venue, a sourced project, and the club roster. Local recruitment and reviewer screens are marked conditional.
- **Why this approach:** Real copy exposes where titles and calls to action wrap. A simple sketch lets Phase 3 establish identity after the content order and workflows are agreed in the plan.
- **Validation:** VER-037 checked 28 panels and their source content. VER-038 verified the staged links, scope, and roadmap sequence.
- **Limitations / remaining work:** The sketches specify layout and reading order. Phase 3 will add visual styling, and the frontend phases will validate actual browser behavior.
- **Viva Q&A:** **Why use a long event name in mobile wireframes?** Real labels reveal where wrapping needs room. A short placeholder can hide a problem until published content arrives.

### TASK-021 — Assign page actions and close Phase 2

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 2.7 and Phase 2 completion review.
- **Status:** Phase 2 planning complete and verified.
- **Objective:** Give every intended control a destination or observable result and reconcile the complete Phase 2 plan.
- **Changes and files:** Added the [page action matrix](PAGES_AND_JOURNEYS.md#page-actions) and linked the [Phase 2 deliverables](../WEBSITE_ROADMAP.md#phase-2--define-pages-and-user-journeys). Updated the guide's implementation status.
- **How it works:** Each public page has a primary action for its active state. Each administrator action names its destination or write result. Shared navigation and recovery actions use the route and state definitions.
- **Why this approach:** Explicit destinations support consistent desktop and mobile controls. State-specific actions keep an unavailable registration or recruitment path from looking actionable.
- **Validation:** VER-039 checked routes, labels, wireframe controls, and workflow boundaries. VER-040 checked all Phase 2 deliverables in the staged repository.
- **Limitations / remaining work:** Phase 3 will establish visual identity. Later development must implement the actions, permission checks, feedback, and routes before they can be exercised in a browser.
- **Viva Q&A:** **When should an action use a link?** Use links to navigate to a destination. Use buttons for state changes such as opening a menu or saving a draft, with progress and outcome feedback where needed.

### TASK-022 — Recheck Phase 1 and Phase 2 deliverables

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 1 and Phase 2 follow-up audit.
- **Status:** Verified after two workflow corrections.
- **Objective:** Check the pushed phase deliverables together and resolve any gaps in the documented journeys.
- **Changes and files:** Updated the [event and recruitment journeys](PAGES_AND_JOURNEYS.md), the [interface states](PAGES_AND_JOURNEYS.md#interface-states), the [page actions](PAGES_AND_JOURNEYS.md#page-actions), and the [launch recruitment rules](LAUNCH_SCOPE.md#recruitment).
- **How it works:** When both event lists load empty, show one message and link to About. When a local application's result is uncertain, retry the same attempt. Return its saved reference only to the verified applicant, even if the deadline elapsed after the original save. An unsaved attempt still follows the closing time and validation rules.
- **Why this approach:** The event fallback avoids links between two empty sections. Confirmation recovery gives students a reliable receipt without creating a second application or exposing another student's record.
- **Validation:** VER-041 checked the pushed baseline, public source responses, and workflow scenarios. VER-042 rendered the diagrams and checked the staged planning documents and wireframes.
- **Limitations / remaining work:** The direct LinkedIn request was blocked. The portal and social checks covered public page reachability. The application flow remains a design until the frontend and API are implemented.
- **Viva Q&A:** **What happens if the network drops after a local application is saved?** A retry of the same attempt can return the original reference once the university email is verified. A new or unsaved attempt must still meet the cycle rules.

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
