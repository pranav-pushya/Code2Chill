# Code2Chill Website — Implementation Roadmap

**Prepared:** 16 November 2026  
**Project:** Dynamic Python full-stack website for Code2Chill, Chitkara University  
**Status:** Planning. Checked steps are complete, and unchecked steps are pending.

## Objective

Build a distinctive, responsive club website backed by a Python API, a persistent database, and an administrator dashboard. Club leads should be able to update events, members, projects, and recruitment without editing source code.

The launch demonstration follows an administrator publishing an event, the update appearing on the public site, and a student reaching the approved university registration page. The [registration decision](docs/LAUNCH_SCOPE.md#event-registration) defines where sign-ups are handled.

## Existing Material and Constraints

- Treat `extra.html` as a prototype and interaction experiment, not the final design.
- Use the original logos in `docs/design/brand/originals/` (`Code2Chill.png` and `Code2Chill_transparent.png`) according to background, contrast, and layout requirements. Preserve both originals.
- Use planning references in `docs/planning/` (`CODE2CHILL_WEBSITE_MASTER.md` and `bluprint.pdf`). Resolve inconsistencies before implementation.
- President: **Lakshay Kalra**; vice-president: **Jiya Arora**, as confirmed by the project owner.
- Confirm the remaining roster, event details, recruitment status, photographs, and statistics before publishing.
- Do not treat prototype statistics or sample events as verified facts.
- Follow `GEMINI.md`: do not commit or push automatically. Obtain confirmation before adding Motion, GSAP, React Bits, Magic UI, or Lenis.

## Source and Design References

| Reference | Intended use |
| --- | --- |
| [Club Instagram](https://www.instagram.com/code2chill/) | Event announcements, club activity, and visual content |
| [University club page](https://chitkarau.life/clubs/code2chill) | Official club information and registration context |
| [Club LinkedIn](https://www.linkedin.com/company/code2chill) | Supporting club announcements and event history |
| [DGIT Squad](https://dgitsquad.vercel.app/) | Example the tech lead does not want the website to resemble |
| [Noddal](https://noddal.xyz/) | Positive design reference supplied by the tech lead |
| [Ksen Panchenko](https://ksenpanchenko.com/) | Positive design reference supplied by the tech lead |

**Club content:** The university listing and event records support the club details and the dates and venue for Byte The Vibe and DOMination. The [content register](docs/CONTENT_REGISTER.md) records checked facts and outstanding publication details.

**Design research:** The [design reference analysis](docs/DESIGN_REFERENCE_ANALYSIS.md) records desktop and phone observations for DGIT Squad, Noddal, and Ksen Panchenko, including the rendered Noddal hero after loading.

## Proposed Technical Foundation

This roadmap assumes that “Python full stack” means a Python backend with a React browser interface. Confirm any assessment requirement that mandates server-rendered Python templates before scaffolding.

| Layer | Proposed choice |
| --- | --- |
| Frontend | React, TypeScript, Vite |
| Styling | Tailwind CSS with custom design tokens |
| Backend | FastAPI |
| Request and response validation | Pydantic |
| Database | PostgreSQL |
| Database access and migrations | SQLAlchemy and Alembic |
| Media | Managed object storage with database metadata |
| Authentication | Administrator authentication; session strategy decided during architecture work |
| Testing | Backend integration tests and browser workflow tests |
| Delivery | CI checks, staging, reproducible builds, and production deployment |

Select compatible, maintained dependency versions during setup rather than copying old version pins from the existing specification. Document the chosen authentication approach and its security requirements.

## Phase 1 — Establish Content and Scope

### Steps

- [x] **1.1 Create a content register.** Record each fact, source URL or owner, verification status, and last checked date in the [content register](docs/CONTENT_REGISTER.md).
- [x] **1.2 Consolidate club identity.** Confirm the official description, leadership roster, domains, and public links. Record available contact paths and missing details in the [content register](docs/CONTENT_REGISTER.md#club-identity-and-contacts).
- [x] **1.3 Collect event material.** Record sourced dates, venues, summaries, upcoming status, and leads or gaps for results and media in the [content register](docs/CONTENT_REGISTER.md#events-and-projects).
- [x] **1.4 Collect project material.** Record project descriptions, contributor credits, verified code and demo links, and missing assets in the [content register](docs/CONTENT_REGISTER.md#events-and-projects).
- [x] **1.5 Decide registration ownership.** Use the university portal for launch sign-ups, with an event-specific handoff and fallback states defined in the [launch scope](docs/LAUNCH_SCOPE.md#event-registration).
- [x] **1.6 Define recruitment rules.** Set the cycle requirements, planned application fields, and public state before a cycle is announced in the [launch scope](docs/LAUNCH_SCOPE.md#recruitment).
- [x] **1.7 Set launch scope.** Record [first-release features, deferred work, and open decisions](docs/LAUNCH_SCOPE.md#first-public-release).

### Deliverables

- [Verified content inventory and asset list](docs/CONTENT_REGISTER.md).
- [Launch and deferred-feature lists](docs/LAUNCH_SCOPE.md#first-public-release), with [open decisions](docs/LAUNCH_SCOPE.md#open-decisions-and-content-gaps).
- Written [event registration](docs/LAUNCH_SCOPE.md#event-registration) and [recruitment](docs/LAUNCH_SCOPE.md#recruitment) rules.

**Completion criterion:** There is one agreed scope and content inventory, with unknown information explicitly marked.

## Phase 2 — Define Pages and User Journeys

### Steps

- [x] **2.1 Define public routes.** Plan nine public pages and their entry points in the [public sitemap](docs/PAGES_AND_JOURNEYS.md#public-sitemap).
- [x] **2.2 Map event discovery.** Trace discovery, event details, official registration, and fallback paths in the [event journey](docs/PAGES_AND_JOURNEYS.md#event-discovery-and-registration).
- [x] **2.3 Map recruitment.** Define the [announcement, interest, application, and confirmation paths](docs/PAGES_AND_JOURNEYS.md#recruitment-journey).
- [x] **2.4 Map administration.** Define [sign-in, content publishing, and authorized application review](docs/PAGES_AND_JOURNEYS.md#administrator-journey).
- [x] **2.5 Specify interface states.** Record [loading, empty, closed, full, error, and success behavior](docs/PAGES_AND_JOURNEYS.md#interface-states).
- [x] **2.6 Create wireframes.** Sketch the planned pages at [desktop and mobile widths](docs/WIREFRAMES.md) with realistic content lengths.
- [x] **2.7 Assign page actions.** Map [primary actions, controls, and recovery destinations](docs/PAGES_AND_JOURNEYS.md#page-actions).

### Deliverables

- [Sitemap and user-flow diagrams](docs/PAGES_AND_JOURNEYS.md#public-sitemap).
- [Desktop and mobile wireframes](docs/WIREFRAMES.md).
- [Interface states](docs/PAGES_AND_JOURNEYS.md#interface-states) and [page actions](docs/PAGES_AND_JOURNEYS.md#page-actions).

**Completion criterion:** Every important interaction has defined behavior, including failure and empty states.

## Phase 3 — Develop the Visual Identity

### Steps

- [x] **3.1 Inspect the references.** Once accessible, record specific observations about typography, spacing, navigation, motion, and mobile behavior.
- [x] **3.2 Establish an original direction.** Use the [club visual direction](docs/VISUAL_IDENTITY.md) for the home and event compositions.
- [x] **3.3 Define design tokens.** Use the shared [CSS tokens](docs/design/tokens.css) and [component specifications](docs/VISUAL_IDENTITY.md#tokens-and-components).
- [x] **3.4 Plan logo usage.** Use the [logo placement matrix](docs/VISUAL_IDENTITY.md#logo-placement) for surfaces, clear space, compact use and alternative text.
- [x] **3.5 Prepare assets.** Use the [responsive brand exports and favicon](docs/VISUAL_IDENTITY.md#brand-exports). Both original PNGs are preserved.
- [x] **3.6 Design representative pages.** Open the responsive [homepage](docs/design/index.html) and [event detail](docs/design/domination.html) designs.
- [ ] **3.7 Incorporate authentic imagery.** [Labeled design placeholders](docs/VISUAL_IDENTITY.md#temporary-media-placements) are in both previews. Approved DOMination photography and a NEXUS screenshot with credits are still pending.

### Proposed Homepage Sequence

1. Clear club introduction and primary action.
2. Featured event.
3. Real club projects.
4. Community moments and event photographs.
5. Team preview.
6. Recruitment and community links.

### Deliverables

- [Design tokens and component specifications](docs/VISUAL_IDENTITY.md#tokens-and-components).
- [Desktop and mobile page designs](docs/VISUAL_IDENTITY.md#responsive-page-previews).
- [Optimized brand asset exports](docs/VISUAL_IDENTITY.md#brand-exports).

**Completion criterion:** The design is coherent, responsive, and sufficiently specified for consistent implementation.

## Phase 4 — Scaffold the Application

### Steps

- [x] **4.1 Create the directory structure.** Establish `frontend/`, `backend/`, and `docs/`.
- [x] **4.2 Configure repository tooling.** Add environment templates, ignore rules, formatting, linting, and dependency lock files.
- [x] **4.3 Initialize the backend.** Configure the Python environment and FastAPI application.
- [x] **4.4 Initialize the frontend.** Configure React, TypeScript, routing, and the styling system.
- [x] **4.5 Connect PostgreSQL.** Establish development database configuration and connection management.
- [x] **4.6 Verify connectivity.** Add a health endpoint and call it from the frontend.
- [x] **4.7 Add CI and setup documentation.** Check builds, formatting, and relevant tests; document startup commands.
- [x] **4.8 Deploy an early staging build.** Verify hosting configuration before substantial implementation.

### Deliverables

- Runnable frontend and backend scaffold.
- Database connection and health endpoint.
- CI configuration, environment templates, and setup instructions.
- Minimal staging deployment.

**Completion criterion:** Frontend, backend, and database communicate locally, and staging can be rebuilt reliably.

## Phase 5 — Model Dynamic Data

### Steps

- [x] **5.1 Model public content.** Define `Member`, `Event`, `Project`, and `MediaAsset` records.
- [x] **5.2 Model recruitment.** Define `RecruitmentCycle` and `Application` records.
- [ ] **5.3 Model registrations where applicable.** Add `EventRegistration` if registration is managed locally.
- [ ] **5.4 Model administrator access.** Define accounts, sessions, and audit records appropriate to the selected authentication strategy.
- [ ] **5.5 Define data integrity.** Specify relationships, required fields, unique slugs, indexes, and duplicate-prevention constraints.
- [ ] **5.6 Define time handling.** Store event times consistently and display them in the appropriate timezone.
- [ ] **5.7 Define publication rules.** Include draft/published status, registration windows, and allowed status transitions.
- [ ] **5.8 Create migrations and seed data.** Seed confirmed content and isolate clearly labeled demonstration records.

### Deliverables

- Entity relationship diagram.
- Database models and migrations.
- Repeatable seed command and documented business rules.

**Completion criterion:** A fresh database can be created and populated reproducibly, with key integrity rules enforced.

## Phase 6 — Complete an Event Workflow End to End

### Steps

- [ ] **6.1 Implement administrator authentication.** Protect event-management endpoints with server-side authorization.
- [ ] **6.2 Build a minimal event editor.** Support creating, editing, previewing, and publishing an event.
- [ ] **6.3 Implement public event endpoints.** Expose published event lists and event details.
- [ ] **6.4 Connect event pages.** Render database records on the frontend.
- [ ] **6.5 Implement registration ownership.** Build local registration or the approved external handoff.
- [ ] **6.6 Enforce local registration rules.** Validate submissions, prevent duplicates, check deadlines, and allocate seats transactionally where applicable.
- [ ] **6.7 Complete feedback and review.** Show the event's registration status and its official destination. Surface confirmation and saved records when the website owns registration.
- [ ] **6.8 Test capacity contention.** Verify simultaneous requests for the last available place if local capacity management is used.

### Deliverables

- Working event editor, API, public event pages, and registration path.
- Relevant integration tests.

**Completion criterion:** An administrator's published update appears publicly without a source-code edit. For local registrations, records survive a server restart and capacity rules hold.

## Phase 7 — Build the Remaining Public Website

### Steps

- [ ] **7.1 Build shared layout.** Implement responsive navigation, mobile menu, footer, and reusable page components.
- [ ] **7.2 Build the homepage.** Populate featured events, projects, and team previews from the API.
- [ ] **7.3 Build the team page.** Include domain grouping, correct roles, and controlled display order.
- [ ] **7.4 Build project pages.** Include listing, detail views, contributor credits, and verified repository/demo links.
- [ ] **7.5 Build About and Contact.** Use confirmed descriptions and contact information.
- [ ] **7.6 Add archives and galleries.** Present past events and available approved media.
- [ ] **7.7 Complete resilience states.** Provide loading feedback, useful empty states, errors, and retry actions.
- [ ] **7.8 Add discovery metadata.** Configure page titles, descriptions, social previews, and meaningful URLs.

### Deliverables

- Complete responsive public pages.
- API-connected content and reusable components.
- Metadata and share-preview assets.

**Completion criterion:** Public routes work on mobile and desktop, and dynamic club records come from the backend.

## Phase 8 — Complete Recruitment and Administration

### Steps

- [ ] **8.1 Build the application form.** Use accessible labels, useful validation, and clearly explained required fields.
- [ ] **8.2 Enforce recruitment rules.** Validate opening and closing windows and duplicate submissions on the backend.
- [ ] **8.3 Save applications.** Persist submissions and return confirmation references.
- [ ] **8.4 Build the review dashboard.** Filter applications by domain, recruitment cycle, and status.
- [ ] **8.5 Implement review transitions.** Support pending, shortlisted, accepted, and rejected states with audit records.
- [ ] **8.6 Complete content editors.** Manage members, projects, media, and site settings.
- [ ] **8.7 Complete publishing controls.** Support draft previews and explicit publication actions.
- [ ] **8.8 Protect private data.** Restrict applicant information and exports with server-side permissions.

### Deliverables

- Recruitment workflow and administrator dashboard.
- Content management and audit history.
- Authorized submission review and export capabilities.

**Completion criterion:** Club leads can maintain content and review applications without modifying code, while private submissions remain protected.

## Phase 9 — Add Interaction and Visual Polish

### Steps

- [ ] **9.1 Add purposeful transitions.** Implement restrained hover, focus, page-entry, and action-feedback effects.
- [ ] **9.2 Implement theme behavior if included.** Save preferences and respect the system theme.
- [ ] **9.3 Respect reduced motion.** Provide appropriate alternatives to nonessential movement.
- [ ] **9.4 Evaluate the ink transition separately.** Check responsiveness, memory use, changing content, and fallback behavior before adopting it.
- [ ] **9.5 Keep actions usable.** Essential interactions must work while visual effects load or fail.
- [ ] **9.6 Optimize visual assets.** Improve image sizing, font loading, and expensive rendering effects.
- [ ] **9.7 Remove experiment controls.** Keep developer-facing animation settings out of the public interface.

### Deliverables

- Polished interaction states and reduced-motion behavior.
- Documented decision on the ink effect and any additional animation libraries.

**Completion criterion:** Effects improve feedback and atmosphere without compromising speed, accessibility, or functionality.

## Phase 10 — Validate Reliability, Accessibility, and Security

### Steps

- [ ] **10.1 Test core journeys.** Cover event publication, registration, recruitment, and application review.
- [ ] **10.2 Test failures and boundaries.** Include invalid input, duplicate requests, closed registration, and unauthorized access.
- [ ] **10.3 Verify authentication.** Check session expiry, logout, password handling, and permission enforcement.
- [ ] **10.4 Protect public submissions and uploads.** Apply suitable rate limits and validate file type, size, and handling.
- [ ] **10.5 Check accessibility.** Verify keyboard navigation, focus order, contrast, labels, form errors, and mobile layouts.
- [ ] **10.6 Check degraded conditions.** Exercise slow connections, API failures, missing media, and empty datasets.
- [ ] **10.7 Measure performance.** Fix the largest measured bottlenecks and record remaining limitations.
- [ ] **10.8 Validate recovery.** Test migrations and backup restoration against a production-like database.

### Deliverables

- Passing critical workflow tests.
- Accessibility and performance findings with fixes.
- Tested backup and restoration procedure.

**Completion criterion:** Critical workflows pass, no known access-control failures remain, and outstanding limitations are documented.

## Phase 11 — Launch, Demonstrate, and Hand Over

### Steps

- [ ] **11.1 Configure production.** Set secrets, database access, persistent media storage, and HTTPS.
- [ ] **11.2 Prepare production data.** Run migrations and load approved real content only.
- [ ] **11.3 Configure operations.** Add logs, error monitoring, health checks, and backups.
- [ ] **11.4 Verify the deployed experience.** Check refreshes, deep links, forms, images, authentication, and permissions.
- [ ] **11.5 Write handover instructions.** Document deployment, rollback, content editing, and administrator onboarding.
- [ ] **11.6 Prepare the technical explanation.** Explain architecture, data flow, validation, authentication, migrations, and tradeoffs accurately.
- [ ] **11.7 Prepare the demonstration.** Record a short walkthrough and capture polished screenshots.
- [ ] **11.8 Establish ownership.** Transfer necessary access securely and identify maintenance responsibilities.

### Deliverables

- Live production website.
- Deployment and administrator documentation.
- Architecture diagrams, demonstration video, and screenshots.

**Completion criterion:** Another authorized club member can operate the website, and the project owner can confidently explain and demonstrate its implementation.

## Milestones for Project Evaluation

| Milestone | Evidence |
| --- | --- |
| Original responsive design | Representative desktop and mobile pages |
| Integrated Python backend | An event published from the dashboard appears on the public site |
| Persistent business workflows | Published event content survives a restart. Local recruitment records persist when the approved workflow is enabled. |
| Useful administration | Club leads update content and authorized reviewers handle applications when local recruitment is active. |
| Reliable delivery | Passing checks, deployed workflows, recovery procedure, and clear documentation |

## Suggested Demonstration Sequence

1. Open the homepage on desktop and mobile.
2. Sign in as an administrator and create an event draft.
3. Publish the event and show it on the public website.
4. Show the event registration state and demonstrate the approved university-portal handoff.
5. Show that the published event and registration destination persist after restarting the backend.
6. Show the recruitment announcement or demonstrate the approved cycle. Use synthetic records for any local application and review demonstration.
7. Update a team member or project and show the public change.
8. Explain the request flow, database constraints, authorization, tests, and deployment.

## Deferred Features

Consider these only after the launch workflows are dependable:

- Student accounts and personal dashboards.
- Attendance QR codes and certificate generation.
- Live chat and community discussion.
- Music playback widgets.
- Advanced external-service integrations.
- Additional elaborate visual effects.

## Execution Notes

- Follow the phase order for dependencies, but gather content throughout development.
- Perform relevant tests during each implementation phase; Phase 10 is the broader release validation pass.
- Keep staging available from Phase 4 onward.
- Update this roadmap as decisions become concrete and check off work only after its completion criterion is met.
- A task is complete when its user-facing behavior works, not merely when its files exist.
