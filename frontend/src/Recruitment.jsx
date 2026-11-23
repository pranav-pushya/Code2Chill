import { useRef, useState } from "react";
import { Link, Navigate, useSearchParams } from "react-router";
import { PublicData } from "./PublicData.jsx";
import { ExternalLink, Page } from "./SiteLayout.jsx";
import { useSiteLinks } from "./SiteLinks.jsx";

const labels = {
  technical: "Technical",
  content: "Content",
  social_media: "Social Media",
  promotion: "Promotion",
};
const campusDate = new Intl.DateTimeFormat("en-IN", {
  dateStyle: "medium",
  timeStyle: "short",
  timeZone: "Asia/Kolkata",
});

function CycleDetails({ cycle }) {
  return (
    <section className="content-block">
      <h2>{cycle.title}</h2>
      <p>{cycle.eligibility}</p>
      <p>
        Opens {campusDate.format(new Date(cycle.opens_at))} IST · Closes{" "}
        {campusDate.format(new Date(cycle.closes_at))} IST
      </p>
      <ul className="domain-list">
        {cycle.domains.map((d) => (
          <li key={d}>{labels[d]}</li>
        ))}
      </ul>
    </section>
  );
}

export function Join({ apply = false }) {
  const { university } = useSiteLinks();
  const [params] = useSearchParams();
  return (
    <PublicData
      path="recruitment"
      name="recruitment details"
      fallbackTitle="Join Code2Chill"
    >
      {(cycle) => {
        const local = cycle.state === "open" && cycle.route === "local";
        if (apply) {
          if (
            !local ||
            (params.has("cycle") && params.get("cycle") !== String(cycle.id))
          )
            return <Navigate to="/join" replace />;
          return <ApplicationForm key={cycle.id} cycle={cycle} />;
        }
        return (
          <Page title="Join Code2Chill">
            {cycle.state === "announcement" ? (
              <section className="content-block">
                <h2>Recruitment dates to be announced</h2>
                <p>
                  Interested in becoming a member? Visit the university club
                  page to express your interest.
                </p>
              </section>
            ) : (
              <CycleDetails cycle={cycle} />
            )}
            {cycle.state === "closed" && <p>Applications are closed.</p>}
            {cycle.state === "scheduled" && (
              <p>Applications open on the scheduled date.</p>
            )}
            {local ? (
              <Link className="action" to={`/join/apply?cycle=${cycle.id}`}>
                Start application
              </Link>
            ) : cycle.route === "external" ? (
              <ExternalLink className="action" href={cycle.external_url}>
                Apply through the official form
              </ExternalLink>
            ) : (
              <>
                {cycle.state === "open" && (
                  <p>Applications are temporarily unavailable.</p>
                )}
                <ExternalLink className="action" href={university}>
                  View the club on the university portal
                </ExternalLink>
              </>
            )}
          </Page>
        );
      }}
    </PublicData>
  );
}

async function post(cycle, path, body) {
  const response = await fetch(`/api/recruitment/${cycle.id}/${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(20000),
    cache: "no-store",
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(
      typeof error.detail === "string" ? error.detail : "Please try again.",
    );
  }
  return response.status === 204 ? null : response.json();
}

function ApplicationForm({ cycle }) {
  const attempt = useRef(null);
  const [sent, setSent] = useState(false);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [receipt, setReceipt] = useState("");
  async function submit(event) {
    event.preventDefault();
    if (busy) return;
    const form = event.currentTarget;
    const data = Object.fromEntries(new FormData(form));
    const email = data.university_email.trim().toLowerCase();
    if (attempt.current?.university_email !== email) {
      attempt.current = {
        attempt_id: crypto.randomUUID(),
        university_email: email,
      };
    }
    const sendCode = !sent || event.nativeEvent.submitter?.value === "resend";
    const identity = attempt.current;
    setBusy(true);
    setError("");
    setNotice("");
    try {
      if (sendCode) {
        await post(cycle, "email-code", identity);
        setSent(true);
        setNotice(
          "Check your university inbox. Your code is valid for 15 minutes.",
        );
        if (form.elements.code) form.elements.code.value = "";
      } else {
        const result = await post(cycle, "applications", {
          ...data,
          ...identity,
        });
        setReceipt(result.receipt);
      }
    } catch (err) {
      const network = err instanceof TypeError || err.name === "TimeoutError";
      setError(
        network
          ? "Couldn’t confirm the result. Keep this page open and try again with the same details."
          : err.message,
      );
    } finally {
      setBusy(false);
    }
  }
  if (receipt)
    return (
      <Page title="Application received">
        <p role="status">
          Save your confirmation reference: <strong>{receipt}</strong>
        </p>
        <Link className="action" to="/join">
          Back to Join
        </Link>
      </Page>
    );
  return (
    <Page title="Recruitment application">
      <CycleDetails cycle={cycle} />
      <p>Name, university email and domain are required.</p>
      <form className="sign-in-form draft-form" onSubmit={submit}>
        <fieldset disabled={busy}>
          <label>
            Full name
            <input
              name="full_name"
              autoComplete="name"
              required
              maxLength={160}
              pattern={".*\\S.*"}
            />
          </label>
          <label>
            University email
            <input
              name="university_email"
              type="email"
              autoComplete="email"
              required
              readOnly={sent}
              maxLength={254}
              aria-describedby="email-help"
            />
          </label>
          <small id="email-help">
            Use your @{cycle.email_domain} address. We’ll email you a
            verification code.
          </small>
          <label>
            Domain
            <select name="domain" required defaultValue="">
              <option value="" disabled>
                Select a domain
              </option>
              {cycle.domains.map((d) => (
                <option key={d} value={d}>
                  {labels[d]}
                </option>
              ))}
            </select>
          </label>
          {cycle.optional_field === "motivation" && (
            <label>
              Why would you like to join? (optional)
              <textarea name="motivation" maxLength={2000} rows={4} />
            </label>
          )}
          {cycle.optional_field === "portfolio_url" && (
            <label>
              Portfolio link (optional, HTTPS)
              <input
                name="portfolio_url"
                type="url"
                pattern="https://.+"
                maxLength={2048}
              />
            </label>
          )}
          {sent && (
            <label>
              Email verification code
              <input
                name="code"
                required
                autoComplete="one-time-code"
                maxLength={64}
              />
            </label>
          )}
          <div className="page-actions">
            <button type="submit" className="action">
              {sent ? "Submit application" : "Send email code"}
            </button>
            {sent && (
              <>
                <button
                  type="submit"
                  className="text-link"
                  value="resend"
                  formNoValidate
                >
                  Send a new code
                </button>
                <button
                  type="button"
                  className="text-link"
                  onClick={() => {
                    setSent(false);
                    setError("");
                    setNotice("");
                  }}
                >
                  Change email
                </button>
              </>
            )}
          </div>
        </fieldset>
        <span role="status">{busy ? "Please wait…" : notice}</span>
        {error && <p role="alert">{error}</p>}
      </form>
      <Link className="text-link" to="/join">
        Back to Join
      </Link>
    </Page>
  );
}
