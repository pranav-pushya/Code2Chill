import { useEffect, useState } from "react";
import { Page } from "./SiteLayout.jsx";

export function PublicData(props) {
  return <Request key={props.path} {...props} />;
}

function Request({ path, name, missing, fallbackTitle, children }) {
  const [result, setResult] = useState({ loading: true });
  const [attempt, setAttempt] = useState(0);
  const hasMissingPage = Boolean(missing);
  // biome-ignore lint/correctness/useExhaustiveDependencies: retry repeats the same request
  useEffect(() => {
    const controller = new AbortController();
    async function load() {
      try {
        const response = await fetch(`/api/${path}`, {
          cache: "no-store",
          signal: AbortSignal.any([
            controller.signal,
            AbortSignal.timeout(10000),
          ]),
        });
        if (response.status === 404 && hasMissingPage) {
          if (!controller.signal.aborted) setResult({ missing: true });
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
  }, [path, attempt, hasMissingPage]);
  if (result.missing) return missing;
  if ("data" in result) return children(result.data);
  const feedback = result.loading ? (
    <p className="data-feedback" role="status">
      Loading {name}…
    </p>
  ) : (
    <div className="data-feedback">
      <p role="alert">Couldn’t load {name}.</p>
      <button
        className="action"
        type="button"
        onClick={() => {
          setResult({ loading: true });
          setAttempt(attempt + 1);
        }}
      >
        Try again
      </button>
    </div>
  );
  return fallbackTitle ? (
    <Page title={fallbackTitle}>{feedback}</Page>
  ) : (
    feedback
  );
}
