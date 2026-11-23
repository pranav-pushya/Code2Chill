import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate, useParams } from "react-router";
import { adminRequest } from "./Admin.jsx";

const sections = {
  members: "Members",
  projects: "Projects",
  media: "Media",
  settings: "Site settings",
};
const controls = {
  members: [
    ["name", "Name", "text", true],
    ["slug", "URL slug", "text", true],
    ["role_title", "Role", "text", true],
    ["domain", "Domain", "domains"],
    ["display_order", "Display order", "number", true],
    ["bio", "Biography", "textarea"],
    ["portrait_id", "Portrait", "media"],
  ],
  projects: [
    ["title", "Title", "text", true],
    ["slug", "URL slug", "text", true],
    ["summary", "Summary", "textarea", true],
    ["credits", "Contributors (one per line)", "lines"],
    ["repository_url", "Repository URL", "url"],
    ["demo_url", "Demo URL", "url"],
    ["screenshot_id", "Screenshot", "media"],
    ["event_id", "Related event", "events"],
  ],
  media: [
    ["storage_key", "Storage key", "text", true],
    ["asset_url", "Hosted image URL", "url"],
    ["content_type", "Content type", "text", true],
    ["source_url", "Source URL", "url"],
    ["alt_text", "Alternative text", "text"],
    ["credit", "Credit", "text"],
    ["approved_for_publication", "Approved for publication", "checkbox"],
  ],
  settings: [
    ["university", "University listing", "url", true],
    ["instagram", "Instagram profile", "url", true],
    ["linkedin", "LinkedIn profile", "url", true],
  ],
};
const paths = {
  members: "/admin/content/members",
  projects: "/admin/content/projects",
  media: "/admin/media",
  settings: "/admin/settings",
};
const domains = ["technical", "content", "social_media", "promotion"].map(
  (value) => ({ id: value, label: value.replace("_", " ") }),
);

export function ContentEditor({ section, preview = false }) {
  const params = useParams();
  const kind = section ?? params.kind;
  const id = kind === "settings" ? "1" : params.id;
  if (
    !Object.hasOwn(sections, kind) ||
    (id && id !== "new" && !/^[1-9]\d*$/.test(id))
  )
    return <p>Content unavailable.</p>;
  return (
    <Workspace
      key={[kind, id, preview].join("/")}
      kind={kind}
      id={id}
      preview={preview}
    />
  );
}

