#!/usr/bin/env python3
"""Build script to generate index.html from template with embedded shapes.py code."""

import re
import logging
import yaml
import markdown
import json
import shutil
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Base path configuration for deployment
# Use '/sketchpy' for GitHub Pages, '' for local development or custom domain
BASE_PATH = '/sketchpy'

# Use parent logger from srv.py when imported, or configure if run standalone
logger = logging.getLogger(__name__)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')


def remove_type_hints_simple(code: str) -> str:
    """
    Remove Python type hints using a simple regex-based approach.
    Handles common types including Union, Optional, List, Tuple, Dict, etc.
    """
    # First, collapse nested generic types by removing innermost brackets iteratively
    # This converts Union[List[str], List[Tuple[str, float]], None] -> Union[List, List, None] -> Union
    for _ in range(5):  # Repeat to handle deep nesting
        before = code
        # Match innermost generic types (no brackets inside)
        code = re.sub(r'(List|Tuple|Optional|Union|Dict)\[([^\[\]]+)\]', r'\1', code)
        if code == before:  # No more changes
            break

    # Now remove all type hints (including the collapsed generics and simple types)
    code = re.sub(r': (List|Tuple|Optional|Union|Dict|float|int|str|bool|None)+', '', code)

    return code


def process_shapes_code(shapes_path: Path) -> str:
    """
    Read and process shapes.py for embedding in Pyodide.

    Removes browser-incompatible code like file I/O (save method).
    Keeps imports and display methods for marimo compatibility.
    """
    code = shapes_path.read_text()

    # Remove the docstring at the top
    code = re.sub(r'^""".*?"""', '', code, flags=re.DOTALL | re.MULTILINE).lstrip()

    # Process code line by line, keeping imports but removing browser-incompatible methods
    lines = code.split('\n')
    filtered_lines = []
    skip_until_blank = False

    for line in lines:
        # Skip unused imports
        if line.startswith('from dataclasses import') or line.startswith('from enum import'):
            continue

        # Skip the Point dataclass (not used, and breaks with type hint removal)
        if line.startswith('class Point:') or '@dataclass' in line:
            skip_until_blank = True
            continue

        # Skip the save() method (file I/O not needed in browser)
        if 'def save(self' in line:
            skip_until_blank = True
            continue

        # Skip CarShapes class and everything after (not needed for basic tutorial)
        if line.startswith('# Convenience functions') or line.startswith('def quick_draw'):
            break

        if line.startswith('# Higher-level car-themed shapes') or line.startswith('class CarShapes'):
            break

        if skip_until_blank:
            if line.strip() == '' or (line and not line[0].isspace() and line.strip()):
                skip_until_blank = False
            continue

        filtered_lines.append(line)

    processed_code = '\n'.join(filtered_lines)

    # Clean up excessive blank lines
    processed_code = re.sub(r'\n\n\n+', '\n\n', processed_code)

    # Remove type hints using iterative regex approach
    processed_code = remove_type_hints_simple(processed_code)

    # Remove return type annotations (these use ` ->` which is easier to match)
    processed_code = re.sub(r' -> [\'"]?Canvas[\'"]?', '', processed_code)
    processed_code = re.sub(r' -> (str|None)', '', processed_code)

    return processed_code.strip()


def execute_snippet(snippet_path: Path, project_root: Path):
    """
    Execute a Python snippet and capture the SVG output.

    Returns a dict with:
    - name: snippet name (without .py extension)
    - code: the Python code as a string
    - svg: the generated SVG output
    """
    # Read the snippet code
    code = snippet_path.read_text()

    # Temporarily add sketchpy to the path
    sys.path.insert(0, str(project_root))

    try:
        # Create a namespace for execution
        namespace = {}

        # Execute the code
        exec(code, namespace)

        # The snippet should have created a Canvas object assigned to 'can'
        # and the last line is 'can', which returns the canvas
        canvas = namespace.get('can')

        if canvas is None:
            logger.warning(f"Snippet {snippet_path.name} did not create a 'can' variable")
            return None

        # Get the SVG output
        svg = canvas.to_svg()

        # Extract just the filename without extension for the name
        name = snippet_path.stem

        return {
            'name': name,
            'code': code,
            'svg': svg
        }

    except Exception as e:
        logger.error(f"Error executing snippet {snippet_path.name}: {e}")
        return None
    finally:
        # Remove from path
        sys.path.pop(0)


