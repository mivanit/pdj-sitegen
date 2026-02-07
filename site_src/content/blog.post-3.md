---
title: Technical Tutorial - Building Static Sites
date: 2023-03-10
excerpt: A technical deep-dive into static site generation with code examples in Python and JavaScript.
__pandoc__:
  filter: links_md2html
  highlight-style: pygments
tags:
  - blog
  - tutorial
  - code
---

# Technical Tutorial: Building Static Sites

In this post, we'll explore the technical aspects of static site generation. For more context, check out our [first blog post](blog.post-1.md) and [second blog post](blog.post-2.md).

## Python Example

Here's a simple Python script that processes Markdown files:

```python
import os
from pathlib import Path

def process_markdown_files(content_dir: str) -> list[dict]:
    """Process all markdown files in a directory."""
    results = []

    for md_file in Path(content_dir).glob("**/*.md"):
        with open(md_file, "r") as f:
            content = f.read()

        # Extract frontmatter and content
        if content.startswith("---"):
            parts = content.split("---", 2)
            frontmatter = parts[1]
            body = parts[2]
        else:
            frontmatter = ""
            body = content

        results.append({
            "path": str(md_file),
            "frontmatter": frontmatter,
            "body": body
        })

    return results

if __name__ == "__main__":
    files = process_markdown_files("content")
    print(f"Processed {len(files)} files")
```

## JavaScript Example

For client-side interactivity, you might use JavaScript like this:

```javascript
// Filter blog posts by tag
function filterByTag(posts, tag) {
    return posts.filter(post => post.tags.includes(tag));
}

// Render a list of posts to the DOM
function renderPosts(posts, container) {
    container.innerHTML = posts
        .map(post => `
            <article class="post">
                <h2><a href="${post.url}">${post.title}</a></h2>
                <time datetime="${post.date}">${post.date}</time>
                <p>${post.excerpt}</p>
            </article>
        `)
        .join('');
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    const posts = JSON.parse(document.getElementById('posts-data').textContent);
    const container = document.getElementById('posts-container');
    renderPosts(posts, container);
});
```

## Shell Commands

Building a static site often involves shell commands:

```bash
# Build the site
python -m pdj_sitegen config.yml

# Smart rebuild (only changed files)
python -m pdj_sitegen config.yml -s

# Serve locally for development
python -m http.server -d output 8000
```

## Configuration Example

Here's a sample YAML configuration:

```yaml
content_dir: content
templates_dir: templates
output_dir: output
prettify: true
__pandoc__:
  mathjax: true
  toc: true
```

## Related Pages

Be sure to check out our [projects](projects.md) and learn more [about us](about.md)!
