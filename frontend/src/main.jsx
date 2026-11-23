import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import favicon from "../../docs/design/brand/favicon.ico";
import { AdminArea, SignIn } from "./Admin.jsx";
import { EventWorkspace } from "./EventWorkspace.jsx";
import { About, Contact } from "./ClubPages.jsx";
import { Join } from "./Recruitment.jsx";
import { ReviewDashboard } from "./ReviewDashboard.jsx";
import { ContentEditor } from "./ContentEditor.jsx";
import { SiteLinksProvider } from "./SiteLinks.jsx";
import { ContentPreview } from "./ContentPreview.jsx";
import { EventDetail, Events } from "./Events.jsx";
import Home from "./Home.jsx";
import { ProjectDetail, Projects } from "./Projects.jsx";
import { Missing, SiteLayout } from "./SiteLayout.jsx";
import Status from "./Status.jsx";
import { Team } from "./Team.jsx";
import "./styles.css";

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
          <Route path="admin/sign-in" element={<SignIn />} />
          <Route
            path="admin/content/events/new"
            element={<EventWorkspace create />}
          />
          <Route path="admin/content/events/:id" element={<EventWorkspace />} />
          <Route
            path="admin/content/events/:id/preview"
            element={<EventWorkspace preview />}
          />
          <Route path="admin" element={<AdminArea key="dashboard" />} />
          <Route
            path="admin/content/:kind/:id/preview"
            element={<ContentPreview />}
          />
          <Route
            path="admin/settings/preview"
            element={<ContentPreview settings />}
          />
          <Route path="admin/content/:kind/:id?" element={<ContentEditor />} />
          <Route
            path="admin/media/:id?"
            element={<ContentEditor section="media" />}
          />
          <Route
            path="admin/settings"
            element={<ContentEditor section="settings" />}
          />
          <Route path="admin/recruitment" element={<ReviewDashboard />} />
          <Route
            path="admin/recruitment/:cycleId/applications"
            element={<ReviewDashboard />}
          />
          <Route
            path="admin/recruitment/:cycleId/applications/:applicationId"
            element={<ReviewDashboard />}
          />
          <Route
            path="admin/content/events"
            element={<AdminArea key="events" events />}
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
