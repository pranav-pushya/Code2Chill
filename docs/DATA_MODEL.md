# Code2Chill data model

## Public content

| Record | Stored information |
| --- | --- |
| Member | Name, route slug, public role, optional club domain and biography, display order, and optional portrait. |
| Event | Title, route slug, summary, confirmed calendar date when known, venue, official source page, and optional poster. |
| Project | Title, route slug, summary, optional repository and demo links, originating event, and screenshot. |
| Project credit | Ordered public credit with an optional link to a club member. Contributors can receive credit without appearing on the roster. |
| Media asset | Storage key, content type, alternative text, credit, optional source, and approval for public use. |

New media starts without approval. Missing times and unapproved photographs remain open in the content register. The database types and relationships are defined in the public models. [Content register](CONTENT_REGISTER.md) · [Public models](../backend/app/content_models.py)
