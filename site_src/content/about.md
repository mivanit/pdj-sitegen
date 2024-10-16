---
title: About
__template__: about.html.jinja2
pandoc_kwargs:
  email-obfuscation: 'references' # options: none|javascript|references
tags:
  - about
  - company
  - contact
---

# About {{ config.globals_.company_name }}

Welcome to {{ config.globals_.company_name }}, where we strive to {{ config.globals_.mission_statement }}.

## Contact Us

Get in touch with us at:

- Email: [`{{ config.globals_.contact_email }}`](mailto:{{ config.globals_.contact_email }})
