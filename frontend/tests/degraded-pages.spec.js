import { expect, test } from "@playwright/test";

test("a slow event list can fail, retry and recover to an empty schedule", async ({
  page,
}) => {
  let release;
  const pending = new Promise((resolve) => {
    release = resolve;
  });
  let failed = true;
  await page.route("**/api/**", async (route) => {
    if (new URL(route.request().url()).pathname !== "/api/events")
      return route.fulfill({ status: 404 });
    if (failed) {
      await pending;
      return route.fulfill({ status: 503 });
    }
    return route.fulfill({ json: { upcoming: [], past: [] } });
  });
  await page.goto("/events");
  await expect(page.getByRole("status")).toHaveText("Loading events…");
  release();
  await expect(page.getByRole("alert")).toHaveText("Couldn’t load events.");
  failed = false;
  await page.getByRole("button", { name: "Try again" }).click();
  await expect(page.getByText("No events are listed.")).toBeVisible();
  await page.getByRole("link", { name: "Learn about the club" }).click();
  await expect(
    page.getByRole("heading", { name: "About Code2Chill" }),
  ).toBeVisible();
});

test("a missing project image preserves its description, credit and navigation", async ({
  page,
}) => {
  await page.route("**/api/**", (route) =>
    new URL(route.request().url()).pathname === "/api/projects/workshop"
      ? route.fulfill({
          json: {
            title: "Student workshop",
            summary: "A club project.",
            credits: [],
            screenshot: {
              asset_url: "/missing-photo.webp",
              alt_text: "Workshop results",
              credit: "Club photographer",
            },
          },
        })
      : route.fulfill({ status: 404 }),
  );
  await page.route("**/missing-photo.webp", (route) =>
    route.fulfill({ status: 404 }),
  );
  await page.goto("/projects/workshop");
  await expect(page.getByText("Image unavailable")).toBeVisible();
  await expect(
    page.getByText("Workshop results · Club photographer"),
  ).toBeVisible();
  await expect(
    page.getByRole("link", { name: "Browse projects" }),
  ).toHaveAttribute("href", "/projects");
});
