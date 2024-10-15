"""build a site from markdown files using Jinja2 and Pandoc

pipeline:

- get all markdown files
- for each markdown file:
    - regex frontmatter and content from the markdown file
    - execute a template on the frontmatter, with globals_ and file metadata as context
    - load the frontmatter into a dict
    - execute a template on the content with frontmatter, globals_ and file metadata as context
    - convert the content to HTML using Pandoc
    - execute a template on the specified or default template with the HTML content, frontmatter, globals_ and file metadata as context
"""


import os
import re
import json
import yaml
import tomllib
from pathlib import Path

from muutils.json_serialize import SerializableDataclass, serializable_dataclass, serializable_field
from typing import Any, Literal, Optional, Callable
from jinja2 import Environment, FileSystemLoader, Template

Format = Literal['yaml', 'json', 'toml']

StructureFormat = Literal['dotlist', 'tree']

FORMAT_MAP: dict[str, Format] = {
    'yaml': 'yaml',
    'yml': 'yaml',
    'json': 'json',
    'toml': 'toml'
}


FRONTMATTER_PARSERS: dict[str, Callable[[str], dict[str, Any]]] = {
    '---': lambda x: yaml.safe_load(x),
    ';;;': lambda x: json.loads(x),
    '+++': lambda x: tomllib.loads(x),
}

FRONTMATTER_REGEX: re.Pattern = re.compile(
	r'^(?P<delimiter>$$DELIMS$$)\n(?P<frontmatter>.*?)\n(?P=delimiter)\n(?P<body>.*)'.replace(
        '$$DELIMS$$',
        '|'.join([
            re.escape(d) for d in
            FRONTMATTER_PARSERS.keys()
        ]),
    ),
)


def read_data_file(file_path: Path, fmt: None|Format = None) -> dict[str, Any]:
    if fmt is None:
        fmt = FORMAT_MAP[file_path.suffix.lstrip('.')]
    
    match fmt:
        case 'yaml':
            with open(file_path, 'r') as f:
                return yaml.safe_load(f)
        case 'json':
            with open(file_path, 'r') as f:
                return json.load(f)
        case 'toml':
            with open(file_path, 'r') as f:
                return tomllib.load(f)
            
def save_data_file(data: dict[str, Any], file_path: Path, fmt: None|Format = None) -> None:
    if fmt is None:
        fmt = FORMAT_MAP[file_path.suffix.lstrip('.')]
    
    match fmt:
        case 'yaml':
            with open(file_path, 'w') as f:
                yaml.safe_dump(data, f)
        case 'json':
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
        case 'toml':
            with open(file_path, 'w') as f:
                f.write(tomllib.dumps(data))

_PATH_FIELD_SERIALIZATION_KWARGS: dict[str, Callable] = dict(
    serialization_fn=lambda x: x.as_posix(),
    deserialize_fn=lambda x: Path(x),
)

@serializable_dataclass
class Config(SerializableDataclass):
    content_dir: Path = serializable_field(
        default=Path('content'),
        **_PATH_FIELD_SERIALIZATION_KWARGS,
    )
    resources_dir: Path = serializable_field(
        default=Path('resources'),
        **_PATH_FIELD_SERIALIZATION_KWARGS,
    )
    templates_dir: Path = serializable_field(
        default=Path('templates'),
        **_PATH_FIELD_SERIALIZATION_KWARGS,
    )
    default_template: Path = serializable_field(
        default=Path('templates/default.html.jinja'),
        **_PATH_FIELD_SERIALIZATION_KWARGS,
    )
    jinja_env_kwargs: dict[str, Any] = serializable_field(
        default_factory=dict,
    )
    structure: StructureFormat = serializable_field(
        default='dotlist',
    )
    globals_: dict[str, Any] = serializable_field(
        default_factory=dict,
    )
    pandoc_cli_extra_args: list[str] = serializable_field(
        default_factory=lambda: ["--mathjax"],
    )
    pandoc_fmt_from: str = serializable_field(
        default='markdown+smart',
    )
    pandoc_fmt_to: str = serializable_field(
        default='html',
    )
    
    @classmethod
    def read(cls, config_path: Path, fmt: None|Format = None) -> 'Config':
        return cls.load(read_data_file(config_path, fmt))
    
    def save(self, config_path: Path, fmt: None|Format = 'json') -> None:
        save_data_file(self.serialize(), config_path, fmt)


    def assemble_pandoc_cmd(
        file_from: Path,
        file_to: Path,

    )