def load_snippets(project_root: Path):
    """Load and execute all snippets from the snippets/ directory."""
    snippets_dir = project_root / 'snippets'

    if not snippets_dir.exists():
        logger.warning("No snippets directory found")
        return []

    snippets = []
    for snippet_file in sorted(snippets_dir.glob('*.py')):
        logger.info(f"  Executing snippet: {snippet_file.name}")
        result = execute_snippet(snippet_file, project_root)
        if result:
            snippets.append(result)

    return snippets


def extract_main_function_body(code: str) -> str:
    """
    Extract the body of the main() function from starter.py code.

    The starter.py files have this structure:
    - imports at the top
    - def main(): with the actual lesson code
    - if __name__ == '__main__': block at the bottom

    For the web editor, we only want the content inside main().
    """
    lines = code.split('\n')
    inside_main = False
    main_body_lines = []
    indent_level = None

    for line in lines:
        # Start capturing when we find "def main():"
        if line.strip().startswith('def main():'):
            inside_main = True
            continue

        # Stop when we hit the if __name__ block or a function at the same level
        if inside_main and line.strip().startswith('if __name__'):
            break

        # Stop if we hit another function definition at the same level
        if inside_main and line.strip().startswith('def ') and not line.startswith('    '):
            break

        # Capture lines inside main()
        if inside_main:
            # Detect the base indentation level from the first non-empty line
            if indent_level is None and line.strip():
                indent_level = len(line) - len(line.lstrip())

            # Remove the base indentation and add to result
            if line.strip():  # Non-empty line
                if line.startswith(' ' * indent_level):
                    main_body_lines.append(line[indent_level:])
                else:
                    main_body_lines.append(line)
            else:  # Empty line
                main_body_lines.append('')

    # Join and clean up
    result = '\n'.join(main_body_lines).strip()

    # Replace "return can" with just "can" for the browser
    result = re.sub(r'\n\s*return\s+can\s*$', '\ncan', result)

    return result


