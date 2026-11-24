import { useState } from "react";
import { Link } from "react-router";
import { ExternalLink, Page } from "./SiteLayout.jsx";
import { useSiteLinks } from "./SiteLinks.jsx";

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
