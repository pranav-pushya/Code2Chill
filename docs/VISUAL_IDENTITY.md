# Code2Chill visual identity

## Art direction

Use the visual language of a campus event programme. The page should feel like something a student would pick up outside Pierre Hall. Warm paper carries the reading surface, dark ink carries the text, and blue ties the event links and artwork to the supplied club mark. The blue silhouette of a person sitting on the numeral 2 gives the engineering identity a human detail already present in the artwork.

### Home composition

- Set “Learn by building.” in large, condensed type with a short introduction naming Code2Chill and Chitkara University. Give **Explore events** the first action. Set the original mark in a dark poster panel beside it. Use broad concentric rules behind the mark as original print artwork.
- Follow with one dated entry from the event archive. Place the large day and month beside the event name, venue and detail link. The archive can remain useful between events.
- Give NEXUS a short description and contributor line. A project row can stand on typography while an approved screenshot is pending. Introduce the team by name and role. End with the recruitment announcement and membership-interest route.
- On a phone, keep the introduction and primary action together, then show the poster, event, project, team and membership in document order. Keep a readable Menu control in the header.

### Event detail composition

Open DOMination with its title, date, venue and **Event ended**. An oversized date block echoes a printed ticket and gives the long title room to wrap. Follow with the event brief and the participant work that came from it. A return link leads to the archive. A future open event can expose the verified university registration action under the [launch rules](LAUNCH_SCOPE.md#event-registration).

### Editorial rules

Use the condensed face for major titles, a readable sans serif for sentences and navigation, and short monospaced dates where alignment helps scanning. Use a single column for descriptions and a generous gap between sections. Links in paragraphs have an underline. Keep event status in words. Preserve normal reading order and visible keyboard focus across widths.

The brand panel and date block are illustrative graphics. Keep documentary photography and screenshots tied to a named event or project, its credit and reuse permission. For the public release, collapse an empty gallery and retain the written event detail. During design review, show the owner-requested labeled placements described below. Movement is optional and immediately responsive to reduced-motion preferences.

### Design basis

The [reference review](DESIGN_REFERENCE_ANALYSIS.md) informed the change of scale between heading and metadata. The [wireframes](WIREFRAMES.md) set the order of the content and the [page actions](PAGES_AND_JOURNEYS.md#page-actions) define its destinations. The [content register](CONTENT_REGISTER.md) supplies the public facts and image availability. The two [supplied logo](../Code2Chill.png) [variants](../Code2Chill_transparent.png) establish the club artwork.

## Tokens and components

The [design stylesheet](design/tokens.css) is the shared source for both mockups. Barlow Condensed Bold gives the title a tall, narrow shape. DM Sans handles body text and navigation, and system monospace handles dates. The Latin fonts ship locally with their [Barlow Condensed license](design/fonts/barlowcondensed-OFL.txt) and [DM Sans license](design/fonts/dmsans-OFL.txt). System fallbacks cover other glyphs and failed loads.

| Use | Specification |
| --- | --- |
| Reading | Ink on paper, muted text for metadata. Keep paragraphs around 55–65 characters wide. Use 16 px body text at the default size with 1.5 line height or greater. |
| Hierarchy | Fluid hero and section sizes cap the largest titles. Wrap long event names naturally. Use the small size for credits and metadata. |
| Layout | Use the spacing scale for local gaps, the responsive gutter for the page edges, and the section gap between topics. Content stops growing at 84 rem. |
| Primary action | Blue fill, light label, minimum height 44 px. Hover or press darkens the fill. A text link retains its underline in a paragraph. |
| Focus | Three-pixel blue outline on paper or sky outline on dark backgrounds, offset by three pixels. Keep the outline clear of clipping containers. Forced colors use the system highlight. |
| Event entry | One thin rule can group the date, title, venue and visible status. The title links to the detail. Underlined links and words communicate meaning independently of color. |
| Menu and status | A labeled disclosure exposes navigation on small screens. Ended events show “Event ended” and a return route to the archive. A pending recruitment cycle shows membership interest. |

The pale rule is a decorative separator. Use a text label or a contrasting border for any control that needs a visible boundary. Mark default focus on a dark panel using the `.on-ink` class. The examples use immediate state changes and require no motion library.

## Logo placement

| Placement | Artwork and use |
| --- | --- |
| Homepage brand panel | Use the trimmed transparent full mark on a uniform night surface. Allow at least one eighth of the mark width as clear space on each side. At 180 CSS px or wider the person, the letterforms and the lettering can be seen together. Keep decorative rules outside the mark. |
| Standalone square | Use the background version for a self-contained square image. Keep the original dark field and its internal margins. Fit the full canvas proportionally into a square. |
| Navigation and footer | Set the club name in real text. The header can pair it with the compact icon. Keep a single accessible name on the Home link and give a redundant adjacent icon empty alt text. |
| Browser tab | Use the central numeral as a light silhouette on a dark tile. The numeral is a small-size derivative for icons. Use the full supplied artwork in the brand panel. |
| Photography or a pale surface | Keep a solid dark tile behind the artwork. The transparent source has uneven antialiased edges that become visible on paper. Use the text wordmark where a dark tile would crowd the layout. |

Keep the original proportions and gradient in both full-logo exports. In an image-only placement use the alt text “Code2Chill club logo”. Where the surrounding text already names the club and the art adds no information, use empty alt text. Both [source files](CONTENT_REGISTER.md#asset-inventory) stay at the repository root. Retain them at their original resolution for future exports.

### Brand exports

| File | Intended placement |
| --- | --- |
| [240 px full mark](design/brand/club-mark-240.webp) and [480 px full mark](design/brand/club-mark-480.webp) | Responsive poster artwork. Both use the visible bounds of the transparent original. Select the source using the rendered width and device pixel density. |
| [384 px square](design/brand/club-square-384.webp) | Opaque profile tile. The 745 × 740 original is scaled proportionally and centered. |
| [64 px icon](design/brand/club-icon-64.png) | Compact club identifier beside a text label. |
| [Favicon](design/brand/favicon.ico) | Browser icon with embedded 16, 32 and 48 px sizes. |

The icon uses the connected silhouette of the numeral and seated figure from the original alpha mask. A light fill on navy keeps it readable in a small tab. The full marks preserve the gradient. Each export is smaller than its source PNG.

## Responsive page previews

Open [Home](design/index.html) or [DOMination event detail](design/domination.html) in a browser. Both pages use the same offline assets, font files and token stylesheet. The home preview uses a local archive section for **Explore events**. Its featured event opens the detail preview, and **Back to events** returns to the same section. The project credit links to its public repository. The membership action opens the university club page.

The wide layout pairs the introduction with a printed club panel and places the ticket beside the event name. Below 48 rem each becomes a vertical reading sequence. The compact navigation uses a native disclosure. Escape closes it and returns focus to Menu. The primary action, archived status and ticket information are available without scripting.

The two preview files cover the representative designs. Their section links stand in for the dedicated About, Events, Projects, Team and Join routes specified in the [production page plan](PAGES_AND_JOURNEYS.md#public-sitemap). The static files contain sample views of verified club records. Database publishing, remaining routes and live state changes belong to later phases.

### Temporary media placements

The owner approved placeholders on 23 November 2026 while the original media is unavailable. Each preview shows a figure labeled “Event photo placeholder” for DOMination and another labeled “Project screenshot placeholder” for NEXUS. Visible captions identify the intended subject. The pattern is CSS, so reviewers can see the footprint without a network request or a misleading photograph.

To replace a figure, record the actual file, subject, credit and permission against ASSET-03 or ASSET-04 in the [content register](CONTENT_REGISTER.md#asset-inventory). Replace the patterned panel in both previews with the approved image, set its intrinsic dimensions and descriptive alt text, then update the caption with the credit. Check the crop at desktop and phone widths before checking off Step 3.7.
