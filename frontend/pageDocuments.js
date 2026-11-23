import { readFile } from "node:fs/promises";
import { get as httpGet } from "node:http";
import { get as httpsGet } from "node:https";
import { resolve } from "node:path";
import { text } from "node:stream/consumers";

// Serve the same initial head as the deployed FastAPI/Caddy pair, while Vite
// still supplies the React refresh preamble and development module URLs.
export function pageDocuments(apiTarget) {
  function middleware(server, preview) {
    return async (req, res, next) => {
      const url = new URL(req.url ?? "/", "http://localhost");
      if (
        !["GET", "HEAD"].includes(req.method) ||
        /^\/(?:api(?:\/|$)|@|src\/|node_modules\/|assets\/|share\/)/.test(
          url.pathname,
        ) ||
        /\.[^/]+$/.test(url.pathname) ||
        !(req.headers.accept ?? "*/*").match(/text\/html|\*\/\*/)
      )
        return next();
      try {
        const target = new URL("/api/page-head", apiTarget);
        target.searchParams.set("path", decodeURIComponent(url.pathname));
        const get = target.protocol === "https:" ? httpsGet : httpGet;
        const response = await new Promise((resolve, reject) => {
          get(
            target,
            {
              headers: { host: req.headers.host },
              signal: AbortSignal.timeout(5000),
            },
            resolve,
          ).on("error", reject);
        });
        const head = await text(response);
        if (!head.startsWith("<title data-page-path=")) return next();
        const directory = preview
          ? resolve(server.config.root, server.config.build.outDir)
          : server.config.root;
        let shell = await readFile(resolve(directory, "index.html"), "utf8");
        if (!preview) shell = await server.transformIndexHtml(req.url, shell);
        res.writeHead(response.statusCode, {
          "Content-Type": "text/html; charset=utf-8",
          "Cache-Control": "no-cache",
        });
        res.end(
          req.method === "HEAD"
            ? undefined
            : shell.replace(
                "<title>Code2Chill | Chitkara University</title>",
                () => head,
              ),
        );
      } catch {
        next();
      }
    };
  }
  return {
    name: "public-page-documents",
    configureServer(server) {
      server.middlewares.use(middleware(server, false));
    },
    configurePreviewServer(server) {
      server.middlewares.use(middleware(server, true));
    },
  };
}
