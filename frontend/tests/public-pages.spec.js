import AxeBuilder from "@axe-core/playwright";
import { expect, test } from "@playwright/test";

const cycle = {
  id: 1,
  title: "Club recruitment",
  eligibility: "Current students",
  domains: ["technical"],
  email_domain: "campus.example",
  opens_at: "2030-01-01T00:00:00Z",
  closes_at: "2030-02-01T00:00:00Z",
  state: "open",
  route: "local",
};

test.beforeEach(async ({ page }) => {
  const responses = {
    events: { upcoming: [], past: [] },
    projects: [],
    team: [],
    recruitment: cycle,
    "site-links": null,
  };
  await page.route("**/api/**", (route) => {
    const path = new URL(route.request().url()).pathname.slice(5);
    if (path === "page-head") return route.fulfill({ body: "" });
    if (path === "recruitment/1/email-code")
      return route.fulfill({ status: 204 });
    if (Object.hasOwn(responses, path))
      return route.fulfill({
        contentType: "application/json",
        body: JSON.stringify(responses[path]),
      });
    return route.fulfill({ status: 404 });
  });
});

test("keyboard navigation reaches content and returns focus from the phone menu", async ({
  page,
}, info) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await page.keyboard.press("Tab");
  await expect(
    page.getByRole("link", { name: "Skip to content" }),
  ).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(page.getByRole("main")).toBeFocused();
  await page.getByRole("link", { name: "Code2Chill home" }).focus();
  await page.keyboard.press("Tab");
  if (info.project.name === "phone") {
    const menu = page.getByRole("button", { name: "Menu" });
    await expect(menu).toBeFocused();
    await page.keyboard.press("Enter");
    await page.keyboard.press("Tab");
    await expect(
      page.getByRole("link", { name: "About", exact: true }),
    ).toBeFocused();
    await page.keyboard.press("Escape");
    await expect(menu).toBeFocused();
    await page.keyboard.press("Enter");
    await page.keyboard.press("Tab");
  }
  await expect(
    page.getByRole("link", { name: "About", exact: true }),
  ).toBeFocused();
  await page.keyboard.press("Enter");
  await expect(
    page.getByRole("heading", { name: "About Code2Chill" }),
  ).toBeVisible();
  await expect(page.getByRole("main")).toBeFocused();
});

test("public content, application and staff sign-in fit the viewport and pass axe checks", async ({
  page,
}) => {
  for (const path of [
    "/",
    "/events",
    "/projects",
    "/team",
    "/join/apply",
    "/admin/sign-in",
  ]) {
    await page.goto(path);
    await expect(page.locator("h1")).toBeVisible();
    if (path === "/join/apply")
      await expect(page.getByLabel("Full name")).toBeVisible();
    await expect(page.getByText(/^Loading .+…$/)).toHaveCount(0);
    await page.evaluate(async () => {
      await document.fonts.ready;
      await Promise.allSettled(
        document.getAnimations().map((animation) => animation.finished),
      );
    });
    expect(
      await page.evaluate(
        () => document.documentElement.scrollWidth <= innerWidth,
      ),
      path,
    ).toBe(true);
    const { violations } = await new AxeBuilder({ page })
      .withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"])
      .analyze();
    expect(
      violations.map(({ id, nodes }) => [id, nodes.map((node) => node.target)]),
      path,
    ).toEqual([]);
  }
});

test("an applicant can correct required fields and reach the verification code", async ({
  page,
}) => {
  await page.goto("/join/apply");
  await page.getByRole("button", { name: "Send email code" }).click();
  await expect(page.getByLabel("Full name")).toBeFocused();
  await page.getByLabel("Full name").fill("Test Student");
  await page.getByLabel("University email").fill("student@campus.example");
  await page
    .getByRole("combobox", { name: "Domain", exact: true })
    .selectOption("technical");
  await page.getByRole("button", { name: "Send email code" }).click();
  await expect(page.getByLabel("Email verification code")).toBeFocused();
  await page.getByRole("button", { name: "Change email" }).click();
  await expect(page.getByLabel("University email")).toBeFocused();
});
