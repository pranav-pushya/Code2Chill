# Code2Chill Wireframes

These low-fidelity sketches use the [sitemap and workflows](PAGES_AND_JOURNEYS.md) and [content register](CONTENT_REGISTER.md). Brackets show controls. Desktop panels show placement and mobile panels show reading order. Shared public navigation and the footer are shown on Home and carry through the public pages.

## Home

**Path** `/`

The first screen introduces the club and leads to its events. The event and project previews reuse verified content.

**Desktop**

```text
+--------------------------------------------------------------------------+
| Code2Chill  ·  About  Events  Projects  Team  Join                       |
+--------------------------------------------------------------------------+
+--------------------------------------------------------------------------+
| A student-led technical club                                             |
| Learn by building at Chitkara University.                                |
| [ Explore events ]                                                       |
+--------------------------------------------------------------------------+
+------------------------------------+-------------------------------------+
| From the archive                   | Student work                        |
| DOMination – The Frontend          | NEXUS                               |
| Challenge                          | Adaptive survival game              |
| 18 July 2026 • Pierre Hall         |                                     |
+------------------------------------+-------------------------------------+
+--------------------------------------------------------------------------+
| Team preview  ·  Recruitment announcement                                |
| Footer  ·  Contact                                                       |
+--------------------------------------------------------------------------+
```

**Mobile**

```text
+------------------------------------+
| Code2Chill  [ Menu ]               |
+------------------------------------+
+------------------------------------+
| A student-led technical club       |
| Learn by building at Chitkara      |
| University.                        |
| [ Explore events ]                 |
+------------------------------------+
+------------------------------------+
| From the archive                   |
| DOMination – The Frontend          |
| Challenge                          |
| 18 July 2026 • Pierre Hall         |
+------------------------------------+
+------------------------------------+
| Student work                       |
| NEXUS                              |
| Team preview                       |
| Recruitment announcement           |
| Footer  ·  Contact                 |
+------------------------------------+
```

## About

**Path** `/about`

The page explains the student-led club and the work its four domains support.

**Desktop**

```text
+--------------------------------------------------------------------------+
| About Code2Chill                                                         |
+--------------------------------------------------------------------------+
+------------------------------------+-------------------------------------+
| Student-led at Chitkara University | Club domains                        |
| Workshops, hackathons, and coding  | Technical • Content                 |
| events                             | Social Media • Promotion            |
| [ Meet the team ]                  |                                     |
+------------------------------------+-------------------------------------+
+--------------------------------------------------------------------------+
| [ Contact ]  ·  Footer                                                   |
+--------------------------------------------------------------------------+
```

**Mobile**

```text
+------------------------------------+
| About Code2Chill                   |
+------------------------------------+
+------------------------------------+
| Student-led at Chitkara University |
| Workshops, hackathons, and coding  |
| events                             |
| [ Meet the team ]                  |
+------------------------------------+
+------------------------------------+
| Club domains                       |
| Technical                          |
| Content                            |
| Social Media                       |
| Promotion                          |
+------------------------------------+
+------------------------------------+
| [ Contact ]  ·  Footer             |
+------------------------------------+
```

## Events

**Path** `/events`

The current example displays the verified archive and shows an empty upcoming schedule.

**Desktop**

```text
+--------------------------------------------------------------------------+
| Events                                                                   |
| [ Upcoming events ]  [ Past events ]                                     |
+--------------------------------------------------------------------------+
+--------------------------------------------------------------------------+
| Upcoming                                                                 |
| No upcoming events are listed.                                           |
| [ Browse past events ]                                                   |
+--------------------------------------------------------------------------+
+------------------------------------+-------------------------------------+
| Past                               | Past                                |
| DOMination – The Frontend          | Byte The Vibe                       |
| Challenge                          | 18 May 2026 • Pierre Hall           |
| 18 July 2026 • Pierre Hall         |                                     |
+------------------------------------+-------------------------------------+
```

**Mobile**

