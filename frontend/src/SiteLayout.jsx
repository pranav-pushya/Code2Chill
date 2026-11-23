import { useEffect, useRef, useState } from "react";
import { Link, NavLink, Outlet, useLocation } from "react-router";
import icon from "../../docs/design/brand/club-icon-64.png";

export const university = "https://chitkarau.life/clubs/code2chill";
export const profiles = {
  Instagram:
    "https://www.instagram.com/code2chill.osl?utm_source=ig_web_button_share_sheet&lqvp=ZDNlZDc0MzIxNw%3D%3D",
  LinkedIn: "https://www.linkedin.com/company/code2chill/posts/?feedView=all",
};

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
          <img src={icon} width="32" height="32" alt="" />
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
          {["Events"].map((label) => (
            <NavLink
              key={label}
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
      <a href="#main" className="action skip">
        Skip to content
      </a>
      <Header key={pathname} />
      <main id="main" ref={main} tabIndex={-1}>
        <Outlet />
      </main>
      <footer className="site-foot">
        <div className="wrap foot-inner">
          <span className="footer-name">Code2Chill · Chitkara University</span>
          <nav aria-label="Footer">
            {Object.entries(profiles).map(([label, href]) => (
              <ExternalLink key={label} href={href}>
                {label}
              </ExternalLink>
            ))}
            <Link to="/status">Service status</Link>
            <Link to="/admin">Admin sign-in</Link>
          </nav>
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

export function Missing({ item = "Page", to = "/", action = "Go home" }) {
  return (
    <Page title={`${item} not found`}>
      <Link className="action" to={to}>
        {action}
      </Link>
    </Page>
  );
}
