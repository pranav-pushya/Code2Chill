# Code2Chill peer repository comparison

**Reviewed:** 23 November 2026  
**Method:** Public GitHub repository metadata, file trees, README files, and selected source files were inspected. This is a source review, not a visual or deployment audit. Features described below are present in source unless explicitly marked as verified at runtime. The local comparison uses the current working tree, including uncommitted Phase 7 work that was completed during this review.

## What matters for this assignment

The brief calls for a **Python full-stack site with dynamic club data**. A useful comparison therefore asks whether a student can see real content, whether a club lead can update it without editing source, whether changes persist, whether a reviewer can run and test the project, and whether the experience has a clear club identity. Page count and animation alone do not answer those questions.

| Repository | Current implementation seen in source | Dynamic data and administration | Main advantage | Main gap against the brief |
| --- | --- | --- | --- | --- |
| [Ours](../README.md) | React/Vite public site, FastAPI API, PostgreSQL, Alembic, staff dashboard, tests and CI | Published events, projects and team are read from the database. Authorized staff can create, edit, preview and publish **events**. | Strong separation of public and draft content, repeatable migrations, verified sharing metadata, evidence and documentation | Project and team editing, recruitment intake, approved media and public deployment are not complete |
| [Jaslagankaur](https://github.com/jaslagankaur-design/CODE2CHILL_website) | Link returned GitHub API 404 at review time | Unknown | Cannot assess fairly | Request a working public link or access before comparing |
| [Sagarjit](https://github.com/sagarjitbatish-22/C2C_Website) | React/Vite/Tailwind client with Express/Mongoose server; event, team, Instagram, query and auth routes | Event creation and RSVP endpoints, team and Instagram data, query submission; MongoDB is optional and the server can use in-memory data | Broad community feature coverage and a published GitHub Pages client referenced in its README | Backend is JavaScript, so it does not satisfy a strict Python-backend requirement; in-memory mode does not persist changes |
| [Maggolaksh](https://github.com/maggolaksh5-ui/Code2Chill) | FastAPI/SQLAlchemy with HTML/CSS/JS pages; join and contact forms | SQLite stores join applications and contact messages | Small, understandable Python full-stack baseline | No event/project/team content management, admin workflow, migrations or tests found in the inspected tree |
| [Aastha](https://github.com/aasthagarg18/code2chill-website/tree/feature/frontend-setup) | React/Vite frontend with navigation, hero and About section | No backend or database found in the branch | Focused frontend starting point | Navigation targets beyond About have no matching sections in the inspected App; dynamic data is not implemented |
| [Ajy](https://github.com/ajysaihajleenlsnzl28-dotcom/Code2Chill) | FastAPI, SQLAlchemy, Jinja templates, admin and member flows, CSS/JS and pytest | Event registration and capacity, member accounts, projects, applications and admin content editing | Most complete directly comparable Python full-stack feature set | SQLite schema is created at startup with no migration files found; repository includes generated database and cache files |
| [ReekursiveMonk](https://github.com/ReekursiveMonk/Code2Chill) | React/Vite pages for home, events, projects, team, join, login, signup and profile | Event/project/team data are local JavaScript arrays; account state uses `sessionStorage` | Broad public UI and honest prototype labeling | README and UI identify it as a frontend prototype with no backend, database or real authentication |

## Repository notes and evidence

### Sagarjit: broad MERN implementation

The [client](https://github.com/sagarjitbatish-22/C2C_Website/tree/main/client) contains Hero, Events, Team, Instagram, authentication and query components. The [server](https://github.com/sagarjitbatish-22/C2C_Website/tree/main/server) defines routes and Mongoose models for events, Instagram posts, queries, team and users. Its API client stores a bearer token in `localStorage`. The README describes a MongoDB Atlas setup and an in-memory fallback. This covers more student interaction than ours currently does, but the fallback is ephemeral. Source inspection also found the server's CORS callback accepting origins outside its stated allow-list; review that before treating the deployment as production hardened. We have not exercised its live backend or measured its visual quality.

### Maggolaksh: compact FastAPI baseline

The [backend](https://github.com/maggolaksh5-ui/Code2Chill/tree/main/backend) exposes `/about`, `/join` and `/contact` and writes the two form types through SQLAlchemy. Its [frontend](https://github.com/maggolaksh5-ui/Code2Chill/tree/main/frontend%20html) is plain HTML, CSS and JavaScript in the inspected tree. The README describes React/Vite, but the current tree does not show that client, so the tree is the safer evidence. `Base.metadata.create_all` runs at import, and a SQLite database is committed. This is viable for demonstrating a simple form, but content editing and repeatable schema changes are still missing.

### Aastha: early frontend scaffold

The inspected [`feature/frontend-setup` branch](https://github.com/aasthagarg18/code2chill-website/tree/feature/frontend-setup) renders a navbar, hero and About block. Links to domains, events, team and join are present in navigation while matching sections are absent from the inspected `App.jsx`. That is a stage observation, not a judgment about the final design.

### Ajy: strongest feature comparator

The [application](https://github.com/ajysaihajleenlsnzl28-dotcom/Code2Chill/tree/main/app) uses server-rendered Jinja pages with FastAPI. The [tests](https://github.com/ajysaihajleenlsnzl28-dotcom/Code2Chill/tree/main/tests) cover public pages, CSRF, validation, event registration and capacity, duplicate registration, project URL validation, escaping, applications, admin and member login, content editing and seed behavior. Its README explains that event capacity locking is process-local and needs database locking with multiple workers. This is a meaningful limit for production, but it does not erase the breadth of working flows. Our event draft/publication split, PostgreSQL migrations and CI are stronger engineering foundations; Ajy's member journeys and admin content breadth are ahead of ours.

### ReekursiveMonk: broad UI prototype

The [frontend](https://github.com/ReekursiveMonk/Code2Chill/tree/main/Frontend/src) includes seven named public/account views plus a profile and missing-page route. Events, projects, statistics and team are static data modules. `AuthContext.jsx` holds a browser-session identity without server validation; the README and `PrototypeNotice.jsx` tell visitors this is a prototype. It is useful as a navigation and content-coverage reference, but forms and login do not yet demonstrate the required dynamic Python system.

### Jaslagankaur: access unresolved

The supplied [repository URL](https://github.com/jaslagankaur-design/CODE2CHILL_website) returned 404 through the public GitHub API on 23 November 2026. It may be private, renamed, removed or mistyped. No implementation or quality conclusion is possible from that result.

## Ours: position and next steps

Our [public API](../backend/app/public_content.py) reads published event, project and member snapshots. The [event editor API](../backend/app/admin_events.py) has staff authorization, saved drafts, preview, publication, revision conflicts and audit records. [Alembic migrations](../backend/alembic/versions), [pytest coverage](../backend/tests) and [CI](../.github/workflows/ci.yml) make these workflows reproducible. The [React routes](../frontend/src/main.jsx) expose Home, About, Events, Projects, Team, Join, Contact and admin pages. The [build guide](BUILD_GUIDE.md) records local verification, including browser checks; this review did not rerun them.

The comparison suggests this order of work:

1. **Publish a reviewable demo.** Phase 7 pages and sharing metadata are complete with labeled media placeholders and have passed local checks. Add approved imagery when supplied, then deploy so a reviewer can see the design and data flow without setting up the repository.
2. **Make more club content editable.** Add the planned admin flows for projects and team. The public APIs already read database records, but staff currently need code or seed changes to update those two collections.
3. **Complete recruitment as a real workflow.** Implement the planned cycle, application and review flows with explicit privacy and access rules. Ajy's implementation shows this is a visible differentiator; our schema alone is not a finished feature.
4. **Demonstrate one end-to-end story.** Show an editor creating an event, previewing it, publishing it, and seeing it on the public page with the approved university registration handoff. Use a concise demo script and screenshots in the viva.
5. **Keep visual quality tied to content.** Use real, permission-cleared event and project media, accurate member roles, good empty states, and restrained motion. Do not claim unverified club facts or fabricate activity to fill space.

## Content and presentation ideas found in peers

These are **fields and page ideas**, not verified facts about the club. Compare each lead with the [content register](CONTENT_REGISTER.md) before publication.

| Peer source | Useful idea or field our live site lacks | What we already have | Evidence needed before publication |
| --- | --- | --- | --- |
| [Sagarjit's team component and seed](https://github.com/sagarjitbatish-22/C2C_Website/tree/main/client/src/components) | Member portraits, a short personal quote, academic year or branch, GitHub and LinkedIn profiles, and domain badges | Verified full names, roles, and four head domains | Ask each member to approve their portrait, profile links, academic details and quote. Seed entries use shortened names and unsourced quotes. |
| [Sagarjit's Instagram section](https://github.com/sagarjitbatish-22/C2C_Website/blob/main/client/src/components/Instagram.jsx) | A social highlight that leads visitors to the official profile | Confirmed Instagram URL and event-gallery placeholders | Select actual posts, obtain the original media and reuse permission, and link to the exact post. Its seed uses stock photos and invented captions, reactions, dates and activities. |
| [Ajy's content and templates](https://github.com/ajysaihajleenlsnzl28-dotcom/Code2Chill/tree/main/app) | A fuller About narrative, event categories, project technology tags, member biographies and a contact or application flow | Short source-backed About, two real event records, two credited projects, Join announcement and official links | Check expanded wording against the university description; ask project authors for actual stacks and members for bios. The example seed projects, future events and people are demo records. |
| [Maggolaksh's Join and Contact pages](https://github.com/maggolaksh5-ui/Code2Chill/tree/main/frontend%20html) | Clear application fields and a direct message form | University interest handoff and social contact paths | Agree on a real recruitment cycle, data owner, retention and review process before collecting applications. Obtain a club-managed inbox or handler before accepting messages. |
| [ReekursiveMonk's Join and project data](https://github.com/ReekursiveMonk/Code2Chill/tree/main/Frontend/src) | FAQ, member interests, project categories and tech tags | Join announcement and two source-backed project descriptions | Club leadership must confirm eligibility, fees, time commitment, mentorship and project types. Its FAQ, events, projects and activity counts are marked sample data. |

**Potential club facts worth collecting next:** member-approved headshots and one-line introductions; real project stacks, screenshots and repository links; event posters, schedule, mentors, organizers and verified winners; an actual recruitment calendar and eligibility; club-approved contact address; and confirmed membership or event totals if the club wants impact figures. The peer repositories themselves do not verify these facts.

**Do not copy as club facts:** Sagarjit's “HackChill 2.0,” “Neural Nights,” weekly Turing Hall meetup, post reactions and captions; Ajy's “Campus Connect,” “Chill Scheduler,” “Code2Chill Kickoff,” “Build Night,” and demo members; ReekursiveMonk's sample events, projects, counts, FAQ answers and invented attendance. Treat peer visual layouts and field choices as inspiration, with original copy and verified records on our site.

## Viva questions

**Which repository is the closest technical competitor?** Ajy's: it is also a Python full-stack application and has more implemented student and admin journeys. Our advantage is the explicit draft/publication workflow, PostgreSQL migrations, API/frontend separation and CI.

**Why is a React page with hardcoded arrays not enough?** The assignment asks for dynamic data. A club lead should be able to change published content through authorized server operations and have it persist in the database.

**What would make ours visibly stronger?** A working public deployment with approved club media and a polished, accessible design, backed by a short event-publishing demonstration and broader content editing.

**What was not verified here?** We did not run the peer repositories, inspect their private configuration, test live APIs, or compare rendered pages at matched viewport sizes. Findings are limited to the public source available at review time.
