import { useEffect, useState } from "react";
import {
  Link,
  Navigate,
  useLocation,
  useNavigate,
  useParams,
  useSearchParams,
} from "react-router";
import { adminRequest } from "./Admin.jsx";

const base = "/admin/recruitment";
const domains = {
  technical: "Technical",
  content: "Content",
  social_media: "Social Media",
  promotion: "Promotion",
};
const statuses = {
  pending: "Pending",
  shortlisted: "Shortlisted",
  accepted: "Accepted",
  rejected: "Rejected",
};
const campusDate = new Intl.DateTimeFormat("en-IN", {
  dateStyle: "medium",
  timeStyle: "short",
  timeZone: "Asia/Kolkata",
});

function ReviewRequest({ path, children }) {
  const [result, setResult] = useState({});
  const [retry, setRetry] = useState(0);
  const location = useLocation();
  const from = location.pathname + location.search;
  // biome-ignore lint/correctness/useExhaustiveDependencies: retry requests the same resource again.
  useEffect(() => {
    const controller = new AbortController();
    async function load() {
      try {
        const response = await adminRequest(path, {
          signal: controller.signal,
        });
        if (controller.signal.aborted) return;
        if (response.status === 401) {
          setResult({ signedOut: true });
          return;
        }
        if (response.status === 403 || response.status === 404) {
          setResult({ denied: true });
          return;
        }
        if (!response.ok) throw new Error();
        const data = await response.json();
        if (!controller.signal.aborted) setResult({ data });
      } catch {
        if (!controller.signal.aborted) setResult({ error: true });
      }
    }
    void load();
    return () => controller.abort();
  }, [path, retry]);
  if (result.signedOut)
    return <Navigate to="/admin/sign-in" replace state={{ from }} />;
  if (result.denied)
    return (
      <p role="alert">You don’t have access to this recruitment record.</p>
    );
  if (result.error)
    return (
      <div>
        <p role="alert">Couldn’t load recruitment records.</p>
        <button
          type="button"
          className="action"
          onClick={() => {
            setResult({});
            setRetry(retry + 1);
          }}
        >
          Try again
        </button>
      </div>
    );
  return result.data ? (
    children(result.data)
  ) : (
    <p role="status">Loading recruitment records…</p>
  );
}

function Filter({ label, value, options, onChange }) {
  return (
    <label>
      {label}
      <select value={value} onChange={(event) => onChange(event.target.value)}>
        <option value="">
          All {label.toLowerCase() === "status" ? "statuses" : "domains"}
        </option>
        {Object.entries(options).map(([key, title]) => (
          <option key={key} value={key}>
            {title}
          </option>
        ))}
      </select>
    </label>
  );
}

function ApplicationList({ cycleId }) {
  const [params, setParams] = useSearchParams();
  const filters = new URLSearchParams();
  for (const [key, options] of [
    ["domain", domains],
    ["status", statuses],
  ]) {
    const value = params.get(key);
    if (Object.hasOwn(options, value)) filters.set(key, value);
  }
  const requestedPage = Number(params.get("page"));
  if (
    Number.isInteger(requestedPage) &&
    requestedPage > 1 &&
    requestedPage <= 1000000
  )
    filters.set("page", String(requestedPage));
  const page = Number(filters.get("page") || 1);
  function update(key, value) {
    const next = new URLSearchParams(filters);
    if (key !== "page") next.delete("page");
    if (value) next.set(key, value);
    else next.delete(key);
    setParams(next);
  }
  const path = `recruitment/${cycleId}/applications?${filters}`;
  return (
    <>
      <div className="review-filters draft-form sign-in-form">
        <Filter
          label="Domain"
          options={domains}
          value={filters.get("domain") || ""}
          onChange={(value) => update("domain", value)}
        />
        <Filter
          label="Status"
          options={statuses}
          value={filters.get("status") || ""}
          onChange={(value) => update("status", value)}
        />
      </div>
      <ReviewRequest key={path} path={path}>
        {(data) => (
          <>
            {data.applications.length === 0 ? (
              <p>No applications match this selection.</p>
            ) : (
              <ul className="admin-events">
                {data.applications.map((item) => (
                  <li key={item.id}>
                    <strong>
                      <Link
                        className="text-link"
                        to={{
                          pathname: `${base}/${cycleId}/applications/${item.id}`,
                          search: filters.toString(),
                        }}
                      >
                        {item.full_name}
                      </Link>
                    </strong>
                    <span>{domains[item.domain]}</span>
                    <span>{statuses[item.status]}</span>
                    <time dateTime={item.submitted_at}>
                      {campusDate.format(new Date(item.submitted_at))} IST
                    </time>
                  </li>
                ))}
              </ul>
            )}
            {(page > 1 || data.has_more) && (
              <nav className="page-actions" aria-label="Application pages">
                {page > 1 && (
                  <button
                    type="button"
                    className="action"
                    onClick={() => update("page", String(page - 1))}
                  >
                    Previous page
                  </button>
                )}
                {data.has_more && (
                  <button
                    type="button"
                    className="action"
                    onClick={() => update("page", String(page + 1))}
                  >
                    Next page
                  </button>
                )}
              </nav>
            )}
          </>
        )}
      </ReviewRequest>
    </>
  );
}

