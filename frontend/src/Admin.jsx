import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router";

export const eventsPath = "/admin/content/events";

export function adminRequest(path, options = {}) {
  const signal = AbortSignal.timeout(15000);
  return fetch(`/api/admin/${path}`, {
    cache: "no-store",
    ...options,
    headers: { "X-Code2Chill-Admin": "1", ...options.headers },
    signal: options.signal ? AbortSignal.any([signal, options.signal]) : signal,
  });
}

export function SignIn() {
  const navigate = useNavigate();
  const location = useLocation();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();
    const fields = new FormData(event.currentTarget);
    setBusy(true);
    setError("");
    try {
      const response = await adminRequest("sign-in", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: fields.get("email"),
          password: fields.get("password"),
        }),
      });
      if (response.status === 401) {
        setError("Sign-in failed. Check your details or try again later.");
        return;
      }
      if (!response.ok) throw new Error();
      const account = await response.json();
      const from = location.state?.from;
      const eventPath =
        account.role !== "reviewer" &&
        typeof from === "string" &&
        /^\/admin\/(?:content\/(?:events|members|projects)|media)(?:\/(?:new|[1-9]\d*(?:\/preview)?))?$/.test(
          from,
        );
      const reviewPath =
        account.role !== "editor" &&
        typeof from === "string" &&
        /^\/admin\/recruitment(?:\/[1-9]\d*\/applications(?:\/[1-9]\d*)?)?(?:\?[^#]*)?$/.test(
          from,
        );
      const settingsPath =
        account.role === "admin" &&
        ["/admin/settings", "/admin/settings/preview"].includes(from);
      navigate(eventPath || reviewPath || settingsPath ? from : "/admin", {
        replace: true,
      });
    } catch {
      setError("Couldn’t reach the sign-in service. Try again.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="wrap service-page">
      <h1>Admin sign-in</h1>
      <form className="sign-in-form" method="post" onSubmit={submit}>
        <label>
          Email address
          <input
            name="email"
            type="email"
            autoComplete="username"
            maxLength={254}
            required
          />
        </label>
        <label>
          Password
          <input
            name="password"
            type="password"
            autoComplete="current-password"
            maxLength={256}
            required
          />
        </label>
        {error && <p role="alert">{error}</p>}
        <button type="submit" className="action" disabled={busy}>
          {busy ? "Signing in…" : "Sign in"}
        </button>
      </form>
    </section>
  );
}

export function AdminArea({ events = false }) {
  const navigate = useNavigate();
  const [result, setResult] = useState({ loading: true });
  const [attempt, setAttempt] = useState(0);
  const [signingOut, setSigningOut] = useState(false);
  const [logoutError, setLogoutError] = useState("");

  // biome-ignore lint/correctness/useExhaustiveDependencies: attempt triggers a fresh request
  useEffect(() => {
    const controller = new AbortController();
    async function load() {
      try {
        const response = await adminRequest(events ? "events" : "session", {
          signal: controller.signal,
        });
        if (controller.signal.aborted) return;
        if (response.status === 401) {
          navigate("/admin/sign-in", {
            replace: true,
            state: { from: events ? eventsPath : "/admin" },
          });
        } else if (response.status === 403) {
          setResult({ forbidden: true });
        } else {
          if (!response.ok) throw new Error();
          const data = await response.json();
          if (!controller.signal.aborted) setResult({ data });
        }
      } catch {
        if (!controller.signal.aborted) setResult({ error: true });
      }
    }
    void load();
    return () => controller.abort();
  }, [events, navigate, attempt]);

  async function signOut() {
    setSigningOut(true);
    setLogoutError("");
    try {
      const response = await adminRequest("sign-out", { method: "POST" });
      if (!response.ok) throw new Error();
      navigate("/admin/sign-in", { replace: true });
    } catch {
      setLogoutError("Couldn’t sign out. Try again.");
      setSigningOut(false);
    }
  }

  return (
    <section className="wrap service-page">
      {events && (
        <Link className="text-link breadcrumb" to="/admin">
          Back to dashboard
        </Link>
      )}
      <h1>
        {result.forbidden
          ? "Access denied"
          : events
            ? "Events"
            : "Admin dashboard"}
      </h1>
      {result.loading && <p role="status">Loading…</p>}
      {result.error && (
        <>
          <p role="alert">Couldn’t load this page.</p>
          <button
            type="button"
            className="action"
            onClick={() => {
              setResult({ loading: true });
              setAttempt((count) => count + 1);
            }}
          >
            Try again
          </button>
        </>
      )}
      {result.forbidden && (
        <p>Your account does not have permission to manage events.</p>
      )}
      {result.data &&
        (events ? (
          <>
            <Link className="action" to={`${eventsPath}/new`}>
              New draft
            </Link>
            <EventList events={result.data} />
          </>
        ) : (
          <>
            <p>Signed in as {result.data.email}</p>
            <div className="page-actions">
              {result.data.role !== "reviewer" && (
                <>
                  <Link className="action" to="/admin/content/members">
                    Manage members
                  </Link>
                  <Link className="action" to="/admin/content/projects">
                    Manage projects
                  </Link>
                  <Link className="action" to="/admin/media">
                    Manage media
                  </Link>
                </>
              )}
              {result.data.role === "admin" && (
                <Link className="action" to="/admin/settings">
                  Site settings
                </Link>
              )}
              {result.data.role !== "reviewer" && (
                <Link to={eventsPath} className="action">
                  Manage events
                </Link>
              )}
              {result.data.role !== "editor" && (
                <Link to="/admin/recruitment" className="action">
                  Review applications
                </Link>
              )}
            </div>
          </>
        ))}
      {(result.data || result.forbidden) && (
        <div className="sign-out">
          {logoutError && <p role="alert">{logoutError}</p>}
          <button
            type="button"
            className="action"
            disabled={signingOut}
            onClick={signOut}
          >
            {signingOut ? "Signing out…" : "Sign out"}
          </button>
        </div>
      )}
    </section>
  );
}

function EventList({ events }) {
  if (events.length === 0) return <p>No events have been saved yet.</p>;
  return (
    <ul className="admin-events">
      {events.map((event) => (
        <li key={event.id}>
          <strong>
            <Link className="text-link" to={`${eventsPath}/${event.id}`}>
              {event.title}
            </Link>
          </strong>
          {event.event_date && (
            <time dateTime={event.event_date}>{event.event_date}</time>
          )}
          <span>
            {event.publication_state === "published" ? "Published" : "Draft"}
          </span>
        </li>
      ))}
    </ul>
  );
}
