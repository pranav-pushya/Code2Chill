import { defineConfig } from "@playwright/test";

const origin = "http://127.0.0.1:4175";
export default defineConfig({
  testDir: "./tests",
  use: { baseURL: origin, channel: process.env.PLAYWRIGHT_CHANNEL },
  projects: [
    { name: "phone", use: { viewport: { width: 320, height: 740 } } },
    { name: "desktop", use: { viewport: { width: 1440, height: 900 } } },
  ],
  webServer: {
    command: "npm run preview -- --host 127.0.0.1 --port 4175 --strictPort",
    url: origin,
    env: { API_PROXY_TARGET: "http://127.0.0.1:1" },
  },
});