def parse_frontmatter(content: str) -> dict[str, Any]:
    match: Optional[re.Match[str]] = re.match(FRONTMATTER_REGEX, content, re.DOTALL)
    if match:
        delimiter: str = match.group('delimiter')
        frontmatter_raw: str = match.group('frontmatter')
        body: str = match.group('body')

        parser: Optional[Callable[[str], dict[str, Any]]] = FRONTMATTER_PARSERS.get(delimiter, None)
        frontmatter: dict[str, Any] = parser(frontmatter_raw) if parser else {}
    else:
        frontmatter = {}
        body = content

    frontmatter['__content__'] = body
    return frontmatter


def collect_markdown_files(content_dir: str, structure: StructureFormat) -> list[str]:
    md_files: list[str] = []
    for root, _, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                md_files.append(os.path.join(root, file))
    return md_files


def build_document_tree(
        md_files: list[str],
        content_dir: str,
        structure: StructureFormat,
    ) -> dict[str, dict[str, Any]]:
    docs: dict[str, dict[str, Any]] = {}

    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content: str = f.read()
        frontmatter: dict[str, Any] = parse_frontmatter(content)
        relative_path: str = os.path.relpath(file_path, content_dir)

        if structure == 'dotlist':
            key: str = os.path.splitext(relative_path.replace(os.sep, '.'))[0]
        elif structure == 'tree':
            key = os.path.splitext(relative_path)[0]
        else:
            key = os.path.splitext(relative_path)[0]

        docs[key] = frontmatter
    return docs


def get_parent_keys(
        key: str,
        structure: StructureFormat,
    ) -> list[str]:
    if structure == 'dotlist':
        parts: list[str] = key.split('.')
        return ['.'.join(parts[:i]) for i in range(1, len(parts))]
    elif structure == 'tree':
        parts: list[str] = key.split(os.sep)
        return [os.path.join(*parts[:i]) for i in range(1, len(parts))]
    else:
        return []


def merge_frontmatter(
    docs: dict[str, dict[str, Any]],
    key: str,
    globals_dict: dict[str, Any],
    structure: str
) -> dict[str, Any]:
    combined: dict[str, Any] = {}
    parent_keys: list[str] = get_parent_keys(key, structure)

    # Merge parent frontmatter from root to immediate parent
    for parent_key in parent_keys:
        parent_doc: dict[str, Any] = docs.get(parent_key, {})
        combined.update(parent_doc)

    # Merge current document's frontmatter
    current_doc: dict[str, Any] = docs.get(key, {})
    combined.update(current_doc)

    # Merge global variables
    combined.update(globals_dict)
    return combined


def execute_template(
        content: str,
        context: dict[str, Any],
        jinja_env: Environment,
    ) -> str:
    template: Template = jinja_env.from_string(content)
    return template.render(context)

def pandoc_render_md(content: str) -> str:
    pass

def process_markdown_files(
    docs: dict[str, dict[str, Any]],
    globals_dict: dict[str, Any],
    structure: str
) -> None:
    for key in docs.keys():
        context: dict[str, Any] = merge_frontmatter(docs, key, globals_dict, structure)
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
    content_dir: str = config.content_dir
    resources_dir: str = config.resources_dir
    structure: str = config.structure
    globals_dict: dict[str, Any] = config.__globals__

    md_files: list[str] = collect_markdown_files(content_dir, structure)
    docs: dict[str, dict[str, Any]] = build_document_tree(md_files, content_dir, structure)
    process_markdown_files(docs, globals_dict, structure)


if __name__ == "__main__":
    main()
