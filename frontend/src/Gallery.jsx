import { Link } from "react-router";

export function MediaPlaceholder({ project = false, children }) {
  return (
    <figure
      className={`media-placeholder ${project ? "screen-slot" : "photo-slot"}`}
    >
      <div className="media-frame">
        <span>
          {project
            ? "Project screenshot placeholder"
            : "Event photo placeholder"}
        </span>
      </div>
      <figcaption>{children}</figcaption>
    </figure>
  );
}

export function EventGallery({ events }) {
  return (
    <section
      className="content-block"
      id="event-gallery"
      aria-labelledby="gallery-heading"
    >
      <h2 id="gallery-heading">Event gallery</h2>
      <div className="gallery-grid">
        {events.map((event) => (
          <MediaPlaceholder key={event.slug}>
            <Link className="text-link" to={`/events/${event.slug}`}>
              {event.title}
            </Link>
            {event.venue && <> · {event.venue}</>}
          </MediaPlaceholder>
        ))}
      </div>
    </section>
  );
}