function Workspace({ kind, id }) {
  const navigate = useNavigate();
  const location = useLocation();
  const [data, setData] = useState(null),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState(location.state?.saved ? "Saved." : "");
  const [reload, setReload] = useState(0);
  const [options, setOptions] = useState({ domains, media: [], events: [] });
  const base = paths[kind],
    api = `content/${kind}`;
  // biome-ignore lint/correctness/useExhaustiveDependencies: reload repeats the same read
  useEffect(() => {
    const controller = new AbortController();
    async function read(path) {
      const r = await adminRequest(path, { signal: controller.signal });
      if (r.status === 401) {
        navigate("/admin/sign-in", {
          replace: true,
          state: { from: location.pathname },
        });
        throw new Error("Sign in to continue.");
      }
      if (!r.ok)
        throw new Error(
          r.status === 403 ? "Access denied." : "Couldn’t load this content.",
        );
      return r.json();
    }
    async function load() {
      setError("");
      setData(null);
      try {
        let value;
        if (id === "new") {
          await read(api);
          value = { fields: { display_order: 0, content_type: "image/webp" } };
        } else {
          value = await read(id ? `${api}/${id}` : api);
        }
        const media =
          id && ["members", "projects"].includes(kind)
            ? await read("content/media")
            : [];
        const events =
          id && kind === "projects"
            ? (await read("events")).map((e) => ({ id: e.id, label: e.title }))
            : [];
        if (!controller.signal.aborted) {
          setOptions({ domains, media, events });
          setData(value);
        }
      } catch (e) {
        if (!controller.signal.aborted) setError(e.message);
      }
    }
    void load();
    return () => controller.abort();
  }, [api, id, kind, location.pathname, navigate, reload]);
  async function save(e) {
    e.preventDefault();
    const form = new FormData(e.currentTarget);
    const fields = {};
    for (const [name, , type] of controls[kind]) {
      const v = form.get(name);
      if (type === "checkbox") fields[name] = v === "on";
      else if (type === "lines")
        fields[name] = v
          .split(/\r?\n/)
          .map((s) => s.trim())
          .filter(Boolean);
      else if (["media", "events", "number"].includes(type))
        fields[name] = v === "" ? null : Number(v);
      else
        fields[name] = v || (["alt_text", "credit"].includes(name) ? "" : null);
    }
    setBusy(true);
    setError("");
    setNotice("");
    try {
      const creating = id === "new";
      const r = await adminRequest(creating ? api : `${api}/${id}`, {
        method: creating ? "POST" : "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ revision: data.revision, fields }),
      });
      if (r.status === 401) {
        navigate("/admin/sign-in", { state: { from: location.pathname } });
        return;
      }
      const saved = await r.json();
      if (!r.ok)
        throw new Error(
          typeof saved.detail === "string"
            ? saved.detail
            : "Check the fields and try again.",
        );
      if (creating)
        navigate(`${base}/${saved.id}`, {
          replace: true,
          state: { saved: true },
        });
      else {
        setData(saved);
        setNotice("Saved.");
      }
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="wrap service-page">
      <Link
        className="text-link breadcrumb"
        to={id && kind !== "settings" ? base : "/admin"}
      >
        {id && kind !== "settings"
          ? `Back to ${sections[kind].toLowerCase()}`
          : "Back to dashboard"}
      </Link>
      <h1>{sections[kind]}</h1>
      {error && (
        <div>
          <p role="alert">{error}</p>
          <button
            className="action"
            type="button"
            onClick={() => setReload((n) => n + 1)}
          >
            Reload saved content
          </button>
        </div>
      )}
      {!data && !error && <p role="status">Loading…</p>}
      {data &&
        (!id ? (
          <>
            <Link className="action" to={`${base}/new`}>
              Add{" "}
              {kind === "media"
                ? "media"
                : kind === "members"
                  ? "member"
                  : "project"}
            </Link>
            {!data.length && <p>No records yet.</p>}
            <ul className="admin-events">
              {data.map((row) => (
                <li key={row.id}>
                  <Link className="text-link" to={`${base}/${row.id}`}>
                    {row.label}
                  </Link>
                </li>
              ))}
            </ul>
          </>
        ) : (
          <form className="draft-form sign-in-form" onSubmit={save}>
            {controls[kind].map(([name, label, type, required]) => (
              <label key={name} htmlFor={name}>
                {label}
                {options[type] ? (
                  <select
                    id={name}
                    name={name}
                    defaultValue={data.fields[name] ?? ""}
                  >
                    <option value="">None</option>
                    {options[type].map((o) => (
                      <option value={o.id} key={o.id}>
                        {o.label}
                      </option>
                    ))}
                  </select>
                ) : type === "textarea" || type === "lines" ? (
                  <textarea
                    id={name}
                    name={name}
                    required={required}
                    defaultValue={
                      type === "lines"
                        ? data.fields[name]?.join("\n")
                        : (data.fields[name] ?? "")
                    }
                  />
                ) : type === "checkbox" ? (
                  <input
                    id={name}
                    name={name}
                    type="checkbox"
                    defaultChecked={data.fields[name]}
                  />
                ) : (
                  <input
                    type={type}
                    id={name}
                    name={name}
                    required={required}
                    min={type === "number" ? 0 : undefined}
                    defaultValue={data.fields[name] ?? ""}
                  />
                )}
              </label>
            ))}
            <button type="submit" className="action" disabled={busy}>
              {busy
                ? "Saving…"
                : kind === "media"
                  ? "Save media"
                  : "Save draft"}
            </button>
          </form>
        ))}
      {notice && <p role="status">{notice}</p>}
    </section>
  );
}