class LessonLoader:
    """Load and process lesson content from lesson directories."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.lessons_dir = project_root / 'lessons'
        self.md = markdown.Markdown(extensions=[
            'fenced_code',
            'tables',
            'codehilite'
        ], extension_configs={
            'codehilite': {
                'css_class': 'highlight',
                'linenums': False,
                'guess_lang': False
            }
        })

    def load_lessons_config(self):
        """Auto-generate lessons config from lesson directories."""
        # Find all lesson directories (format: NN-lesson-name)
        lesson_dirs = sorted([
            d for d in self.lessons_dir.iterdir()
            if d.is_dir() and d.name[0].isdigit()
        ])

        lessons = []
        for lesson_dir in lesson_dirs:
            lesson_id = lesson_dir.name

            # Extract metadata from lesson.md
            lesson_md_path = lesson_dir / 'lesson.md'
            if not lesson_md_path.exists():
                logger.warning(f"Skipping {lesson_id}: no lesson.md found")
                continue

            # Parse the markdown to extract title and description
            lesson_md = lesson_md_path.read_text()
            lines = lesson_md.split('\n')

            # Find title (first ## heading)
            title = None
            for line in lines:
                if line.startswith('## '):
                    # Remove emoji and extract title
                    title = line.replace('##', '').strip()
                    # Remove leading emoji if present
                    title = re.sub(r'^[^\w\s]+\s*', '', title)
                    break

            if not title:
                logger.warning(f"Skipping {lesson_id}: no title found in lesson.md")
                continue

            # Extract description from "Goal" section
            description = None
            for i, line in enumerate(lines):
                if line.strip() == '### Goal':
                    # Next non-empty line is the description
                    for j in range(i + 1, len(lines)):
                        if lines[j].strip():
                            description = lines[j].strip()
                            break
                    break

            if not description:
                description = "Learn new Python concepts through drawing"

            # Determine difficulty based on lesson number
            lesson_num = int(lesson_id.split('-')[0])
            if lesson_num <= 3:
                difficulty = 'beginner'
            elif lesson_num <= 10:
                difficulty = 'intermediate'
            else:
                difficulty = 'advanced'

            # Estimate duration (15 min for early lessons, 20-30 for later ones)
            duration = 15 if lesson_num <= 5 else (20 if lesson_num <= 10 else 25)

            lessons.append({
                'id': lesson_id,
                'title': title,
                'description': description,
                'difficulty': difficulty,
                'duration': duration
            })

        return {'lessons': lessons}

    def load_lesson_content(self, lesson_id: str):
        """Load lesson markdown, starter code, and optional help."""
        lesson_dir = self.lessons_dir / lesson_id

        content = {}

        # Required files
        content['instructions_html'] = self.md.convert(
            (lesson_dir / 'lesson.md').read_text()
        )

        # Load starter code and extract only the main() function body for the web editor
        starter_code_full = (lesson_dir / 'starter.py').read_text()
        content['starter_code'] = extract_main_function_body(starter_code_full)

        # Optional files
        help_file = lesson_dir / 'help.md'
        if help_file.exists():
            content['help_html'] = self.md.convert(help_file.read_text())
        else:
            content['help_html'] = '<p>No additional help available.</p>'

        return content


def build_lessons(project_root: Path, shapes_code: str):
    """Build individual lesson pages."""
    loader = LessonLoader(project_root)
    lessons_config = loader.load_lessons_config()

    templates_dir = project_root / 'templates'
    output_dir = project_root / 'output'

    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(templates_dir))

    # Build each lesson
    all_lessons = []
    for lesson_meta in lessons_config['lessons']:
        lesson_id = lesson_meta['id']
        logger.info(f"  Building lesson: {lesson_id}")

        # Load lesson content
        content = loader.load_lesson_content(lesson_id)

        # Merge metadata and content
        lesson_data = {**lesson_meta, **content}
        all_lessons.append(lesson_data)

        # Render lesson page
        template = env.get_template('lesson.html.jinja')
        html = template.render(
            lesson=lesson_data,
            all_lessons=lessons_config['lessons'],
            shapes_code=shapes_code,
            base_path=BASE_PATH
        )

        # Write output
        lesson_path = output_dir / 'lessons' / f"{lesson_id}.html"
        lesson_path.parent.mkdir(parents=True, exist_ok=True)
        lesson_path.write_text(html)
        logger.info(f"    → lessons/{lesson_id}.html ({len(html)} bytes)")

    # Write lessons.json for client-side use
    lessons_json_path = output_dir / 'static' / 'data' / 'lessons.json'
    lessons_json_path.parent.mkdir(parents=True, exist_ok=True)
    lessons_json_path.write_text(json.dumps(all_lessons, indent=2))
    logger.info(f"  → static/data/lessons.json")

    # Copy static files (js, css, etc.) to output
    static_src = project_root / 'static'
    static_dest = output_dir / 'static'
    if static_src.exists():
        # Copy static files, but skip the data directory (we just created it)
        for item in static_src.iterdir():
            if item.name != 'data':
                dest = static_dest / item.name
                if item.is_dir():
                    shutil.copytree(item, dest, dirs_exist_ok=True)
                else:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest)
        logger.info(f"  → static/ files copied")


def main():
    """Generate index.html from template."""
    # Setup paths
    project_root = Path(__file__).parent.parent
    shapes_path = project_root / 'sketchpy' / 'shapes.py'
    templates_dir = project_root / 'templates'
    output_dir = project_root / 'output'

    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)

    # Process shapes.py code
    shapes_code = process_shapes_code(shapes_path)

    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(templates_dir))

    # Build old single-page version (keep as fallback for now)
    # template = env.get_template('index.html.jinja')
    # html_content = template.render(shapes_code=shapes_code)
    # output_file = output_dir / 'index.html'
    # output_file.write_text(html_content)
    # logger.info(f"🔨 Built output/index.html ({len(html_content)} bytes)")

    # Build new multi-lesson version
    loader = LessonLoader(project_root)
    lessons_config = loader.load_lessons_config()
    build_lessons(project_root, shapes_code)

    # Load and execute snippets
    logger.info("Loading snippets...")
    snippets = load_snippets(project_root)
    logger.info(f"  Loaded {len(snippets)} snippets")

    # Build landing page
    logger.info("Building landing page...")
    index_template = env.get_template('index.html.jinja')
    index_html = index_template.render(
        all_lessons=lessons_config['lessons'],
        snippets=snippets,
        base_path=BASE_PATH
    )
    index_path = output_dir / 'index.html'
    index_path.write_text(index_html)
    logger.info(f"  → index.html ({len(index_html)} bytes)")

    logger.info("✅ Build complete!")


if __name__ == '__main__':
    main()
