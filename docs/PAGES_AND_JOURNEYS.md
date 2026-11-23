# Code2Chill Pages and User Journeys

This is the website plan. It uses the [first-release scope](LAUNCH_SCOPE.md#first-public-release) and the [verified content register](CONTENT_REGISTER.md).

## Public sitemap

| ID | Page | Path | Purpose |
| --- | --- | --- | --- |
| PUB-01 | Home | `/` | Introduce the club and point students to its activities. |
| PUB-02 | About | `/about` | Explain the club, its university affiliation, and its areas of work. |
| PUB-03 | Events | `/events` | Show upcoming and past events. |
| PUB-04 | Event Detail | `/events/:slug` | Show the published event, its status, and the official sign-up destination when available. |
| PUB-05 | Projects | `/projects` | Present published student projects and their contributors. |
| PUB-06 | Project Detail | `/projects/:slug` | Explain an individual project, credit its contributors, and link to checked resources. |
| PUB-07 | Team | `/team` | Show the approved leadership roster and domain roles. |
| PUB-08 | Join | `/join` | Show the current recruitment state and the official membership interest path. |
| PUB-09 | Contact | `/contact` | Connect visitors with the verified university listing and club social profiles. |

```text
Home /
├── About /about
├── Events /events
│   └── Event Detail /events/:slug
├── Projects /projects
│   └── Project Detail /projects/:slug
├── Team /team
├── Join /join
└── Contact /contact
```

The header logo links to Home. Desktop and mobile navigation provide About, Events, Projects, Team, and Join. Contact stays in the shared footer and is available from About. Detail routes are reachable from their lists and by direct URL. `:slug` stands for the published item's unique URL identifier within its list. Example paths are `/events/byte-the-vibe`, `/events/domination-the-frontend-challenge`, and `/projects/nexus`. An unknown or unpublished item shows a not-found page with a link to its list. An unrecognized top-level path offers a link to Home.

## Event discovery and registration

```mermaid
flowchart TD
    H[Home or shared navigation] --> L[Events]
    L --> U[Upcoming events]
    L --> P[Past events]
    U -->|No published upcoming events| P
    U --> D[Published event detail]
    P --> D
    S[Shared event URL] --> D
    S -->|Event unavailable| L
    D --> R{Registration state and link}
    R -->|Open with verified destination| F[University event page]
    R -->|Closed full or ended| X[Show status and event details]
    R -->|Unconfirmed or missing link| Y[Show registration details pending]
```

On `/events`, put Upcoming before Past. Offer section links to `/events#upcoming-events` and `/events#past-events`. An empty upcoming section links to Past. Cards link to published detail pages and show the title, date, and verified venue when available. Use the [two dated event records](CONTENT_REGISTER.md#events-and-projects) for the starting archive.

| Detail case | Student experience |
| --- | --- |
| Open with an organizer-verified destination | **Register on the university portal** opens the official event page in the same tab. The portal owns account prompts, ticket selection, and confirmation. |
| Closed, full, or ended | Show the corresponding status with the event details. **Back to events** returns to Past for ended events and Upcoming for events yet to take place. |
| Open without a verified link, or availability is unknown | Show **Registration details pending**. Provide the event information and the link back to the relevant list section. |
| Event missing or unpublished | Show **Event not found** and offer **Browse events** to `/events`. |
| Request failure | Show an error with **Try again** for the same view and keep public navigation available. |

The [launch registration rules](LAUNCH_SCOPE.md#event-registration) apply across list and detail. Code2Chill displays the organizer-verified state. A student who sees a different outcome on the university site can return with the browser Back action.

## Recruitment journey

```mermaid
flowchart TD
    J[Join page] --> C{Recruitment cycle state}
    C -->|No approved cycle| A[Dates to be announced]
    A --> I[University club listing for membership interest]
    C -->|Scheduled or closed| T[Show the relevant dates or status]
    C -->|Open with approved external route| E[Official application destination]
    C -->|Open with approved local route| D[Read eligibility and choose an enabled domain]
    D --> F[Complete and submit local application]
    F -->|Saved successfully| R[Show confirmation and reference]
    F -->|Submission needs attention| S[Show error and recovery]
```

| Cycle or submission state | Student experience |
| --- | --- |
| No approved cycle | `/join` shows **Recruitment dates to be announced**. **View the club on the university portal** opens the official listing for general membership interest. |
| Scheduled cycle | Show the enabled domains, eligibility, and opening time in India Standard Time. |
| Open with an approved external route | **Apply through the official form** opens the approved destination. That provider handles the submission and confirmation. |
| Open with an approved local route | **Start application** opens the planned `/join/apply` page. Show eligibility and enabled domains. Collect the name, university email, and domain with the cycle's configured optional prompt. |
| Invalid local submission | Explain the field errors beside the inputs and in a focusable summary. Keep the student's entered values while they correct the form. |
| Local request fails or its result is uncertain | Keep the entered values in the current page and offer **Try again**. The server's duplicate rule prevents a retry from creating another record. |
| Local save confirmed | Show **Application received** and the confirmation reference. Keep applicant details out of the URL. Give the student a link back to Join. |
| Window closes, including while the local form is open | Show **Applications are closed** and return students to Join. The server checks the time again before accepting a submission. |

For a local application, only show duplicate-record details after verifying that the requester controls the university email. The implementation phase will choose how to verify ownership. The [recruitment rules](LAUNCH_SCOPE.md#recruitment) define cycle configuration and time boundaries. A direct visit to `/join/apply` when the local route is unavailable returns the student to the current Join state.
