import { useState } from "react";
import { Link } from "react-router";
import { ExternalLink, Page } from "./SiteLayout.jsx";
import { useSiteLinks } from "./SiteLinks.jsx";

const IMPACT_METRICS = [
  {
    value: "3+",
    label: "Flagship Sprints",
    desc: "Byte The Vibe, DOMination & (O)n Fire",
  },
  {
    value: "₹17,300+",
    label: "Cash Prizes Distributed",
    desc: "Awarded directly to winning student teams",
  },
  {
    value: "11",
    label: "Core Mentors & Leads",
    desc: "Cross-domain leadership and guidance",
  },
  {
    value: "100+",
    label: "Student Hackers",
    desc: "Active campus participation",
  },
];

const DOMAINS = [
  {
    icon: "⚡",
    title: "Technical",
    desc: "Full-stack web architecture, algorithm practice, open-source tooling, and maintaining club digital platforms.",
    tags: ["React 19", "FastAPI", "LeetCode", "PostgreSQL"],
  },
  {
    icon: "✍️",
    title: "Content",
    desc: "Curating event problem statements, authoring developer guides, technical documentation, and recap editorials.",
    tags: ["Tech Writing", "Challenge Specs", "Recaps"],
  },
  {
    icon: "📣",
    title: "Social Media",
    desc: "Digital storytelling, campus reels, LinkedIn developer spotlights, and engaging the student community.",
    tags: ["LinkedIn", "Instagram", "Brand Voice"],
  },
  {
    icon: "🎯",
    title: "Promotion",
    desc: "On-ground event logistics at Pierre & Einstein Hall, cross-club collaborations, sponsor liaison, and registrations.",
    tags: ["Venue Ops", "Sponsorship", "OSL Desk"],
  },
];

const MILESTONES = [
  {
    date: "May 18, 2026 · Pierre Hall",
    title: "Byte The Vibe — Team Coding Sprint",
    desc: "Inaugural team sprint pairing fast-paced coding with mentor guidance, judged final pitches, and ₹5,000 in cash awards powered by F Lounge & The Fifth Note Perfumes.",
  },
  {
    date: "July 18, 2026 · Le Corbusier Block",
    title: "DOMination — The Frontend Challenge",
    desc: "Flagship frontend architecture contest where teams built responsive interfaces evaluated on DOM speed, accessibility, performance, and clean design systems.",
  },
  {
    date: "September 23, 2026 · Einstein Hall",
    title: "(O)n Fire — The LeetCode Competition",
    desc: "Competitive algorithmic sprint solving high-difficulty LeetCode problems under intense countdown timers, featuring ₹12,300+ in cash prizes and trophies.",
  },
  {
    date: "Next Up · Campus & Open Source",
    title: "Community Mentorship & Winter Builds",
    desc: "Expanding peer-to-peer coding sessions, contributor open-source repositories, and cross-discipline student hackathons.",
    isUpcoming: true,
  },
];

const FAQS = [
  {
    question: "Do I need prior competitive coding or web development experience to participate?",
    answer: "No. Our workshops and sprints feature tiered challenge tracks and active peer mentors to guide students who are new to building software.",
  },
  {
    question: "Can non-technical students join the Content, Social Media, or Promotion teams?",
    answer: "Yes! Our Content, Media, and Operations domains welcome creative writers, graphic designers, video editors, and event organizers.",
  },
  {
    question: "How do I get involved if recruitment is currently between cycles?",
    answer: "You can attend all our open hackathons and workshops, submit project entries, or register interest through our Contact Desk or University Clubs portal.",
  },
];

