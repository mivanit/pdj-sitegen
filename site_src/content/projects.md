---
title: Our Projects
description: A showcase of our recent client projects and case studies
author: Lorem Ipsum Technologies
date: 2023-06-01
categories:
  - portfolio
  - case-studies
__template__: custom.html.jinja2
tags:
  - projects
  - index
---

# Our Projects

Here's a showcase of our recent projects:

{% for project in child_docs_dotlist.values() | sort(attribute="frontmatter.completion_date", reverse=true) %}
## [{{ project.frontmatter.title }}]({{ project.file_meta.path_html }})

**Completed on:** {{ project.frontmatter.completion_date }}

{{ project.frontmatter.short_description }}

[Learn more]({{ project.file_meta.path_html }})

---
{% endfor %}