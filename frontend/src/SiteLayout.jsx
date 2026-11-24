import { useEffect, useRef, useState } from "react";
import { Link, NavLink, Outlet, useLocation } from "react-router";
import icon from "../../docs/design/brand/club-icon-64.png";
import { PageMetadata } from "./PageMetadata.jsx";

import { useSiteLinks } from "./SiteLinks.jsx";

export function ExternalLink({ href, children, className = "text-link" }) {
  return (
    <a
      className={className}
      href={href}
      target="_blank"
      rel="noopener noreferrer"
    >
      {children}
    </a>
  );
}

function Header() {
  const [open, setOpen] = useState(false);
  const menu = useRef(null);
  const header = useRef(null);
  useEffect(() => {
    if (!open) return;
    function dismiss(event) {
      if (event.key === "Escape") {
        setOpen(false);
        if (header.current.contains(document.activeElement))
          menu.current.focus();
      }
    }
    function outside(event) {
      if (!header.current.contains(event.target)) setOpen(false);
    }
    const desktop = window.matchMedia("(min-width: 48rem)");
    function resize() {
      if (desktop.matches) setOpen(false);
    }
    document.addEventListener("keydown", dismiss);
    document.addEventListener("pointerdown", outside);
    desktop.addEventListener("change", resize);
    return () => {
      document.removeEventListener("keydown", dismiss);
      document.removeEventListener("pointerdown", outside);
      desktop.removeEventListener("change", resize);
    };
  }, [open]);

  return (
    <header className="site-head" ref={header}>
      <div className="wrap head-inner">
        <Link
          className="brand"
          to="/"
          aria-label="Code2Chill home"
          onClick={() => setOpen(false)}
        >
          Code2Chill
        </Link>
        <button
          className="menu-toggle"
          type="button"
          ref={menu}
          aria-expanded={open}
          aria-controls="primary-nav"
          onClick={() => setOpen(!open)}
        >
          Menu
        </button>
        <nav
          id="primary-nav"
          aria-label="Main"
          className={open ? "nav-links is-open" : "nav-links"}
        >
          {["About", "Events", "Projects", "Team", "Join"].map((label) => (
            <NavLink
              key={label}
              className={label === "Join" ? "join-link" : undefined}
              to={`/${label.toLowerCase()}`}
              onClick={() => setOpen(false)}
            >
              {label}
            </NavLink>
          ))}
        </nav>
      </div>
    </header>
  );
}

export function SiteLayout() {
  const { university, instagram, linkedin } = useSiteLinks();
  const { pathname, hash } = useLocation();
  const previous = useRef(pathname);
  const main = useRef(null);
  useEffect(() => {
    if (previous.current !== pathname && !hash) {
      window.scrollTo(0, 0);
      main.current.focus({ preventScroll: true });
    }
    previous.current = pathname;
  }, [pathname, hash]);
  return (
    <>
      <PageMetadata />
      <a href="#main" className="action skip">
        Skip to content
      </a>
      <Header key={pathname} />
      <main id="main" ref={main} tabIndex={-1}>
        <div key={pathname} className="page-enter">
          <Outlet />
        </div>
      </main>
      <footer className="site-foot">
        <div className="wrap foot-container">
          <div className="foot-grid">
            <div className="foot-brand-col">
              <Link className="brand" to="/" aria-label="Code2Chill home">
                <img
                  src={icon}
                  width="32"
                  height="32"
                  alt=""
                  decoding="async"
                />
                Code2Chill
              </Link>
              <p className="foot-desc">
                Where serious code meets chill vibes. Official student-led
                technical community under the{" "}
                <strong>Office of Student Life at Chitkara University</strong>.
              </p>
              <p className="foot-motto">
                <em>Build together, grow together.</em>
              </p>
            </div>

            <nav className="foot-nav-col" aria-label="Explore pages">
              <h2 className="foot-eyebrow">Explore</h2>
              <ul className="foot-links">
                {["Home", "About", "Events", "Projects", "Team", "Join"].map(
                  (label) => (
                    <li key={label}>
                      <Link
                        to={label === "Home" ? "/" : `/${label.toLowerCase()}`}
                        className="foot-link"
                      >
                        {label}
                      </Link>
                    </li>
                  ),
                )}
              </ul>
            </nav>

            <div className="foot-connect-col">
              <h2 className="foot-eyebrow">Connect & Operations</h2>
              <div className="foot-connect-group">
                <ExternalLink href={instagram} className="foot-social-link">
                  <span>Instagram</span>
                  <span className="foot-arrow" aria-hidden="true">
                    ↗
                  </span>
                </ExternalLink>
                <ExternalLink href={linkedin} className="foot-social-link">
                  <span>LinkedIn</span>
                  <span className="foot-arrow" aria-hidden="true">
                    ↗
                  </span>
                </ExternalLink>
                {university && (
                  <ExternalLink href={university} className="foot-social-link">
                    <span>University Portal</span>
                    <span className="foot-arrow" aria-hidden="true">
                      ↗
                    </span>
                  </ExternalLink>
                )}
              </div>
              <div className="foot-meta-links">
                <Link to="/contact" className="foot-meta-link">
                  Contact Desk
                </Link>
                <span className="foot-sep" aria-hidden="true">
                  ·
                </span>
                <Link to="/admin" className="foot-meta-link">
                  Staff Sign-In
                </Link>
              </div>
            </div>
          </div>

          <div className="foot-sub">
            <p className="foot-copy">
              © {new Date().getFullYear()} Code2Chill · Chitkara University. All
              rights reserved.
            </p>
            <p className="foot-credit">
              <span className="foot-dot" aria-hidden="true">
                ●
              </span>{" "}
              Built by the Code2Chill community ·{" "}
              <ExternalLink
                href="https://github.com/pranav-pushya/Code2Chill"
                className="foot-repo-link"
              >
                Source on GitHub
              </ExternalLink>
            </p>
          </div>
        </div>
      </footer>
    </>
  );
}

