/**
 * Verified offline fallback data for Code2Chill public portal.
 * Ensures zero-downtime rendering even if the backend is waking from cold start,
 * undergoing redeployment, or temporarily unreachable.
 */

export const PROJECTS_FALLBACK = [
  {
    slug: "nexus",
    title: "NEXUS",
    summary:
      "A survival game that adjusts difficulty using gameplay, facial and audio signals.",
    credits: ["Ayush Sharma", "Arnav Sharma", "Anveer Singh Sandhu"],
    repository_url: "https://github.com/thisIsAyushFr/Nexus-Emotion-Detection",
    demo_url: "https://c2c-event.vercel.app/",
    screenshot: null,
  },
  {
    slug: "chronoatlas",
    title: "ChronoAtlas – Travel Through Time",
    summary: "A frontend project built at DOMination.",
    credits: ["Vibhanshu Jain", "Dheraj Sharma"],
    repository_url: null,
    demo_url: null,
    screenshot: null,
  },
  {
    slug: "domination-starter",
    title: "DOMination Starter Kit",
    summary:
      "Official base template supplied to hackathon teams at DOMination with semantic landmarks, reset styles, and accessibility criteria.",
    credits: ["Code2Chill Team"],
    repository_url: "https://github.com/Cypher45/c2c-event",
    demo_url: "https://c2c-event.vercel.app/",
    screenshot: null,
  },
];

export const EVENTS_FALLBACK = {
  upcoming: [],
  past: [
    {
      slug: "on-fire",
      title: "(O)n Fire – The LeetCode Competition",
      summary:
        "A competitive programming contest focused on solving algorithmic LeetCode challenges under time pressure, featuring Rs 12,300+ in cash prizes, trophies and participation certificates.",
      event_date: "2026-09-23",
      venue: "Einstein Hall",
      starts_at: "2026-09-23T04:30:00Z",
      ends_at: "2026-09-23T10:30:00Z",
      registration_status: "ended",
      registration_url: null,
      official_url: "https://chitkarau.life/events/on-fire",
      poster: {
        asset_url: "/media/on-fire-poster.jpg",
        alt_text: "(O)n Fire: The LeetCode Competition official event poster",
        credit: "Code2Chill & OSL",
      },
    },
    {
      slug: "domination-the-frontend-challenge",
      title: "DOMination – The Frontend Challenge",
      summary:
        "Teams built web interfaces evaluated on design, responsiveness, accessibility, performance and relevance.",
      event_date: "2026-07-18",
      venue: "Pierre Hall, Architecture Block",
      starts_at: "2026-07-18T05:30:00Z",
      ends_at: null,
      registration_status: "ended",
      registration_url: null,
      official_url:
        "https://chitkarau.life/events/domination-the-frontend-challenge",
      poster: {
        asset_url: "/media/domination.jpg",
        alt_text: "DOMination – The Frontend Challenge official event banner",
        credit: "Code2Chill & OSL",
      },
    },
    {
      slug: "byte-the-vibe",
      title: "Byte The Vibe",
      summary:
        "A team coding sprint with mentor guidance and judged final pitches.",
      event_date: "2026-05-18",
      venue: "Pierre Hall, Architecture Block",
      starts_at: "2026-05-18T07:30:00Z",
      ends_at: "2026-05-18T10:30:00Z",
      registration_status: "ended",
      registration_url: null,
      official_url: "https://chitkarau.life/events/byte-the-vibe",
      poster: {
        asset_url: "/media/byte-the-vibe.jpg",
        alt_text: "Byte The Vibe official event banner",
        credit: "Code2Chill & OSL",
      },
    },
  ],
};

export const TEAM_FALLBACK = [
  {
    slug: "lakshay-kalra",
    name: "Lakshay Kalra",
    role_title: "President",
    domain: null,
    bio: null,
    portrait: null,
  },
  {
    slug: "jiya-arora",
    name: "Jiya Arora",
    role_title: "Vice-president",
    domain: null,
    bio: null,
    portrait: null,
  },
  {
    slug: "divyana-garg",
    name: "Divyana Garg",
    role_title: "Core Member",
    domain: null,
    bio: null,
    portrait: null,
  },
  {
    slug: "hunar-mehndiratta",
    name: "Hunar Mehndiratta",
    role_title: "Core Member",
    domain: null,
    bio: null,
    portrait: null,
  },
  {
    slug: "pranav-pushya",
    name: "Pranav Pushya",
    role_title: "Core Member",
    domain: null,
    bio: null,
    portrait: null,
  },
  {
    slug: "samanyu-thakur",
    name: "Samanyu Thakur",
    role_title: "Technical Head",
    domain: "technical",
    bio: null,
    portrait: null,
  },
  {
    slug: "bhupinder-singh",
    name: "Bhupinder Singh",
    role_title: "Technical Head",
    domain: "technical",
    bio: null,
    portrait: null,
  },
  {
    slug: "tamanna-kakkar",
    name: "Tamanna Kakkar",
    role_title: "Content Head",
    domain: "content",
    bio: null,
    portrait: null,
  },
  {
    slug: "ayush-sharma",
    name: "Ayush Sharma",
    role_title: "Content Head",
    domain: "content",
    bio: null,
    portrait: null,
  },
  {
    slug: "jashan-bhalla",
    name: "Jashan Bhalla",
    role_title: "Social Media Head",
    domain: "social_media",
    bio: null,
    portrait: null,
  },
  {
    slug: "muskan-dhanda",
    name: "Muskan Dhanda",
    role_title: "Promotion Head",
    domain: "promotion",
    bio: null,
    portrait: null,
  },
];

export const RECRUITMENT_FALLBACK = {
  is_open: false,
  cycle: null,
  domains: ["technical", "content", "social_media", "promotion"],
};

export const STATIC_FALLBACKS = {
  projects: PROJECTS_FALLBACK,
  events: EVENTS_FALLBACK,
  team: TEAM_FALLBACK,
  recruitment: RECRUITMENT_FALLBACK,
};

export function getFallbackData(path) {
  if (STATIC_FALLBACKS[path]) {
    return STATIC_FALLBACKS[path];
  }
  if (path.startsWith("projects/")) {
    const slug = path.replace("projects/", "");
    return PROJECTS_FALLBACK.find((p) => p.slug === slug) || null;
  }
  if (path.startsWith("events/")) {
    const slug = path.replace("events/", "");
    return (
      EVENTS_FALLBACK.past.find((e) => e.slug === slug) ||
      EVENTS_FALLBACK.upcoming.find((e) => e.slug === slug) ||
      null
    );
  }
  return null;
}
