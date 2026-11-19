# Code2Chill Launch Scope

## Event registration

Use the [Chitkara University Clubs & Events portal](https://chitkarau.life/) as the registration system for the public launch. Code2Chill publishes event information and links to the event's official registration page when it is available. The university portal handles any sign-in, registration, capacity, deadlines, and confirmation. This is the website's launch design. The organizer still confirms the destination and availability for each event.

The university's [Byte The Vibe](https://chitkarau.life/events/byte-the-vibe) and [DOMination](https://chitkarau.life/events/domination-the-frontend-challenge) records display historical sign-up information and show both events as ended. The public Code2Chill site will keep its own content records and send students to the approved event-specific university URL for a live sign-up.

| Event state | Public website behavior |
| --- | --- |
| Registration confirmed closed, full, or event ended | Show the applicable status and keep the event available for reference. |
| Registration confirmed open with an event-specific university link | Show **Register on the university portal** and link to the verified event page. |
| All other cases, including a missing link or unconfirmed status | Show the event details and indicate that registration details are pending. |

An administrator confirms the link, event identity, and registration state before enabling the action. The Code2Chill website stores event content, the official link, and the current published registration state. Student records, seat allocation, and confirmation stay with the portal. Verify the destination and event state again before launch and whenever the organizer changes registration details.

The viva walkthrough will show an administrator publishing or updating an event, the public page reflecting the saved change, and the registration button opening the approved destination. Use a clearly labeled demonstration record when no live event is open. Keep a future local registration workflow subject to a club and university decision about ownership and data access.

## Recruitment

The public Join page starts with **Recruitment dates to be announced**. It can link to the [university's Code2Chill listing](https://chitkarau.life/clubs/code2chill) for membership interest. The club listing labels its action “I'm Interested.” A Code2Chill domain application requires a separately configured cycle and an approved application route.

| Cycle setting | Planned rule |
| --- | --- |
| Dates | Store opening and closing datetimes for each cycle. Require a closing time after opening time. Display both in India Standard Time. The opening time is inclusive and the closing time is exclusive. |
| Available domains | Publish the subset explicitly enabled for the cycle. Technical, Content, Social Media, and Promotion are the known club domains. A new cycle starts with an empty selection. |
| Eligibility | Show the club's approved eligibility before the application. Check applicable rules on the server for a local form. Reviewers verify eligibility rules that require manual review. |
| Reviewers | Club leadership assigns reviewers for the cycle. A local review dashboard must restrict private application records to the authorized reviewers and administrators. |
| Application route | Use one approved destination for each cycle. A local form can be enabled after Phase 8 implements it and the club assigns reviewers and approves any data collection. |

| Planned local form field | Requirement |
| --- | --- |
| Full name | Required for identification during review. |
| University email | Required for correspondence and the one-application-per-cycle rule. Verify the acceptable email policy for the cycle. |
| Domain choice | Required. Show the domains enabled for that cycle. |
| Short motivation or a public portfolio link | Optional. The club can request the relevant prompt when configuring the cycle. |

The approved dates, eligibility, domains, reviewers, and application route must be present before the public Apply action can appear. Before opening, show the scheduled date. While open, point to the approved route. After closing, show that applications are closed. Phase 8 will enforce the same window, domain choices, and duplicate rule on the backend for local forms. The club still needs to supply the actual cycle settings and assignments.
