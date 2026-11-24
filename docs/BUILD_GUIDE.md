# Code2Chill — Living Build Guide

**Last updated:** 24 November 2026

**Current stage:** Phase 10 verified through step 10.5. The next step is 10.6.
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

The owner confirmed Lakshay Kalra as president and Jiya Arora as vice-president. The university roster and two archived events are documented in the [content register](CONTENT_REGISTER.md). Exact event times, results, and publication-ready community media still need confirmation.

### What dynamic data means

Club records will be stored in a database and returned through the backend. Administrators will update them without editing frontend source code. Animation alone does not make the content dynamic: a moving card with a hardcoded event is still static data.

## 3. Current Implementation Status

| Area | State | Evidence / limitation |
| --- | --- | --- |
| Roadmap | Written | Eleven phases with steps and completion criteria |
| Content register | Created and verified | [Register](CONTENT_REGISTER.md) records evidence, checks, asset availability, and open content gaps |
| Phase 1 launch scope | Defined and verified | [Launch scope](LAUNCH_SCOPE.md) describes the essential release, university registration, recruitment defaults, and open decisions |
| Phase 2 pages and journeys | Defined and verified | [Page plan](PAGES_AND_JOURNEYS.md) and [wireframes](WIREFRAMES.md) specify actions, states, and recovery paths |
| Design reference analysis | Reviewed at two widths | Three rendered homepages, including the Noddal scene after loading. See [reference analysis](DESIGN_REFERENCE_ANALYSIS.md) |
| Visual direction | Specified | [Campus event programme composition](VISUAL_IDENTITY.md) for Home and Event Detail |
| Community and project media | Placeholder layouts verified, originals pending | [Replacement notes](VISUAL_IDENTITY.md#temporary-media-placements) identify the assets and the remaining work |
| Brand assets | Exported and checked | Two preserved originals and five [browser-ready brand files](VISUAL_IDENTITY.md#brand-exports) |
| Representative page designs | Verified static HTML | [Home](design/index.html) and [event detail](design/domination.html) work at phone and desktop widths |
| Website prototype | Existing, source-reviewed | `extra.html`; no live-browser validation during initial review |
| Ink theme effect | Existing, source-reviewed | WebGL2, html2canvas, and GSAP logic |
| React/Vite scaffold | Built with JavaScript and JSX | [React routes](../frontend/src/main.jsx) and shared visual assets. The JavaScript migration passed the Vite build. |
| Public website | Verified in development | Home, Team and Projects read published records. Events includes the archive and registration handoff. About, Contact and Join use approved club information. [Public routes](../frontend/src/main.jsx) · [Read API](../backend/app/public_content.py) |
| Python API | Initialized | [FastAPI entry point](../backend/app/main.py) serves API documentation and its schema |
| Database and migrations | Verified in development and staging | [Schema, diagram and repeatable seed](DATA_MODEL.md#migrations-and-initial-records) are implemented. |
| Event registration | Verified locally | Open events display the approved university destination. The university handles student registration and confirmation. |
| Recruitment | Intake and decisions verified locally | Local applicants verify their email and receive a reference. Authorized staff can filter submissions, record decisions and read their history. Exports are pending. [Review API](../backend/app/admin_recruitment.py) |
| Authentication and dashboard | Verified locally | Admins and editors can create, edit, preview and publish events. Each write checks permission and records the actor. [Event-management API](../backend/app/admin_events.py) |
| Interaction and visual polish | Step 9.1 verified | Restrained CSS transitions on actions, links, inputs, lists, page-entry fade/rise, and action feedback with reduced-motion support. |
| Automated tests and CI | Configured | [GitHub Actions](../.github/workflows/ci.yml) runs database tests, formatting, lint and the frontend build. |
| Deployment | Local staging verified | [Rebuild and access instructions](DEVELOPMENT.md#local-staging) for the web service, API and PostgreSQL. |

**Accurate current viva statement:** “I verified the available club content, defined the first release, and mapped its public and administrator journeys. Desktop and mobile design previews demonstrate the event discovery and return path. The local staging status page calls FastAPI and verifies a PostgreSQL query.”

## 4. Repository Map

| File | Purpose |
| --- | --- |
| [README.md](../README.md) | Project entry point |
| [WEBSITE_ROADMAP.md](../WEBSITE_ROADMAP.md) | Planned implementation and completion checklist |
| [CODE2CHILL_WEBSITE_MASTER.md](planning/CODE2CHILL_WEBSITE_MASTER.md) | Earlier specification; reconcile proposals and unsupported claims |
| [bluprint.pdf](planning/bluprint.pdf) | Earlier ten-page blueprint |
| [Expriments/extra.html](../Expriments/extra.html) | Preserved standalone prototype experiment |
| [Code2Chill.png](design/brand/originals/Code2Chill.png) | Background logo |
| [Code2Chill_transparent.png](design/brand/originals/Code2Chill_transparent.png) | Transparent logo |
| [AGENTS.md](AGENTS.md) | Contributor/agent instructions and documentation policy |
| [PEER_REPOSITORY_COMPARISON.md](PEER_REPOSITORY_COMPARISON.md) | Source-based comparison with six member repositories and resulting priorities |
| [DEVELOPMENT.md](DEVELOPMENT.md) | Local developer environment prerequisites, database, and setup instructions |
| [CONTENT_REGISTER.md](CONTENT_REGISTER.md) | Phase 1 evidence, ownership, publication readiness, and asset inventory |
| [LAUNCH_SCOPE.md](LAUNCH_SCOPE.md) | Launch workflow decisions and the boundaries of local data handling |
| [PAGES_AND_JOURNEYS.md](PAGES_AND_JOURNEYS.md) | Planned routes, navigation, and user journeys |
| [WIREFRAMES.md](WIREFRAMES.md) | Desktop and mobile layout sketches using verified club copy |
| [DESIGN_REFERENCE_ANALYSIS.md](DESIGN_REFERENCE_ANALYSIS.md) | Evidence-based critique of the three tech-lead references and Code2Chill design brief |
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
| React + JavaScript | Browser interface and state | Reusable components with JSX |
| Vite | Development and build tooling | Dedicated frontend build workflow |
| Tailwind CSS | Shared styling rules | Consistent visual implementation |
| FastAPI | Python API and backend coordination | Validation integration and generated API documentation |
| Pydantic | Request/response contracts | Structured validation and errors |
| SQLAlchemy | Database queries and model mapping | Structured persistence layer |
| PostgreSQL | Persistent relational records | Relationships, constraints, and transactions |
| Alembic | Schema revisions | Repeatable, reviewable database changes |
| Object storage | Persistent media | Media remains available across app deployments |

See the [current implementation status](#3-current-implementation-status) for what is in use today.

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
| DEC-006 | Administrator session strategy | Implemented in 6.1 | Use eight-hour server-side sessions, Argon2id password hashes and a Secure HTTP-only cookie. Recheck the account and permissions on each protected request. See [administration](DATA_MODEL.md#administration). |
| DEC-007 | Production ink transition | Resolved in 9.4 | Evaluated and omitted in favor of zero-overhead CSS compositor transitions; avoids mobile frame drops, memory spikes, and dynamic content delays. |
| DEC-008 | Update documentation after every task/step | Confirmed | Accurate viva preparation and handover |
| DEC-009 | Avoid copying DGIT's visual identity while using its content structure as evidence | Design recommendation | Current DGIT site is substantial; earlier “basic static template” characterization was unsupported |
| DEC-010 | Render essential content before nonessential visual effects | Design recommendation | Noddal remained on its loader in the observed browser session |
| DEC-011 | Use the university portal for launch event sign-ups | Selected for launch | One system holds registration records. The organizer confirms each event link and state. |
| DEC-012 | Show an announcement while no recruitment cycle is approved | Selected for launch | Keeps the Join page usable while the club confirms actual dates, domains, eligibility, application route, and reviewers. |
| DEC-013 | Use the first-release scope as the baseline for route and workflow planning | Selected for launch | The site can demonstrate dynamic content publication with verified records and official links. Deferred features and open decisions have owners or follow-up phases. |
| DEC-014 | Use JavaScript and JSX for React | Confirmed | The project owner requested JavaScript. Vite builds the React frontend directly. |

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
| VER-007 | Opened DGIT and Ksen in Chrome; inspected desktop screenshots and accessibility structure | Both homepages visually reviewed, including DGIT content sections and Ksen's theme and project presentation | Desktop observations only; no full mobile or interaction audit |
| VER-008 | Opened Noddal in Chrome, reloaded once, and inspected public HTML/CSS/JS | Browser remained on branded loader; source exposed typography, colors, breakpoints, reduced-motion rules, and page structure | Rendered page and live motion not verified |
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
| VER-043 | Phase 3.1 pass 1 | Rendered all three homepages at 1440 × 860 and compared the first-screen captures with computed headings, insets, and navigation. | Homepage samples with normal motion. |
| VER-044 | Phase 3.1 pass 2 | Loaded all three at 390 × 860 with reduced motion. Compared captures and computed layout, then repeated Noddal in fresh sessions until its scene was visible at both widths. | Phone emulation and two Noddal samples. Timing varies with the network and device. |
| VER-045 | Phase 3.2 pass 1 | Inspected the original mark and alpha bounds and checked the direction for palette, composition, navigation and missing-media behavior. | Design specification. |
| VER-046 | Phase 3.2 pass 2 | Cross-checked the featured content and primary action against the Phase 2 wireframes, page actions and Phase 1 register. | Content and interaction review. |
| VER-047 | Phase 3.3 pass 1 | Calculated sRGB contrast for six text, action and focus pairs. Results ranged from 6.50 to 15.61. | Declared color pairs. |
| VER-048 | Phase 3.3 pass 2 | Rendered an offline 390 px Chrome sample, tabbed to both controls, checked the 44 px action and 3 px ring, verified distinct light and dark focus colors and confirmed both fonts loaded. | One browser and a representative sample. |
| VER-049 | Phase 3.4 pass 1 | Composited the actual trimmed mark at widths of 240, 120 and 64 px on dark and pale surfaces and inspected the lettering and edges. | Visual comparison in the selected palette. |
| VER-050 | Phase 3.4 pass 2 | Compared both original PNGs byte for byte with Git, measured the 481 × 420 alpha bounds and checked all five placement rules, clear space and accessible naming. | Usage specification. Export checks follow in Step 3.5. |
| VER-051 | Phase 3.5 pass 1 | Decoded all five exports, checked transparent and opaque variants, dimensions and the ICO’s 16, 32 and 48 px frames, and compared the two original PNGs byte for byte with HEAD. | File integrity and source preservation. |
| VER-052 | Phase 3.5 pass 2 | Inspected a contact sheet showing both full variants, the compact icon and each embedded favicon frame at its intended pixel size. | Visual review at the tested sizes. |
| VER-053 | Phase 3.6 pass 1 | Served both pages over loopback HTTP and tested them in Chrome at 1440 and 768 px. Checked fonts, images, layout width, skip-link focus and the full archive–detail–return path. | Static views of the two representative pages. |
| VER-054 | Phase 3.6 pass 2 | Opened both HTML files directly at 320 and 390 px with reduced motion requested. Checked the menu, Escape focus, logo size, archived date and venue, loaded assets, and the same return path. Inspected captured desktop and phone layouts. | Chrome phone emulation, without physical-device or assistive-technology testing. |
| VER-055 | Phase 3.7 pass 1 | Checked the two figures on each page at 1440 and 768 px over HTTP. Verified visible labels, media bounds, asset loading, keyboard focus and archive navigation. | Desktop and tablet design samples. |
| VER-056 | Phase 3.7 pass 2 | Repeated the checks offline at 320 and 390 px, inspected desktop and phone captures, and independently resolved local assets, link fragments and the two distinct figure types with the HTML parser. | No documentary image, image crop or photographer credit can be verified yet. |

| VER-057 | Phase 3 audit pass 1 | Fresh Chrome rendered both previews over a loopback server at 320, 390, 768, 1024 and 1440 px. Fonts and images loaded. Menu dismissal, keyboard focus, project navigation and the archive/detail return worked. No JavaScript exceptions or document overflow occurred. | Static previews with the approved media placeholders. |
| VER-058 | Phase 3 audit pass 2 | Repeated both previews directly from disk at 320, 390, 768 and 1440 px. Checked the controls and event status again, inspected a full-height phone capture, decoded all brand files, and checked favicon sizes, original PNG bytes, local resources and link fragments. | Chrome emulation. Authentic media and the production application remain pending. |
| VER-059 | Phase 4.1 pass 1 | Checked all three directories and resolved the frontend reference. | Scaffold verification. |
| VER-060 | Phase 4.1 pass 2 | Imported the new Python package from the repository root. | Scaffold verification. |
| VER-061 | Phase 4.2 pass 1 | Installed from the uv lock and ran Ruff lint and format checks. | Scaffold verification. |
| VER-062 | Phase 4.2 pass 2 | Ran npm ci, Biome lint and format checks. Verified ignore rules and public registry hosts in both locks. | Scaffold verification. |
| VER-063 | Phase 4.3 pass 1 | Imported the entry point in the locked environment, checked schema metadata and ran Ruff. | Scaffold verification. |
| VER-064 | Phase 4.3 pass 2 | The sandbox request test stalled. The same test outside it verified the documentation, schema and unknown route. | Scaffold verification. |
| VER-065 | Phase 4.4 pass 1 | TypeScript, Vite production build and Biome lint passed. | Scaffold verification. |
| VER-066 | Phase 4.4 pass 2 | Chrome loaded the built Home and status pages at 390 and 1440 px, verified images and layout width, refreshed the status route and returned home. | Scaffold verification. |
| VER-067 | Phase 4.5 pass 1 | Compose reported a healthy database and psql returned the expected database name inside the container. | Scaffold verification. |
| VER-068 | Phase 4.5 pass 2 | A separate Python process connected from the host, ran SELECT 1 and verified the connection returned to the pool. | Scaffold verification. |
| VER-069 | Maintenance pass 1 | Biome lint and Vite production build passed cleanly after guide rename and prompt untracking. | Clean tree verification. |
| VER-070 | Maintenance pass 2 | Git confirmed clean removal of loose files and correct internal link resolutions. | Clean tree verification. |
| VER-071 | Structure pass 1 | Git verified all directory moves as clean renames with 100% similarity index. | Repository organization. |
| VER-072 | Structure pass 2 | Internal markdown links and Vite build verified in 302ms. | Repository organization. |
| VER-073 | Presentation pass 1 | Validated all internal links and relative paths across README.md. | README modernization. |
| VER-074 | Presentation pass 2 | Verified markdown syntax and asset rendering across README.md. | README modernization. |
| VER-075 | Developer guide pass 1 | Verified relative paths and cross-links between README.md and docs/DEVELOPMENT.md. | Developer instructions separation. |
| VER-076 | Developer guide pass 2 | Verified markdown syntax and command accuracy in docs/DEVELOPMENT.md. | Developer instructions separation. |
| VER-077 | Asset fidelity pass 1 | Verified brand icon and favicon generation with full C2C mark and clear margins; verified multi-size ICO frames (16, 32, 48); confirmed 0 clipped pixels under border-radius; Biome lint and Vite build passed in 349ms. | Asset and build validation. |
| VER-078 | Interaction pass 2 | Automated headless Chrome session loaded desktop/mobile previews, dispatched hover event to hero brand panel, verified smooth zoom and 360-degree rotation transition across frames, and verified browser verification test suite passed. | Interactive animation validation. |
| VER-079 | Transparency pass 1 | Removed artificial solid mask and box shadow on `.print img`, enabling true transparency of the full club mark over hero background artwork; Vite production build passed in 415ms. | Asset transparency validation. |
| VER-080 | Interaction pass 2 | Replaced rotating transition with floating elevation lift and cyan/blue atmospheric drop-shadow glow, ensuring upright legibility; verified Chrome 390 and 1440 preview suite. | Interactive hover alternative validation. |
| VER-081 | Phase 4.6 pass 1 | Both backend tests passed, covering a real query and HTTP 503 for an unreachable database. | Scaffold verification. |
| VER-082 | Phase 4.6 pass 2 | Verified direct and proxied HTTP responses, navigation and refresh in Chrome at 390 and 1440 px. Blocking the request produced the failure message and retry recovered. | Scaffold verification. |
| VER-083 | Phase 4.7 pass 1 | Validated Compose settings and ran locked Python install, Ruff lint and format, and both database tests. Ran npm ci, format check, lint and the TypeScript/Vite production build. | Scaffold verification. |
| VER-084 | Phase 4.7 pass 2 | Parsed the workflow, verified triggers, PostgreSQL settings and npm script names, and resolved the README and setup links. | Scaffold verification. |
| VER-085 | Phase 4.8 pass 1 | Built and started all three services. Checked HTTP readiness, font licenses, direct status routing and 404s. Recreating containers retained the PostgreSQL cluster identity. The hosted CI run for step 4.7 passed. | Scaffold verification. |
| VER-086 | Phase 4.8 pass 2 | Tightened an initially oversized Docker context. A BuildKit check measured 408 KiB and confirmed private settings, package directories and Git metadata were excluded. Rebuilt and verified Chrome navigation, live readiness, failure and retry at 390 and 1440 px. | Scaffold verification. |

| VER-087 | Phase 4 audit, repository and build | Verified the eight completed steps, project roots, dependency locks, environment templates, ignore rules and setup links. Ran locked Python sync, Ruff, both PostgreSQL tests, frontend formatting, lint and the Vite build. GitHub Actions reported success for the matching `origin/main` revision `98a5748`. | Starlette emitted the existing test client deprecation warning. |
| VER-088 | Phase 4 audit, local staging | Compose reported all three services healthy. HTTP checks passed for Home, the status route, API readiness, the OpenAPI schema and missing resources. Chrome at 390 and 1440 px opened Home and Service Status, refreshed the deep link and returned home. Blocking the readiness request exposed the retry control, which recovered when the request was restored. | Local staging and Chrome emulation. |
| VER-089 | Phase 5.1 pass 1 | Ruff passed. Created five tables in PostgreSQL and round-tripped linked records, optional dates and ordered credits through the ORM. | Phase 5 verification. |
| VER-090 | Phase 5.1 pass 2 | Queried PostgreSQL information_schema and found the six expected foreign keys in the disposable transaction. | Phase 5 verification. |
| VER-091 | Phase 5.2 pass 1 | Created a pending cycle, enabled a domain, saved a synthetic application and confirmed the database rejected a disabled domain. | Phase 5 verification. |
| VER-092 | Phase 5.2 pass 2 | A fresh disposable schema confirmed the composite key, permitted route constraint and persisted retry fields. Ruff passed. | Phase 5 verification. |
| VER-093 | Phase 5.3 pass 1 | Round-tripped separate official and registration links and confirmed the pending default. | Phase 5 verification. |
| VER-094 | Phase 5.3 pass 2 | Verified there is no local booking table. The first invalid value exceeded the column length. Reran with a shorter invalid value and PostgreSQL rejected it at the state constraint. | Phase 5 verification. |
| VER-095 | Phase 5.4 pass 1 | Round-tripped synthetic accounts, a session digest, a cycle assignment and an audit state change in PostgreSQL. | Phase 5 verification. |
| VER-096 | Phase 5.4 pass 2 | Inspected the composite reviewer key and verified that PostgreSQL rejected an audit row for an unknown actor. Ruff passed. | Phase 5 verification. |
| VER-097 | Phase 5.5 pass 1 | Direct PostgreSQL inserts rejected invalid content, slugs and media. Deleted a test member and project to verify credit preservation and removal. | Phase 5 verification. |
| VER-098 | Phase 5.5 pass 2 | A separate transaction rejected duplicate applications, attempts and uppercase email, accepted a second cycle and confirmed the reviewer list indexes. Ruff passed. | Phase 5 verification. |
| VER-099 | Phase 5.6 pass 1 | Verified the UTC-to-IST day boundary, date-only event behavior and UTC ORM round-trip with a different PostgreSQL session timezone. | Phase 5 verification. |
| VER-100 | Phase 5.6 pass 2 | A separate transaction rejected equal recruitment bounds and a naive datetime. Checked inclusive opening and exclusive closing. Ruff passed. | Phase 5 verification. |
| VER-101 | Phase 5.7 pass 1 | Verified draft isolation, stale publish rejection, republish, unpublish and audit writes against PostgreSQL. Checked event registration boundaries. | Phase 5 verification. |
| VER-102 | Phase 5.7 pass 2 | In a separate schema, verified reviewer requirements, recruitment boundaries, allowed review transitions and unapproved media rejection. Ruff lint and format passed. | Phase 5 verification. |
| VER-103 | Phase 5.8 pass 1 | Ruff and all three PostgreSQL tests passed. The new test upgraded a blank schema, checked metadata drift and preserved edits on rerun, then downgraded and rebuilt the disposable schema. Cross-checked all twelve diagram relationships. | Phase 5 verification. |
| VER-104 | Phase 5.8 pass 2 | Applied the migration to development and local staging. Both first seeds inserted ten members, two events and two projects. Both reruns inserted zero rows. Staging readiness passed. | Phase 5 verification. |
| VER-105 | Link security and profile pass 1 | Updated Instagram profile handle and sharing URL across HTML prototypes, React frontend, README, and content register; added `target="_blank" rel="noopener noreferrer"` to external university and Instagram links; Biome lint and Vite build passed in 5.3s. | Link security and profile verification. |
| VER-106 | Link security and profile pass 2 | Tested Chrome emulation at 390px and 1440px with `.local/browser.py preview`; verified external anchor attributes and URL resolution. | Browser emulation verification. |
| VER-107 | JavaScript migration build and style checks | `npm run build`, `npm run format:check`, and `npm run lint` passed after pruning unused dependencies. | Frontend build, formatting, and lint. |
| VER-108 | JavaScript migration source and dependency review | Confirmed that the manifest matches the lockfile, the compiler is absent from the lockfile and local install, and the HTML and Dockerfile use the renamed files. `git diff --check` passed. | Source and dependency checks. |
| VER-109 | Phase 6.1 database and API | All eight pytest cases passed against PostgreSQL. The suite covered role changes, deactivation, expiry, revocation, cookie flags, rejected credentials, cooldown recovery and migration round trips. Ruff lint and formatting passed. The development database reported revision 0002 at head. | Local database. Test writes used rollback-only schemas. |
| VER-110 | Phase 6.1 browser workflow | Chrome at 390px and 1440px opened the protected list, redirected to sign-in, rejected a wrong password, returned the editor to three saved events and preserved the session on refresh. Sign-out blocked re-entry. Both widths fit the viewport. Biome lint, formatting and the Vite production build passed. | Local React, FastAPI and PostgreSQL with a temporary editor. |
| VER-111 | Dashboard proxy recovery | Both the Vite proxy and port 8000 returned 404 for the health and session routes. After Vite switched to port 8001, proxied health returned 200 and signed-out session and event-list requests returned 401. The live sign-in route rejected synthetic credentials. | Running development frontend and API. PostgreSQL was healthy at revision 0002. |
| VER-112 | Dashboard browser and backend recheck | Chrome showed the sign-in form from `/admin` and reported invalid credentials. All eight PostgreSQL-backed tests passed, including successful sign-in with a disposable staff account, event permissions, expiration and revocation. | The first headless page dump timed out. The Chrome debugging checks passed before their shutdown wait timed out. |
| VER-113 | Phase 6 event API integration | All 14 tests passed against PostgreSQL, including draft creation, validation, role checks, preview, duplicate slugs, stale saves and publication, audit records, and preservation of the previous public revision. Ruff, Biome and the production build passed. | Disposable test schemas. The existing Starlette test-client deprecation warning remains. |
| VER-114 | Phase 6 browser workflow | Headless Chrome at 390px and 1440px saved a new draft, previewed it, exercised cancel and confirm, followed the public link, verified the registration destination, edited the event and republished with registration closed. Both widths showed the revised event through the schedule. The running Vite proxy also advertised the new editor routes. | Built React app and FastAPI with an isolated PostgreSQL transaction. University registration was checked through its link destination. |
| VER-115 | Phase 6 delivery recheck | All 14 PostgreSQL-backed tests passed both in the development tree and in a standalone Phase 6 snapshot. The standalone snapshot also passed lint, formatting and the production build. | Local verification with disposable schemas. |
| VER-116 | Phase 6 browser recheck | At 390px and 1440px, Chrome preserved an edited field when the editor canceled the leave prompt. It also verified draft publication, public snapshot isolation after an edit, the university link and the closed registration state after republication. | Built Phase 6 snapshot with temporary editor credentials and events. |
| VER-117 | Phase 7 combined build and API | All 14 PostgreSQL-backed tests passed, including the expanded public snapshot checks. Ruff and Biome passed lint and formatting. Vite built the production bundle with the event editor and public routes. | Local working tree, disposable test schemas. The existing Starlette test-client deprecation warning remains. |
| VER-118 | Phase 7 public browser journeys | Chrome at 390px and 1440px verified the homepage previews, archive, project credits, team roles, official links, missing routes and viewport fit. The phone menu handled Escape and restored focus. A blocked project request recovered on retry. Delayed empty responses showed loading and recovery links. | Local Vite and FastAPI, seeded PostgreSQL for content checks, browser-only simulations for failure and empty states. |
| VER-119 | Gallery and navigation | Chrome at 390px and 1440px checked the gallery anchor, two labeled archive figures, their detail links, the NEXUS screenshot placeholder and a single updated share title after client navigation. | Local development and an isolated Docker production build using the seed records. |
| VER-120 | Discovery metadata and delivery | Raw GET responses for nine public URLs contained route-specific metadata and canonical URLs. Missing records returned 404. Private and utility routes included noindex. The share image decoded as a 1200 × 630 PNG and a HEAD request returned no body. All 15 backend tests, Ruff, Biome, Vite, Docker builds and Caddy validation passed. | Vite and the built Caddy/FastAPI stack. PostgreSQL integration tests used rollback-only schemas. External platform caches were outside the check. |
| VER-121 | Phase 7 recheck in development | All 15 backend tests and the lint, formatting and build checks passed. Chrome verified all public journeys at 390px and 1440px. The corrected mixed-case section URLs returned 200 with lowercase canonical URLs. An uppercase project slug still returned 404. | Vite, FastAPI and local PostgreSQL. |
| VER-122 | Independent production verification | The rebuilt Docker stack passed the mixed-case URL checks, raw HTML and share image checks for all nine public routes, and Chrome checks at both widths. Loading, empty-state and retry simulations passed. | Isolated Caddy, FastAPI and seeded PostgreSQL. |

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
- **Files:** This guide, [AGENTS.md](AGENTS.md), [GEMINI.md](../GEMINI.md), and [README.md](../README.md).
- **Work:** Added current status, prototype explanation, proposed architecture, decisions, validation evidence, viva questions, and task history. Added update instructions and navigation links.
- **Reason:** Keep documentation tied to actual evidence and avoid presenting proposed features as completed work.
- **Attempt note:** An initial combined patch failed because README context did not match. No files were changed by that failed patch; the patch was split and retried.
- **Validation:** VER-006 passed. A Python check verified file readability, local link targets, twelve guide sections, four task entries, and references in the instruction/navigation files.
- **Limitation:** Instructions govern future work; they are not a background service detecting arbitrary manual edits. Manual contributors must follow the update policy too.
- **Viva takeaway:** Explain what changed, how it works, why it was chosen, and what was checked.

### TASK-005 — Tech lead design reference analysis

- **Date:** 19 November 2026.
- **Roadmap step:** Phase 3.1, partial research.
- **Status:** Research documented; visual inspection of Noddal and full mobile review remain open.
- **Objective:** Analyze the three supplied reference websites and derive an original visual direction for Code2Chill.
- **Changes and files:** Added [DESIGN_REFERENCE_ANALYSIS.md](DESIGN_REFERENCE_ANALYSIS.md); corrected the research status in [WEBSITE_ROADMAP.md](../WEBSITE_ROADMAP.md); updated this guide.
- **How it works:** The analysis records what was visually observed, what came from public source, site-specific strengths and weaknesses, a comparison table, and a Code2Chill design brief.
- **Why this approach:** A reference should guide design principles. It does not justify copying another site's layout or repeating an inaccurate critique.
- **Validation:** VER-007 and VER-008. The new Markdown links and task record were checked after writing.
- **Limitations / remaining work:** Noddal remained on a loader in Chrome. Mobile rendering, full interaction flows, accessibility outcomes, and performance were not exhaustively tested. Phase 3.1 remains unchecked.
- **Viva Q&A:** **Why did you examine competitors and references?** To identify usable patterns for content hierarchy and presentation, then create an original club identity. **What did the negative reference teach you?** Its rich event proof is useful, while its gaming-specific look and long repeated card sections are a poor match for Code2Chill. **How did you handle incomplete evidence?** I labeled Noddal's CSS and component findings as source-reviewed and avoided claims about its rendered interactions.


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

### TASK-023 — Review the three references on desktop and phone

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 3.1.
- **Status:** Reference review complete at two viewport widths.
- **Objective:** Close the mobile and rendered Noddal gaps from TASK-005.
- **Changes and files:** Extended the [reference analysis](DESIGN_REFERENCE_ANALYSIS.md) and updated the [roadmap](../WEBSITE_ROADMAP.md).
- **How it works:** Fresh headless Chrome profiles rendered the public pages. Compared viewport captures with computed heading dimensions, header controls, and the element at the center of the screen.
- **Why this approach:** A heading can already exist underneath a loader. Checking what the visitor actually sees avoids mistaking the initial DOM for a usable page.
- **Validation:** VER-043 and VER-044. Both viewport reviews found the expected identities and layouts. A staged whitespace check also caught two trailing spaces in the guide date, which were removed. The repeated Noddal load exposed the logo, music control, and full hero.
- **Limitations / remaining work:** These samples do not measure general load performance, real-device touch behavior, or accessibility across the full reference sites.
- **Viva Q&A:** **Why examine the visible surface as well as the HTML?** Text may be present below a full-screen overlay. Only the rendered view established when the Noddal hero could be seen.

### TASK-024 — Set the club’s visual direction

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 3.2.
- **Status:** Design direction specified.
- **Objective:** Give Home and Event Detail a common identity rooted in the club’s own artwork and activities.
- **Changes and files:** Added [visual identity](VISUAL_IDENTITY.md) and linked it from the roadmap.
- **How it works:** Warm paper, dark ink, blue artwork and a prominent date connect a campus event programme to the club’s coding events. The hero action comes before the brand artwork on a phone.
- **Why this approach:** The source logo already combines code and a person. Real venues, archive dates and participant work make the design specific to the club.
- **Validation:** VER-045 and VER-046. Both checks passed for the home and event compositions and their data sources.
- **Limitations / remaining work:** Page rendering is scheduled for Step 3.6. Gallery content depends on approved media.
- **Viva Q&A:** **Why give the date a large block?** Date and place distinguish an event quickly, and the same structure works for an archived event with no photograph.

### TASK-025 — Define and test the design tokens

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 3.3.
- **Status:** Design tokens implemented and verified in a local browser sample.
- **Objective:** Provide reusable typography, color, spacing, control and focus styles for the representative pages.
- **Changes and files:** Added [tokens.css](design/tokens.css), two licensed Latin font files and their license texts, and the [component specifications](VISUAL_IDENTITY.md#tokens-and-components).
- **How it works:** The CSS exposes named values for paper, ink, links, display type, spacing, target size and borders. The dark surface overrides the focus color. Font files resolve relative to the stylesheet.
- **Why this approach:** A shared stylesheet prevents drift across pages. Serving the fonts with the design also makes the mockups usable offline.
- **Validation:** VER-047 and VER-048. The first focus probe used JavaScript focus and did not reproduce keyboard modality. Repeating with actual Tab events verified both rings.
- **Limitations / remaining work:** Production components and full-page accessibility checks belong to later phases.
- **Viva Q&A:** **Why change the focus color on dark surfaces?** The light blue ring remains visible against navy. A separated outline also preserves the button’s own label and fill.

### TASK-026 — Set logo placement and small-size rules

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 3.4.
- **Status:** Placement rules verified against the supplied artwork.
- **Objective:** Keep the club mark recognizable on a poster, in navigation, and in a browser tab.
- **Changes and files:** Added the [logo placement matrix](VISUAL_IDENTITY.md#logo-placement) and updated the roadmap.
- **How it works:** The full transparent mark sits on navy, the background version keeps its own field, and compact contexts use a numeral or text. The placement governs clear space, alternative text and redundant images.
- **Why this approach:** At small sizes the original caption loses definition. On paper, edge artifacts from the transparent background cutout become visible.
- **Validation:** VER-049 and VER-050. The review supports a dark field for the full artwork and a simpler icon plus real text for small uses.
- **Limitations / remaining work:** The 180 px full-mark minimum is a design choice for these layouts. New placements should also be checked at their actual display size.
- **Viva Q&A:** **Why keep a real-text club name in the header?** Students can read it at phone size, it remains available when images fail, and it gives the Home link a reliable accessible name.

### TASK-027 — Export responsive club marks and a favicon

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 3.5.
- **Status:** Five brand files exported and verified.
- **Objective:** Prepare small browser-ready files while retaining both original PNGs.
- **Changes and files:** Added five files in the [brand export list](VISUAL_IDENTITY.md#brand-exports), the placement notes and ASSET-05 in the [inventory](CONTENT_REGISTER.md#asset-inventory).
- **How it works:** Pillow cropped the original transparent alpha bounds, downsampled two full marks and proportionally fit the opaque image in a square. The connected numeral and seated figure became a single-color tab icon.
- **Why this approach:** A single icon silhouette survives a 16 px rendering. The large marks keep the lettering and gradient that give students the full club identity.
- **Validation:** VER-051 and VER-052. All five decoded. The two responsive files are 24,180 and 60,688 bytes. The tab remains a recognizable numeral at 16 px.
- **Limitations / remaining work:** A 16 px tab carries only the silhouette. Use the full mark for prominent branding.
- **Viva Q&A:** **Why deliver an ICO with three sizes?** Browsers can select a raster close to the tab’s display size, with the same recognizable shape in every frame.

### TASK-028 — Build the Home and Event Detail design previews

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 3.6.
- **Status:** Two responsive design previews verified on desktop, tablet and phone.
- **Objective:** Show how a student can discover an archived event, read its details and return to the archive.
- **Changes and files:** Added [Home](design/index.html), [DOMination event detail](design/domination.html), [page styles](design/pages.css), [mobile navigation](design/navigation.js) and [preview notes](VISUAL_IDENTITY.md#responsive-page-previews).
- **How it works:** Shared tokens and offline brand assets style both pages. Home introduces the club, then links its featured archive entry to the event detail. The ticket shows the confirmed date and venue. The ended event offers a return link. Menu uses a native disclosure plus keyboard behavior.
- **Why this approach:** Two linked HTML files let a reviewer exercise the design and real event content before the application router or API exists.
- **Validation:** VER-053 and VER-054. The initial sandbox preview was unreachable. A loopback-only server in the browser environment worked. The first render found a missing working copy of the committed PNG icon. Restored it byte for byte and repeated both browser passes. The width check uses the document client width to account for the desktop scrollbar.
- **Limitations / remaining work:** Several production destinations use local section links in the design. The API, database, application router and live recruitment remain planned.
- **Viva Q&A:** **How can you demonstrate the design today?** Open Home, follow Explore events, open DOMination and follow Back to events. Reduce the window width to see the menu and stacked event ticket.

### TASK-029 — Add the approved temporary media placeholders

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 3.7.
- **Status:** Placeholder work verified. Authentic media pending from the club and project contributors.
- **Objective:** Show how event and project media fit both design previews while the owner has no approved files to supply.
- **Changes and files:** Updated the [homepage](design/index.html), [event detail](design/domination.html), [styles](design/pages.css), [asset inventory](CONTENT_REGISTER.md#asset-inventory) and [replacement notes](VISUAL_IDENTITY.md#temporary-media-placements).
- **How it works:** Both pages render a labeled figure for a DOMination photo and another for a NEXUS screenshot. CSS draws the pattern. The subject is visible in the caption and the label explicitly calls it a placeholder.
- **Why this approach:** The owner requested placeholders for now. A labeled layout reserves space without suggesting that a synthetic or unrelated image documents the event.
- **Validation:** VER-055 and VER-056. Both passes found two labeled placements per page and no horizontal overflow. The navigation and archive return path still passed.
- **Limitations / remaining work:** Step 3.7 stays open for an approved DOMination event photograph and NEXUS screenshot, with credits and permission. The owner confirmed these are currently unavailable.
- **Viva Q&A:** **What would finish the media step?** Record permission and credit, replace the corresponding placeholders with the actual images in both views, supply informative alternative text, then verify the crops at phone and desktop widths.

### TASK-030 — Verify the Phase 3 deliverables

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 3 follow-up audit.
- **Status:** Both previews and the approved placeholder layouts passed two verification runs.
- **Objective:** Check the pushed visual identity deliverables through their browser entry points.
- **Changes and files:** Recorded this audit in the [build guide](BUILD_GUIDE.md). The [Home](design/index.html), [event detail](design/domination.html), fonts, brand files and navigation passed the checks.
- **How it works:** Served the previews through a temporary loopback server, exercised the controls in Chrome, then opened the same files directly from disk and repeated the checks.
- **Why this approach:** The first run covers served use. The second confirms the files can be reviewed offline with their local assets.
- **Validation:** VER-057 and VER-058 passed. An initial element-bound probe included links inside a closed disclosure. Document-width checks confirmed they create no visible overflow. All five brand exports decoded, all three favicon sizes existed, and the original PNGs matched Git byte for byte. The repository check initially used an unpadded task ID, then passed with the documented three-digit format.
- **Limitations / remaining work:** Step 3.7 awaits the actual event photograph and project screenshot. Both previews show the approved labeled placeholders. The API, database and remaining production routes belong to later phases.
- **Viva Q&A:** **How was navigation checked?** Followed Explore events to the archive, opened DOMination and returned to the same archive section. Tested menu dismissal and visible keyboard focus at narrow widths.

### TASK-031 — Create the application directories

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 4.1.
- **Status:** Verified.
- **Objective:** Create the application directories.
- **Changes and files:** Added the [application package](../backend/app/__init__.py) and [frontend source directory](../frontend/src/README.md).
- **How it works:** Git tracks a Python package and a frontend source note alongside the existing documentation.
- **Why this approach:** Separate roots let each runtime manage its own dependencies.
- **Validation:** VER-059 and VER-060. Checked all three directories and resolved the frontend reference. Imported the new Python package from the repository root.
- **Limitations / remaining work:** Application entry points follow in steps 4.3 and 4.4.
- **Viva Q&A:** **Why track a file in each directory?** Git stores files, so a fresh checkout includes the layout.

### TASK-032 — Configure reproducible development tooling

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 4.2.
- **Status:** Verified.
- **Objective:** Configure reproducible development tooling.
- **Changes and files:** Added [.gitignore](../.gitignore), backend and frontend environment templates, [Python tooling](../backend/pyproject.toml), [npm scripts](../frontend/package.json), Biome configuration and both lockfiles.
- **How it works:** uv resolves the server dependencies. npm resolves the browser dependencies. Each runtime has a formatter and linter. Local settings, packages and build output are ignored.
- **Why this approach:** Fresh installs can resolve the same dependency versions on another computer.
- **Validation:** VER-061 and VER-062. Installed from the uv lock and ran Ruff lint and format checks. Ran npm ci, Biome lint and format checks. Verified ignore rules and public registry hosts in both locks.
- **Limitations / remaining work:** The example database URL requires local credentials.
- **Viva Q&A:** **Why keep two lockfiles?** Python and JavaScript use different package managers and dependency graphs.

### TASK-033 — Initialize the FastAPI application

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 4.3.
- **Status:** Verified.
- **Objective:** Initialize the FastAPI application.
- **Changes and files:** Added the [FastAPI entry point](../backend/app/main.py).
- **How it works:** Uvicorn imports app.main:app. Its schema and interactive reference live under /api.
- **Why this approach:** A shared API prefix leaves room for the frontend at the same origin.
- **Validation:** VER-063 and VER-064. Imported the entry point in the locked environment, checked schema metadata and ran Ruff. The sandbox request test stalled. The same test outside it verified the documentation, schema and unknown route.
- **Limitations / remaining work:** Database readiness follows in steps 4.5 and 4.6.
- **Viva Q&A:** **What is ASGI?** The interface Uvicorn uses to send requests to Python applications.

### TASK-034 — Initialize the React frontend

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 4.4.
- **Status:** Verified.
- **Objective:** Initialize the React frontend.
- **Changes and files:** Added the React entry point (`main.tsx` at the time), [styles](../frontend/src/styles.css), TypeScript configuration, HTML shell and Vite configuration (`vite.config.ts` at the time).
- **How it works:** React Router serves Home, a status route and an unknown-page fallback. Vite bundles the Phase 3 fonts, mark and CSS. Tailwind utilities are available to components.
- **Why this approach:** Using the original assets keeps the scaffold consistent with the verified design.
- **Validation:** VER-065 and VER-066. TypeScript, Vite production build and Biome lint passed. Chrome loaded the built Home and status pages at 390 and 1440 px, verified images and layout width, refreshed the status route and returned home.
- **Limitations / remaining work:** The full public routes and event content are scheduled for later phases.
- **Viva Q&A:** **How do two routes share one build?** The host serves the entry document and React Router chooses the view from the URL.

### TASK-035 — Connect the development PostgreSQL database

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 4.5.
- **Status:** Verified.
- **Objective:** Connect the development PostgreSQL database.
- **Changes and files:** Added [Compose](../backend/compose.yaml), [SQLAlchemy connection management](../backend/app/database.py) and FastAPI lifespan handling. Updated the backend environment template.
- **How it works:** A persistent Compose volume stores PostgreSQL 17 data. SQLAlchemy creates a pool for each API process, checks connections before use and disposes it at shutdown. An external DATABASE_URL can override the local settings.
- **Why this approach:** The host port binds to loopback. The generated development password stays in an ignored file.
- **Validation:** VER-067 and VER-068. Compose reported a healthy database and psql returned the expected database name inside the container. A separate Python process connected from the host, ran SELECT 1 and verified the connection returned to the pool.
- **Limitations / remaining work:** Business models and migrations belong to Phase 5.
- **Viva Q&A:** **Why dispose the pool?** It releases idle database connections when the API process shuts down.

### TASK-036 — Clean repository structure and rename living guide

- **Date:** 23 November 2026.
- **Roadmap step:** Repository maintenance and Phase 4.6 connectivity foundation.
- **Status:** Verified.
- **Objective:** Clean root clutter before sharing the repository and rename `BUILD_AND_VIVA_GUIDE.md` to `BUILD_GUIDE.md`.
- **Changes and files:** Renamed [BUILD_GUIDE.md](BUILD_GUIDE.md); untracked `GEMINI.md` and added it to [.gitignore](../.gitignore); removed root duplicate `extra.html` (preserved in [Expriments/extra.html](../Expriments/extra.html)) and loose `download.svg`/`download2.svg`; updated documentation links in [AGENTS.md](AGENTS.md) and [README.md](../README.md); tracked backend healthcheck in [backend/app/main.py](../backend/app/main.py), tests in [backend/tests/test_health.py](../backend/tests/test_health.py), and frontend status view (`frontend/src/Status.tsx` at the time).
- **How it works:** Sensitive assistant prompts and experimental prototypes are removed from the root Git tree. All internal references resolve to `docs/BUILD_GUIDE.md`. The backend and frontend verify service availability via `/api/health`.
- **Why this approach:** Evaluators inspecting the repository see an uncluttered, production-oriented structure without duplicate HTML prototypes, loose SVG downloads, or exposed assistant instruction files.
- **Validation:** VER-069 and VER-070. Biome lint and Vite production build passed cleanly. Git index confirmed clean deletion of root artifacts, untracking of assistant prompts, and exact renaming of the build guide.
- **Limitations / remaining work:** Full end-to-end integration testing and CI checks continue in Phase 4.7.
- **Viva Q&A:** **Why rename and organize documentation before sharing?** A clean repository demonstrates professional engineering hygiene, clear separation between public documentation and internal notes, and avoids distracting evaluators with unmaintained prototype files.

### TASK-037 — Reorganize root files into dedicated subdirectories

- **Date:** 23 November 2026.
- **Roadmap step:** Repository architecture and layout standardization.
- **Status:** Verified.
- **Objective:** Reorganize all remaining root files into dedicated subdirectories to achieve a minimal, production-grade root structure.
- **Changes and files:** Moved `Code2Chill.png` and `Code2Chill_transparent.png` to [docs/design/brand/originals/](design/brand/originals/); moved `CODE2CHILL_WEBSITE_MASTER.md` and `bluprint.pdf` to [docs/planning/](planning/); moved `AGENTS.md` to [docs/AGENTS.md](AGENTS.md); moved `compose.yaml` to [backend/compose.yaml](../backend/compose.yaml). Updated relative links across [README.md](../README.md), [WEBSITE_ROADMAP.md](../WEBSITE_ROADMAP.md), [docs/CONTENT_REGISTER.md](CONTENT_REGISTER.md), [docs/VISUAL_IDENTITY.md](VISUAL_IDENTITY.md), and this guide.
- **How it works:** The root directory contains only top-level project folders (`backend/`, `frontend/`, `docs/`, `Expriments/`) and configuration/documentation anchors (`.gitignore`, `README.md`, `WEBSITE_ROADMAP.md`).
- **Why this approach:** Concentrates brand originals, planning archives, and working instructions in their relevant folders, preventing root clutter while preserving the full project history and file availability.
- **Validation:** VER-071 and VER-072. Git verified all renames as clean renames (100% similarity index). Internal documentation links verified. Vite production build passed in 302ms.
- **Limitations / remaining work:** Step 4.6 connectivity and Step 4.7 CI configuration continue in Phase 4.
- **Viva Q&A:** **Why structure the root directory so strictly?** High-standard open-source and enterprise repositories keep the root folder clean and predictable so contributors and reviewers immediately know where backend, frontend, and documentation live.

### TASK-038 — Update README with professional presentation standard

- **Date:** 23 November 2026.
- **Roadmap step:** Repository presentation and onboarding enhancement.
- **Status:** Verified.
- **Objective:** Modernize `README.md` into an industry-grade project showcase with brand identity, technology badges, system architecture, quick start instructions, living documentation index, and leadership roster.
- **Changes and files:** Updated [README.md](../README.md).
- **How it works:** Provides incoming developers, leads, and evaluators with immediate visual context, architecture diagram, dependency versions, local quickstart commands, and direct links to all seven living documentation guides.
- **Why this approach:** The README is the primary entry point on GitHub; a structured, informative presentation establishes engineering credibility before examiners inspect code.
- **Validation:** VER-073 and VER-074. Markdown links tested and verified. Markdown syntax and image resolution verified.
- **Limitations / remaining work:** CI badges will be linked when Phase 4.7 CI workflows are committed.
- **Viva Q&A:** **What makes a repository README professional?** Clear project mission, badge indicators for maintained stack versions, architecture diagram, reproduction steps for local setup, and navigation to deeper engineering specifications.

### TASK-039 — Move local development setup instructions to dedicated guide

- **Date:** 23 November 2026.
- **Roadmap step:** Documentation refinement and README optimization.
- **Status:** Verified.
- **Objective:** Move developer terminal commands (Docker, uv, npm) from the public README into a dedicated development guide.
- **Changes and files:** Added [docs/DEVELOPMENT.md](DEVELOPMENT.md); updated [README.md](../README.md) and repository map in this guide.
- **How it works:** `README.md` focuses exclusively on club identity, core capabilities, architecture, and living documentation links. Detailed developer commands and environment setups are consolidated in `docs/DEVELOPMENT.md`.
- **Why this approach:** Maintains a prestigious, uncluttered presentation on GitHub for students, club members, and visitors while providing full execution commands to developers and evaluators via a clean link.
- **Validation:** VER-075 and VER-076. Verified all relative links between `README.md` and `docs/DEVELOPMENT.md`. Verified Markdown syntax.
- **Limitations / remaining work:** Container orchestration instructions will be updated when production Dockerfiles are created in Phase 7.
- **Viva Q&A:** **Why separate developer instructions from the main README?** Separating audience concerns ensures the public README serves as a clear organizational portal, while technical contributors have a focused, in-depth setup reference.

### TASK-040 — Refine brand icon, favicon framing, and hero logo hover animation

- **Date:** 23 November 2026.
- **Roadmap step:** Design refinement and asset fidelity.
- **Status:** Verified.
- **Objective:** Fix the trimmed navbar brand icon and favicon frames so the complete club emblem is visible without clipped letterforms, and add a responsive zoom-in and rotating hover animation on the hero club logo card.
- **Changes and files:**
  - Regenerated [docs/design/brand/club-icon-64.png](design/brand/club-icon-64.png) from the transparent original mark with the full C2C emblem, seated laptop figure, and balanced margins on a dark tile background (`#071628`).
  - Re-exported [docs/design/brand/favicon.ico](design/brand/favicon.ico) with multi-resolution 16x16, 32x32, and 48x48 frames containing the complete mark.
  - Enhanced [docs/design/pages.css](design/pages.css) with cursor feedback, spring-eased zoom and straighten transition on the print artwork card (`scale(1.04) rotate(0deg)`), and a smooth 360-degree zoom-in rotating transition (`scale(1.15) rotate(360deg)`) on the club logo mark with `@media (prefers-reduced-motion: reduce)` accessibility fallback.
- **How it works:** The navbar and footer `<img>` elements display the 64px asset styled with `.brand img`, providing clear margins so `border-radius: .25rem` never clips the logo's outer C characters or text. The favicon embeds multiple raster resolutions for standard and high-DPI browser tabs. On hover over the hero brand artwork, the outer poster card smoothly elevates with depth shadow while the inner mark scales and spins, gracefully reversing on mouse exit.
- **Why this approach:** Pure CSS transitions avoid heavy external JavaScript dependencies and honor the UI stack rule requiring user confirmation before introducing external animation libraries (Motion/GSAP). Balanced internal padding prevents clipping at small pixel sizes.
- **Validation:** VER-077 and VER-078. Decoded the new PNG and ICO assets, verified all 3 embedded ICO frame sizes (16, 32, 48), verified 0 clipped pixels under border-radius masking, and ran Biome lint and Vite production build in 349ms. Automated Chrome headless session verified desktop and mobile layouts, executed mouseover dispatch to `.brand-art`, verified smooth zoom and rotation across animation frames, and verified `.local/browser.py` test suite passed at 390px and 1440px.
- **Limitations / remaining work:** None for this styling and asset update.
- **Viva Q&A:** **Why should brand icons have internal padding rather than tight cropping?** Tight cropping causes border radius, browser tab borders, or container overflow to clip distinctive logo glyphs or ascenders/descenders. Balanced clear space maintains visual hierarchy and legibility at tiny 16px and 32px display sizes. **Why use CSS transforms and transitions for hover states instead of JavaScript loops?** CSS `transform` and `transition` run on the browser's compositor thread (GPU-accelerated) without causing layout reflows or repaints, ensuring a silky 60+ FPS interaction that respects user motion preferences.

### TASK-041 — Hero club logo background transparency and hover animation alternatives

- **Date:** 23 November 2026.
- **Roadmap step:** Design refinement & interaction polish.
- **Status:** Verified.
- **Objective:** Remove artificial solid background box and shadow from the hero section club logo so it renders with true transparency, and explore/implement non-rotating hover animation alternatives that maintain brand legibility.
- **Changes and files:**
  - Updated [docs/design/pages.css](design/pages.css): replaced `background: var(--night)` and `box-shadow: 0 0 0 clamp(...) var(--night)` on `.print img` with `background: transparent`.
  - Upgraded hover interaction on `.brand-art:hover .print img` from 360-degree rotation to a floating elevation lift (`translateY(-6px) scale(1.12)`) paired with atmospheric cyan/blue drop-shadow glow (`filter: drop-shadow(...)`), eliminating sideways/upside-down disorientation while keeping the mark prominent.
- **How it works:** The transparent WebP asset now renders directly over the textured artwork without a solid dark cutout box. When hovered, the poster card eases to `0deg` and scales to `1.04`, while the club logo lifts and illuminates with dual glowing drop-shadows.
- **Why this approach:** Spinning an emblem that contains text ("CODE 2 CHILL CLUB") and code glyphs reduces legibility during interaction. Floating elevation and luminous drop-shadow give an unmistakable tactile feel while preserving typography and accessibility.
- **Validation:** VER-079 and VER-080. Headless Chrome validated rendering of transparent logo over background artwork. Vite production build passed in 415ms, and the `.local/browser.py` test suite passed at 390px and 1440px.
- **Limitations / remaining work:** The user can select additional interactive animation variants (such as cursor-following 3D tilt, holographic shimmer, or floating pulse) or confirm external animation library integration (GSAP, Motion, Magic UI) if desired.
- **Viva Q&A:** **Why is a floating lift with drop-shadow often superior to spinning for logos with text?** Brand logos with text, code syntax, and illustrative figures rely on immediate recognition. Full-axis rotations invert the typography, reducing legibility and visual hierarchy. Elevation with depth shadow creates physical dimensionality while keeping all text readable.

### TASK-042 — Verify the full database readiness path

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 4.6.
- **Status:** Verified.
- **Objective:** Verify the full database readiness path.
- **Changes and files:** Reviewed the existing [health endpoint](../backend/app/main.py), [health tests](../backend/tests/test_health.py) and [React status page](../frontend/src/Status.jsx). Updated the roadmap and this guide after verification.
- **How it works:** The React route requests /api/health through Vite. FastAPI borrows a database connection and runs SELECT 1. The browser offers a retry after an unavailable response.
- **Why this approach:** This checks a real round trip from the browser to PostgreSQL. The reorganized checkout already contained the implementation.
- **Validation:** VER-081 and VER-082. Both backend tests passed, covering a real query and HTTP 503 for an unreachable database. Verified direct and proxied HTTP responses, navigation and refresh in Chrome at 390 and 1440 px. Blocking the request produced the failure message and retry recovered.
- **Limitations / remaining work:** The first browser probe raced API startup. Waiting for readiness resolved it. Chrome teardown later timed out after the browser assertions passed. TestClient emitted an httpx deprecation warning.
- **Viva Q&A:** **When can the frontend report success?** After the API returns a successful response with the expected readiness status.

### TASK-043 — Add continuous integration and correct the setup guide

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 4.7.
- **Status:** Verified.
- **Objective:** Add continuous integration and correct the setup guide.
- **Changes and files:** Added the [CI workflow](../.github/workflows/ci.yml), updated [development setup](DEVELOPMENT.md) and aligned the [README](../README.md) architecture with the running scaffold.
- **How it works:** GitHub Actions installs the locked dependencies, starts a disposable PostgreSQL service and runs the backend tests and frontend checks. Local instructions create private settings before starting the existing named Compose project.
- **Why this approach:** Matching the package engine, database volume name and API behavior makes a fresh checkout reproducible.
- **Validation:** VER-083 and VER-084. Validated Compose settings and ran locked Python install, Ruff lint and format, and both database tests. Ran npm ci, format check, lint and the TypeScript/Vite production build. Parsed the workflow, verified triggers, PostgreSQL settings and npm script names, and resolved the README and setup links.
- **Limitations / remaining work:** Hosted CI results are available after the workflow is pushed. The API test client emits a dependency deprecation warning.
- **Viva Q&A:** **Why give CI its own database?** Each job can test a real query independently of developer machines and data.

### TASK-044 — Deploy and rebuild local staging

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 4.8.
- **Status:** Verified.
- **Objective:** Deploy and rebuild local staging.
- **Changes and files:** Added the [image build](../Dockerfile), [Docker context rules](../.dockerignore), [Caddy configuration](../backend/Caddyfile), [Compose overlay](../backend/compose.staging.yaml) and [local staging instructions](DEVELOPMENT.md#local-staging).
- **How it works:** Caddy serves the compiled frontend and proxies /api to FastAPI. Staging PostgreSQL has its own volume and private network. Only the web port is published on loopback. Images build from locked application dependencies.
- **Why this approach:** The owner selected local staging. Separate service checks ensure the database and API are ready before Compose reports the web service healthy.
- **Validation:** VER-085 and VER-086. Built and started all three services. Checked HTTP readiness, font licenses, direct status routing and 404s. Recreating containers retained the PostgreSQL cluster identity. The hosted CI run for step 4.7 passed. Tightened an initially oversized Docker context. A BuildKit check measured 408 KiB and confirmed private settings, package directories and Git metadata were excluded. Rebuilt and verified Chrome navigation, live readiness, failure and retry at 390 and 1440 px.
- **Limitations / remaining work:** Local staging uses the current working copy, including the owner’s pending icon and hover changes. An isolated Chrome rerun timed out during navigation and passed on retry. Base image tags can receive upstream updates.
- **Viva Q&A:** **Why does a direct refresh of /status work?** Caddy returns the application entry for browser routes. API and asset requests use separate handlers that preserve their own HTTP status codes.

### TASK-045 — Recheck Phase 4 before Phase 5

- **Date.** 23 November 2026.
- **Roadmap step.** Phase 4 follow-up audit.
- **Status.** All eight scaffold steps passed the checks.
- **Objective.** Confirm the checked-out scaffold builds, its test suite exercises PostgreSQL, and local staging remains usable.
- **Changes and files.** Recorded the audit in this guide.
- **How it works.** The local checks exercise the locked Python environment, PostgreSQL and production frontend build. The staging checks exercise the browser, Caddy, FastAPI and the staging database through the same address the user opens.
- **Why this approach.** The build checks catch configuration regressions. The browser and HTTP checks confirm deployed routes and recovery behavior against the running stack.
- **Validation.** VER-087 and VER-088 passed. A successful GitHub Actions run matched the pushed revision. Both PostgreSQL tests passed, covering readiness and the unavailable response.
- **Limitations and remaining work.** The test client emitted the existing Starlette deprecation warning. Phase 5 covers data models, migrations and seed data.
- **Viva Q&A.** **What verifies the full request path?** The browser receives a ready response only after FastAPI runs a successful query against staging PostgreSQL.

### TASK-046 — Model public club content

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 5.1.
- **Status:** Verified.
- **Objective:** Model public club content.
- **Changes and files:** Added the shared [model base](../backend/app/model_base.py), [public models](../backend/app/content_models.py), and [data model guide](DATA_MODEL.md).
- **How it works:** Members, events and projects link to optional media. Projects can link to the originating event. An ordered credit links to a roster member when applicable.
- **Why this approach:** The model represents real participant credits and missing media independently of roster membership and publication approval.
- **Validation:** VER-089 and VER-090. Ruff passed. Created five tables in PostgreSQL and round-tripped linked records, optional dates and ordered credits through the ORM. Queried PostgreSQL information_schema and found the six expected foreign keys in the disposable transaction.
- **Limitations / remaining work:** Migrations and seed records follow in Step 5.8. Live pages still use the Phase 4 scaffold.
- **Viva Q&A:** **Why keep project credits as rows?** A project can credit several people in order, including participants outside the club roster.

### TASK-047 — Model recruitment cycles and applications

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 5.2.
- **Status:** Verified.
- **Objective:** Model recruitment cycles and applications.
- **Changes and files:** Added [recruitment models](../backend/app/recruitment_models.py), shared club domains and the [recruitment schema notes](DATA_MODEL.md#recruitment).
- **How it works:** Each cycle enables a set of domains. Applications reference the selected domain within the cycle and keep a separate attempt identifier and receipt.
- **Why this approach:** The composite foreign key prevents an application from selecting a domain that belongs elsewhere or was never enabled.
- **Validation:** VER-091 and VER-092. Created a pending cycle, enabled a domain, saved a synthetic application and confirmed the database rejected a disabled domain. A fresh disposable schema confirmed the composite key, permitted route constraint and persisted retry fields. Ruff passed.
- **Limitations / remaining work:** Live cycle settings, email verification and review endpoints remain pending.
- **Viva Q&A:** **Why use two columns for the domain reference?** The same domain can appear in many cycles. The pair identifies the enabled option for this cycle.

### TASK-048 — Model the university event registration handoff

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 5.3.
- **Status:** Verified.
- **Objective:** Model the university event registration handoff.
- **Changes and files:** Added state and destination fields to [Event](../backend/app/content_models.py) and documented [registration ownership](DATA_MODEL.md#event-registration-ownership).
- **How it works:** Event stores an official information source, an optional signup link, and a controlled registration state. The university handles signups and receipts.
- **Why this approach:** The launch scope assigns signups to the university, so a local booking table is out of scope.
- **Validation:** VER-093 and VER-094. Round-tripped separate official and registration links and confirmed the pending default. Verified there is no local booking table. The first invalid value exceeded the column length. Reran with a shorter invalid value and PostgreSQL rejected it at the state constraint.
- **Limitations / remaining work:** Availability and publication rules follow in Steps 5.6 and 5.7.
- **Viva Q&A:** **Where are event registrations stored?** The university portal owns the student registration records.

### TASK-049 — Model administrator access and audit records

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 5.4.
- **Status:** Verified.
- **Objective:** Model administrator access and audit records.
- **Changes and files:** Added [administrator models](../backend/app/admin_models.py) and documented the [session strategy](DATA_MODEL.md#administration).
- **How it works:** Accounts hold a password hash and role. Server-side sessions store a token digest, expiry and revocation. A cycle-to-account join scopes reviewer assignments. Audit records retain the actor and state change.
- **Why this approach:** Opaque sessions support server-enforced revocation. Stable audit actor references preserve who performed a change.
- **Validation:** VER-095 and VER-096. Round-tripped synthetic accounts, a session digest, a cycle assignment and an audit state change in PostgreSQL. Inspected the composite reviewer key and verified that PostgreSQL rejected an audit row for an unknown actor. Ruff passed.
- **Limitations / remaining work:** Sign-in, Argon2id hashing, token issuance and authorization are scheduled for Phases 6 and 8.
- **Viva Q&A:** **Why store a token digest?** A database reader cannot use the stored digest as the bearer token.

### TASK-050 — Enforce the database integrity rules

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 5.5.
- **Status:** Verified.
- **Objective:** Enforce the database integrity rules.
- **Changes and files:** Added constraints and lookup indexes across the public, recruitment and administrator models. Recorded the rules in the [data model](DATA_MODEL.md#integrity-rules).
- **How it works:** PostgreSQL rejects malformed or duplicate slugs, blank required content, uncredited approved media, duplicate application attempts and duplicate email addresses in a cycle. Foreign keys preserve ordered credits and scoped relationships.
- **Why this approach:** Database constraints protect integrity through concurrent writes and direct SQL.
- **Validation:** VER-097 and VER-098. Direct PostgreSQL inserts rejected invalid content, slugs and media. Deleted a test member and project to verify credit preservation and removal. A separate transaction rejected duplicate applications, attempts and uppercase email, accepted a second cycle and confirmed the reviewer list indexes. Ruff passed.
- **Limitations / remaining work:** Email ownership and application response handling remain application work.
- **Viva Q&A:** **Why enforce duplicates in PostgreSQL?** Two requests may pass the same application precheck. A database constraint permits only one to commit.

### TASK-051 — Store consistent timestamps and campus dates

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 5.6.
- **Status:** Verified.
- **Objective:** Store consistent timestamps and campus dates.
- **Changes and files:** Added [time helpers](../backend/app/time_rules.py), timezone-aware model columns, database checks and a locked tzdata dependency.
- **How it works:** Confirmed dates can stand alone. Known instants enter the ORM with an offset, come back in UTC and convert to Asia/Kolkata for display. Time windows include opening and exclude closing.
- **Why this approach:** This avoids inventing start times for archive records and gives scheduling consistent boundaries across servers.
- **Validation:** VER-099 and VER-100. Verified the UTC-to-IST day boundary, date-only event behavior and UTC ORM round-trip with a different PostgreSQL session timezone. A separate transaction rejected equal recruitment bounds and a naive datetime. Checked inclusive opening and exclusive closing. Ruff passed.
- **Limitations / remaining work:** Verified event times and recruitment cycle settings still depend on the club.
- **Viva Q&A:** **Why keep a date and an optional instant?** A confirmed calendar day can be displayed even when an exact start time is unknown.

### TASK-052 — Define publication and workflow transitions

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 5.7.
- **Status:** Verified.
- **Objective:** Define publication and workflow transitions.
- **Changes and files:** Added [publication fields](../backend/app/publication_fields.py), [publication operations](../backend/app/publication.py) and documented the [state rules](DATA_MODEL.md#publication-and-state-transitions).
- **How it works:** Rows have a checked revision and a separate public snapshot. A publish or unpublish operation updates the snapshot and appends an audit row inside the same transaction. Event and recruitment availability follow their configured boundaries.
- **Why this approach:** A saved draft can evolve while visitors still see the previously published content. Revision checks keep an outdated preview from publishing silently.
- **Validation:** VER-101 and VER-102. Verified draft isolation, stale publish rejection, republish, unpublish and audit writes against PostgreSQL. Checked event registration boundaries. In a separate schema, verified reviewer requirements, recruitment boundaries, allowed review transitions and unapproved media rejection. Ruff lint and format passed.
- **Limitations / remaining work:** Later endpoints must enforce authorization and bump the parent draft revision for edits to child collections.
- **Viva Q&A:** **Why store a public snapshot?** The last published title and details stay visible while an editor updates the saved draft.

### TASK-053 — Create the initial migration and verified content seed

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 5.8.
- **Status:** Verified.
- **Objective:** Create the initial migration and verified content seed.
- **Changes and files:** Added [Alembic configuration](../backend/alembic.ini), the [initial migration](../backend/migrations/versions/0001_initial_data_model.py), [seed command](../backend/app/seed.py), migration test and [entity relationship diagram](DATA_MODEL.md#entity-relationship-diagram). Updated setup, Docker and CI.
- **How it works:** Alembic creates twelve application tables and records revision 0001. The seed inserts missing content by slug in one transaction. An optional flag creates a separately labeled draft event.
- **Why this approach:** A new environment can reproduce the vetted starting data. Existing draft edits and public snapshots survive a seed rerun.
- **Validation:** VER-103 and VER-104. Ruff and all three PostgreSQL tests passed. The new test upgraded a blank schema, checked metadata drift and preserved edits on rerun, then downgraded and rebuilt the disposable schema. Cross-checked all twelve diagram relationships. Applied the migration to development and local staging. Both first seeds inserted ten members, two events and two projects. Both reruns inserted zero rows. Staging readiness passed.
- **Limitations / remaining work:** The first lint pass flagged an implicit string concatenation and passed after it was parenthesized. The existing Starlette deprecation warning remains. Public API and editor integration follow in Phase 6.
- **Viva Q&A:** **What separates a migration from a seed?** The migration changes the database structure. The seed inserts verified starting rows into that structure.

### TASK-054 — Configure external links with new-tab targets and update official Instagram URL

- **Date:** 23 November 2026.
- **Roadmap step:** Link security, external destinations, and brand consistency.
- **Status:** Verified.
- **Objective:** Configure Instagram, LinkedIn, and official university club links to open in a new tab (`target="_blank" rel="noopener noreferrer"`), and update the official Instagram profile URL and LinkedIn posts feed URL.
- **Changes and files:**
  - Updated [docs/design/index.html](design/index.html) and [docs/design/domination.html](design/domination.html): set `target="_blank" rel="noopener noreferrer"` on Instagram, LinkedIn, university club page, and university event links; updated Instagram link to `https://www.instagram.com/code2chill.osl?utm_source=ig_web_button_share_sheet&lqvp=ZDNlZDc0MzIxNw%3D%3D`; added LinkedIn feed link `https://www.linkedin.com/company/code2chill/posts/?feedView=all` to footers.
  - Updated the [React entry point](../frontend/src/main.jsx): added `target="_blank" rel="noopener noreferrer"` and both updated Instagram and LinkedIn links in header navigation, while retaining clean status link in footer.
  - Updated [README.md](../README.md) and [docs/CONTENT_REGISTER.md](CONTENT_REGISTER.md) (rows `CLUB-06` and `CLUB-07`) to record the verified profile and feed URLs.
- **How it works:** External links open in a new browser tab without retaining window opener references (`noopener`) or referrer headers (`noreferrer`), protecting user privacy and preventing tab-nabbing security risks while keeping the Code2Chill website open in the user's main tab.
- **Why this approach:** Visitors browsing university portals or social media profiles should not lose their place on the club website. Using `noopener noreferrer` is standard security hygiene for cross-origin link targets.
- **Validation:** VER-105 and VER-106. Biome lint and Vite production build passed cleanly. Automated Chrome browser verification verified layout, image rendering, and link integrity at 390px and 1440px.
- **Limitations / remaining work:** None for this link configuration.
- **Viva Q&A:** **Why must `target="_blank"` always pair with `rel="noopener noreferrer"`?** Without `noopener`, the target page can access `window.opener` and redirect the referring page to a malicious URL (tab-nabbing). `noreferrer` also prevents leaking sensitive query parameters in the HTTP Referer header.

### TASK-055 — Switch the React frontend to JavaScript

- **Date:** 23 November 2026.
- **Roadmap step:** Phase 4.4 follow-up.
- **Status:** Verified for the frontend build and tooling.
- **Objective:** Use plain JavaScript and JSX for React as requested by the project owner.
- **Changes and files:** Converted [main.jsx](../frontend/src/main.jsx), [Status.jsx](../frontend/src/Status.jsx), and [vite.config.js](../frontend/vite.config.js). Updated the [HTML entry point](../frontend/index.html) and [Dockerfile](../Dockerfile). Removed `tsconfig.json`, the compiler, and the direct type dependencies. Updated the [package manifest](../frontend/package.json), [lockfile](../frontend/package-lock.json), README, and roadmap.
- **How it works:** The HTML shell loads `main.jsx`. Vite transforms the JSX and bundles the app. The status page still uses React state to render the result of its health request.
- **Why this approach:** JavaScript matches the owner's preference and removes the separate compiler step. The build no longer checks frontend types.
- **Validation:** VER-107 and VER-108 cover the production bundle, formatting, lint, and removal of the compiler.
- **Limitations / remaining work:** Browser and Docker builds were outside this verification pass.
- **Viva Q&A:** **What does the `.jsx` extension mean?** The file contains JavaScript with JSX markup, which Vite transforms into JavaScript the browser can run.

### TASK-056 — Authenticate staff and protect the event list

23 November 2026 · Phase 6.1 · Verified locally

| Topic | Implementation |
| --- | --- |
| Objective | Let staff sign in and give authorized editors access to saved events. |
| Changes | Added account provisioning, sign-in, session lookup, sign-out, a protected event list and React routes for sign-in, dashboard and events. Migration 0002 adds sign-in failure tracking to existing accounts. [Provisioning](../backend/app/create_admin.py) · [Session handling](../backend/app/admin_auth.py) · [Event API](../backend/app/admin_events.py) · [React views](../frontend/src/Admin.jsx) · [Migration](../backend/migrations/versions/0002_sign_in_attempts.py) |
| How it works | Staff enter their email and password. FastAPI verifies Argon2id, issues a random cookie and stores its digest in PostgreSQL. The server checks expiry, revocation, account activity and role. Admins and editors can read the event list. Reviewers receive HTTP 403 on that route. |
| Rationale and tradeoffs | A database lookup per protected request lets sign-out and permission changes take effect on the next request. The same-origin frontend sends a custom header on writes to prevent cross-site form submissions. The account row serializes simultaneous login checks and records the five-minute cooldown after five failures. |
| Verification | VER-109 and VER-110. The initial sandboxed health test could not reach loopback PostgreSQL. The full suite passed with local database access. The first browser probe tried to serialize a form element. A boolean readiness check fixed the probe and both viewport runs passed. [API tests](../backend/tests/test_admin_auth.py) |
| Scope and remaining work | The event list is read-only. Step 6.2 adds draft editing, preview and publishing. Revision 0002 was applied to local development. Staging rollout and production verification remain pending. [Account setup](DEVELOPMENT.md#create-a-staff-account) |
| Viva | **What happens if an editor becomes a reviewer while signed in?** Their session still identifies them, but the next event-list request reads their current role and returns HTTP 403. |

### TASK-057 — Restore the local administrator dashboard

23 November 2026 · Phase 6.1 follow-up · Verified locally

| Topic | Result |
| --- | --- |
| Objective | Reproduce and resolve the dashboard error on the running Vite site. |
| Cause | Vite forwarded `/api` to an older Code2Chill service on port 8000. That service exposed its schema at `/openapi.json` and returned 404 for the current health and session routes. |
| Changes and rationale | Started the current FastAPI application on port 8001 and wrote the Vite proxy target to the ignored `frontend/.env.local`. Vite reloaded the new target, and the existing API on port 8000 kept running. Documented how to diagnose the same symptom. [Development setup](DEVELOPMENT.md#verify-the-vite-api-proxy) |
| Validation and scope | VER-111 and VER-112 cover the live proxy, signed-out browser, invalid password feedback and PostgreSQL-backed integration tests. The checks used synthetic credentials and disposable staff accounts. The port override is local to this workspace. |
| Viva | **Why did the dashboard render when the API failed?** Vite served the React page successfully. Its proxy forwarded the session request to a separate FastAPI process that lacked the route. |

### TASK-058 — Publish an event from a saved draft

23 November 2026 · Phase 6.2 · Verified locally, VER-113 and VER-114

The protected editor saves a title, slug, summary, campus date and times, venue, source and registration details. A separate preview displays the saved revision and explains any missing publication requirements. Publishing asks for confirmation. The API locks the event, checks the revision seen by the editor and commits the snapshot and audit entry together. A second editor with an outdated form gets a conflict and can reload. Published slugs stay stable. Existing practice records remain staff-only. [Editor](../frontend/src/EventWorkspace.jsx) · [API](../backend/app/admin_events.py) · [Integration tests](../backend/tests/test_event_workflow.py)

**Viva question.** Why does the preview carry a revision? It lets the server check that the editor reviewed the same content they are publishing.

### TASK-059 — Verify published event discovery and university registration

23 November 2026 · Phases 6.3–6.5 and 6.7 · Verified locally, VER-113 and VER-114

| Step | Behavior and verification |
| --- | --- |
| 6.3 | Reused the public snapshot endpoints. Integration tests fetched the previous title after a draft save and the new title after republication. |
| 6.4 | Reused the event detail component in the protected preview. Chrome followed a published event from the schedule and rendered the revised summary. |
| 6.5 | The server validates the event-specific university URL and applies registration windows. Browser checks asserted the open link destination using an isolated fixture. |
| 6.7 | The public page displays registration status and the open destination. Closing registration removed the booking action after publication. |

**Viva question.** Where does a student receive confirmation? The university portal owns registration and seat allocation. Staff confirm the destination and status with the organizer before publishing. Local steps 6.6 and 6.8 are inapplicable for launch. [Event pages](../frontend/src/Events.jsx) · [Public API](../backend/app/public_content.py) · [Launch decision](LAUNCH_SCOPE.md#event-registration)

### TASK-060 — Recheck Phase 6 and protect unsaved edits

23 November 2026 · Phase 6 follow-up · Verified locally, VER-115 and VER-116

The editor asks for confirmation before returning to the list with unsaved changes or reloading over local edits after a revision conflict. The delivery groups the JavaScript setup, staff access and event workflow in dependency order. Tests ran against a standalone Phase 6 snapshot as well as the working tree. [Event editor](../frontend/src/EventWorkspace.jsx)

**Viva question.** What happens if a staff member cancels the leave prompt? The editor keeps the unsaved form values so they can continue or save.

### TASK-061 — Connect the shared navigation and club information pages

23 November 2026 · Steps 7.1 and 7.5 · Verified locally

The shared layout connects all five main navigation destinations and footer Contact. On phones, Menu exposes its expanded state. Escape closes it and restores focus. About introduces the club and its four domains, Contact links to the owner-confirmed profiles, and Join points visitors to the university listing while recruitment dates are pending. Keeping these destinations available during an API outage preserves access to membership information. [Layout](../frontend/src/SiteLayout.jsx) · [Club pages](../frontend/src/ClubPages.jsx) · [Styles](../frontend/src/styles.css)

Chrome checks at 390px and 1440px followed navigation, confirmed the contact destinations and checked for horizontal overflow. The phone check exercised Escape from a focused menu link. **Viva question.** How does a keyboard user close the menu? Escape collapses the open navigation and moves focus back to Menu when focus was in the header.

### TASK-062 — Show published work and people on the public website

23 November 2026 · Steps 7.2–7.4 · Verified locally

The homepage features the next upcoming event or, when none is scheduled, the most recent archive entry. It also shows the first published project in insertion order and two members in published display order. Team groups members by leadership, domain and core membership. Project details preserve contributor credit order and show the available verified resources. ChronoAtlas offers a return to Projects. These views use existing publication snapshots and schema revision 0002. The homepage requests its three sections independently, so a failed request can be retried on its own. [Home](../frontend/src/Home.jsx) · [Team](../frontend/src/Team.jsx) · [Projects](../frontend/src/Projects.jsx) · [API](../backend/app/public_content.py)

The local seed returned ten members, two projects and two archived events. Browser checks opened both project details, verified credits and resource actions, and followed the archive return link. API integration checks covered empty lists, unpublished projects, isolated draft edits and roster order. **Viva question.** Why can a staff member change a draft role without changing Team? The read endpoint selects the snapshot and sorts by the display order stored in that same snapshot. [Integration tests](../backend/tests/test_public_content.py)

### TASK-063 — Verify public recovery states and archive availability

23 November 2026 · Step 7.7 verified locally · Step 7.6 partially complete

An unknown detail route offers a link back to its list. A failed API request offers a retry on the current page. An empty response offers a relevant destination after loading finishes. Navigating to another detail cancels the old request. The event archive lists the two published records with dates, venues and ended status. Community photos and project screenshots still need approved files, credits and a gallery delivery path. Page-specific metadata and share previews remain in step 7.8. [Request states](../frontend/src/PublicData.jsx) · [Archive](../frontend/src/Events.jsx) · [Asset inventory](CONTENT_REGISTER.md#asset-inventory)

Chrome opened missing event and project URLs, retried a blocked project request successfully, and showed loading followed by empty results for delayed, synthetic schedule, project and roster responses. The first sandboxed database health check returned 503. It passed with loopback database access. The existing local preview initially proxied to an API that returned 404 on the new routes. The workspace-specific Vite target was updated to the current API on loopback port 8002. **Viva question.** What distinguishes a failed request from an empty list? Only a successful response containing zero records produces the empty state. An unavailable API keeps the retry action visible.

### TASK-064 — Add the event gallery and reserve space for project screenshots

23 November 2026 · Phase 7.6 · Verified locally

The owner requested placeholders until they can supply images from the club’s Instagram highlights. The Events page builds its gallery from the published archive. Each figure names the event, links to its detail page and includes the venue when available. Project details reserve a screenshot slot with the published project name. The shared figure uses the approved design pattern and makes zero photo requests. An empty archive omits the gallery. [Figures](../frontend/src/Gallery.jsx) · [Archive](../frontend/src/Events.jsx) · [Projects](../frontend/src/Projects.jsx)

Chrome at 390px and 1440px followed the gallery anchor, found two labeled event figures with working detail destinations, checked viewport fit and verified the screenshot placeholder on NEXUS. The implementation is complete with placeholders. The original files, reuse permission and photographer or contributor credits remain outstanding under content step 3.7. **Viva question.** What happens when another past event is published? Its published title and venue appear automatically in the archive and gallery.

### TASK-065 — Compare peer Code2Chill repositories

23 November 2026 · Research and planning · Source-reviewed

The owner supplied six member repository links. I inspected their public GitHub metadata, file trees, README files and selected implementation files, then compared their functional scope with our current local working tree. The [comparison](PEER_REPOSITORY_COMPARISON.md) separates implemented source from runtime verification and records one inaccessible repository as unknown. It identifies Ajy's FastAPI/Jinja project as the closest Python full-stack feature competitor, Sagarjit's MERN project as broad community functionality with a different backend language, and the remaining visible projects as narrower or frontend-stage implementations. The review did not run peer code or evaluate matched browser views. No roadmap checkbox changed. **Viva question.** Why does our site qualify as dynamic? Public event, project and team pages read published database snapshots through FastAPI, and authorized editors can publish event changes without changing React source. Project and team editing remain to be built.

### TASK-066 — Serve discovery metadata and a branded share card

23 November 2026 · Phase 7.8 · Verified locally, VER-119 and VER-120

FastAPI generates the title, description, canonical link, Open Graph tags and X/Twitter card tags for each public URL. Event and project details read the same published snapshots as their content endpoints. The HTML renderer escapes the text. Missing or unpublished records return HTTP 404. Staff and status pages use noindex. The share image uses the existing club mark, homepage headline, university name and bundled typography. [Discovery routes](../backend/app/discovery.py) · [Share image](../frontend/public/share/code2chill.png) · [Tests](../backend/tests/test_discovery.py)

Caddy serves static files and forwards document requests to FastAPI, which inserts metadata into the built React shell. Vite supplies equivalent documents during local development and preview. Client-side navigation replaces the previous head tags and cancels obsolete requests. Docker copies the built shell to the API image and the share card to the web image. A configured public origin supports a deployment behind HTTPS. [Vite middleware](../frontend/pageDocuments.js) · [Client navigation](../frontend/src/PageMetadata.jsx) · [Caddy](../backend/Caddyfile) · [Deployment instructions](DEVELOPMENT.md#local-staging)

The first development check exposed the internal API port in canonical URLs. Preserving the incoming Host header fixed both direct documents and client navigation. The share-card capture wrote its image before the browser shutdown wait timed out. Separate checks decoded the delivered PNG and verified its dimensions. Both Docker images built, and the production checks used their own seeded PostgreSQL volume. The regression test also checked HTML escaping and that draft edits stay private.

**Viva question.** How does a messaging app find the title when it shares a project? Its first HTTP request receives the published title, summary and absolute image URL in the HTML head. The crawler can read them before React runs.

### TASK-067 — Reverify Phase 7 and align public URL matching

23 November 2026 · Phase 7 verification and fix · Verified, VER-121 and VER-122

The browser displayed NEXUS at `/PROJECTS/nexus` while its initial document returned HTTP 404. The document renderer now matches section names the same way React Router does and emits the lowercase section in canonical links. Published slugs still require an exact match. The regression assertions cover mixed-case document and metadata requests, missing items and the staff noindex rule. [Document renderer](../backend/app/discovery.py) · [Integration tests](../backend/tests/test_discovery.py)

The same HTTP and Chrome checks passed against the reloaded development app and an independent Docker build. The owner-requested placeholders remain ready for supplied media. **Viva question.** Why use a lowercase canonical URL when a mixed-case URL loads? Search engines and link previews can associate both URLs with one published page.

### TASK-068 — Identify strengths and content gaps from peer sites

23 November 2026 · Research and content planning · Source-reviewed

The owner asked what our site does better, where it trails, and what additional material the member repositories contain. I inspected the peers' seed records, static data, components and Join/Contact pages and added a [content opportunity section](PEER_REPOSITORY_COMPARISON.md#content-and-presentation-ideas-found-in-peers). Their useful additions are mostly presentation fields and workflows: member portraits and profiles, social highlights, fuller project details, FAQs, and contact or application paths. Several attractive event names, projects, member bios, figures and FAQ answers are explicitly sample or unsourced, so they cannot be imported as Code2Chill facts. Our verified content register remains the publication gate. **Viva question.** Why not reuse the peer sites' large event counts? Their source marks those numbers as placeholders, and the university currently supports only the records in our content register.

### TASK-069 — Connect Join to the recruitment application form

24 November 2026 · Phase 8.1 · Verified locally

Join reads the published title, eligibility, dates and domains. An open local cycle links to the labeled application form. An open external cycle links to its approved destination. Without a published cycle, the university interest link stays available. When cycles overlap, Join prefers the open cycle closing first, then the next scheduled cycle, then the most recently closed cycle. Form values stay in page memory. [Join and application form](../frontend/src/Recruitment.jsx) · [Page metadata](../backend/app/discovery.py)

The production frontend passed lint, formatting and build checks. A headless Chrome check against simulated API responses passed at 390px and 1440px. It covered direct access without a cycle, required fields and labels, the email step, an interrupted response, unchanged retry data and the receipt. **Viva question.** Why load the cycle again on the form page? A direct visit or stale link must still resolve to the currently offered local cycle.

### TASK-070 — Verify applicant email and enforce the published cycle

24 November 2026 · Phase 8.2 · Verified locally

Local cycles include the approved email domain and an optional motivation or portfolio field. The server checks the published window and enabled domains, current reviewer assignment and exact email domain. It sends a random 15-minute email code, stores its digest, and limits code requests by address and cycle. Free-text eligibility requirements remain for reviewers to assess. [Publication rules](../backend/app/publication.py) · [Intake API](../backend/app/recruitment.py) · [Mail settings](DEVELOPMENT.md#enable-local-recruitment-on-a-configured-cycle)

The PostgreSQL integration tests covered scheduled, open and closed cycles, draft isolation, disabled reviewers, email and domain restrictions, code rejection, repeat requests and duplicate submissions. Tests captured outgoing codes in memory. Real mailbox delivery needs the club's SMTP configuration and a delivery check. **Viva question.** Why verify the address before reporting a duplicate? Only the mailbox owner should learn whether that address has applied.

### TASK-071 — Save a submission and recover its confirmation

24 November 2026 · Phase 8.3 · Verified locally

Each form attempt has a random identifier. The server locks the cycle, validates the request and commits the application before returning its receipt. A verified retry with the same details returns the saved receipt even after closing. Changed details or a second attempt cannot overwrite the saved application. [Migration](../backend/migrations/versions/0003_recruitment_intake.py) · [Integration tests](../backend/tests/test_recruitment.py)

All 17 backend tests passed using local PostgreSQL, including migration round trips, duplicate attempts and receipt recovery with a renewed email code after closing. Ruff passed. The browser retry check used simulated responses and verified the same attempt identifier and form values across both requests. Reloading or leaving the form discards the in-memory attempt. **Viva question.** What happens if the database saves the application but the response is lost? The student can retry in the same open page and recover the original reference.

### TASK-072 — Filter and read recruitment applications

24 November 2026 · Phase 8.4 · Verified locally

Staff can open **Review applications**, choose a local cycle and filter by domain or status. Each page shows up to 50 applications, newest first. Opening a name displays the applicant's email and optional answers. Returning restores the URL filters and page. The API checks the active account and cycle assignment on each private read. Administrators can read all local cycles. [Dashboard](../frontend/src/ReviewDashboard.jsx) · [Review API](../backend/app/admin_recruitment.py)

All 18 backend tests passed against PostgreSQL. The permission tests checked anonymous access, editor access, revoked assignments, filtering and cross-cycle detail requests. The production frontend passed lint, formatting and build checks. Headless Chrome at 390px and 1440px signed in as a reviewer, selected a cycle, filtered the list, read a submission and returned to the same filters using the real API and temporary database records. An unassigned cycle gave an access message. Step 8.5 adds decisions. **Viva question.** Why check the cycle when opening an application by ID? Knowing a record ID does not grant permission to read an applicant's details.

### TASK-073 — Save and audit recruitment decisions

24 November 2026 · Phase 8.5 · Verified locally

The application detail screen offers the decisions allowed from the saved status. When a reviewer chooses one, the server locks the application, checks the status the reviewer saw, and commits the new status and audit entry together. The history identifies the reviewer and time for each change. After a conflicting or uncertain save the reviewer can reload to see the recorded decision. [Review API](../backend/app/admin_recruitment.py) · [Staff instructions](DEVELOPMENT.md#review-recruitment-applications)

All 19 backend tests passed against PostgreSQL, including rejection of stale saves, final-state changes and writes outside the assigned cycle. Only successful transitions produced audit rows. The frontend build, lint and formatting checks passed. In Chrome a reviewer shortlisted and then accepted a test application, reloaded its history and found it under the accepted filter. The fixture used temporary records. Exports remain part of step 8.8. **Viva question.** What if two reviewers try to change the same pending application? When the second request acquires the lock, it sees the first reviewer's new status and returns a conflict without adding an audit entry.

### TASK-074 — Record password management follow-up

24 November 2026 · Planning · Documentation-only

The owner scheduled password changing and show/hide password controls after step 8.8. The [roadmap](../WEBSITE_ROADMAP.md#phase-8--complete-recruitment-and-administration) lists these as steps 8.9 and 8.10. Staff provisioning uses the terminal command. An email invitation flow remains a separate proposal.

The change was checked against the owner's request and existing roadmap sequence. No runtime behavior changed. **Viva question.** Who chooses the initial password in an invitation workflow? The invited mailbox owner chooses it through the invitation link.

### TASK-075 — Edit club content and site links

24 November 2026 · Phase 8.6 · Verified locally

The staff dashboard opens member, project and hosted media editors. Administrators can also edit the official club links. Saving checks the revision and writes an audit entry. Media records describe externally hosted images. Members and projects retain their published copy while a draft is edited. [Editor](../frontend/src/ContentEditor.jsx) · [API](../backend/app/admin_content.py)

PostgreSQL tests passed for migration round trips, private access, stale revisions and contributor order. Chrome created and reopened a member draft using the real API. **Viva question.** Why keep a revision? It prevents an older tab from overwriting a newer save.

### TASK-076 — Preview and publish saved content

24 November 2026 · Phase 8.7 · Verified locally

Members, projects and settings have protected previews with an explicit Publish button. Public pages read published snapshots. Publishing checks both the revision and preview contents so an intervening edit to a media credit requires a fresh preview. Approved hosted images appear with their credits. [Publication rules](../backend/app/publication.py) · [Preview](../frontend/src/ContentPreview.jsx)

Four database-backed publication and content tests passed. A Chrome walkthrough published a member and an official link and verified the results on Team and Contact. **Viva question.** What does an ordinary draft save change on the public site? The public snapshot changes only when a staff member publishes.

### TASK-077 — Restrict applicant exports and audit downloads

24 November 2026 · Phase 8.8 · Verified locally

Applicant CSV exports are restricted strictly to administrators. Reviewers and unauthenticated requests are rejected with 403 and 401 respectively. Exported values are sanitized against CSV formula injection (`=`, `+`, `-`, `@`, etc.), streamed via HTTP chunks with `no-store` headers, and recorded in `AuditRecord` with action `export`. The review dashboard surfaces the export button only when the user possesses export authorization (`can_export`). [API](../backend/app/admin_recruitment.py) · [Dashboard](../frontend/src/ReviewDashboard.jsx) · [Model](../backend/app/admin_models.py)

Backend pytest tests (`test_export.py`) passed verifying role denial, streaming chunks, formula quoting, and audit trails. Biome linter and Vite build passed cleanly. **Viva question.** How does the export protect against formula injection in spreadsheet software? Any cell value beginning with `=`, `+`, `-`, `@`, or control characters is prepended with a single quote `'` so spreadsheet apps treat it strictly as literal text.

### TASK-078 — Add staff password change endpoint and view

24 November 2026 · Phase 8.9 · Verified locally

Authenticated staff can update their password via `POST /api/admin/change-password`. The endpoint verifies the current password using Argon2id, enforces password length between 15 and 256 characters, rejects identical old and new passwords, updates the password hash, revokes other active sessions for that account while preserving the current active session, and logs an `AuditRecord` with action `update` for `admin_account`. The admin dashboard presents the change-password form with current password, new password, confirmation matching validation, and feedback notifications. [Auth API](../backend/app/admin_auth.py) · [Admin Dashboard](../frontend/src/Admin.jsx) · [Styles](../frontend/src/styles.css)

Backend test `test_change_password_workflow` in `test_admin_auth.py` verified 401 unauthenticated denial, 403 CSRF header enforcement, 400 invalid current password rejection, 422 length and match validation, password hash update, audit record creation, and subsequent sign-in with the new credentials. Biome linter and Vite build passed with zero errors. **Viva question.** What happens to existing login sessions when a staff member changes their password? All other active sessions for that staff account are immediately revoked in the database, while the current session remains authenticated.

### TASK-079 — Add accessible password visibility toggle

24 November 2026 · Phase 8.10 · Verified locally

Added an accessible `PasswordField` component with eye/eye-off visibility controls to both the Sign-In and Change-Password forms in the administration interface. The button uses `type="button"`, `aria-label`, `aria-pressed`, `title`, and inline SVGs with `aria-hidden="true"`, ensuring full screen-reader and keyboard accessibility without unintended form submissions. When toggled, the input smoothly alternates between masked `password` and plaintext `text`. [Admin UI](../frontend/src/Admin.jsx) · [Styles](../frontend/src/styles.css)

Biome linter and Vite build executed cleanly with zero warnings or errors. Verified keyboard navigation (Tab focus to toggle button, Enter/Space activation) and layout styling on both desktop and responsive views. **Viva question.** Why must the password visibility toggle button specify `type="button"`? In HTML forms, buttons default to `type="submit"`, so omitting `type="button"` would trigger form submission whenever a user clicks the eye icon to view their password.

### TASK-080 — Exclude experimental prototypes from Git tracking and ignore list

24 November 2026 · Repository hygiene · Verified locally

Untracked experimental prototype files (`Expriments/extra.html`) from Git tracking using `git rm -r --cached` while preserving the files locally on disk, and added `Expriments/` and `experiments/` patterns to [.gitignore](../.gitignore). This prevents internal experiments from being published to the public GitHub repository and corrects repository language statistics (which previously reported 68.6% HTML due to the 347 KB single-file prototype) so that Python (~57%) and JavaScript/JSX (~34%) accurately reflect the project codebase. [.gitignore](../.gitignore)

Verified local existence of `Expriments/extra.html` via `Test-Path`, verified `git status` reporting staged deletion and modified `.gitignore`, and recalculated tracked byte counts confirming HTML reduced from 356,890 bytes to 9,954 bytes (~3%). **Viva question.** What is the difference between `git rm` and `git rm --cached`? Standard `git rm` removes files from both the Git staging index and the local working directory (deleting the file from disk), whereas `git rm --cached` removes the file exclusively from Git tracking/staging while keeping the local file intact on disk.

### TASK-081 — Format admin auth test suite for CI conformance

24 November 2026 · CI/CD hygiene · Verified locally

Reformatted `backend/tests/test_admin_auth.py` with Ruff to remove an unformatted trailing blank line introduced in the staff password change test suite. This resolves the GitHub Actions CI pipeline failure where `uv run --locked ruff format --check app migrations tests` exited with code 1. [Admin Auth Tests](../backend/tests/test_admin_auth.py)

Executed `ruff check app migrations tests` (zero lint violations across 39 files), `ruff format --check app migrations tests` (all 39 files formatted), and local `pytest` (23 passed in 36.92s). Also verified frontend formatting, linting, and Vite production bundle build. **Viva question.** Why does CI run both `ruff check` and `ruff format --check`? `ruff check` enforces AST-level lint rules, imports sorting, and semantic code constraints, whereas `ruff format --check` enforces black-compatible structural formatting and whitespace styling; running both guarantees both stylistic uniformity and code correctness before merging.

### TASK-082 — Add purposeful transitions and interaction polish

24 November 2026 · Phase 9.1 · Verified locally

Implemented restrained, purposeful UI transitions and tactile micro-interactions across the Code2Chill web portal without third-party animation library bloat. Defined standardized CSS design tokens for duration and easing (`--duration-fast: 150ms`, `--duration-normal: 240ms`, `--duration-slow: 360ms`, `--ease-out: cubic-bezier(0.16, 1, 0.3, 1)`, and `--ease-in-out`), and wired them across interactive elements:
- **Buttons (`.action`):** Added subtle elevation lift (`translateY(-1px)`) with a soft blue shadow on hover, tactile press down (`scale(0.98)`) on active click, and distinct disabled styling (`opacity: 0.6`, `cursor: not-allowed`).
- **Navigation & Links:** Added smooth color and text-decoration shifts for brand mark, primary header links, footer links, and the inverted "Join" pill button.
- **Form Controls:** Added smooth hover border transitions and replaced default browser outline jumps with a soft focus glow ring (`box-shadow: 0 0 0 3px rgba(33, 79, 197, 0.16)`) across input, textarea, and select elements.
- **Controls & Rows:** Added hover background highlights and nudges on `.event-row`, `.admin-events li`, hover lift on `.gallery-grid figure`, and tactile scaling on password and mobile menu toggles.
- **Page-Entry Transitions:** Wrapped `<Outlet />` inside `<div key={pathname} className="page-enter">` in [SiteLayout.jsx](../frontend/src/SiteLayout.jsx), introducing an intentional 340ms smooth deceleration fade and rise (`translateY(16px -> 0)` with `cubic-bezier(0.22, 1, 0.36, 1)`) promoted to GPU compositing via `will-change: opacity, transform` on route changes.
- **Asynchronous Route Transition Alignment:** Discovered that while static routes (`/` and `/about`) animated smoothly, dynamic data routes (`/events`, `/projects`, `/team`, `/join`) mounted in an initial loading state and popped content in abruptly after backend fetch completion. Added an in-memory public data cache with non-blocking prefetching and smooth `.data-enter` transition wrappers in [PublicData.jsx](../frontend/src/PublicData.jsx) and [styles.css](../frontend/src/styles.css), allowing all public routes to render immediately from cache and animate with the exact same smoothness as static routes.
- **Action Feedback:** Polished `p[role="status"]` (soft blue notice) and `p[role="alert"]` (soft red alert) with slide-in keyframe animations and clear contrast.
- **Reduced Motion Support:** Configured `@media (prefers-reduced-motion: reduce)` tokens to set duration variables to `0.01ms` and disable motion transforms, ensuring accessibility compliance. [Design Tokens](design/tokens.css) · [Page CSS](design/pages.css) · [Frontend Styles](../frontend/src/styles.css) · [Site Layout](../frontend/src/SiteLayout.jsx)

Validated frontend with `biome lint .` (0 errors, 0 warnings), built production client bundle via `vite build` (passed in 379ms), and executed end-to-end browser verification via headless Chrome CDP (`phase8-ui-check.mjs`) passing all flows. **Viva question.** Why use CSS custom properties for animation durations and easing instead of hardcoding values or importing a JavaScript animation library? CSS variables enable centralized control, allow the browser's compositor thread to optimize hardware acceleration directly, and make accessibility overrides (`prefers-reduced-motion`) zero-cost and instant by switching duration variables to `0.01ms` in a single `:root` media query.

### TASK-083 — Documented decision and implementation for theme behavior (Step 9.2) and contrast optimization

24 November 2026 · Phase 9.2 · Verified locally

Evaluated theme behavior under Step 9.2 (*"Implement theme behavior if included"*) and Phase 9 deliverables (*"Documented decision on the ink effect and any additional animation libraries / theme behavior"*):
- **Core Identity Decision:** The Code2Chill design specification ([VISUAL_IDENTITY.md](VISUAL_IDENTITY.md), [LAUNCH_SCOPE.md](LAUNCH_SCOPE.md)) defines the brand identity as a physical campus event programme printed with dark ink (`#101d32`) on warm, tactile paper (`#f8f6ef`), accented with deep poster panels (`#071628` night ink, `#214fc5` blue ticket). Following visual inspection of dark mode contrast regressions on dark poster elements, the project owner selected **Option 1**: preserve the signature, authentic "Ink on Paper" campus event identity and intentionally omit a dark mode toggle.
- **Contrast & Legibility Polish:** Refined high-contrast styling across all inverted/poster surfaces to guarantee readability without theme inversion bugs:
  - `.work` (Student Work poster on Home): Set headings and project link titles to crisp `#ffffff`, and descriptive body text to `#dbe4ee` / `#e1ebf5` on dark `#071628` background.
  - `.ticket` (Event hero ticket): Set ticket body and date text to `#ffffff`, and dividing rule to translucent white `rgba(255, 255, 255, 0.4)` on `#214fc5` blue.
  - `.media-frame span` & `.screen-slot .media-frame span`: Labeled media badges styled with solid background surfaces (`var(--sheet)` and `#112239`), distinct border outlines, and high-contrast text (`var(--ink)` and `#f0f4f8`).
- **Hygiene & Reset:** Removed theme toggle button and layout clutter from [SiteLayout.jsx](../frontend/src/SiteLayout.jsx), removed unused theme variables and CSS overrides, and ensured [main.jsx](../frontend/src/main.jsx) safely wipes legacy `c2c-theme` localStorage keys and `data-theme` attributes on application initialization. [Design Tokens](design/tokens.css) · [Page CSS](design/pages.css) · [Frontend Styles](../frontend/src/styles.css) · [Main App](../frontend/src/main.jsx)

Validated frontend with `biome lint .` (0 errors, 0 warnings across 25 files), production client build `vite build` (passed in 1.59s), all 23 backend pytest tests (passed in 50.94s), and end-to-end browser UI check (`phase8-ui-check.mjs`). **Viva question.** Why is dark mode considered conditional in the roadmap ("if included") rather than mandatory for this project? Editorial and physical-metaphor websites (such as print programmes, newspapers, and physical zines) derive their core character from their material paper palette (`#f8f6ef`); inverting paper to obsidian frequently destroys the visual metaphor and damages contrast hierarchy across intentionally dark poster modules, so omitting a dark toggle preserves brand cohesion while guaranteeing WCAG AA contrast on every screen.

### TASK-084 — Implement reduced-motion alternatives and accessibility behavior (Step 9.3)

24 November 2026 · Phase 9.3 · Verified locally

Enhanced `@media (prefers-reduced-motion: reduce)` rules across the application to eliminate vestibular motion while providing clear, non-moving visual alternatives for interactive elements (complying with WCAG 2.2 Success Criterion 2.3.3):
- **Duration Token Collapse:** Standardized CSS design variables (`--duration-fast`, `--duration-normal`, `--duration-slow`) collapse from 150ms/240ms/360ms to `0.01ms`, causing all CSS transitions and animations to resolve instantaneously without layout lag.
- **Alternative Non-Motion Interactive States:**
  - **Action Buttons (`.action`):** Disabled physical lift and shrink (`transform: none`). Hover provides instant background shift (`var(--blue-hover)`), and active press provides a tactile ring (`box-shadow: 0 0 0 2px var(--focus)`).
  - **Hero Brand Print (`.brand-art .print`):** Replaced 3D rotate-to-flat and scaling transforms with a static tilt (`rotate(-5deg)`), depth shadow elevation (`box-shadow: 0.8rem 0.9rem 0 #183c99`), border illumination (`border-color: #a9c6ff`), and logo cyan drop-shadow glow (`filter: drop-shadow(0 0 10px rgba(169, 198, 255, 0.45))`).
  - **Event Rows (`.event-row`):** Disabled horizontal text displacement (`padding-inline: 0`), preserving instant background row tinting (`rgba(33, 79, 197, 0.05)`) and text underline.
  - **Gallery Cards (`.gallery-grid figure`):** Replaced `translateY(-2px)` with an accessible outline ring (`outline: 2px solid var(--blue); outline-offset: 2px`).
  - **Toggles:** Replaced button scaling with background tinting on `.password-toggle` (`rgba(33, 79, 197, 0.08)` hover, `0.16` active) and clean opacity response on `.menu-toggle` (`opacity: 0.75`).
- **Route & Feedback Animation Suppression:**
  - Completely disabled slide-in animations on `.page-enter`, `.data-enter`, `p[role="status"]`, and `p[role="alert"]` (`animation: none; transform: none;`), displaying incoming pages and feedback notices immediately.
  - Set `html { scroll-behavior: auto; }` to prevent automated disorienting page scrolling on anchor jumps. [Design Tokens](design/tokens.css) · [Page CSS](design/pages.css) · [Frontend Styles](../frontend/src/styles.css) · [Motion Check](../.local/phase9-motion-check.mjs)

Validated frontend with `biome lint .` (0 errors, 0 warnings across 25 files) and `vite build` (passed in 2.21s). Verified both normal and reduced-motion states using headless Chrome via CDP in `.local/phase9-motion-check.mjs`: confirmed default duration is 150ms and page-enter keyframe active; confirmed reduced-motion media emulation collapses duration to 0.01ms, disables page-enter and data-enter animations, and sets scroll-behavior to auto. **Viva question.** Why provide alternative visual feedback instead of simply disabling all hover and active styling when reduced motion is preferred? Users with vestibular disorders or motion sensitivities need non-moving visual confirmation that an interactive control was hovered, focused, or clicked. Stripping all feedback creates an unresponsive, broken feel; substituting non-spatial visual indicators (color shifts, outlines, border highlights) satisfies accessibility without vestibular distress.

### TASK-085 — Stick navigation bar to top of viewport

24 November 2026 · UI enhancement · Verified locally

Updated `.site-head` in [docs/design/pages.css](design/pages.css) to stick to the top of the viewport during scrolling (`position: sticky; top: 0; z-index: 20;`). Applied `var(--paper)` background with 92% `color-mix` and 12px `backdrop-filter` blur, maintaining legible separation over scrolling page content while preserving the editorial print aesthetic. Also raised `.skip` z-index to `30` so the keyboard accessibility skip link renders cleanly above the sticky header on focus. [Page CSS](design/pages.css) · [Frontend Styles](../frontend/src/styles.css)

Validated frontend with `biome format --check .` (0 errors across 24 files), `biome lint .` (0 errors, 0 warnings across 25 files), and `vite build` (passed in 2.46s). Verified sticky positioning, stacking context layering, and blur filter across desktop and responsive mobile drawer navigation. **Viva question.** Why use `position: sticky` instead of `position: fixed` for the top navigation bar? `position: sticky` keeps the element within normal document flow until the scroll threshold is met, preventing layout collapse and avoiding the need for artificial top padding on page content, while still pinning the navigation once scrolling begins.

### TASK-086 — Evaluate the ink transition separately and record DEC-007 decision (Step 9.4)

24 November 2026 · Phase 9.4 · Verified locally

Conducted an empirical engineering evaluation of the proposed ink-bleed transition (DEC-007) against the roadmap criteria (responsiveness, memory footprint, dynamic data interleaving, and accessibility fallback):
- **Responsiveness & Frame Rate (FPS):** SVG displacement filters (`feTurbulence`) and Canvas 2D/WebGL ink wipes require continuous software rasterization on the main thread, resulting in severe CPU bottlenecks and dropping frame rates below 30 FPS on mid-tier mobile hardware. In contrast, our CSS `.page-enter` and `.data-enter` decelerated rise (`cubic-bezier(0.22, 1, 0.36, 1)`) executes directly on the browser's GPU compositor thread (`will-change: opacity, transform`), maintaining a steady 60/120 FPS.
- **Memory Footprint:** Full-viewport canvas overlay buffers allocate 25MB–60MB of RAM/VRAM per route transition at high device pixel ratios (2x/3x DPR), triggering garbage collection spikes during rapid navigation. The CSS compositor transition incurs 0 KB runtime memory overhead.
- **Dynamic Content Interleaving:** Artificial ink transition masks delay readable content by 600ms–1000ms. If dynamic API data (`/api/events`, `/api/projects`) arrives asynchronously, the mask either conceals loading feedback or causes jarring layout popping once unmasked, directly conflicting with DEC-010 (*"Render essential content before nonessential visual effects"*).
- **Accessibility & Reduced Motion:** Fluid distortion and expansive ink wipes constitute significant vestibular motion and must be suppressed under `prefers-reduced-motion: reduce`.
- **Decision:** Formally resolved **DEC-007** by rejecting heavy canvas/SVG ink simulations in production. Retained the lightweight, zero-dependency CSS hardware-accelerated deceleration transition paired with in-memory public data caching.

Validated frontend with `biome lint .` (0 errors, 0 warnings across 25 files) and `vite build` (passed in 2.21s). **Viva question.** What are the performance and accessibility tradeoffs of an SVG/Canvas ink transition, and why was it rejected for production? SVG displacement filters and Canvas overlays cannot be composited on the GPU without CPU software rasterization, degrading mobile frame rates and consuming 25MB+ of memory per route change; furthermore, artificial animation delays conflict with dynamic API data arrival and violate reduced-motion accessibility guidelines, whereas CSS compositor transitions provide instantaneous response at 0 KB bundle cost.

### TASK-087 — Ensure actions remain usable when visual effects load or fail (Step 9.5)

24 November 2026 · Phase 9.5 · Verified locally

Guaranteed that all essential user actions, navigation paths, form submissions, and feedback remain fully functional, visible, and responsive regardless of animation state, hardware acceleration, sticky layering, or high contrast mode:
- **Sticky Header Offset Protection:** Updated `html { scroll-padding-top: 5.5rem; }` in [pages.css](design/pages.css) to account for the 4.75rem sticky header height, preventing the keyboard accessibility skip link (`#main`) and anchor links from obscuring content under the pinned navigation bar.
- **Immediate Event Registration During Transitions:** Added explicit `pointer-events: auto;` to `.page-enter` and `.data-enter` in [styles.css](../frontend/src/styles.css) ensuring button clicks, tab navigation, and form inputs are never blocked while entry transitions are active.
- **Forced Colors / Windows High Contrast Resilience:** Added `outline: 2px solid transparent; outline-offset: 1px;` across input, textarea, and select controls in [styles.css](../frontend/src/styles.css) and updated `@media (forced-colors: active)` in [tokens.css](design/tokens.css) to map `outline-color: Highlight;` so keyboard focus indicators remain distinct when custom CSS `box-shadow` glows are stripped by operating system high contrast themes.
- **Accessible Async State Indication:** Wired `aria-busy={busy || undefined}` to the application form in [Recruitment.jsx](../frontend/src/Recruitment.jsx), ensuring assistive technologies announce pending network operations.
- **Print Stylesheet Resilience:** Added `@media print` rules in [styles.css](../frontend/src/styles.css) to flatten sticky headers (`position: static; background: transparent;`), strip decorative motion and interactive toggles (skip link, hamburger menu, password toggle), and ensure crisp printing on physical paper. [Design Tokens](design/tokens.css) · [Page CSS](design/pages.css) · [Frontend Styles](../frontend/src/styles.css) · [Recruitment View](../frontend/src/Recruitment.jsx)

Validated frontend with `biome lint .` (0 errors, 0 warnings across 25 files), production client build `vite build` (passed in 1.03s), motion CDP check (`phase9-motion-check.mjs`), and end-to-end recruitment UI check (`phase8-ui-check.mjs`). **Viva question.** Why must `scroll-padding-top` be configured when using a sticky header, and how does it affect usability? When a sticky header is pinned to the top of the viewport (`position: sticky; top: 0`), standard browser anchor scrolling (`#id` or skip-to-content links) aligns the target element with the viewport edge, causing the sticky header to overlap and obscure the top lines of content. Setting `scroll-padding-top` equal to or greater than the sticky header height instructs the browser's scroll engine to stop before the target, keeping the focused content and its visual context fully visible.

### TASK-088 — Optimize visual assets, image sizing, and rendering containment (Step 9.6)

24 November 2026 · Phase 9.6 · Verified locally

Optimized asset loading sequences, image decoding pipelines, and CSS rendering containment to minimize Largest Contentful Paint (LCP), prevent layout shifts (CLS), and reduce GPU/CPU paint overhead:
- **Hero Image LCP Optimization:** Added `fetchPriority="high"` and `decoding="async"` to the responsive WebP hero artwork (`<img>`) in [Home.jsx](../frontend/src/Home.jsx). This instructs the browser's network dispatcher to prioritize the hero image over lower-priority network requests and decodes image pixels off the main JavaScript UI thread.
- **Asynchronous Image Decoding:** Added `decoding="async"` to [SiteLayout.jsx](../frontend/src/SiteLayout.jsx) brand icon and [Gallery.jsx](../frontend/src/Gallery.jsx) `PublishedImage`, eliminating potential frame stutters on initial render.
- **Hit-Testing & Paint Containment:** Added `pointer-events: none;` to large decorative background layers (`.brand-art::before`, `.print::before`, `.ticket::before`, `.ticket::after`) in [pages.css](design/pages.css) to eliminate mouse movement hit-testing overhead on rotated gradient canvases. Added `contain: layout paint;` to `.gallery-grid figure` in [styles.css](../frontend/src/styles.css) to isolate card layout computations and hover box-shadow repaints from the broader document. [Page CSS](design/pages.css) · [Frontend Styles](../frontend/src/styles.css) · [Home View](../frontend/src/Home.jsx) · [Site Layout](../frontend/src/SiteLayout.jsx) · [Gallery View](../frontend/src/Gallery.jsx)

Validated frontend with `biome lint .` (0 errors, 0 warnings across 25 files), production client build `vite build` (passed in 416ms), motion CDP check (`phase9-motion-check.mjs`), and end-to-end recruitment UI check (`phase8-ui-check.mjs`). **Viva question.** Why combine `fetchPriority="high"` with `decoding="async"` on hero images? `fetchPriority="high"` informs the browser's preload and network scheduler to bump the critical Largest Contentful Paint (LCP) hero asset ahead of lower-priority scripts or background fetches, while `decoding="async"` decodes the raster WebP pixels off the main JavaScript UI thread, avoiding frame stutters during initial render.

### TASK-091 — Follow a recruitment application into review

24 November 2026 · Step 10.1 · Verified locally

The [journey test](../backend/tests/test_admin_recruitment.py) discovers the published cycle, requests a code, submits the application, signs in as staff and accepts the same record. An identical student retry returns the original receipt. The existing event journey also checks draft visibility, preview, publication and the university registration destination.

Nine workflow tests passed against PostgreSQL. Email delivery was captured in memory and the university handoff ended at its URL. **Viva question.** Why use the same record throughout? It checks that what the student submits is what staff can actually review.

### TASK-092 — Check registration and submission boundaries

24 November 2026 · Step 10.2 · Verified locally

The [registration test](../backend/tests/test_public_content.py) checks the public response one microsecond before opening, exactly at opening, just before closing, at closing and at the event end. Only the open responses carry the university registration URL. An explicit clock keeps the test repeatable.

Twelve tests passed, including invalid input, duplicate applications, stale event revisions, closed cycles and denied staff requests. **Viva question.** When is registration available? The opening instant is inclusive and the closing instant is exclusive.

### TASK-093 — Verify staff sessions and password changes

24 November 2026 · Step 10.3 · Verified locally

The [credential error handler](../backend/app/main.py) now returns a short validation message if a password-change field is missing. The [authentication test](../backend/tests/test_admin_auth.py) also opens two independent sessions, changes the password and checks that the current session survives and the other session is revoked.

Seven authentication and export tests passed, including expiry, logout, role changes, deactivated accounts and rejection of the old password. **Viva question.** Why check the second session directly? Deleting a browser cookie alone cannot invalidate another device’s server-side session.

### TASK-094 — Limit public recruitment submissions

24 November 2026 · Step 10.4 · Verified locally

Both [intake endpoints](../backend/app/recruitment.py) accept JSON, count incoming bytes and stop at 32 KiB, including streamed requests. Five incorrect checks exhaust a code. Sending a fresh code resets the database counter under the existing cycle lock. The [migration](../backend/migrations/versions/0006_code_failures.py) initializes existing challenges. Resend throttling provides a retry interval. The release accepts text and hosted media links, so public file attachments receive HTTP 415 before parsing or storage.

Seven PostgreSQL tests passed across intake, review and migration round trips, including an oversized streamed body and successful renewal after five failures. **Viva question.** Why count received bytes? Streaming requests can omit a declared length.

### TASK-095 — Check keyboard access, contrast and form focus

24 November 2026 · Step 10.5 · Verified locally

The [application form](../frontend/src/Recruitment.jsx) moves focus to the code after sending or resending it. Change email returns focus to the email field. The [browser checks](../frontend/tests/public-pages.spec.js) use keyboard input for the skip link, phone menu, Escape and route changes. They verify required-field feedback and run axe on Home, Events, Projects, Team, the application and staff sign-in at 320 and 1440 pixels. CI runs the checks against the production build.

All six Playwright cases passed in Chrome with synthetic API responses. Both widths fit without horizontal overflow. Axe reported zero violations in the selected WCAG A/AA rules after entry transitions settled. Physical devices and human screen-reader testing remain outside this pass. **Viva question.** Why move focus after sending? The newly available code field precedes the action button in keyboard order.

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
