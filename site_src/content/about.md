---
title: About
__template__: about.html.jinja2
__pandoc__:
  email-obfuscation: 'references' # options: none|javascript|references
  toc: true
  number-sections: true
tags:
  - about
  - company
  - contact
---

# About {{ config.globals_.company_name }}

Welcome to {{ config.globals_.company_name }}, where we strive to {{ config.globals_.mission_statement }}.

## Our Growth

Since our founding in {{ config.globals_.founding_year }}, we have grown to {{ config.globals_.employee_count }} employees. Our compound annual growth rate can be expressed mathematically:

$$CAGR = \left(\frac{V_{final}}{V_{initial}}\right)^{\frac{1}{n}} - 1$$

Where $V_{final}$ is our current employee count ({{ config.globals_.employee_count }}), $V_{initial}$ is our starting team size, and $n$ is the number of years.

For a quick estimate of doubling time, we use the Rule of 72:

$$t_{double} \approx \frac{72}{r}$$

## Our Values

{% for value in config.globals_.company_values %}
- {{ value }}
{% endfor %}

## Contact Us

Get in touch with us at:

- Email: [`{{ config.globals_.contact_email }}`](mailto:{{ config.globals_.contact_email }})