```text
+------------------------------------+
| Events                             |
| [ Upcoming events ]                |
| [ Past events ]                    |
+------------------------------------+
+------------------------------------+
| Upcoming                           |
| No upcoming events are listed.     |
| [ Browse past events ]             |
+------------------------------------+
+------------------------------------+
| Past                               |
| DOMination – The Frontend          |
| Challenge                          |
| 18 July 2026 • Pierre Hall         |
+------------------------------------+
+------------------------------------+
| Byte The Vibe                      |
| 18 May 2026 • Pierre Hall          |
+------------------------------------+
```

## Event detail

**Path** `/events/:slug`

The archive example shows an ended event. A verified open event uses the action from the event state matrix.

**Desktop**

```text
+--------------------------------------------------------------------------+
| Events / DOMination                                                      |
+--------------------------------------------------------------------------+
+------------------------------------+-------------------------------------+
| DOMination – The Frontend          | Event ended                         |
| Challenge                          | [ Back to events ]                  |
| 18 July 2026                       |                                     |
| Pierre Hall, Architecture Block    |                                     |
| Teams built web interfaces for the |                                     |
| challenge.                         |                                     |
+------------------------------------+-------------------------------------+
```

**Mobile**

```text
+------------------------------------+
| Events / DOMination                |
+------------------------------------+
+------------------------------------+
| DOMination – The Frontend          |
| Challenge                          |
| 18 July 2026                       |
| Pierre Hall, Architecture Block    |
| Event ended                        |
| [ Back to events ]                 |
+------------------------------------+
+------------------------------------+
| Teams built web interfaces for the |
| challenge.                         |
+------------------------------------+
```

## Projects

**Path** `/projects`

The example uses NEXUS as a sourced candidate. A card can be presented with text while imagery is unavailable.

**Desktop**

```text
+--------------------------------------------------------------------------+
| Projects                                                                 |
| Student projects from Code2Chill activities                              |
+--------------------------------------------------------------------------+
+------------------------------------+-------------------------------------+
| NEXUS                              | Contributors                        |
| Adaptive survival game from        | Ayush Sharma, Arnav Sharma,         |
| DOMination                         | and Anveer Singh Sandhu             |
| [ View project ]                   |                                     |
+------------------------------------+-------------------------------------+
```

**Mobile**

```text
+------------------------------------+
| Projects                           |
| Student projects from club         |
| activities                         |
+------------------------------------+
+------------------------------------+
| NEXUS                              |
| Adaptive survival game from        |
| DOMination                         |
| Ayush Sharma, Arnav Sharma,        |
| and Anveer Singh Sandhu            |
| [ View project ]                   |
+------------------------------------+
```

## Project detail

**Path** `/projects/:slug`

Primary and secondary resources occupy clear positions beside the title and contributor credits.

**Desktop**

```text
+--------------------------------------------------------------------------+
| Projects / NEXUS                                                         |
+--------------------------------------------------------------------------+
+------------------------------------+-------------------------------------+
| NEXUS                              | [ Open project demo ]               |
| A survival game with adaptive      | [ View source repository ]          |
| difficulty.                        |                                     |
| Built for DOMination.              |                                     |
| Ayush Sharma, Arnav Sharma, and    |                                     |
| Anveer Singh Sandhu                |                                     |
+------------------------------------+-------------------------------------+
```

**Mobile**

```text
+------------------------------------+
| Projects / NEXUS                   |
+------------------------------------+
+------------------------------------+
| NEXUS                              |
| A survival game with adaptive      |
| difficulty.                        |
| Built for DOMination.              |
| [ Open project demo ]              |
| [ View source repository ]         |
+------------------------------------+
+------------------------------------+
| Contributors                       |
| Ayush Sharma, Arnav Sharma,        |
| and Anveer Singh Sandhu            |
+------------------------------------+
```

## Team

**Path** `/team`

Leadership is followed by the published roles. On a narrow screen the same sections follow in a single column.

**Desktop**

