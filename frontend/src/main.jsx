import { lazy, Suspense } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import favicon from "../../docs/design/brand/favicon.ico";
import { About, Contact } from "./ClubPages.jsx";
import { Join } from "./Recruitment.jsx";
import { SiteLinksProvider } from "./SiteLinks.jsx";
import { EventDetail, Events } from "./Events.jsx";
import Home from "./Home.jsx";
import { ProjectDetail, Projects } from "./Projects.jsx";
import { Missing, SiteLayout } from "./SiteLayout.jsx";
import Status from "./Status.jsx";
import { Team } from "./Team.jsx";
import "./styles.css";

function StaffLoadError() {
  return (
    <div className="wrap public-page">
      <h1>Couldn’t load the staff workspace</h1>
      <button
        className="action"
        type="button"
        onClick={() => window.location.reload()}
      >
        Reload page
      </button>
    </div>
  );
}

const StaffRoutes = lazy(() =>
  import("./StaffRoutes.jsx").catch(() => ({ default: StaffLoadError })),
);

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          element={
            <SiteLinksProvider>
              <SiteLayout />
            </SiteLinksProvider>
          }
        >
          <Route index element={<Home />} />
          <Route path="about" element={<About />} />
          <Route path="contact" element={<Contact />} />
          <Route path="events" element={<Events />} />
          <Route path="events/:slug" element={<EventDetail />} />
          <Route path="projects" element={<Projects />} />
          <Route path="projects/:slug" element={<ProjectDetail />} />
          <Route path="team" element={<Team />} />
          <Route path="join" element={<Join key="join" />} />
          <Route path="join/apply" element={<Join key="apply" apply />} />
          <Route path="status" element={<Status />} />
          <Route
            path="admin/*"
            element={
              <Suspense
                fallback={
                  <p className="wrap" role="status">
                    Opening staff workspace…
                  </p>
                }
              >
                <StaffRoutes />
              </Suspense>
            }
          />
          <Route path="*" element={<Missing />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

const tabIcon = document.createElement("link");
tabIcon.rel = "icon";
tabIcon.href = favicon;
document.head.append(tabIcon);
try {
  localStorage.removeItem("c2c-theme");
  document.documentElement.removeAttribute("data-theme");
} catch {}
const root = document.getElementById("root");
if (root) createRoot(root).render(<App />);
