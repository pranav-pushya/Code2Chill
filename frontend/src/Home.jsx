import { Link } from "react-router";
import markSmall from "../../docs/design/brand/club-mark-240.webp";
import mark from "../../docs/design/brand/club-mark-480.webp";
import { EventRow } from "./Events.jsx";
import { ProjectRow } from "./Projects.jsx";
import { PublicData } from "./PublicData.jsx";
import { Roster } from "./Team.jsx";

export default function Home() {
  return (
    <>
      <section className="wrap hero">
        <div className="hero-copy">
          <p className="kicker">Chitkara University</p>
          <h1>
            Learn by <span>building.</span>
          </h1>
          <p>
            Code2Chill is a student-led technical club. We bring students
            together for workshops, hackathons and coding events.
          </p>
          <Link className="action" to="/events">
            Explore events
          </Link>
        </div>
        <div className="brand-art" aria-hidden="true">
          <div className="print">
            <img
              src={mark}
              srcSet={`${markSmall} 240w, ${mark} 480w`}
              sizes="(max-width: 47.99rem) 53vw, 26vw"
              width="480"
              height="419"
              alt=""
              fetchPriority="high"
              decoding="async"
            />
          </div>
        </div>
      </section>
      <section className="wrap ledger">
        <h2>Featured event</h2>
        <PublicData path="events" name="the featured event">
          {({ upcoming, past }) => {
            const featured = upcoming[0] ?? past[0];
            return featured ? (
              <EventRow event={featured} />
            ) : (
              <p>No events are listed.</p>
            );
          }}
        </PublicData>
      </section>
      <section className="work on-ink">
        <div className="wrap">
          <h2>Student work</h2>
          <PublicData path="projects" name="student projects">
            {(projects) =>
              projects.length ? (
                <ProjectRow project={projects[0]} />
              ) : (
                <p>No projects are published yet.</p>
              )
            }
          </PublicData>
          <Link className="text-link section-link" to="/projects">
            Browse projects
          </Link>
        </div>
      </section>
      <section className="wrap people">
        <div>
          <h2>Meet the team</h2>
          <Link className="text-link section-link" to="/team">
            View the team
          </Link>
        </div>
        <PublicData path="team" name="the team">
          {(members) =>
            members.length ? (
              <Roster members={members.slice(0, 2)} />
            ) : (
              <p>Team information is coming soon.</p>
            )
          }
        </PublicData>
      </section>
      <section className="membership">
        <div className="wrap">
          <div>
            <h2>Join the club</h2>
            <p>Find out how to express your interest in membership.</p>
          </div>
          <Link className="action" to="/join">
            Explore joining
          </Link>
        </div>
      </section>
    </>
  );
}