```text
+--------------------------------------------------------------------------+
| Team                                                                     |
| Lakshay Kalra • President   |   Jiya Arora • Vice-president              |
+--------------------------------------------------------------------------+
+------------------------------------+-------------------------------------+
| Technical                          | Social Media                        |
| Samanyu Thakur • Bhupinder Singh   | Jashan Bhalla                       |
| Content                            | Promotion                           |
| Tamanna Kakkar • Ayush Sharma      | Muskan Dhanda                       |
+------------------------------------+-------------------------------------+
+--------------------------------------------------------------------------+
| Core members: Divyana Garg, Hunar Mehndiratta                            |
| [ Explore joining ]                                                      |
+--------------------------------------------------------------------------+
```

**Mobile**

```text
+------------------------------------+
| Team                               |
| Lakshay Kalra • President          |
| Jiya Arora • Vice-president        |
+------------------------------------+
+------------------------------------+
| Technical • Content                |
| Samanyu Thakur • Bhupinder Singh   |
| Tamanna Kakkar • Ayush Sharma      |
+------------------------------------+
+------------------------------------+
| Social Media • Promotion           |
| Jashan Bhalla • Muskan Dhanda      |
+------------------------------------+
+------------------------------------+
| Core members                       |
| Divyana Garg • Hunar Mehndiratta   |
| [ Explore joining ]                |
+------------------------------------+
```

## Join

**Path** `/join`

The launch view gives students an official membership interest destination while the next cycle is pending.

**Desktop**

```text
+--------------------------------------------------------------------------+
| Join Code2Chill                                                          |
+--------------------------------------------------------------------------+
+------------------------------------+-------------------------------------+
| Recruitment dates to be announced  | Club domains                        |
| [ View the club on the university  | Technical • Content • Social Media  |
| portal ]                           | • Promotion                         |
+------------------------------------+-------------------------------------+
```

**Mobile**

```text
+------------------------------------+
| Join Code2Chill                    |
+------------------------------------+
+------------------------------------+
| Recruitment dates to be announced  |
| [ View the club on the university  |
| portal ]                           |
+------------------------------------+
+------------------------------------+
| Club domains                       |
| Technical • Content                |
| Social Media • Promotion           |
+------------------------------------+
```

## Contact

**Path** `/contact`

The university page and verified social profiles provide contact paths.

**Desktop**

```text
+--------------------------------------------------------------------------+
| Contact Code2Chill                                                       |
+--------------------------------------------------------------------------+
+------------------------------------+-------------------------------------+
| Chitkara University                | Club profiles                       |
| [ View the club on the university  | [ Instagram ]  [ LinkedIn ]         |
| portal ]                           |                                     |
+------------------------------------+-------------------------------------+
```

**Mobile**

```text
+------------------------------------+
| Contact Code2Chill                 |
| Chitkara University                |
| [ View the club on the university  |
| portal ]                           |
+------------------------------------+
+------------------------------------+
| Club profiles                      |
| [ Instagram ]                      |
| [ LinkedIn ]                       |
+------------------------------------+
```

## Local recruitment application

**Path** `/join/apply`

Conditional screen for an approved local cycle. On mobile the same form inputs stay in a single reading order.

**Desktop**

```text
+--------------------------------------------------------------------------+
| Join / Application                                                       |
| Eligibility and deadline                                                 |
+--------------------------------------------------------------------------+
+------------------------------------+-------------------------------------+
| Application                        | Cycle details                       |
| [ Full name                    ]   | Available domains                   |
| [ University email             ]   | [ Back to Join ]                    |
| [ Select an enabled domain     ]   |                                     |
| [ Optional cycle prompt        ]   |                                     |
| [ Submit application ]             |                                     |
+------------------------------------+-------------------------------------+
```

**Mobile**

```text
+------------------------------------+
| Join / Application                 |
| Eligibility and deadline           |
+------------------------------------+
+------------------------------------+
| [ Full name ]                      |
| [ University email ]               |
| [ Select an enabled domain ]       |
| [ Optional cycle prompt ]          |
| [ Submit application ]             |
| [ Back to Join ]                   |
+------------------------------------+
```

