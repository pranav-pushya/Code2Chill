import { expect, test } from "@playwright/test";

const mockCycle = {
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
    events: {
      upcoming: [],
      past: [
        {
          slug: "byte-the-vibe",
          title: "Byte The Vibe",
          summary: "A team coding sprint with mentor guidance.",
          event_date: "2026-05-18",
          venue: "Pierre Hall, Architecture Block",
          registration_status: "ended",
        },
      ],
    },
    projects: [
      {
        slug: "nexus",
        title: "NEXUS",
        summary: "A survival game that adjusts difficulty using signals.",
        credits: ["Ayush Sharma", "Arnav Sharma"],
      },
    ],
    team: [
      {
        slug: "lakshay-kalra",
        name: "Lakshay Kalra",
        role_title: "President",
        domain: null,
      },
    ],
    recruitment: mockCycle,
    "site-links": {
      university: "https://chitkarau.life/clubs/code2chill",
      instagram: "https://instagram.com/code2chill.osl",
      linkedin: "https://linkedin.com/company/code2chill",
    },
    health: { status: "ok" },
  };

  await page.route("**/api/**", (route) => {
    const url = new URL(route.request().url());
    const path = url.pathname.slice(5); // strip '/api/'
    if (path === "page-head") return route.fulfill({ body: "" });
    if (path === "admin/session")
      return route.fulfill({
        status: 401,
        body: JSON.stringify({ detail: "Signed out" }),
      });
    if (path === "admin/sign-in")
      return route.fulfill({
        status: 401,
        body: JSON.stringify({ detail: "Incorrect email or password." }),
      });
    if (Object.hasOwn(responses, path))
      return route.fulfill({
        contentType: "application/json",
        body: JSON.stringify(responses[path]),
      });
    return route.fulfill({ status: 404 });
  });
});

test("deep link navigation and refresh persistence across production routes", async ({
  page,
}) => {
  const routes = [
    "/events",
    "/projects",
    "/team",
    "/join",
    "/status",
    "/admin",
  ];

  for (const target of routes) {
    await page.goto(target);
    await expect(page.getByRole("main")).toBeVisible();

    // Verify page refresh maintains route and does not 404
    await page.reload();
    await expect(page.getByRole("main")).toBeVisible();
    expect(page.url()).toContain(target);
  }
});

test("brand mark and responsive image assets load successfully", async ({
  page,
}) => {
  await page.goto("/");
  const brandImg = page.locator(".brand-art img").first();
  await expect(brandImg).toBeVisible();

  // Verify that the browser successfully decoded the image
  const naturalWidth = await brandImg.evaluate((img) => img.naturalWidth);
  expect(naturalWidth).toBeGreaterThan(0);
});

test("staff sign-in form validates input and shows feedback on invalid credentials", async ({
  page,
}) => {
  await page.goto("/admin");
  await expect(
    page.getByRole("heading", { name: "Admin sign-in" }),
  ).toBeVisible();

  // Test submitting invalid credentials
  const emailInput = page.getByLabel("Email address");
  const passwordInput = page.locator('input[name="password"]');

  await emailInput.fill("unauthorized@example.com");
  await passwordInput.fill("wrongpassword123");
  await page.getByRole("button", { name: "Sign in" }).click();

  await expect(
    page.getByText("Sign-in failed. Check your details or try again later."),
  ).toBeVisible();
});
