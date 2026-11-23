import { useCallback, useEffect, useState } from "react";
import { Link, useLocation, useNavigate, useParams } from "react-router";
import { adminRequest, eventsPath } from "./Admin.jsx";
import { EventArticle } from "./Events.jsx";

const times = [
  ["starts_at", "Event starts"],
  ["ends_at", "Event ends"],
  ["registration_opens_at", "Registration opens"],
  ["registration_closes_at", "Registration closes"],
];
const emptyDraft = { registration_status: "pending" };

function campusInput(instant) {
  if (!instant) return "";
  // A datetime-local input displays a wall time. Campus time is UTC+05:30.
  const local = new Date(new Date(instant).getTime() + 330 * 60000);
  const value = local.toISOString().slice(0, 19);
  return value.endsWith(":00") ? value.slice(0, 16) : value;
}

function requestMessage(detail) {
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail))
    return detail
      .map((e) => {
        const field = e.loc?.slice(1).join(" ")?.replaceAll("_", " ");
        return [field, e.msg].filter(Boolean).join(" — ");
      })
      .join(". ");
  return "The request failed. Try again.";
}

export function EventWorkspace({ create = false, preview = false }) {
  const { id } = useParams();
  const path = create
    ? "session"
    : `events/${encodeURIComponent(id)}${preview ? "/preview" : ""}`;
  return <Workspace key={path} path={path} create={create} preview={preview} />;
}