## Admin sign-in and dashboard

**Paths** `/admin/sign-in` and `/admin`

The sign-in screen precedes the permitted dashboard. The two panels represent successive screens.

**Desktop**

```text
+------------------------------------+-------------------------------------+
| Admin sign-in                      | Dashboard                           |
| [ Email ]                          | Content • Settings • Media          |
| [ Password ]                       | Local applications, when assigned   |
| [ Sign in ]                        | [ Manage content ]                  |
+------------------------------------+-------------------------------------+
```

**Mobile**

```text
+------------------------------------+
| Admin sign-in                      |
| [ Email ]                          |
| [ Password ]                       |
| [ Sign in ]                        |
+------------------------------------+
+------------------------------------+
| Dashboard after sign-in            |
| [ Manage content ]                 |
| Settings • Media                   |
| Local applications, when assigned  |
+------------------------------------+
```

## Admin content and preview

**Paths** `/admin/content/:type` and `/admin/content/:type/:id/preview`

Staff move from the content list into a draft and then into a protected preview. The preview shows the saved draft before the publish confirmation.

**Desktop**

```text
+--------------------------------------------------------------------------+
| Admin / Events  ·  [ New draft ]                                         |
+--------------------------------------------------------------------------+
+------------------------------------+-------------------------------------+
| Event editor                       | Protected preview                   |
| DOMination – The Frontend          | DOMination – The Frontend Challenge |
| Challenge                          | [ Back to editor ]                  |
| Date • Venue • Registration status | [ Publish ]                         |
| [ Save draft ]                     |                                     |
| [ Preview draft ]                  |                                     |
+------------------------------------+-------------------------------------+
```

**Mobile**

```text
+------------------------------------+
| Admin / Events                     |
| [ New draft ]                      |
+------------------------------------+
+------------------------------------+
| Event editor                       |
| DOMination – The Frontend          |
| Challenge                          |
| Date • Venue • Registration status |
| [ Save draft ]                     |
| [ Preview draft ]                  |
+------------------------------------+
+------------------------------------+
| Protected preview                  |
| [ Back to editor ]                 |
| [ Publish ]                        |
+------------------------------------+
```

## Admin settings and media

**Paths** `/admin/settings` and `/admin/media`

These planned areas support official links and approved media. Staff enter either screen from the dashboard.

**Desktop**

```text
+------------------------------------+-------------------------------------+
| Site settings                      | Media                               |
| University listing URL             | Approved media • Credit             |
| Club social profiles               | [ Add media ]                       |
| [ Save settings ]                  |                                     |
+------------------------------------+-------------------------------------+
```

**Mobile**

```text
+------------------------------------+
| Site settings                      |
| University listing URL             |
| Club social profiles               |
| [ Save settings ]                  |
+------------------------------------+
+------------------------------------+
| Media                              |
| Approved media • Credit            |
| [ Add media ]                      |
+------------------------------------+
```

## Admin local application review

**Path** `/admin/recruitment/:cycleId/applications`

Conditional screen for an assigned reviewer. The placeholder is a label for layout and contains no applicant data.

**Desktop**

```text
+--------------------------------------------------------------------------+
| Admin / Local applications                                               |
+--------------------------------------------------------------------------+
+------------------------------------+-------------------------------------+
| Applications                       | Application details                 |
| [ Domain filter ] [ Status filter  | Applicant and review fields         |
| ]                                  | [ Save decision ]                   |
| [ Open application ]               |                                     |
+------------------------------------+-------------------------------------+
```

**Mobile**

```text
+------------------------------------+
| Admin / Local applications         |
| [ Domain filter ]                  |
| [ Status filter ]                  |
| [ Open application ]               |
+------------------------------------+
+------------------------------------+
| Application details                |
| Applicant and review fields        |
| [ Save decision ]                  |
+------------------------------------+
```
