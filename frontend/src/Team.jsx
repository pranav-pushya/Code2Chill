import { Link } from "react-router";
import { PublicData } from "./PublicData.jsx";
import { Page } from "./SiteLayout.jsx";

const domains = {
  technical: "Technical",
  content: "Content",
  social_media: "Social Media",
  promotion: "Promotion",
};

export function Roster({ members }) {
  return (
    <dl className="roster">
      {members.map((member) => (
        <div key={member.slug}>
          <dt>{member.name}</dt>
          <dd>{member.role_title}</dd>
        </div>
      ))}
    </dl>
  );
}

function TeamGroups({ members }) {
  if (!members.length)
    return (
      <>
        <p>Team information is coming soon.</p>
        <Link className="text-link" to="/events">
          Explore events
        </Link>
      </>
    );
  const groups = new Map();
  for (const member of members) {
    const group =
      domains[member.domain] ??
      (["president", "vice-president"].includes(member.role_title.toLowerCase())
        ? "Leadership"
        : "Core members");
    if (!groups.has(group)) groups.set(group, []);
    groups.get(group).push(member);
  }
  return (
    <>
      <div className="team-groups">
        {["Leadership", ...Object.values(domains), "Core members"]
          .filter((group) => groups.has(group))
          .map((group) => (
            <section key={group}>
              <h2>{group}</h2>
              <Roster members={groups.get(group)} />
            </section>
          ))}
      </div>
      <Link className="action" to="/join">
        Explore joining
      </Link>
    </>
  );
}

export function Team() {
  return (
    <Page title="Team">
      <PublicData path="team" name="the team">
        {(members) => <TeamGroups members={members} />}
      </PublicData>
    </Page>
  );
}
