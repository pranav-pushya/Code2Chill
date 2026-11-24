import { useState } from "react";
import { Link, useParams } from "react-router";
import { MediaPlaceholder, PublishedImage } from "./Gallery.jsx";
import { PublicData } from "./PublicData.jsx";
import { ExternalLink, Missing, Page } from "./SiteLayout.jsx";

const PROJECT_METADATA = {
  nexus: {
    origin: "DOMination 2026",
    category: "ai",
    tags: ["Face-API.js", "Web Audio API", "HTML5 Canvas", "Vite"],
  },
  chronoatlas: {
    origin: "DOMination 2026",
    category: "frontend",
    tags: ["DOM Manipulation", "CSS Grid", "Responsive UI"],
  },
  "domination-starter": {
    origin: "Official Starter",
    category: "starters",
    tags: ["Vanilla JS", "Vite Scaffold", "Open Source"],
  },
};

const CATEGORIES = [
  { id: "all", label: "All projects" },
  { id: "frontend", label: "Frontend & UI" },
  { id: "ai", label: "AI & Interactive" },
  { id: "starters", label: "Starters & Tooling" },
];

const COMMUNITY_STARTER = {
  slug: "domination-starter",
  title: "DOMination Starter Kit",
  summary:
    "Official base template supplied to hackathon teams at DOMination with semantic landmarks, reset styles, and accessibility criteria.",
  credits: ["Code2Chill Team"],
  repository_url: "https://github.com/Cypher45/c2c-event",
  demo_url: "https://c2c-event.vercel.app/",
};

function getProjectMeta(project) {
  if (PROJECT_METADATA[project.slug]) {
    return PROJECT_METADATA[project.slug];
  }
  const text = `${project.title} ${project.summary ?? ""}`.toLowerCase();
  let category = "frontend";
  if (
    text.includes("starter") ||
    text.includes("template") ||
    text.includes("tool") ||
    text.includes("scaffold")
  ) {
    category = "starters";
  } else if (
    text.includes("ai") ||
    text.includes("emotion") ||
    text.includes("game") ||
    text.includes("signals")
  ) {
    category = "ai";
  }
  return {
    origin: "Student Build",
    category,
    tags: ["Web", "Open Source"],
  };
}

function ProjectSpotlight({ project }) {
  if (!project) return null;
  return (
    <section
      className="project-spotlight-card"
      aria-label="Featured project spotlight"
    >
      <div className="spotlight-content">
        <span className="spotlight-award-badge">
          🏆 1st Place · DOMination 2026
        </span>
        <h2 className="spotlight-title">{project.title}</h2>
        <p className="spotlight-summary">{project.summary}</p>
        {project.credits?.length > 0 && (
          <p className="spotlight-credits">
            Built by: <strong>{project.credits.join(", ")}</strong>
          </p>
        )}
        <div className="spotlight-actions">
          {project.demo_url && (
            <ExternalLink
              className="btn-spotlight-primary"
              href={project.demo_url}
            >
              Launch Live Demo ↗
            </ExternalLink>
          )}
          {project.repository_url && (
            <ExternalLink
              className="btn-spotlight-secondary"
              href={project.repository_url}
            >
              View Repository ↗
            </ExternalLink>
          )}
          <Link
            className="spotlight-case-link"
            to={`/projects/${project.slug}`}
          >
            Case Study →
          </Link>
        </div>
      </div>
      <div className="spotlight-mockup" aria-hidden="true">
        <div className="mockup-bar">
          <span className="mockup-dot red" />
          <span className="mockup-dot yellow" />
          <span className="mockup-dot green" />
          <span className="mockup-title">nexus-engine.app</span>
        </div>
        <div className="mockup-screen">
          <div className="mockup-icon">🎮</div>
          <div className="mockup-engine-text">NEXUS ENGINE v1.0</div>
          <div className="mockup-status-text">
            Facial Emotion Telemetry Active
          </div>
        </div>
      </div>
    </section>
  );
}

function ProjectSubmissionBanner() {
  return (
    <section
      className="project-submit-banner"
      aria-labelledby="project-submit-heading"
    >
      <div className="project-submit-content">
        <h2 id="project-submit-heading" className="project-submit-title">
          Built something cool at a Code2Chill event?
        </h2>
        <p className="project-submit-desc">
          Whether you built a winning hackathon prototype, a sprint submission,
          or a community open-source tool, get your project listed in our
          official campus showcase.
        </p>
      </div>
      <Link to="/contact" className="action project-submit-btn">
        Submit Your Project ↗
      </Link>
    </section>
  );
}

