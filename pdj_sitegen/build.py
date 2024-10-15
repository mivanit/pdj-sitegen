"""Build a site from markdown files using Jinja2 and Pandoc

Pipeline:

- Get all markdown files
- For each markdown file:
    - Regex frontmatter and content from the markdown file
    - Execute a template on the frontmatter, with globals_ and file metadata as context
    - Load the frontmatter into a dict
    - Execute a template on the content with frontmatter, globals_ and file metadata as context
    - Convert the content to HTML using Pandoc
    - Execute a template on the specified or default template with the HTML content, frontmatter, globals_ and file metadata as context
"""

import os
import re
import json
import yaml
import tomllib
import subprocess
import sys
from pathlib import Path

from muutils.json_serialize import SerializableDataclass, serializable_dataclass, serializable_field
from muutils.dictmagic import dotlist_to_nested_dict, update_with_nested_dict, kwargs_to_nested_dict
from typing import Any, Literal, Optional, Callable, Tuple, Dict
from jinja2 import Environment, FileSystemLoader, Template

Format = Literal['yaml', 'json', 'toml']

StructureFormat = Literal['dotlist', 'tree']

FORMAT_MAP: Dict[str, Format] = {
    'yaml': 'yaml',
    'yml': 'yaml',
    'json': 'json',
    'toml': 'toml'
}

FRONTMATTER_PARSERS: Dict[str, Callable[[str], Dict[str, Any]]] = {
    '---': lambda x: yaml.safe_load(x),
    ';;;': lambda x: json.loads(x),
    '+++': lambda x: tomllib.loads(x),
}

FRONTMATTER_REGEX: re.Pattern = re.compile(
    r'^(?P<delimiter>{delims})\n(?P<frontmatter>.*?)\n(?P=delimiter)\n(?P<body>.*)'.format(
        delims='|'.join([
            re.escape(d) for d in
            FRONTMATTER_PARSERS.keys()
        ]),
    ),
    re.DOTALL
)


def read_data_file(file_path: Path, fmt: Optional[Format] = None) -> Dict[str, Any]:
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
            with open(file_path, 'rb') as f:
                return tomllib.load(f)
        case _:
            raise ValueError(f"Unsupported format: {fmt}")
            

def emit_data_file(data: Dict[str, Any], fmt: Format) -> str:
    match fmt:
        case 'yaml':
            return yaml.safe_dump(data)
        case 'json':
            return json.dumps(data, indent='\t')
        case 'toml':
            raise NotImplementedError("Saving to TOML is not implemented.")
        case _:
            raise ValueError(f"Unsupported format: {fmt}")

def save_data_file(data: Dict[str, Any], file_path: Path, fmt: Optional[Format] = None) -> None:
    if fmt is None:
        fmt = FORMAT_MAP[file_path.suffix.lstrip('.')]
    
    emitted_data: str = emit_data_file(data, fmt)
    with open(file_path, 'w') as f:
        f.write(emitted_data)

_PATH_FIELD_SERIALIZATION_KWARGS: Dict[str, Callable] = dict(
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
        default=Path('default.html.jinja2'),
        **_PATH_FIELD_SERIALIZATION_KWARGS,
    )
    output_dir: Path = serializable_field(
        default=Path('output'),
        **_PATH_FIELD_SERIALIZATION_KWARGS,
    )
    jinja_env_kwargs: Dict[str, Any] = serializable_field(
        default_factory=dict,
    )
    structure: StructureFormat = serializable_field(
        default='dotlist',
        assert_type=False,
    )
    globals_: Dict[str, Any] = serializable_field(
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
    def read(cls, config_path: Path, fmt: Optional[Format] = None) -> 'Config':
        return cls.load(read_data_file(config_path, fmt))
    
    def as_str(self, fmt: Format) -> str:
        return emit_data_file(self.serialize(), fmt)

    def save(self, config_path: Path, fmt: Optional[Format] = 'json') -> None:
        save_data_file(self.serialize(), config_path, fmt)


def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    match: Optional[re.Match[str]] = re.match(FRONTMATTER_REGEX, content)
    if match:
        delimiter: str = match.group('delimiter')
        frontmatter_raw: str = match.group('frontmatter')
        body: str = match.group('body')

        parser: Optional[Callable[[str], Dict[str, Any]]] = FRONTMATTER_PARSERS.get(delimiter, None)
        frontmatter: Dict[str, Any] = parser(frontmatter_raw) if parser else {}
    else:
        frontmatter = {}
        body = content

    return frontmatter, body


def collect_markdown_files(content_dir: str) -> list[str]:
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
    ) -> Dict[str, Dict[str, Any]]:
    docs: Dict[str, Dict[str, Any]] = {}

    for file_path in md_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content: str = f.read()
        frontmatter, body = parse_frontmatter(content)
        relative_path: str = os.path.relpath(file_path, content_dir)

        if structure == 'dotlist':
            key: str = os.path.splitext(relative_path.replace(os.sep, '.'))[0]
        elif structure == 'tree':
            key = os.path.splitext(relative_path)[0]
        else:
            key = os.path.splitext(relative_path)[0]

        file_metadata: Dict[str, Any] = {
            'file_path': file_path,
            'relative_path': relative_path,
            'modified_time': os.path.getmtime(file_path),
            'key': key,
        }

        docs[key] = {
            'frontmatter': frontmatter,
            'body': body,
            'file_metadata': file_metadata,
        }
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
    docs: Dict[str, Dict[str, Any]],
    key: str,
    globals_dict: Dict[str, Any],
    structure: StructureFormat
) -> Dict[str, Any]:
    combined: Dict[str, Any] = {}
    parent_keys: list[str] = get_parent_keys(key, structure)

    # Merge parent frontmatter from root to immediate parent
    for parent_key in parent_keys:
        parent_doc = docs.get(parent_key, {})
        parent_frontmatter = parent_doc.get('frontmatter', {})
        combined.update(parent_frontmatter)

    # Merge current document's frontmatter
    current_doc = docs.get(key, {})
    current_frontmatter = current_doc.get('frontmatter', {})
    combined.update(current_frontmatter)

    # Merge global variables
    combined.update(globals_dict)
    return combined