function Detail({ initial, path, reload }) {
  const [item, setItem] = useState(initial);
  const [choice, setChoice] = useState("");
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [needsReload, setNeedsReload] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  async function save(event) {
    event.preventDefault();
    if (!choice || saving) return;
    setSaving(true);
    setMessage("");
    try {
      const response = await adminRequest(path, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ expected_status: item.status, status: choice }),
      });
      if (response.status === 401) {
        navigate("/admin/sign-in", {
          replace: true,
          state: { from: location.pathname + location.search },
        });
        return;
      }
      if (response.status === 403 || response.status === 404) {
        reload();
        return;
      }
      if (response.status === 409) {
        setNeedsReload(true);
        setMessage(
          "The status changed. Reload the application before recording a decision.",
        );
        return;
      }
      if (!response.ok) throw new Error();
      const updated = await response.json();
      setItem(updated);
      setChoice("");
      setMessage("Decision saved.");
    } catch {
      setNeedsReload(true);
      setMessage(
        "Couldn’t confirm the save. Reload to check the recorded status.",
      );
    } finally {
      setSaving(false);
    }
  }
  return (
    <section className="content-block">
      <h2>{item.full_name}</h2>
      <dl className="review-detail">
        <dt>University email</dt>
        <dd>{item.university_email}</dd>
        <dt>Domain</dt>
        <dd>{domains[item.domain]}</dd>
        <dt>Status</dt>
        <dd>{statuses[item.status]}</dd>
        <dt>Submitted</dt>
        <dd>
          <time dateTime={item.submitted_at}>
            {campusDate.format(new Date(item.submitted_at))} IST
          </time>
        </dd>
        {item.motivation && (
          <>
            <dt>Motivation</dt>
            <dd>{item.motivation}</dd>
          </>
        )}
        {item.portfolio_url && (
          <>
            <dt>Portfolio</dt>
            <dd>{item.portfolio_url}</dd>
          </>
        )}
      </dl>
      {item.allowed_statuses.length > 0 && (
        <form onSubmit={save} className="sign-in-form draft-form">
          <label>
            Review decision
            <select
              required
              value={choice}
              disabled={saving || needsReload}
              onChange={(event) => setChoice(event.target.value)}
            >
              <option value="">Choose a decision</option>
              {item.allowed_statuses.map((status) => (
                <option key={status} value={status}>
                  {statuses[status]}
                </option>
              ))}
            </select>
          </label>
          <button
            type="submit"
            className="action"
            disabled={!choice || saving || needsReload}
          >
            {saving ? "Saving…" : "Save decision"}
          </button>
        </form>
      )}
      {message && <p role="status">{message}</p>}
      {needsReload && (
        <button className="action" type="button" onClick={reload}>
          Reload application
        </button>
      )}
      {item.history.length > 0 && (
        <section className="content-block">
          <h2>Decision history</h2>
          <ol>
            {item.history.map((entry) => (
              <li key={entry.new_state}>
                {statuses[entry.previous_state]} → {statuses[entry.new_state]} ·{" "}
                {entry.reviewer} ·{" "}
                <time dateTime={entry.occurred_at}>
                  {campusDate.format(new Date(entry.occurred_at))} IST
                </time>
              </li>
            ))}
          </ol>
        </section>
      )}
    </section>
  );
}

export function ReviewDashboard() {
  const [revision, setRevision] = useState(0);
  const { cycleId, applicationId } = useParams();
  const navigate = useNavigate();
  const location = useLocation();
  if (
    [cycleId, applicationId].some(
      (id) => id !== undefined && !/^[1-9]\d*$/.test(id),
    )
  ) {
    return <Navigate to={base} replace />;
  }
  const listPath = `${base}/${cycleId}/applications`;
  const detail = `recruitment/${cycleId}/applications/${applicationId}`;
  return (
    <section className="wrap service-page">
      <Link
        className="text-link breadcrumb"
        to={applicationId ? listPath + location.search : "/admin"}
      >
        {applicationId ? "Back to applications" : "Back to dashboard"}
      </Link>
      <h1>{applicationId ? "Application details" : "Review applications"}</h1>
      {applicationId ? (
        <ReviewRequest key={`${detail}:${revision}`} path={detail}>
          {(item) => (
            <Detail
              initial={item}
              path={detail}
              reload={() => setRevision((value) => value + 1)}
            />
          )}
        </ReviewRequest>
      ) : (
        <ReviewRequest path="recruitment">
          {(cycles) => (
            <>
              {cycles.length === 0 ? (
                <p>No recruitment cycles are available for this account.</p>
              ) : (
                <label className="cycle-select draft-form">
                  Recruitment cycle
                  <select
                    value={cycleId || ""}
                    onChange={(event) =>
                      navigate(
                        event.target.value
                          ? `${base}/${event.target.value}/applications`
                          : base,
                      )
                    }
                  >
                    <option value="">Choose a cycle</option>
                    {cycles.map((cycle) => (
                      <option key={cycle.id} value={cycle.id}>
                        {cycle.title}
                      </option>
                    ))}
                  </select>
                </label>
              )}
              {cycleId && <ApplicationList key={cycleId} cycleId={cycleId} />}
            </>
          )}
        </ReviewRequest>
      )}
    </section>
  );
}
