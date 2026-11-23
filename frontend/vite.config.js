import { fileURLToPath } from "node:url";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig, loadEnv } from "vite";
import { pageDocuments } from "./pageDocuments.js";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "API_");
  const apiTarget = env.API_PROXY_TARGET || "http://127.0.0.1:8000";
  return {
    plugins: [react(), tailwindcss(), pageDocuments(apiTarget)],
    server: {
      fs: {
        allow: [
          process.cwd(),
          fileURLToPath(new URL("../docs/design", import.meta.url)),
        ],
      },
      proxy: { "/api": { target: apiTarget, changeOrigin: false } },
    },
  };
});