export function Page({ title, children }) {
  return (
    <section className="wrap public-page">
      <h1>{title}</h1>
      {children}
    </section>
  );
}

export function Missing({
  item = "Page",
  to = "/",
  action = "Return to homepage",
}) {
  const location = useLocation();
  const isPage = item.toLowerCase() === "page";
  const pathDisplay = location?.pathname || `/${item.toLowerCase()}`;

  return (
    <section className="wrap public-page not-found-page">
      <PageMetadata
        title={`${item} Not Found`}
        description={`The requested ${item.toLowerCase()} could not be found on Code2Chill.`}
      />

      <div className="not-found-header">
        <p className="kicker">
          <span>
            HTTP_STATUS: 404 {"//"} {item.toUpperCase()}_UNRESOLVED
          </span>
        </p>
        <span className="not-found-stamp">VOID PASS</span>
      </div>

      <div className="not-found-hero">
        <div className="not-found-digit" aria-hidden="true">
          4<span>0</span>4
        </div>
        <div>
          <h1 className="not-found-lead">
            {isPage
              ? "Lost beyond the scheduled programme."
              : `${item} out of bounds.`}
          </h1>
          <p className="not-found-desc">
            {isPage
              ? "You've wandered off the scheduled programme. The page, project, or event you requested was either deprecated, moved to another branch, or is currently chilling out of bounds."
              : `The ${item.toLowerCase()} you requested could not be located in the current edition. It may have concluded, changed URL, or hasn't been published yet.`}
          </p>
        </div>
      </div>

      <section className="void-ticket" aria-label="Ticket Inspection Details">
        <div className="void-ticket-head">
          <span className="void-ticket-badge">
            <span className="void-ticket-dot" aria-hidden="true" />
            TICKET_INSPECTOR: ROUTE_AUDIT
          </span>
          <span className="void-ticket-origin">CODE2CHILL_PROGRAMME</span>
        </div>
        <div className="void-ticket-grid">
          <div className="void-ticket-item">
            <span>Queried Target</span>
            <strong>{pathDisplay}</strong>
          </div>
          <div className="void-ticket-item">
            <span>Error Status</span>
            <strong className="error-code">404 NOT_FOUND</strong>
          </div>
          <div className="void-ticket-item">
            <span>Suggested Action</span>
            <strong style={{ color: "var(--blue)" }}>
              {action.toUpperCase()}
            </strong>
          </div>
        </div>
      </section>

      <div className="not-found-actions">
        <Link className="action" to={to}>
          {action} →
        </Link>
        <Link className="not-found-pill" to="/events">
          Browse Events
        </Link>
        <Link className="not-found-pill" to="/projects">
          Student Projects
        </Link>
        <Link className="not-found-pill" to="/team">
          Meet the Team
        </Link>
      </div>
    </section>
  );
}
