import { useEffect, useState } from "react";
import { Link, useLocation, useNavigate, useParams } from "react-router";
import { adminRequest } from "./Admin.jsx";
import { Contact } from "./ClubPages.jsx";
import { ProjectArticle } from "./Projects.jsx";
import { Roster } from "./Team.jsx";

export function ContentPreview({ settings }) {
  const { kind, id } = useParams();
  if (
    !settings &&
    (!["members", "projects"].includes(kind) || !/^[1-9]\d*$/.test(id))
  )
    return <p>Preview unavailable.</p>;
  return (
    <Preview
      key={settings ? "settings" : kind + id}
      kind={settings ? "settings" : kind}
      id={settings ? 1 : id}
    />
  );
}
function Preview({ kind, id }) {
  const path = `content/${kind}/${id}`;
  const back =
    kind === "settings" ? "/admin/settings" : `/admin/content/${kind}/${id}`;
  const [data, setData] = useState(null),
    [error, setError] = useState(""),
    [busy, setBusy] = useState(false),
    [published, setPublished] = useState(false),
    [reload, setReload] = useState(0);
  const navigate = useNavigate(),
    location = useLocation();
  // biome-ignore lint/correctness/useExhaustiveDependencies: reload fetches the latest saved draft.
  useEffect(() => {
    const controller = new AbortController();
    async function load() {
      setData(null);
      setError("");
      setPublished(false);
      try {
        const r = await adminRequest(`${path}/preview`, {
          signal: controller.signal,
        });
        if (r.status === 401) {
          navigate("/admin/sign-in", {
            state: { from: location.pathname },
            replace: true,
          });
          return;
        }
        const d = await r.json();
        if (!r.ok) throw new Error(d.detail);
        if (!controller.signal.aborted) setData(d);
      } catch (e) {
        if (!controller.signal.aborted) setError(e.message);
      }
    }
    void load();
    return () => controller.abort();
  }, [path, reload, navigate, location.pathname]);
  async function publish() {
    setBusy(true);
    setError("");
    try {
      const r = await adminRequest(`${path}/publish`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          revision: data.revision,
          fingerprint: data.fingerprint,
        }),
      });
      if (r.status === 401) {
        navigate("/admin/sign-in", {
          state: { from: location.pathname },
          replace: true,
        });
        return;
      }
      if (!r.ok) throw new Error((await r.json()).detail);
      setPublished(true);
      if (kind === "settings")
        window.dispatchEvent(new Event("site-links-published"));
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }
  return (
    <>
      <section className="wrap service-page">
        <Link className="text-link" to={back}>
          Back to editor
        </Link>
        <h1>Saved draft preview</h1>
        {error && (
          <>
            <p role="alert">{error}</p>
            <button
              type="button"
              className="action"
              onClick={() => setReload((v) => v + 1)}
            >
              Reload preview
            </button>
          </>
        )}
        {data && !published && (
          <button
            type="button"
            className="action"
            disabled={busy || !!error}
            onClick={publish}
          >
            Publish
          </button>
        )}
        {published && <p role="status">Published.</p>}
      </section>
      {data &&
        (kind === "settings" ? (
          <Contact preview={data.content} />
        ) : kind === "projects" ? (
          <ProjectArticle project={data.content} />
        ) : (
          <div className="wrap">
            <Roster members={[data.content]} />
          </div>
        ))}
    </>
  );
}
