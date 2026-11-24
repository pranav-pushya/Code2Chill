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
        {events.map((event) =>
          event.poster?.asset_url ? (
            <figure key={event.slug} className="media-placeholder photo-slot">
              <div className="media-frame media-frame-photo">
                <Link
                  to={`/events/${event.slug}`}
                  className="media-frame-link"
                  aria-label={`View ${event.title}`}
                >
                  <img
                    loading="lazy"
                    decoding="async"
                    src={event.poster.asset_url}
                    alt={event.poster.alt_text || event.title}
                    className="gallery-poster-img"
                    style={{
                      objectPosition:
                        event.slug === "on-fire"
                          ? "center 22%"
                          : "center center",
                    }}
                  />
                </Link>
              </div>
              <figcaption>
                <Link className="text-link" to={`/events/${event.slug}`}>
                  {event.title}
                </Link>
                {event.venue && <> · {event.venue}</>}
              </figcaption>
            </figure>
          ) : (
            <MediaPlaceholder key={event.slug}>
              <Link className="text-link" to={`/events/${event.slug}`}>
                {event.title}
              </Link>
              {event.venue && <> · {event.venue}</>}
            </MediaPlaceholder>
          ),
        )}
      </div>
    </section>
  );
}
