---
title: index
description: index of all pages
author: "(auto generated)"
---

{% for key, post in docs.items() %}

- [{{ post.frontmatter.title }}]({{ post.file_meta.path_html }})
	{{ post.frontmatter.description }}  

{% endfor %}