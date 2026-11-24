import { useState } from "react";
import { Link } from "react-router";

export function PublishedImage({ image }) {
  const [failedUrl, setFailedUrl] = useState(null);
  if (!image?.asset_url) return null;
  if (failedUrl === image.asset_url)
    return (
      <figure className="media-placeholder">
        <div className="media-frame">Image unavailable</div>
        <figcaption>
          {image.alt_text} · {image.credit}
        </figcaption>
      </figure>
    );
  return (
    <figure>
      <img
        style={{ maxWidth: "100%", height: "auto" }}
        loading="lazy"
        decoding="async"
        src={image.asset_url}
        alt={image.alt_text}
        onError={() => setFailedUrl(image.asset_url)}
      />
      <figcaption>{image.credit}</figcaption>
    </figure>
  );
}

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
