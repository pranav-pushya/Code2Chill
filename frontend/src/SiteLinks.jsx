import { createContext, useContext, useEffect, useState } from "react";

const defaults = {
  university: "https://chitkarau.life/clubs/code2chill",
  instagram:
    "https://www.instagram.com/code2chill.osl?utm_source=ig_web_button_share_sheet&lqvp=ZDNlZDc0MzIxNw%3D%3D",
  linkedin: "https://www.linkedin.com/company/code2chill/posts/?feedView=all",
};
const Context = createContext(defaults);
export function useSiteLinks() {
  return useContext(Context);
}
export function SiteLinksProvider({ children }) {
  const [links, setLinks] = useState(defaults);
  useEffect(() => {
    const controller = new AbortController();
    async function refresh() {
      try {
        const response = await fetch("/api/site-links", {
          signal: controller.signal,
          cache: "no-store",
        });
        if (response.ok) {
          const data = await response.json();
          if (!controller.signal.aborted) setLinks(data || defaults);
        }
      } catch {
        /* Keep official defaults when offline. */
      }
    }
    void refresh();
    window.addEventListener("site-links-published", refresh);
    return () => {
      controller.abort();
      window.removeEventListener("site-links-published", refresh);
    };
  }, []);
  return <Context.Provider value={links}>{children}</Context.Provider>;
}