function Workspace({ path, create, preview }) {
  const navigate = useNavigate();
  const location = useLocation();
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [conflict, setConflict] = useState(false);
  const [busy, setBusy] = useState(false);
  const [dirty, setDirty] = useState(false);
  const [reload, setReload] = useState(0);
  const [notice, setNotice] = useState(
    location.state?.saved ? "Draft saved." : "",
  );

  const request = useCallback(
    async (endpoint, options) => {
      const response = await adminRequest(endpoint, options);
      if (response.status === 401) {
        navigate("/admin/sign-in", {
          replace: true,
          state: { from: location.pathname },
        });
        throw new Error("Sign in to continue.");
      }
      const body = await response.json();
      if (!response.ok) {
        const failure = new Error(requestMessage(body.detail));
        failure.status = response.status;
        throw failure;
      }
      return body;
    },
    [navigate, location.pathname],
  );

  // biome-ignore lint/correctness/useExhaustiveDependencies: reload explicitly fetches the latest saved revision
  useEffect(() => {
    const controller = new AbortController();
    async function load() {
      setData(null);
      setConflict(false);
      setError("");
      setDirty(false);
      try {
        const body = await request(path, { signal: controller.signal });
        if (create && body.role === "reviewer")
          throw new Error(
            "Your account does not have permission to manage events.",
          );
        if (!controller.signal.aborted) setData(create ? emptyDraft : body);
      } catch (e) {
        if (!controller.signal.aborted) setError(e.message);
      }
    }
    void load();
    return () => controller.abort();
  }, [request, path, create, reload]);

  async function write(endpoint, method, payload) {
    setBusy(true);
    setError("");
    setNotice("");
    try {
      const saved = await request(endpoint, {
        method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      setDirty(false);
      if (create)
        navigate(`${eventsPath}/${saved.id}`, {
          replace: true,
          state: { saved: true },
        });
      else if (preview) {
        setData({ ...data, draft: saved });
        setNotice(
          saved.is_demo
            ? "Demo revision published for staff preview."
            : "Event published.",
        );
      } else {
        setData(saved);
        setNotice("Draft saved.");
      }
      return true;
    } catch (e) {
      setError(e.message);
      setConflict(e.status === 409 && !create && !e.message.includes("slug"));
      return false;
    } finally {
      setBusy(false);
    }
  }

  const draft = preview ? data?.draft : data;
  const editorPath = `${eventsPath}/${draft?.id}`;
  return (
    <>
      <section className="wrap service-page editor-page">
        <Link
          className="breadcrumb text-link"
          to={preview && draft ? editorPath : eventsPath}
          onClick={(event) => {
            if (dirty && !window.confirm("Leave without saving your changes?"))
              event.preventDefault();
          }}
        >
          {preview && draft ? "Back to editor" : "Back to events list"}
        </Link>
        {preview && data ? (
          <h2>Saved draft preview</h2>
        ) : (
          <h1>
            {create
              ? "New event draft"
              : preview
                ? "Event preview"
                : "Edit event"}
          </h1>
        )}
        {!data && !error && <p role="status">Loading…</p>}
        {error && <p role="alert">{error}</p>}
        {(conflict || (!data && error)) && (
          <button
            className="action"
            type="button"
            onClick={() => {
              if (!dirty || window.confirm("Discard your changes and reload?"))
                setReload((n) => n + 1);
            }}
          >
            {conflict ? "Reload draft" : "Try again"}
          </button>
        )}
        {notice && <p role="status">{notice}</p>}
        {draft?.is_demo && <p>Practice event · Visible to staff only</p>}
        {draft && !preview && (
          <DraftForm
            key={draft.revision ?? "new"}
            draft={draft}
            dirty={dirty}
            markDirty={() => setDirty(true)}
            busy={busy || conflict}
            onSave={(fields) =>
              write(create ? "events" : path, create ? "POST" : "PUT", fields)
            }
          />
        )}
        {preview && data && (
          <>
            {data.issue && <p role="alert">{data.issue}</p>}
            <div className="page-actions">
              <button
                type="button"
                className="action"
                disabled={
                  busy || conflict || Boolean(data.issue) || Boolean(notice)
                }
                onClick={() => {
                  if (
                    window.confirm(
                      `Publish this saved revision of “${draft.title}”?`,
                    )
                  )
                    void write(`events/${draft.id}/publish`, "POST", {
                      revision: draft.revision,
                    });
                }}
              >
                Publish event
              </button>
              {draft.publication_state === "published" && !draft.is_demo && (
                <Link className="text-link" to={`/events/${draft.slug}`}>
                  View published page
                </Link>
              )}
            </div>
          </>
        )}
      </section>
      {preview && data && (
        <EventArticle
          preview
          event={
            data.event ?? {
              ...draft,
              registration_status: "pending",
              registration_url: null,
              official_url: null,
            }
          }
        />
      )}
    </>
  );
}

function DraftForm({ draft, busy, dirty, markDirty, onSave }) {
  useEffect(() => {
    if (!dirty) return;
    function warn(event) {
      event.preventDefault();
      event.returnValue = "";
    }
    window.addEventListener("beforeunload", warn);
    return () => window.removeEventListener("beforeunload", warn);
  }, [dirty]);

  async function submit(event) {
    event.preventDefault();
    const fields = Object.fromEntries(new FormData(event.currentTarget));
    for (const key of [
      "venue",
      "official_url",
      "registration_url",
      "event_date",
    ])
      fields[key] ||= null;
    for (const [key] of times) {
      const local = fields[key];
      fields[key] =
        local === campusInput(draft[key])
          ? (draft[key] ?? null)
          : local
            ? `${local}+05:30`
            : null;
    }
    if (draft.id) fields.revision = draft.revision;
    await onSave(fields);
  }
  return (
    <form
      className="sign-in-form draft-form"
      onChange={markDirty}
      onSubmit={submit}
    >
      <fieldset disabled={busy}>
        <legend>Event details</legend>
        <label>
          Event title
          <input
            name="title"
            required
            maxLength={200}
            defaultValue={draft.title}
          />
        </label>
        <label>
          Event URL slug
          <input
            name="slug"
            required
            maxLength={120}
            pattern="[a-z0-9]+(-[a-z0-9]+)*"
            title="Use lowercase letters, digits and single hyphens between words."
            readOnly={draft.publication_state === "published"}
            defaultValue={draft.slug}
          />
        </label>
        <label>
          Summary
          <textarea
            name="summary"
            required
            rows={4}
            defaultValue={draft.summary}
          />
        </label>
        <label>
          Event date
          <input
            name="event_date"
            type="date"
            defaultValue={draft.event_date ?? ""}
          />
        </label>
        <label>
          Venue
          <input
            name="venue"
            maxLength={240}
            defaultValue={draft.venue ?? ""}
          />
        </label>
        <label>
          Official event page
          <input
            name="official_url"
            type="url"
            defaultValue={draft.official_url ?? ""}
          />
        </label>
      </fieldset>
      <fieldset disabled={busy}>
        <legend>University registration</legend>
        <label>
          Registration status
          <select
            name="registration_status"
            defaultValue={draft.registration_status}
          >
            {["pending", "open", "closed", "full", "ended"].map((s) => (
              <option key={s} value={s}>
                {s[0].toUpperCase() + s.slice(1)}
              </option>
            ))}
          </select>
        </label>
        <label>
          Verified university registration URL
          <input
            name="registration_url"
            type="url"
            defaultValue={draft.registration_url ?? ""}
          />
        </label>
      </fieldset>
      <fieldset disabled={busy}>
        <legend>Optional times (IST)</legend>
        {times.map(([key, label]) => (
          <label key={key}>
            {label}
            <input
              name={key}
              type="datetime-local"
              step="any"
              defaultValue={campusInput(draft[key])}
            />
          </label>
        ))}
      </fieldset>
      <div className="page-actions">
        <button type="submit" className="action" disabled={busy}>
          Save draft
        </button>
        {draft.id && !dirty && (
          <Link className="text-link" to={`${eventsPath}/${draft.id}/preview`}>
            Preview draft
          </Link>
        )}
        {dirty && <span>Unsaved changes</span>}
      </div>
    </form>
  );
}
