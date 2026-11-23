import { useEffect, useRef, useState } from "react";
import { Page } from "./SiteLayout.jsx";

const cache = new Map();

export function prefetchPublicData(
  paths = ["events", "projects", "team", "recruitment"],
) {
  for (const path of paths) {
    if (cache.has(path)) continue;
    fetch(`/api/${path}`, { cache: "no-store" })
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (data) cache.set(path, data);
      })
      .catch(() => {});
  }
}

export function clearPublicDataCache() {
  cache.clear();
}

prefetchPublicData();

export function PublicData(props) {
  return <Request key={props.path} {...props} />;
}

function Request({ path, name, missing, fallbackTitle, children }) {
  const initialData = cache.get(path);
  const [result, setResult] = useState(
    initialData !== undefined ? { data: initialData } : { loading: true },
  );
  const isAsync = useRef(initialData === undefined);
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
        cache.set(path, data);
        if (!controller.signal.aborted) setResult({ data });
      } catch {
        if (!controller.signal.aborted) setResult({ error: true });
      }
    }
    void load();
    return () => controller.abort();
  }, [path, attempt, hasMissingPage]);
  if (result.missing) return missing;
  if ("data" in result) {
    const content = children(result.data);
    return isAsync.current ? (
      <div className="data-enter">{content}</div>
    ) : (
      content
    );
  }
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
