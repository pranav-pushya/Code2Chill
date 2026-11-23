import mark from "../../docs/design/brand/club-mark-480.webp";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import favicon from "../../docs/design/brand/favicon.ico";
import { AdminArea, SignIn } from "./Admin.jsx";
import { EventWorkspace } from "./EventWorkspace.jsx";
import { EventDetail, Events } from "./Events.jsx";
import { Missing, SiteLayout } from "./SiteLayout.jsx";
import Status from "./Status.jsx";
import "./styles.css";

function Home() {
  return (
    <section className="wrap hero">
      <div className="hero-copy">
        <p className="kicker">Chitkara University</p>
        <h1>
          Learn by <span>building.</span>
        </h1>
        <p>
          Code2Chill is a student-led technical club. We bring students together
          for workshops, hackathons and coding events.
        </p>
        <a
          className="action"
          href="https://chitkarau.life/clubs/code2chill"
          target="_blank"
          rel="noopener noreferrer"
        >
          Explore the club
        </a>
      </div>
      <div className="brand-art" aria-hidden="true">
        <div className="print">
          <img src={mark} width="480" height="419" alt="" />
        </div>
      </div>
    </section>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<SiteLayout />}>
          <Route index element={<Home />} />
          <Route path="events" element={<Events />} />
          <Route path="events/:slug" element={<EventDetail />} />
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
