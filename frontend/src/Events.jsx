import { useEffect } from "react";
import { Link, useLocation, useParams } from "react-router";
import { PublicData } from "./PublicData.jsx";
import { ExternalLink, Missing, Page } from "./SiteLayout.jsx";

const states = {
  ended: "Event ended",
  open: "Registration open",
  full: "Event full",
  closed: "Registration closed",
  pending: "Registration details pending",
};
const monthYear = new Intl.DateTimeFormat("en-IN", {
  month: "short",
  year: "numeric",
  timeZone: "UTC",
});
const campusTime = new Intl.DateTimeFormat("en-IN", {
  timeStyle: "short",
  timeZone: "Asia/Kolkata",
});

function EventDate({ date, ticket = false }) {
  return (
    <time className={ticket ? undefined : "date-stamp"} dateTime={date}>
      <strong className={ticket ? "ticket-day" : undefined}>
        {date.slice(-2)}
      </strong>{" "}
      {monthYear.format(new Date(`${date}T00:00:00Z`)).toUpperCase()}
    </time>
  );
}

export function EventRow({ event }) {
  return (
    <Link className="event-row" to={`/events/${event.slug}`}>
      <EventDate date={event.event_date} />
      <span className="event-name">{event.title}</span>
      <span className="event-place">
        {event.venue}
        <span className="meta">{states[event.registration_status]}</span>
      </span>
    </Link>
  );
}

function Schedule({ upcoming, past }) {
  const { hash } = useLocation();
  useEffect(() => {
    if (hash) document.getElementById(hash.slice(1))?.scrollIntoView();
  }, [hash]);
  if (!upcoming.length && !past.length)
    return (
      <>
        <p>No events are listed.</p>
        <Link className="text-link" to="/">
          Back to home
        </Link>
      </>
    );
  return (
    <>
      <nav className="page-actions" aria-label="Event sections">
        {upcoming.length > 0 && (
          <a className="text-link" href="#upcoming-events">
            Upcoming events
          </a>
        )}
        {past.length > 0 && (
          <a className="text-link" href="#past-events">
            Past events
          </a>
        )}
      </nav>
      <section className="content-block" id="upcoming-events">
        <h2>Upcoming events</h2>
        {upcoming.length ? (
          upcoming.map((event) => <EventRow key={event.slug} event={event} />)
        ) : (
          <>
            <p>No upcoming events are listed.</p>
            <a className="text-link" href="#past-events">
              Browse past events
            </a>
          </>
        )}
      </section>
      <section className="content-block" id="past-events">
        <h2>Past events</h2>
        {past.length ? (
          past.map((event) => <EventRow key={event.slug} event={event} />)
        ) : (
          <>
            <p>No past events are listed.</p>
            <a className="text-link" href="#upcoming-events">
              Back to upcoming events
            </a>
          </>
        )}
      </section>
    </>
  );
}

export function Events() {
  return (
    <Page title="Events">
      <PublicData path="events" name="events">
        {(data) => <Schedule {...data} />}
      </PublicData>
    </Page>
  );
}

export function EventDetail() {
  const { slug } = useParams();
  return (
    <PublicData
      path={`events/${encodeURIComponent(slug)}`}
      name="event details"
      fallbackTitle="Event details"
      missing={<Missing item="Event" to="/events" action="Browse events" />}
    >
      {(event) => <EventArticle event={event} />}
    </PublicData>
  );
}

export function EventArticle({ event, preview = false }) {
  return (
    <article className="wrap">
      <div className="event-hero">
        <div>
          {!preview && (
            <Link
              className="breadcrumb text-link"
              to={`/events#${event.registration_status === "ended" ? "past" : "upcoming"}-events`}
            >
              Back to events
            </Link>
          )}
          <h1>{event.title}</h1>
          <p className="status">{states[event.registration_status]}</p>
        </div>
        <div className="ticket">
          {event.event_date ? (
            <EventDate ticket date={event.event_date} />
          ) : (
            <p>Date pending</p>
          )}
          {event.venue && <p>{event.venue}</p>}
        </div>
      </div>
      <section className="brief">
        <h2>Event details</h2>
        <div>
          <p>{event.summary}</p>
          {event.starts_at && (
            <p className="event-time">
              <time dateTime={event.starts_at}>
                {campusTime.format(new Date(event.starts_at))} IST
              </time>
            </p>
          )}
          {event.registration_status === "open" ? (
            <div>
              <ExternalLink className="action" href={event.registration_url}>
                Register on the university portal
              </ExternalLink>
              <p className="registration-destination">
                {new URL(event.registration_url).host}
                {new URL(event.registration_url).pathname}
              </p>
            </div>
          ) : (
            event.official_url && (
              <ExternalLink href={event.official_url}>
                {new URL(event.official_url).hostname === "chitkarau.life"
                  ? "University event page"
                  : "Event source"}
              </ExternalLink>
            )
          )}
        </div>
      </section>
    </article>
  );
}