def render_frontmatter(
    frontmatter: Dict[str, Any],
    context: Dict[str, Any],
    jinja_env: Environment
) -> Dict[str, Any]:
    def render_value(value: Any) -> Any:
        if isinstance(value, str):
            template = jinja_env.from_string(value)
            return template.render(context)
        elif isinstance(value, dict):
            return {k: render_value(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [render_value(item) for item in value]
        else:
            return value

    return {k: render_value(v) for k, v in frontmatter.items()}


def execute_template(
        content: str,
        context: Dict[str, Any],
        jinja_env: Environment,
    ) -> str:
    template: Template = jinja_env.from_string(content)
    return template.render(context)


def pandoc_render_md(
    content: str,
    fmt_from: str,
    fmt_to: str,
    extra_args: list[str],
) -> str:
    cmd = ['pandoc', '-f', fmt_from, '-t', fmt_to] + extra_args
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = process.communicate(input=content)
    if process.returncode != 0:
        raise Exception(f"Pandoc failed: {stderr}")
    return stdout


def process_markdown_files(
    docs: Dict[str, Dict[str, Any]],
    globals_dict: Dict[str, Any],
    structure: StructureFormat,
    jinja_env: Environment,
    config: Config,
) -> None:
    for key in docs.keys():
        doc = docs[key]
        frontmatter = doc.get('frontmatter', {})
        body = doc.get('body', '')
        file_metadata = doc.get('file_metadata', {})

        # Build initial context
        context = merge_frontmatter(docs, key, globals_dict, structure)
        # Include file metadata in context
        context.update(file_metadata)

        # Render frontmatter templates
        frontmatter = render_frontmatter(frontmatter, context, jinja_env)
        context.update(frontmatter)

        # Now, execute a template on the content with context
        # Render Markdown content with Jinja2
        rendered_md: str = execute_template(body, context, jinja_env)

        # Convert Markdown to HTML using Pandoc
        html_content: str = pandoc_render_md(
            rendered_md,
            config.pandoc_fmt_from,
            config.pandoc_fmt_to,
            config.pandoc_cli_extra_args,
        )
        context['content'] = html_content

        # Determine which HTML template to use
        template_name: str = frontmatter.get(
            '__template__',
            config.default_template.as_posix(),
        )
        if not template_name:
            raise Exception(f"No HTML template specified for {key}.")

        # Render final HTML
        template = jinja_env.get_template(template_name)
        final_html: str = template.render(context)

        # Output HTML file
        output_dir = str(config.output_dir)
        relative_output_path = file_metadata.get('relative_path', '').replace('.md', '.html')
        output_path = os.path.join(output_dir, relative_output_path)
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(final_html)
        print(f"Generated {output_path}")


def main() -> None:
    import sys
    from muutils.dictmagic import dotlist_to_nested_dict, update_with_nested_dict, kwargs_to_nested_dict

    # First arg is config path; subsequent args are key-value pairs for config
    args = sys.argv[1:]

    if len(args) >= 1 and not args[0].startswith('--'):
        config_path = Path(args[0])
        kv_args = args[1:]
    else:
        config_path = Path('config.yaml')
        kv_args = args

    # Read the config file
    config: Config = Config.read(config_path)

    # Parse key-value pairs from command line arguments
    # Assuming the format is key=value
    kwargs_dict: Dict[str, Any] = {}
    for arg in kv_args:
        if '=' in arg:
            key, value = arg.split('=', 1)
            # Try to parse the value using yaml.safe_load
            try:
                value = yaml.safe_load(value)
            except yaml.YAMLError:
                pass  # Keep value as string if parsing fails
            kwargs_dict[key] = value
        else:
            print(f"Invalid argument format: {arg}")
            sys.exit(1)

    # Convert flat kwargs_dict to nested dict
    nested_kwargs = kwargs_to_nested_dict(kwargs_dict)

    # Update the config with nested kwargs
    config_dict = config.serialize()
    update_with_nested_dict(config_dict, nested_kwargs)
    # Deserialize back to config object
    config = Config.load(config_dict)

    content_dir: Path = config.content_dir
    resources_dir: Path = config.resources_dir
    structure: StructureFormat = config.structure
    globals_dict: Dict[str, Any] = config.globals_

    md_files: list[str] = collect_markdown_files(str(content_dir))
    docs: Dict[str, Dict[str, Any]] = build_document_tree(md_files, str(content_dir), structure)

    # Set up Jinja2 environment
    jinja_env = Environment(
        loader=FileSystemLoader([config.templates_dir]),
        **config.jinja_env_kwargs,
    )

    process_markdown_files(docs, globals_dict, structure, jinja_env, config)


if __name__ == "__main__":
    main()
