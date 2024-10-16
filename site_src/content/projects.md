---
title: Our Projects
tags:
  - projects
  - index
---

# Our Projects

Here's a showcase of our recent projects:

{% for project in child_docs.values() | sort(attribute="frontmatter.completion_date", reverse=true) %}
## [{{ project.frontmatter.title }}]({{ project.file_meta.path_html }})

**Completed on:** {{ project.frontmatter.completion_date }}

{{ project.frontmatter.short_description }}

[Learn more]({{ project.file_meta.path_html }})

---
{% endfor %}