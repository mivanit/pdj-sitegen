---
title: Our Blog
description: lorem ipsum blog posts
tags:
  - blog
  - index
---

# Welcome to Our Blog

Here you'll find our latest thoughts, ideas, and updates.

## Recent Posts

{% for post in docs.values() %}
{% if post.file_meta.path.startswith("blog.post-") %}
### [{{ post.frontmatter.title }}]({{ post.file_meta.path_html }})

*Posted on {{ post.frontmatter.date }}*

{{ post.frontmatter.excerpt }}

[Read more]({{ post.file_meta.path_html }})

---
{% endif %}
{% endfor %}