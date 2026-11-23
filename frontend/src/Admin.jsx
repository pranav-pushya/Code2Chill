import { useEffect, useId, useState } from "react";
import { Link, useLocation, useNavigate } from "react-router";

export const eventsPath = "/admin/content/events";

function EyeIcon() {
  return (
    <svg
      aria-hidden="true"
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7-10-7-10-7Z" />
      <circle cx="12" cy="12" r="3" />
    </svg>
  );
}

function EyeOffIcon() {
  return (
    <svg
      aria-hidden="true"
      width="20"
      height="20"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="m2 2 20 20" />
      <path d="M9.88 9.88a3 3 0 1 0 4.24 4.24" />
      <path d="M10.73 5.08A10.43 10.43 0 0 1 12 5c7 0 10 7 10 7a13.16 13.16 0 0 1-1.67 2.68" />
      <path d="M6.61 6.61A13.526 13.526 0 0 0 2 12s3 7 10 7a9.74 9.74 0 0 0 5.39-1.61" />
    </svg>
  );
}

export function PasswordField({
  label,
  name,
  autoComplete,
  minLength,
  maxLength = 256,
  required = true,
}) {
  const [visible, setVisible] = useState(false);
  const id = useId();
  const toggleLabel = `${visible ? "Hide" : "Show"} ${label.toLowerCase()}`;

  return (
    <label htmlFor={id}>
      {label}
      <div className="password-control">
        <input
          id={id}
          name={name}
          type={visible ? "text" : "password"}
          autoComplete={autoComplete}
          minLength={minLength}
          maxLength={maxLength}
          required={required}
        />
        <button
          type="button"
          className="password-toggle"
          aria-label={toggleLabel}
          aria-pressed={visible}
          title={toggleLabel}
          onClick={() => setVisible((prev) => !prev)}
        >
          {visible ? <EyeOffIcon /> : <EyeIcon />}
        </button>
      </div>
    </label>
  );
}

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
        <PasswordField
          label="Password"
          name="password"
          autoComplete="current-password"
          maxLength={256}
          required
        />
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
            <ChangePassword />
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

export function ChangePassword() {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function submit(event) {
    event.preventDefault();
    const fields = new FormData(event.currentTarget);
    const currentPassword = fields.get("current_password");
    const newPassword = fields.get("new_password");
    const confirmPassword = fields.get("confirm_password");

    setError("");
    setSuccess("");

    if (newPassword !== confirmPassword) {
      setError("New passwords do not match.");
      return;
    }
    if (
      typeof newPassword !== "string" ||
      newPassword.length < 15 ||
      newPassword.length > 256
    ) {
      setError("Use a new password between 15 and 256 characters.");
      return;
    }
    if (newPassword === currentPassword) {
      setError("New password must be different from current password.");
      return;
    }

    setBusy(true);
    try {
      const response = await adminRequest("change-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      });
      if (response.status === 401) {
        setError("Sign in again to change your password.");
        return;
      }
      const data = await response.json();
      if (!response.ok) {
        setError(data.detail || "Couldn’t change password.");
        return;
      }
      setSuccess("Password changed successfully.");
      event.target.reset();
    } catch {
      setError("Couldn’t reach the server. Try again.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <section className="change-password-section">
      <h2>Change password</h2>
      <form className="sign-in-form" method="post" onSubmit={submit}>
        <PasswordField
          label="Current password"
          name="current_password"
          autoComplete="current-password"
          maxLength={256}
          required
        />
        <PasswordField
          label="New password (15 to 256 characters)"
          name="new_password"
          autoComplete="new-password"
          minLength={15}
          maxLength={256}
          required
        />
        <PasswordField
          label="Confirm new password"
          name="confirm_password"
          autoComplete="new-password"
          minLength={15}
          maxLength={256}
          required
        />
        {error && <p role="alert">{error}</p>}
        {success && <p role="status">{success}</p>}
        <button type="submit" className="action" disabled={busy}>
          {busy ? "Updating…" : "Update password"}
        </button>
      </form>
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
