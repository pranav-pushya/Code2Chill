import { Link } from "react-router";
import { ExternalLink, Page, profiles, university } from "./SiteLayout.jsx";

export function About() {
  return (
    <Page title="About Code2Chill">
      <p className="lede">
        Code2Chill is a student-led technical club at Chitkara University.
        Students learn by building together through workshops, hackathons and
        coding events.
      </p>
      <section className="content-block">
        <h2>Club domains</h2>
        <ul className="domain-list">
          {["Technical", "Content", "Social Media", "Promotion"].map((name) => (
            <li key={name}>{name}</li>
          ))}
        </ul>
      </section>
      <div className="page-actions">
        <Link className="action" to="/team">
          Meet the team
        </Link>
        <Link className="text-link" to="/contact">
          Contact
        </Link>
      </div>
    </Page>
  );
}

export function Contact() {
  return (
    <Page title="Contact Code2Chill">
      <p className="lede">
        Find the club on Chitkara University’s portal or follow its
        announcements on social media.
      </p>
      <ExternalLink className="action" href={university}>
        View the club on the university portal
      </ExternalLink>
      <section className="content-block">
        <h2>Club profiles</h2>
        <div className="page-actions">
          {Object.entries(profiles).map(([label, href]) => (
            <ExternalLink key={label} href={href}>
              {label}
            </ExternalLink>
          ))}
        </div>
      </section>
    </Page>
  );
}
