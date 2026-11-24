import { useEffect, useState } from "react";
import { Link, useLocation, useParams } from "react-router";
import { EventGallery, PublishedImage } from "./Gallery.jsx";
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

const CATEGORIES = [
  { id: "all", label: "All events" },
  { id: "competition", label: "Coding Competitions" },
  { id: "hackathon", label: "Hackathons & Sprints" },
  { id: "challenge", label: "Frontend Challenges" },
  { id: "workshop", label: "Workshops" },
];

function classifyEvent(event) {
  const text = `${event.title} ${event.summary ?? ""}`.toLowerCase();
  if (
    text.includes("leetcode") ||
    text.includes("competition") ||
    text.includes("competitive") ||
    text.includes("on fire")
  ) {
    return "competition";
  }
  if (
    text.includes("hackathon") ||
    text.includes("sprint") ||
    text.includes("byte the vibe")
  ) {
    return "hackathon";
  }
  if (
    text.includes("challenge") ||
    text.includes("domination") ||
    text.includes("frontend")
  ) {
    return "challenge";
  }
  if (
    text.includes("workshop") ||
    text.includes("bootcamp") ||
    text.includes("duel")
  ) {
    return "workshop";
  }
  return "general";
}

const EVENT_EXTRAS = {
  "on-fire": {
    prize: "🏆 ₹12,300+ Cash Pool",
    barcode: "C2C-E03-2026",
  },
  "domination-the-frontend-challenge": {
    prize: "⚡ OSL Honors & Awards",
    barcode: "C2C-E02-2026",
  },
  "byte-the-vibe": {
    prize: "🏆 ₹5,000 Prizes",
    barcode: "C2C-E01-2026",
  },
};

function getEventExtras(slug) {
  return (
    EVENT_EXTRAS[slug] || {
      prize: "⚡ OSL Technical Event",
      barcode: "C2C-EVENT",
    }
  );
}

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
  const extras = getEventExtras(event.slug);
  const eventDateObj = new Date(`${event.event_date}T00:00:00Z`);
  const day = event.event_date ? event.event_date.slice(-2) : "--";
  const monthStr = event.event_date
    ? monthYear.format(eventDateObj).toUpperCase()
    : "PENDING";
  const timeStr = event.starts_at
    ? `${campusTime.format(new Date(event.starts_at))} IST`
    : null;

  return (
    <Link
      className="ticket-pass"
      to={`/events/${event.slug}`}
      aria-label={`View event pass: ${event.title}`}
    >
      <div className="ticket-stub-left">
        <div className="ticket-day">{day}</div>
        <div className="ticket-month">{monthStr}</div>
        {timeStr && <div className="ticket-time">{timeStr}</div>}
      </div>

      <div className="ticket-body">
        <div className="ticket-badges">
          <span className="badge-pill badge-prize">{extras.prize}</span>
          <span
            className={`badge-pill badge-status badge-status-${event.registration_status}`}
          >
            <span className="status-dot" aria-hidden="true" />
            {states[event.registration_status]}
          </span>
        </div>
        <h3 className="ticket-title">{event.title}</h3>
        {event.venue && (
          <p className="ticket-venue">
            <span aria-hidden="true">📍</span> {event.venue}
          </p>
        )}
      </div>

      <div className="ticket-stub-right">
        <div className="barcode" aria-hidden="true">
          {extras.barcode}
        </div>
        <span className="ticket-action">
          {event.registration_status === "ended"
            ? "View Recap →"
            : "View Pass →"}
        </span>
      </div>
    </Link>
  );
}

function UpcomingSprintAlert() {
  return (
    <div className="sprint-alert">
      <div className="sprint-alert-content">
        <span className="alert-tag">⚡ Next Season in Preparation</span>
        <h3 className="alert-title">Don't miss the next hackathon</h3>
        <p className="alert-desc">
          We are curating high-impact problem statements, mentorship tracks, and
          campus venues for our upcoming sprint under the Office of Student
          Life.
        </p>
      </div>
      <div className="alert-actions">
        <Link to="/contact" className="btn-alert-primary">
          Inquire at Desk ↗
        </Link>
        <ExternalLink
          href="https://www.instagram.com/code2chill.osl"
          className="btn-alert-secondary"
        >
          Instagram Alerts ↗
        </ExternalLink>
      </div>
    </div>
  );
}

function Schedule({ upcoming, past }) {
  const { hash } = useLocation();
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    if (hash) document.getElementById(hash.slice(1))?.scrollIntoView();
  }, [hash]);

  if (!upcoming.length && !past.length)
    return (
      <>
        <p>No events are listed.</p>
        <Link className="text-link" to="/about">
          Learn about the club
        </Link>
      </>
    );

  const allEvents = [...upcoming, ...past];
  const filteredUpcoming = upcoming.filter(
    (ev) => filter === "all" || classifyEvent(ev) === filter,
  );
  const filteredPast = past.filter(
    (ev) => filter === "all" || classifyEvent(ev) === filter,
  );

  const getCategoryCount = (catId) => {
    if (catId === "all") return allEvents.length;
    return allEvents.filter((ev) => classifyEvent(ev) === catId).length;
  };

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
        {past.length > 0 && (
          <a className="text-link" href="#event-gallery">
            Event gallery
          </a>
        )}
      </nav>

      <div
        className="filter-bar"
        role="tablist"
        aria-label="Event category filters"
      >
        {CATEGORIES.map((cat) => {
          const count = getCategoryCount(cat.id);
          return (
            <button
              key={cat.id}
              type="button"
              role="tab"
              aria-selected={filter === cat.id}
              className={`filter-pill ${filter === cat.id ? "active" : ""}`}
              onClick={() => setFilter(cat.id)}
            >
              {cat.label} <span className="filter-count">({count})</span>
            </button>
          );
        })}
      </div>

      <section className="content-block" id="upcoming-events">
        <h2>Upcoming events</h2>
        {filteredUpcoming.length ? (
          filteredUpcoming.map((event) => (
            <EventRow key={event.slug} event={event} />
          ))
        ) : filter === "all" ? (
          <UpcomingSprintAlert />
        ) : (
          <p className="empty-category-msg">
            No upcoming events in this category. Check back soon or inquire at
            our desk.
          </p>
        )}
      </section>

      <section className="content-block" id="past-events">
        <h2>Past events</h2>
        {filteredPast.length ? (
          filteredPast.map((event) => (
            <EventRow key={event.slug} event={event} />
          ))
        ) : (
          <p className="empty-category-msg">
            {filter === "all"
              ? "No past events are listed."
              : "No past events in this category."}
          </p>
        )}
      </section>
      {past.length > 0 && <EventGallery events={past} />}
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
      {event.poster && (
        <section className="brief event-poster-section">
          <h2>Event poster</h2>
          <div className="event-poster-card">
            <PublishedImage image={event.poster} />
          </div>
        </section>
      )}
    </article>
  );
}
