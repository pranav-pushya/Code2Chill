import { Link, useParams } from "react-router";
import { MediaPlaceholder } from "./Gallery.jsx";
import { PublicData } from "./PublicData.jsx";
import { ExternalLink, Missing, Page } from "./SiteLayout.jsx";

export function ProjectRow({ project }) {
  return (
    <article className="work-row project-row">
      <h3 className="project-name">
        <Link to={`/projects/${project.slug}`}>{project.title}</Link>
      </h3>
      <div>
        <p>{project.summary}</p>
        {project.credits.length > 0 && (
          <p className="meta">{project.credits.join(", ")}</p>
        )}
        <Link
          className="text-link"
          to={`/projects/${project.slug}`}
          aria-label={`View project: ${project.title}`}
        >
          View project
        </Link>
      </div>
    </article>
  );
}

export function Projects() {
  return (
    <Page title="Projects">
      <PublicData path="projects" name="projects">
        {(projects) =>
          projects.length ? (
            projects.map((project) => (
              <ProjectRow key={project.slug} project={project} />
            ))
          ) : (
            <>
              <p>No projects are published yet.</p>
              <Link className="text-link" to="/events">
                Explore events
              </Link>
            </>
          )
        }
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
      {(project) => (
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
                project.demo_url || project.repository_url
                  ? "text-link"
                  : "action"
              }
              to="/projects"
            >
              Browse projects
            </Link>
          </div>
          <MediaPlaceholder project>{project.title}</MediaPlaceholder>
        </Page>
      )}
    </PublicData>
  );
}
