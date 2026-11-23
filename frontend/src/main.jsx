import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import favicon from "../../docs/design/brand/favicon.ico";
import { AdminArea, SignIn } from "./Admin.jsx";
import { EventWorkspace } from "./EventWorkspace.jsx";
import { About, Contact, Join } from "./ClubPages.jsx";
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
        <Route element={<SiteLayout />}>
          <Route index element={<Home />} />
          <Route path="about" element={<About />} />
          <Route path="contact" element={<Contact />} />
          <Route path="events" element={<Events />} />
          <Route path="events/:slug" element={<EventDetail />} />
          <Route path="projects" element={<Projects />} />
          <Route path="projects/:slug" element={<ProjectDetail />} />
          <Route path="team" element={<Team />} />
          <Route path="join" element={<Join />} />
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
const root = document.getElementById("root");
if (root) createRoot(root).render(<App />);
