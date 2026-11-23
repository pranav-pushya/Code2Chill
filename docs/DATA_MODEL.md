# Code2Chill data model

## Public content

| Record | Stored information |
| --- | --- |
| Member | Name, route slug, public role, optional club domain and biography, display order, and optional portrait. |
| Event | Title, route slug, summary, confirmed calendar date when known, venue, official source page, and optional poster. |
| Project | Title, route slug, summary, optional repository and demo links, originating event, and screenshot. |
| Project credit | Ordered public credit with an optional link to a club member. Contributors can receive credit without appearing on the roster. |
| Media asset | Storage key, content type, alternative text, credit, optional source, and approval for public use. |

New media starts without approval. Missing times and unapproved photographs remain open in the content register. The database types and relationships are defined in the public models. [Content register](CONTENT_REGISTER.md) · [Public models](../backend/app/content_models.py)

## Recruitment

A recruitment cycle has a route, optional opening and closing instants, eligibility text and the domains explicitly enabled for that cycle. A new cycle starts pending with an empty domain list. An application refers to a cycle and a domain together. PostgreSQL checks that the domain belongs to that cycle.

Applications carry the submitted name and university email, optional motivation or portfolio, a review status, a submission attempt identifier and an opaque receipt. These records are private. The application intake, email ownership verification and review screens are scheduled for Phase 8. [Recruitment models](../backend/app/recruitment_models.py) · [Launch rules](LAUNCH_SCOPE.md#recruitment)

## Event registration ownership

An event can have an official source page and a confirmed signup destination. The two links serve different purposes. The stored registration state is pending, open, closed, full or ended. A new event defaults to pending.

The university portal owns event submissions and confirmations for launch. Step 5.3 therefore needs fields on Event. A future change in registration ownership would require a separate design for seats, duplicates and confirmation. [Launch registration decision](LAUNCH_SCOPE.md#event-registration)

## Administration

Phase 6 will use local administrator accounts and opaque server-side sessions. An account stores its normalized email, password hash, role and active flag. Phase 6 will hash passwords with Argon2id, place a cryptographically random session token in a secure HTTP-only cookie, and look up a SHA-256 digest of the token in the session table. Sessions carry creation, expiry and revocation instants. Request authorization and cookie handling belong to Phase 6.

The reviewer assignment joins an account to a particular recruitment cycle. The audit table stores the actor, action, typed record identifier, time and optional state changes. A typed identifier keeps an audit entry meaningful after the target record is removed. Deactivate accounts with audit history to retain attribution. Audit writes should store state names and record IDs, with applicant details and secrets kept out of the log. [Administrator models](../backend/app/admin_models.py) · [Administrator journey](PAGES_AND_JOURNEYS.md#administrator-journey)

## Integrity rules

- Public route slugs use lowercase letters, digits, and single hyphens between words. Slugs are unique within each content type. Recruitment cycle slugs follow the same format.
- Primary and foreign keys protect relationships. Removing a project removes its credit rows. Removing a linked roster member keeps the credited name and clears the optional member reference. A used media asset or originating event requires its references to be cleared before deletion.
- PostgreSQL checks required public text, nonnegative display order and credit positions, and approved media descriptions and credits. Storage keys are unique.
- Accounts and applications store trimmed lowercase email addresses. PostgreSQL permits one application per cycle and email, and one row per cycle and attempt identifier. A receipt and a session token digest each have their own unique identifier. Authenticating email ownership and recovering a receipt remain Phase 8 application responsibilities.
- Indexes support event date ordering, roster display order, projects by event, scoped applicant filtering, account sessions, and audit lookup by record.

Database constraints act even when records are written outside the HTTP API. [Public models](../backend/app/content_models.py) · [Recruitment models](../backend/app/recruitment_models.py) · [Administrator models](../backend/app/admin_models.py)

## Time handling

Store confirmed campus dates as dates. Leave the time fields empty when the source gives only a date. When the organizer supplies an exact start, store the instant and its corresponding campus date. PostgreSQL checks that the two agree in Asia/Kolkata and that an optional end is after the start.

Application timestamps, session timestamps, registration windows and event instants use PostgreSQL timestamp with time zone. The ORM requires a timezone offset and returns UTC. Use the shared campus conversion for dates and labels in India Standard Time. Windows include their opening instant and exclude their closing instant. A completed recruitment cycle needs both bounds. An external event can carry either confirmed bound. [Time helpers](../backend/app/time_rules.py)
