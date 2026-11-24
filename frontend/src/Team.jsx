import { Link } from "react-router";
import { PublishedImage } from "./Gallery.jsx";
import { PublicData } from "./PublicData.jsx";
import { ExternalLink, Page } from "./SiteLayout.jsx";

const domains = {
  technical: "Technical",
  content: "Content",
  social_media: "Social Media",
  promotion: "Promotion",
};

const VERIFIED_TEAM_DATA = {
  "lakshay-kalra": {
    linkedin: "https://www.linkedin.com/in/lakshay-kalra-5667ba387",
    bio: "President & Community Lead. Driving technical innovation and student collaboration at Chitkara University.",
  },
  "jiya-arora": {
    linkedin: "https://www.linkedin.com/in/jiya-arora-13b214377",
    bio: "Vice-president & Operations. Ensuring smooth execution across club tracks and member initiatives.",
  },
  "samanyu-thakur": {
    linkedin: "https://www.linkedin.com/in/samanyu-thakur-76622b386",
    bio: "Technical Head. Guiding architecture, web development, and hands-on coding bootcamps.",
  },
  "bhupinder-singh": {
    linkedin: "https://www.linkedin.com/in/bhupindersinghmann",
    bio: "Technical Head. Backend engineering, algorithmic problem solving, and technical duels.",
  },
  "tamanna-kakkar": {
    linkedin: "https://www.linkedin.com/in/tamanna-kakkar-995b73385",
    bio: "Content Head. Creative direction, technical writing, and event storytelling.",
  },
  "ayush-sharma": {
    linkedin: "https://www.linkedin.com/in/ayushthisside",
    bio: "Content Head. Technical documentation, curriculum design, and creative ideation.",
  },
  "jashan-bhalla": {
    linkedin: "https://www.linkedin.com/in/jashan-bhalla-7b6539213",
    bio: "Social Media Head. Media production, visual branding, and campus outreach.",
  },
  "muskan-dhanda": {
    linkedin: "https://www.linkedin.com/company/code2chill",
    bio: "Promotion Head. Campus relations, event marketing, and community growth.",
  },
  "divyana-garg": {
    linkedin: "https://www.linkedin.com/company/code2chill",
    bio: "Core Member. Project coordination and technical event management.",
  },
  "hunar-mehndiratta": {
    linkedin: "https://www.linkedin.com/company/code2chill",
    bio: "Core Member. Technical initiatives and community engagement.",
  },
  "pranav-pushya": {
    linkedin: "https://www.linkedin.com/in/pranav-pushya/",
    bio: "Core Member. Technical initiatives and software development.",
  },
};

export function Roster({ members }) {
  return (
    <dl className="roster">
      {members.map((member) => {
        const verified = VERIFIED_TEAM_DATA[member.slug] ?? {};
        const bio = member.bio || verified.bio;
        const linkedin = member.linkedin_url || verified.linkedin;
        return (
          <div key={member.slug} className="roster-item">
            <div className="roster-identity">
              <dt>{member.name}</dt>
              {bio && <p className="roster-bio">{bio}</p>}
            </div>
            <div className="roster-meta">
              <dd className="roster-role">{member.role_title}</dd>
              {linkedin && (
                <dd className="roster-link">
                  <ExternalLink href={linkedin} className="text-link">
                    LinkedIn &rarr;
                  </ExternalLink>
                </dd>
              )}
              {member.portrait?.asset_url && (
                <dd>
                  <PublishedImage image={member.portrait} />
                </dd>
              )}
            </div>
          </div>
        );
      })}
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
      <div className="page-actions team-actions">
        <Link className="action" to="/join">
          Explore joining
        </Link>
      </div>
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
