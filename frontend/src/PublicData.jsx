import { useEffect, useRef, useState } from "react";
import { Page } from "./SiteLayout.jsx";
import { getFallbackData } from "./fallbackData.js";

const cache = new Map();

export function PublicData(props) {
  return <Request key={props.path} {...props} />;
}

function Request({ path, name, missing, fallbackTitle, children }) {
  const fallback = getFallbackData(path);
  const initialData = cache.get(path) ?? fallback ?? undefined;
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
            AbortSignal.timeout(30000),
          ]),
        });
        if (response.status === 404 && hasMissingPage) {
          if (!controller.signal.aborted) {
            cache.delete(path);
            setResult({ missing: true });
          }
          return;
        }
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        if (!controller.signal.aborted) {
          cache.set(path, data);
          setResult({ data });
        }
      } catch {
        if (!controller.signal.aborted) {
          if (fallback !== null && fallback !== undefined) {
            cache.set(path, fallback);
            setResult({ data: fallback });
          } else {
            setResult({ error: true });
          }
        }
      }
    }
    void load();
    return () => controller.abort();
  }, [path, attempt, hasMissingPage, fallback]);
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
