import Status from "./Status.jsx";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Link, Route, Routes } from "react-router";
import icon from "../../docs/design/brand/club-icon-64.png";
import mark from "../../docs/design/brand/club-mark-480.webp";
import favicon from "../../docs/design/brand/favicon.ico";
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
      <a href="#main" className="action skip">
        Skip to content
      </a>
      <header className="site-head">
        <div className="wrap head-inner">
          <Link className="brand" to="/">
            <img src={icon} width="32" height="32" alt="" />
            Code2Chill
          </Link>
          <div className="nav-links">
            <a
              className="text-link"
              href="https://www.instagram.com/code2chill.osl?utm_source=ig_web_button_share_sheet&lqvp=ZDNlZDc0MzIxNw%3D%3D"
              target="_blank"
              rel="noopener noreferrer"
            >
              Instagram
            </a>
            <a
              className="text-link"
              href="https://www.linkedin.com/company/code2chill/posts/?feedView=all"
              target="_blank"
              rel="noopener noreferrer"
            >
              LinkedIn
            </a>
          </div>
        </div>
      </header>
      <main id="main">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/status" element={<Status />} />
          <Route
            path="*"
            element={
              <section className="wrap service-page">
                <h1>Page unavailable</h1>
                <Link className="text-link" to="/">
                  Back to home
                </Link>
              </section>
            }
          />
        </Routes>
      </main>
      <footer className="site-foot">
        <div className="wrap foot-inner">
          <span>Code2Chill · Chitkara University</span>
          <Link to="/status">Service status</Link>
        </div>
      </footer>
    </BrowserRouter>
  );
}

const tabIcon = document.createElement("link");
tabIcon.rel = "icon";
tabIcon.href = favicon;
document.head.append(tabIcon);
const root = document.getElementById("root");
if (root) createRoot(root).render(<App />);
