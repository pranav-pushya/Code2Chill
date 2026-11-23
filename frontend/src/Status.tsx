import { useEffect, useState } from "react";
import { Link } from "react-router";

export default function Status() {
  const [state, setState] = useState<"loading" | "ready" | "unavailable">(
    "loading",
  );
  const [attempt, setAttempt] = useState(0);

  // biome-ignore lint/correctness/useExhaustiveDependencies: attempt is an explicit retry trigger
  useEffect(() => {
    const controller = new AbortController();
    async function check() {
      try {
        const response = await fetch("/api/health", {
          cache: "no-store",
          signal: AbortSignal.any([
            controller.signal,
            AbortSignal.timeout(10000),
          ]),
        });
        const ready = response.ok && (await response.json()).status === "ok";
        if (!controller.signal.aborted)
          setState(ready ? "ready" : "unavailable");
      } catch {
        if (!controller.signal.aborted) setState("unavailable");
      }
    }
    void check();
    return () => controller.abort();
  }, [attempt]);

  return (
    <section className="wrap service-page">
      <h1>Service status</h1>
      <p role="status">
        {state === "loading"
          ? "Checking services…"
          : state === "ready"
            ? "All services are operational."
            : "Services are temporarily unavailable."}
      </p>
      {state === "unavailable" && (
        <p>
          <button
            type="button"
            className="action"
            onClick={() => {
              setState("loading");
              setAttempt((n) => n + 1);
            }}
          >
            Try again
          </button>
        </p>
      )}
      <Link className="text-link" to="/">
        Back to home
      </Link>
    </section>
  );
}