export function About() {
  return (
    <Page title="About Code2Chill">
      <p className="lede">
        Where serious code meets chill vibes. Official student-led technical community under the{" "}
        <strong>Office of Student Life at Chitkara University</strong>, dedicated to learning by building real software together through workshops, hackathons, and peer coding sprints.
      </p>

      {/* 1. Verified Impact Metrics Bar */}
      <section className="about-section" aria-labelledby="about-metrics-heading">
        <h2 id="about-metrics-heading" className="sr-only">Key Impact Numbers</h2>
        <div className="about-metrics-grid">
          {IMPACT_METRICS.map((metric) => (
            <div key={metric.label} className="about-metric-item">
              <div className="about-metric-value">{metric.value}</div>
              <div className="about-metric-label">{metric.label}</div>
              <div className="about-metric-desc">{metric.desc}</div>
            </div>
          ))}
        </div>
      </section>

      {/* 2. Domain Deep-Dive Cards */}
      <section className="about-section" aria-labelledby="about-domains-heading">
        <h2 id="about-domains-heading" className="about-section-heading">Club Domains</h2>
        <p className="about-section-sub">
          Our four specialized tracks allow students to sharpen engineering, editorial, media, and organizational leadership skills.
        </p>
        <div className="about-domains-grid">
          {DOMAINS.map((domain) => (
            <div key={domain.title} className="about-domain-card">
              <span className="about-domain-icon" aria-hidden="true">{domain.icon}</span>
              <h3>{domain.title}</h3>
              <p>{domain.desc}</p>
              <div className="about-domain-tags">
                {domain.tags.map((tag) => (
                  <span key={tag} className="about-domain-tag">{tag}</span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* 3. Milestones & Growth Timeline */}
      <section className="about-section" aria-labelledby="about-milestones-heading">
        <h2 id="about-milestones-heading" className="about-section-heading">Our Journey & Milestones</h2>
        <p className="about-section-sub">
          From our inaugural sprint to competitive algorithm contests across campus halls.
        </p>
        <div className="about-timeline">
          {MILESTONES.map((item) => (
            <div key={item.title} className={`about-timeline-item ${item.isUpcoming ? "upcoming" : ""}`}>
              <div className="about-timeline-dot" aria-hidden="true" />
              <div className="about-timeline-date">{item.date}</div>
              <h3 className="about-timeline-title">{item.title}</h3>
              <p className="about-timeline-desc">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* 5. Office of Student Life (OSL) Charter */}
      <section className="about-section" aria-labelledby="about-osl-heading">
        <div className="about-osl-banner">
          <div className="about-osl-mark" aria-hidden="true">OSL</div>
          <div className="about-osl-content">
            <h3 id="about-osl-heading">Chartered under Chitkara University Office of Student Life</h3>
            <p>
              Code2Chill operates with official university recognition, providing verified extracurricular technical activities, certified event participation, and reserved state-of-the-art campus halls (Pierre Hall, Einstein Hall).
            </p>
          </div>
        </div>
      </section>

      {/* 6. Student & Member FAQ */}
      <section className="about-section" aria-labelledby="about-faq-heading">
        <h2 id="about-faq-heading" className="about-section-heading">Frequently Asked Questions</h2>
        <div className="about-faq-list">
          {FAQS.map((faq) => (
            <details key={faq.question} className="about-faq-item">
              <summary className="about-faq-summary">
                <span>{faq.question}</span>
                <span className="about-faq-chevron" aria-hidden="true">+</span>
              </summary>
              <p className="about-faq-answer">{faq.answer}</p>
            </details>
          ))}
        </div>
      </section>

      <div className="page-actions" style={{ marginTop: "var(--space-8)" }}>
        <Link className="action" to="/team">
          Meet the team
        </Link>
        <Link className="action" to="/events">
          Explore events
        </Link>
        <Link className="text-link" to="/contact">
          Contact desk
        </Link>
      </div>
    </Page>
  );
}

function ContactInquiryForm() {
  const [form, setForm] = useState({
    fullName: "",
    email: "",
    category: "general",
    message: "",
  });
  const [status, setStatus] = useState("idle"); // idle | submitting | success | error
  const [errorMessage, setErrorMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.fullName.trim() || !form.email.trim() || !form.message.trim()) {
      setErrorMessage("Please complete all required fields.");
      setStatus("error");
      return;
    }
    setStatus("submitting");
    setErrorMessage("");

    try {
      const response = await fetch("/api/inquiries", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          full_name: form.fullName.trim(),
          email: form.email.trim(),
          category: form.category,
          message: form.message.trim(),
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(
          errorData.detail ||
            "Unable to send inquiry. Please check your details.",
        );
      }

      setStatus("success");
      setForm({ fullName: "", email: "", category: "general", message: "" });
    } catch (err) {
      setStatus("error");
      setErrorMessage(err.message || "Failed to submit. Please try again.");
    }
  };

  if (status === "success") {
    return (
      <div className="inquiry-success-card" role="status">
        <div className="success-badge" aria-hidden="true">
          ✓
        </div>
        <h3>Inquiry received</h3>
        <p>
          Thank you! Your note has been delivered to the Code2Chill coordinator
          desk. A team lead will follow up via your university email within
          24–48 hours.
        </p>
        <button
          type="button"
          className="text-link"
          onClick={() => setStatus("idle")}
        >
          Send another message &rarr;
        </button>
      </div>
    );
  }

  return (
    <form className="inquiry-form" onSubmit={handleSubmit} noValidate>
      <div className="inquiry-field-grid">
        <label className="inquiry-field">
          <span>
            Full name{" "}
            <span className="required-mark" aria-hidden="true">
              *
            </span>
          </span>
          <input
            type="text"
            required
            value={form.fullName}
            onChange={(e) => setForm({ ...form, fullName: e.target.value })}
            placeholder="e.g. Jasleen Kaur"
            disabled={status === "submitting"}
          />
        </label>
        <label className="inquiry-field">
          <span>
            University email{" "}
            <span className="required-mark" aria-hidden="true">
              *
            </span>
          </span>
          <input
            type="email"
            required
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            placeholder="rollno@chitkara.edu.in"
            disabled={status === "submitting"}
          />
        </label>
      </div>

      <label className="inquiry-field">
        <span>Inquiry topic</span>
        <select
          value={form.category}
          onChange={(e) => setForm({ ...form, category: e.target.value })}
          disabled={status === "submitting"}
        >
          <option value="events">
            Event details & hackathon participation
          </option>
          <option value="recruitment">
            Recruitment cycles & joining the team
          </option>
          <option value="projects">
            Project collaboration & open-source showcase
          </option>
          <option value="general">General inquiries & feedback</option>
        </select>
      </label>

      <label className="inquiry-field">
        <span>
          Message{" "}
          <span className="required-mark" aria-hidden="true">
            *
          </span>
        </span>
        <textarea
          rows={4}
          required
          value={form.message}
          onChange={(e) => setForm({ ...form, message: e.target.value })}
          placeholder="Ask about team registration rules, hackathon guidelines, or club activities..."
          disabled={status === "submitting"}
        />
      </label>

      {status === "error" && (
        <p className="inquiry-error-msg" role="alert">
          {errorMessage}
        </p>
      )}

      <div className="inquiry-actions">
        <button
          type="submit"
          className="action"
          disabled={status === "submitting"}
        >
          {status === "submitting" ? "Sending..." : "Send inquiry"}
        </button>
        <span className="inquiry-hint">
          Delivered directly to club coordinators &bull; Response in 24–48h
        </span>
      </div>
    </form>
  );
}

export function Contact({ preview }) {
  const links = useSiteLinks();
  const { university, instagram, linkedin } = preview ?? links;
  const profiles = { Instagram: instagram, LinkedIn: linkedin };
  return (
    <Page title="Contact Code2Chill">
      <p className="lede">
        Have questions about upcoming hackathons, recruitment cycles, or
        technical collaborations? Send a direct inquiry or connect with us on
        campus channels.
      </p>

      <section className="content-block">
        <h2>Send a message</h2>
        <ContactInquiryForm />
      </section>

      <section className="content-block">
        <h2>Official channels</h2>
        <p>
          Find the club on Chitkara University’s portal or follow announcements
          on social media.
        </p>
        <div className="page-actions">
          <ExternalLink className="action" href={university}>
            University portal
          </ExternalLink>
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
