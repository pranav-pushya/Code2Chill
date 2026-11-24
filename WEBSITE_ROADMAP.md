# Code2Chill Website — Implementation Roadmap

**Prepared:** 16 November 2026  
**Project:** Dynamic Python full-stack website for Code2Chill, Chitkara University  
Phase 10 verified through step 10.6. The next step is 10.7. Step 3.7 awaits approved club images and credits.

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
| Frontend | React, JavaScript, Vite |
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
- [x] **4.4 Initialize the frontend.** Configure React with JavaScript, routing, and the styling system.
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
- [x] **5.3 Model registrations where applicable.** Add `EventRegistration` if registration is managed locally.
- [x] **5.4 Model administrator access.** Define accounts, sessions, and audit records appropriate to the selected authentication strategy.
- [x] **5.5 Define data integrity.** Specify relationships, required fields, unique slugs, indexes, and duplicate-prevention constraints.
- [x] **5.6 Define time handling.** Store event times consistently and display them in the appropriate timezone.
- [x] **5.7 Define publication rules.** Include draft/published status, registration windows, and allowed status transitions.
- [x] **5.8 Create migrations and seed data.** Seed confirmed content and isolate clearly labeled demonstration records.

### Deliverables

- [Entity relationship diagram](docs/DATA_MODEL.md#entity-relationship-diagram).
- [Database models and migrations](docs/DATA_MODEL.md#migrations-and-initial-records).
- [Repeatable seed command](docs/DEVELOPMENT.md#initialize-the-data-schema) and [business rules](docs/DATA_MODEL.md).

**Completion criterion:** A fresh database can be created and populated reproducibly, with key integrity rules enforced.

## Phase 6 — Complete an Event Workflow End to End

### Steps

- [x] **6.1 Implement administrator authentication.** Staff can sign in and sign out. The server restricts the event-management API to active admins and editors. [Account setup](docs/DEVELOPMENT.md#create-a-staff-account)
- [x] **6.2 Build a minimal event editor.** Admins and editors can save, preview and explicitly publish a revision. [Publishing instructions](docs/DEVELOPMENT.md#publish-an-event)
- [x] **6.3 Implement public event endpoints.** The list and detail routes serve the published snapshots of ordinary events.
- [x] **6.4 Connect event pages.** The schedule and detail pages render published records. Staff preview the saved revision in the same event layout.
- [x] **6.5 Implement registration ownership.** Open registration links to the organizer-verified event page on the university portal.
- **6.6 Enforce local registration rules.** Not applicable for launch. The university portal handles submissions, duplicates, deadlines, and seats.
- [x] **6.7 Complete feedback and review.** Show the effective registration state and display the university destination alongside the open registration action.
- **6.8 Test capacity contention.** Not applicable for launch. The university portal allocates the last seat. [Registration ownership](docs/LAUNCH_SCOPE.md#event-registration)

### Deliverables

- Working event editor, API, public event pages, and registration path.
- Relevant integration tests.

**Completion criterion:** An administrator's published update appears publicly without a source-code edit. For local registrations, records survive a server restart and capacity rules hold.

## Phase 7 — Build the Remaining Public Website

### Steps

- [x] **7.1 Build shared layout.** Desktop navigation, a keyboard-accessible mobile menu, footer and shared page components connect the public routes.
- [x] **7.2 Build the homepage.** The homepage loads a featured event, student project and team preview from the API.
- [x] **7.3 Build the team page.** The published roster shows leadership, domain roles and core members in their configured order within each group.
- [x] **7.4 Build project pages.** Each published project has a detail route, contributor credits and available verified demo or repository links.
- [x] **7.5 Build About and Contact.** Both routes use the confirmed club description and official contact links.
- [x] **7.6 Add archives and galleries.** The archive has a linked, responsive event gallery. Event photography and project screenshots use the owner-requested labeled placeholders until approved files and credits arrive. [Asset inventory](docs/CONTENT_REGISTER.md#asset-inventory)
- [x] **7.7 Complete resilience states.** Public lists, details and homepage previews handle loading, empty results, missing records and retryable errors.
- [x] **7.8 Add discovery metadata.** Public URLs return page-specific titles and descriptions, canonical links and a branded social preview in the initial HTML. Detail pages use published snapshots. [Verification](docs/BUILD_GUIDE.md#task-065--serve-discovery-metadata-and-a-branded-share-card)

### Deliverables

- Complete responsive public pages.
- API-connected content and reusable components.
- Metadata and share-preview assets.

**Completion criterion:** Public routes work on mobile and desktop, and dynamic club records come from the backend.

## Phase 8 — Complete Recruitment and Administration

### Steps

- [x] **8.1 Build the application form.** Join shows the configured cycle and takes eligible applicants to the accessible local form or approved external destination.
- [x] **8.2 Enforce recruitment rules.** The backend checks the published window, active reviewer assignment, enabled domain, verified university email and one application per cycle and email.
- [x] **8.3 Save applications.** Persist the application and return a confirmation reference. A verified retry of the same attempt and details can recover the original reference after closing.
- [x] **8.4 Build the review dashboard.** Authorized staff can choose a cycle, filter by domain and status, and return from an application to the same filtered list.
- [x] **8.5 Implement review transitions.** Authorized staff can shortlist, accept or reject applications. Each saved decision records the actor, time and status change, and a stale review must reload before saving.
- [x] **8.6 Complete content editors.** Manage members, projects, media, and site settings.
- [x] **8.7 Complete publishing controls.** Support draft previews and explicit publication actions.
- [x] **8.8 Protect private data.** Restrict applicant information and exports with server-side permissions. [Verification](docs/BUILD_GUIDE.md#task-077--restrict-applicant-exports-and-audit-downloads)
- [x] **8.9 Change staff passwords.** Let signed-in staff verify their current password and set a new one. [Verification](docs/BUILD_GUIDE.md#task-078--add-staff-password-change-endpoint-and-view)
- [x] **8.10 Show or hide passwords.** Add accessible eye controls to the sign-in and change-password forms. [Verification](docs/BUILD_GUIDE.md#task-079--add-accessible-password-visibility-toggle)

### Deliverables

- Recruitment workflow and administrator dashboard.
- Content management and audit history.
- Authorized submission review and export capabilities.

**Completion criterion:** Club leads can maintain content and review applications without modifying code, while private submissions remain protected.

## Phase 9 — Add Interaction and Visual Polish

### Steps

- [x] **9.1 Add purposeful transitions.** Implement restrained hover, focus, page-entry, and action-feedback effects.
- [x] **9.2 Implement theme behavior if included.** Preserved signature warm ink-on-paper campus event programme identity; documented decision to omit theme toggle and refined high-contrast readability across poster sections.
- [x] **9.3 Respect reduced motion.** Provide appropriate alternatives to nonessential movement. Collapsed transition durations to 0.01ms, disabled vestibular spatial transforms and page-enter translations, and provided clear color, outline, and shadow alternatives for interactive controls.
- [x] **9.4 Evaluate the ink transition separately.** Evaluated responsiveness, memory footprint, dynamic data interleaving, and accessibility; resolved DEC-007 by adopting zero-overhead CSS compositor transitions in production.
- [x] **9.5 Keep actions usable.** Essential interactions must work while visual effects load or fail. Protected sticky header anchor scroll padding, guaranteed non-blocking transition pointer events, enabled forced-colors high contrast focus outlines, and provided print media fallbacks.
- [x] **9.6 Optimize visual assets.** Improve image sizing, font loading, and expensive rendering effects. Added fetchPriority="high" and decoding="async" on hero and gallery images, isolated decorative background hit-testing with pointer-events: none, and applied layout/paint containment to cards.
- [ ] **9.7 Remove experiment controls.** Keep developer-facing animation settings out of the public interface.

### Deliverables

- Polished interaction states and reduced-motion behavior.
- Documented decision on the ink effect and any additional animation libraries.

**Completion criterion:** Effects improve feedback and atmosphere without compromising speed, accessibility, or functionality.

## Phase 10 — Validate Reliability, Accessibility, and Security

### Steps

- [x] **10.1 Test core journeys.** Cover event publication, registration, recruitment, and application review.
- [x] **10.2 Test failures and boundaries.** Include invalid input, duplicate requests, closed registration, and unauthorized access.
- [x] **10.3 Verify authentication.** Check session expiry, logout, password handling, and permission enforcement.
- [x] **10.4 Protect public submissions and uploads.** Apply suitable rate limits and validate file type, size, and handling.
- [x] **10.5 Check accessibility.** Verify keyboard navigation, focus order, contrast, labels, form errors, and mobile layouts.
- [x] **10.6 Check degraded conditions.** Exercise slow connections, API failures, missing media, and empty datasets.
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
