import { expect, test } from "@playwright/test";

test("public routes fetch only their own content and staff code loads on demand", async ({
  page,
}) => {
  const paths = [];
  await page.route("**/api/**", (route) => {
    const path = new URL(route.request().url()).pathname;
    paths.push(path);
    if (path === "/api/events")
      return route.fulfill({ json: { upcoming: [], past: [] } });
    return route.fulfill({ status: 404 });
  });
  const staffBundle = "**/assets/StaffRoutes-*.js";
  let staffRequests = 0;
  await page.route(staffBundle, (route) => {
    staffRequests++;
    return route.abort();
  });
  await page.goto("/events");
  await expect(page.getByText("No events are listed.")).toBeVisible();
  expect(
    paths.filter((path) => /\/(events|projects|team|recruitment)$/.test(path)),
  ).toEqual(["/api/events"]);
  expect(staffRequests).toBe(0);
  await page.getByRole("link", { name: "Admin sign-in" }).click();
  await expect(
    page.getByRole("heading", { name: "Couldn’t load the staff workspace" }),
  ).toBeVisible();
  await page.unroute(staffBundle);
  await page.route("**/api/admin/session", (route) =>
    route.fulfill({ status: 401 }),
  );
  await page.getByRole("button", { name: "Reload page" }).click();
  await expect(
    page.getByRole("heading", { name: "Admin sign-in" }),
  ).toBeVisible();
  await expect(page).toHaveURL(/\/admin\/sign-in$/);
});
