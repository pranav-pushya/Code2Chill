import fs from "node:fs";
import path from "node:path";
import { chromium } from "@playwright/test";

const outputDir = path.resolve(
  import.meta.dirname,
  "..",
  "docs",
  "screenshots",
);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

const baseUrl = "http://localhost:5173";

async function main() {
  const browser = await chromium.launch();

  // Desktop context
  const desktop = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2,
  });
  const desktopPage = await desktop.newPage();

  // Mobile context
  const mobile = await browser.newContext({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true,
  });
  const mobilePage = await mobile.newPage();

  console.log("Capturing screenshots from", baseUrl);

  // 1. Home desktop
  await desktopPage.goto(baseUrl, { waitUntil: "networkidle" });
  await desktopPage.screenshot({
    path: path.join(outputDir, "01_home_desktop.png"),
    fullPage: false,
  });
  console.log("✓ 01_home_desktop.png");

  // 2. Home mobile
  await mobilePage.goto(baseUrl, { waitUntil: "networkidle" });
  await mobilePage.screenshot({
    path: path.join(outputDir, "02_home_mobile.png"),
    fullPage: false,
  });
  console.log("✓ 02_home_mobile.png");

  // 3. Events desktop
  await desktopPage.goto(`${baseUrl}/events`, { waitUntil: "networkidle" });
  await desktopPage.screenshot({
    path: path.join(outputDir, "03_events_desktop.png"),
    fullPage: false,
  });
  console.log("✓ 03_events_desktop.png");

  // 4. Projects desktop
  await desktopPage.goto(`${baseUrl}/projects`, { waitUntil: "networkidle" });
  await desktopPage.screenshot({
    path: path.join(outputDir, "04_projects_desktop.png"),
    fullPage: false,
  });
  console.log("✓ 04_projects_desktop.png");

  // 5. Team desktop
  await desktopPage.goto(`${baseUrl}/team`, { waitUntil: "networkidle" });
  await desktopPage.screenshot({
    path: path.join(outputDir, "05_team_desktop.png"),
    fullPage: false,
  });
  console.log("✓ 05_team_desktop.png");

  // 6. Join desktop
  await desktopPage.goto(`${baseUrl}/join`, { waitUntil: "networkidle" });
  await desktopPage.screenshot({
    path: path.join(outputDir, "06_join_desktop.png"),
    fullPage: false,
  });
  console.log("✓ 06_join_desktop.png");

  // 7. Admin sign-in desktop
  await desktopPage.goto(`${baseUrl}/admin`, { waitUntil: "networkidle" });
  await desktopPage.screenshot({
    path: path.join(outputDir, "07_admin_sign_in_desktop.png"),
    fullPage: false,
  });
  console.log("✓ 07_admin_sign_in_desktop.png");

  // 8. Service status desktop
  await desktopPage.goto(`${baseUrl}/status`, { waitUntil: "networkidle" });
  await desktopPage.screenshot({
    path: path.join(outputDir, "08_service_status_desktop.png"),
    fullPage: false,
  });
  console.log("✓ 08_service_status_desktop.png");

  await browser.close();
  console.log("Screenshots captured successfully in docs/screenshots/");
}

main().catch((err) => {
  console.error("Screenshot capture error:", err);
  process.exit(1);
});