export function ProjectRow({ project }) {
  const meta = getProjectMeta(project);
  return (
    <article className="work-row project-row">
      <div>
        <div className="project-row-header">
          <span className="project-origin-pill">{meta.origin}</span>
          <h3 className="project-name">
            <Link to={`/projects/${project.slug}`}>{project.title}</Link>
          </h3>
        </div>
        <p>{project.summary}</p>
        <div className="project-tags">
          {meta.tags.map((tag) => (
            <span key={tag} className="project-tag">
              {tag}
            </span>
          ))}
        </div>
      </div>
      <div className="project-row-actions">
        {project.credits?.length > 0 && (
          <p className="meta">{project.credits.join(", ")}</p>
        )}
        <div className="project-links-row">
          {project.demo_url && (
            <ExternalLink className="text-link" href={project.demo_url}>
              Demo ↗
            </ExternalLink>
          )}
          {project.repository_url && (
            <ExternalLink className="text-link" href={project.repository_url}>
              GitHub ↗
            </ExternalLink>
          )}
          <Link
            className="text-link"
            to={`/projects/${project.slug}`}
            aria-label={`View project details: ${project.title}`}
          >
            Details &rarr;
          </Link>
        </div>
      </div>
    </article>
  );
}

export function Projects() {
  const [activeCategory, setActiveCategory] = useState("all");

  return (
    <Page title="Projects">
      <p className="lede">
        Open-source tools, hackathon prototypes, and web applications engineered
        by students across Code2Chill competitions and coding sprints.
      </p>

      <PublicData path="projects" name="projects">
        {(apiProjects) => {
          const allProjects = [...apiProjects];
          if (!allProjects.some((p) => p.slug === COMMUNITY_STARTER.slug)) {
            allProjects.push(COMMUNITY_STARTER);
          }

          const spotlightProject =
            allProjects.find((p) => p.slug === "nexus") || allProjects[0];

          const filteredProjects =
            activeCategory === "all"
              ? allProjects
              : allProjects.filter(
                  (p) => getProjectMeta(p).category === activeCategory,
                );

          return (
            <div className="projects-container">
              {/* Proposal 1: Spotlight Hero */}
              {spotlightProject && (
                <ProjectSpotlight project={spotlightProject} />
              )}

              {/* Proposal 2: Category Filter Pills */}
              <div className="projects-filter-bar">
                <div
                  className="projects-filter-pills"
                  role="tablist"
                  aria-label="Filter projects by category"
                >
                  {CATEGORIES.map((cat) => {
                    const count =
                      cat.id === "all"
                        ? allProjects.length
                        : allProjects.filter(
                            (p) => getProjectMeta(p).category === cat.id,
                          ).length;
                    const isActive = activeCategory === cat.id;

                    return (
                      <button
                        key={cat.id}
                        type="button"
                        role="tab"
                        aria-selected={isActive}
                        className={`projects-filter-pill ${isActive ? "active" : ""}`}
                        onClick={() => setActiveCategory(cat.id)}
                      >
                        <span>{cat.label}</span>
                        <span className="projects-filter-count">{count}</span>
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Projects List */}
              <div className="projects-list">
                {filteredProjects.length > 0 ? (
                  filteredProjects.map((project) => (
                    <ProjectRow key={project.slug} project={project} />
                  ))
                ) : (
                  <p className="projects-empty">
                    No projects found in this category.
                  </p>
                )}
              </div>

              {/* Proposal 5: Submission Callout Banner */}
              <ProjectSubmissionBanner />
            </div>
          );
        }}
      </PublicData>
    </Page>
  );
}

export function ProjectDetail() {
  const { slug } = useParams();
  return (
    <PublicData
      path={`projects/${encodeURIComponent(slug)}`}
      name="project details"
      fallbackTitle="Project details"
      missing={
        <Missing item="Project" to="/projects" action="Browse projects" />
      }
    >
      {(project) => <ProjectArticle project={project} />}
    </PublicData>
  );
}

export function ProjectArticle({ project }) {
  return (
    <Page title={project.title}>
      <p className="lede">{project.summary}</p>
      {project.credits.length > 0 && (
        <section className="content-block">
          <h2>Contributors</h2>
          <p>{project.credits.join(", ")}</p>
        </section>
      )}
      <div className="page-actions">
        {project.demo_url && (
          <ExternalLink className="action" href={project.demo_url}>
            Open project demo
          </ExternalLink>
        )}
        {project.repository_url && (
          <ExternalLink
            className={project.demo_url ? "text-link" : "action"}
            href={project.repository_url}
          >
            View source repository
          </ExternalLink>
        )}
        <Link
          className={
            project.demo_url || project.repository_url ? "text-link" : "action"
          }
          to="/projects"
        >
          Browse projects
        </Link>
      </div>
      {project.screenshot?.asset_url ? (
        <PublishedImage image={project.screenshot} />
      ) : (
        <MediaPlaceholder project>{project.title}</MediaPlaceholder>
      )}
    </Page>
  );
}
