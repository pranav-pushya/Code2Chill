import { useEffect } from "react";
import { useLocation } from "react-router";

const managedTags =
  'title, meta[name="description"], meta[name="robots"], meta[property^="og:"], meta[name^="twitter:"], link[rel="canonical"]';

export function PageMetadata() {
  const { pathname } = useLocation();
  useEffect(() => {
    const path = pathname.replace(/\/+$/, "") || "/";
    if (document.querySelector("title")?.dataset.pagePath === path) return;
    const controller = new AbortController();
    // Drop the previous route's preview while the new route is loading.
    for (const tag of document.head.querySelectorAll(managedTags)) tag.remove();
    document.title = "Code2Chill";
    const robots = document.createElement("meta");
    robots.name = "robots";
    robots.content = "noindex, nofollow";
    document.head.append(robots);
    async function update() {
      try {
        const response = await fetch(
          `/api/page-head?${new URLSearchParams({ path })}`,
          {
            signal: AbortSignal.any([
              controller.signal,
              AbortSignal.timeout(8000),
            ]),
          },
        );
        const markup = await response.text();
        if (controller.signal.aborted) return;
        const head = new DOMParser().parseFromString(markup, "text/html").head;
        if (!head.querySelector("title[data-page-path]")) return;
        for (const tag of document.head.querySelectorAll(managedTags))
          tag.remove();
        document.head.append(...head.querySelectorAll(managedTags));
      } catch {
        // Keep the generic title if the service is unavailable.
      }
    }
    void update();
    return () => controller.abort();
  }, [pathname]);
  return null;
}
