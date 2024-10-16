---
title: index
description: index of all pages
author: "(auto generated)"
tags:
  - index
---

# index

<select id="tagFilter" onchange="filterPosts()">
<option value="">Select a tag</option>
{% set unique_tags = [] %}
{% for key, post in docs.items() %}
    {% for tag in post.frontmatter.tags %}
    {% if tag not in unique_tags %}
    {% set unique_tags = unique_tags.append(tag) %}
    {% endif %}
    {% endfor %}
{% endfor %}
{% for tag in unique_tags %}
<option value="{{ tag }}">{{ tag }}</option>
{% endfor %}
</select>

<ul id="postList">
{% for key, post in docs.items() %}
<li class="post-item" data-tags="{{ post.frontmatter.tags | join(", ") }}">
    <a href="{{ post.file_meta.path_html }}">{{ post.frontmatter.title }}</a>
    <p>{{ post.frontmatter.description }}</p>
    {% if post.frontmatter.tags %}
    <p>tags: {{ post.frontmatter.tags | join(", ") }}</p>
    {% endif %}
</li>
{% endfor %}
</ul>

<script>
function filterPosts() {
    const filter = document.getElementById('tagFilter').value.toLowerCase();
    const posts = document.querySelectorAll('.post-item');

    posts.forEach(post => {
        const tags = post.getAttribute('data-tags').toLowerCase();
        if (filter === "" || tags.includes(filter)) {
            post.style.display = '';
        } else {
            post.style.display = 'none';
        }
    });
}
</script>