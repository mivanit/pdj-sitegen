"""Pandoc filters for pdj-sitegen.

This package contains pandoc JSON filters that can be used during markdown
to HTML conversion. Available filters:

- `csv_code_table`: Convert fenced code blocks with class `csv_table` to HTML tables
- `links_md2html`: Convert internal `.md` links to `.html` links

Filters can be enabled in frontmatter or global config via the `__pandoc__` section:

    __pandoc__:
      filter: links_md2html

Or for multiple filters:

    __pandoc__:
      filter:
        - links_md2html
        - csv_code_table
"""
