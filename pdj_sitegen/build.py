import os
import re
import json
import yaml
import tomllib  # Available in Python 3.11+
import markdown
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable
from jinja2 import Environment, FileSystemLoader


@dataclass
class Config:
    markdown_dir: str = 'content'
    resources_dir: str = 'resources'
    structure: str = 'dotlist'  # Options: 'dotlist' or 'tree'
    __globals__: Dict[str, Any] = field(default_factory=dict)


def read_config(config_path: str) -> Config:
    with open(config_path, 'r') as f:
        config_data: Dict[str, Any] = yaml.safe_load(f)
    return Config(**config_data)


def parse_frontmatter(content: str) -> Dict[str, Any]:
    pattern: str = r'^(?P<delimiter>---|\+\+\+|;;;)\n(?P<frontmatter>.*?)\n(?P=delimiter)\n(?P<body>.*)'
    match: Optional[re.Match[str]] = re.match(pattern, content, re.DOTALL)
    if match:
        delimiter: str = match.group('delimiter')
        frontmatter_raw: str = match.group('frontmatter')
        body: str = match.group('body')

        frontmatter_parsers: Dict[str, Callable[[str], Dict[str, Any]]] = {
            '---': lambda x: yaml.safe_load(x),
            ';;;': lambda x: json.loads(x),
            '+++': lambda x: tomllib.loads(x)
        }

        parser: Optional[Callable[[str], Dict[str, Any]]] = frontmatter_parsers.get(delimiter)
        frontmatter: Dict[str, Any] = parser(frontmatter_raw) if parser else {}
    else:
        frontmatter = {}
        body = content

    frontmatter['__content__'] = body
    return frontmatter


def collect_markdown_files(markdown_dir: str, structure: str) -> List[str]:
    md_files: List[str] = []
    for root, _, files in os.walk(markdown_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files


def build_document_tree(md_files: List[str], markdown_dir: str, structure: str) -> Dict[str, Dict[str, Any]]:
    docs: Dict[str, Dict[str, Any]] = {}
    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content: str = f.read()
        frontmatter: Dict[str, Any] = parse_frontmatter(content)
        relative_path: str = os.path.relpath(file_path, markdown_dir)

        if structure == 'dotlist':
            key: str = os.path.splitext(relative_path.replace(os.sep, '.'))[0]
        elif structure == 'tree':
            key = os.path.splitext(relative_path)[0]
        else:
            key = os.path.splitext(relative_path)[0]

        docs[key] = frontmatter
    return docs


def get_parent_keys(key: str, structure: str) -> List[str]:
    if structure == 'dotlist':
        parts: List[str] = key.split('.')
        return ['.'.join(parts[:i]) for i in range(1, len(parts))]
    elif structure == 'tree':
        parts: List[str] = key.split(os.sep)
        return [os.path.join(*parts[:i]) for i in range(1, len(parts))]
    return []


def merge_frontmatter(
    docs: Dict[str, Dict[str, Any]],
    key: str,
    globals_dict: Dict[str, Any],
    structure: str
) -> Dict[str, Any]:
    combined: Dict[str, Any] = {}
    parent_keys: List[str] = get_parent_keys(key, structure)

    # Merge parent frontmatter from root to immediate parent
    for parent_key in parent_keys:
        parent_doc: Dict[str, Any] = docs.get(parent_key, {})
        combined.update(parent_doc)

    # Merge current document's frontmatter
    current_doc: Dict[str, Any] = docs.get(key, {})
    combined.update(current_doc)

    # Merge global variables
    combined.update(globals_dict)
    return combined


def render_markdown(content: str, context: Dict[str, Any]) -> str:
    template = Environment().from_string(content)
    return template.render(context)


def process_markdown_files(
    docs: Dict[str, Dict[str, Any]],
    globals_dict: Dict[str, Any],
    structure: str
) -> None:
    for key in docs.keys():
        context: Dict[str, Any] = merge_frontmatter(docs, key, globals_dict, structure)
        md_content: str = context.get('__content__', '')

        # Render Markdown content with Jinja2
        rendered_md: str = render_markdown(md_content, context)

        # Convert Markdown to HTML
        html_content: str = markdown.markdown(rendered_md)
        context['content'] = html_content

        # Determine which HTML template to use
        template_name: str = context.get('__template__', globals_dict.get('default_template', ''))
        if not template_name:
            raise Exception(f"No HTML template specified for {key}.")

        template_dir: str = os.path.dirname(template_name)
        template_file: str = os.path.basename(template_name)

        # Render final HTML
        env: Environment = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template(template_file)
        final_html: str = template.render(context)

        # Output HTML file
        output_path: str = os.path.join('output', key + '.html')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Generated {output_path}")


def main() -> None:
    config: Config = read_config('config.yaml')
    markdown_dir: str = config.markdown_dir
    resources_dir: str = config.resources_dir
    structure: str = config.structure
    globals_dict: Dict[str, Any] = config.__globals__

    md_files: List[str] = collect_markdown_files(markdown_dir, structure)
    docs: Dict[str, Dict[str, Any]] = build_document_tree(md_files, markdown_dir, structure)
    process_markdown_files(docs, globals_dict, structure)


if __name__ == "__main__":
    main()
