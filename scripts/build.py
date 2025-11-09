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
from datetime import datetime
from jinja2 import Environment, FileSystemLoader

# Base path configuration for deployment
# Use '/sketchpy' for GitHub Pages, '' for local development or custom domain
BASE_PATH = '/sketchpy'

# Generate build timestamp for cache busting
BUILD_VERSION = datetime.now().strftime('%Y%m%d%H%M%S')

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


def process_shapes_code(sketchpy_dir: Path) -> str:
    """
    Combine modular sketchpy code for embedding in Pyodide.

    Reads from modular structure:
    - palettes.py: Color classes
    - canvas.py: Canvas with all drawing methods
    - helpers/ocean.py: OceanShapes class
    - helpers/cars.py: CarShapes class

    Combines them into single browser-ready bundle, removing:
    - Import statements (modules will be in same scope)
    - Type hints (browser doesn't need them)
    - save() method (file I/O not supported)
    - Docstrings at module level
    """
    modules_to_include = [
        sketchpy_dir / 'palettes.py',
        sketchpy_dir / 'canvas.py',
        sketchpy_dir / 'helpers' / 'ocean.py',
        sketchpy_dir / 'helpers' / 'cars.py',
    ]

    combined_parts = []

    for module_path in modules_to_include:
        if not module_path.exists():
            logger.warning(f"Module not found: {module_path}")
            continue

        code = module_path.read_text()

        # Remove module-level docstrings at the top
        code = re.sub(r'^""".*?"""', '', code, flags=re.DOTALL | re.MULTILINE).lstrip()

        # Remove all import statements (modules will be combined)
        lines = code.split('\n')
        filtered_lines = []
        skip_until_blank = False

        for line in lines:
            # Skip import statements
            if line.startswith('from ') or line.startswith('import '):
                continue

            # Skip try/except import blocks
            if line.strip().startswith('try:') or line.strip().startswith('except ImportError:'):
                skip_until_blank = True
                continue

            # Skip the save() method (file I/O not needed in browser)
            if 'def save(self' in line:
                skip_until_blank = True
                continue

            if skip_until_blank:
                # End of import block or save method
                if line.strip() == '' or (line and not line[0].isspace() and line.strip() and not line.strip().startswith('pass')):
                    skip_until_blank = False
                    # Don't include the line that ends the block if it's 'pass'
                    if line.strip() == 'pass':
                        continue
                continue

            filtered_lines.append(line)

        module_code = '\n'.join(filtered_lines)
        combined_parts.append(module_code)

    # Combine all modules
    combined_code = '\n\n'.join(combined_parts)

    # Clean up excessive blank lines
    combined_code = re.sub(r'\n\n\n+', '\n\n', combined_code)

    # Remove type hints using iterative regex approach
    combined_code = remove_type_hints_simple(combined_code)

    # Remove ALL return type annotations (these use ` ->` which is easier to match)
    # This catches all remaining types including List, Tuple, Dict, etc.
    # Pattern matches from " ->" to the ":" at the end of function signatures
    combined_code = re.sub(r' ->[^:]+:', ':', combined_code)

    return combined_code.strip()


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
    """Load and process lesson content from theme directories."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.themes_dir = project_root / 'themes'
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

    def load_themes_config(self):
        """Auto-generate themes config by discovering theme directories."""
        # Find all theme directories
        theme_dirs = sorted([
            d for d in self.themes_dir.iterdir()
            if d.is_dir() and d.name.startswith('theme-')
        ])

        themes = []
        for theme_dir in theme_dirs:
            theme_yaml_path = theme_dir / 'theme.yaml'
            if not theme_yaml_path.exists():
                logger.warning(f"Skipping {theme_dir.name}: no theme.yaml found")
                continue

            # Load theme metadata
            with open(theme_yaml_path) as f:
                theme_meta = yaml.safe_load(f)

            # Find all lesson directories in this theme
            lesson_dirs = sorted([
                d for d in theme_dir.iterdir()
                if d.is_dir() and d.name[0].isdigit()
            ])

            lessons = []
            for lesson_dir in lesson_dirs:
                lesson_id = lesson_dir.name

                # Extract metadata from lesson.md
                lesson_md_path = lesson_dir / 'lesson.md'
                if not lesson_md_path.exists():
                    logger.warning(f"Skipping {theme_dir.name}/{lesson_id}: no lesson.md found")
                    continue

                # Parse the markdown to extract title and description
                lesson_md = lesson_md_path.read_text()
                lines = lesson_md.split('\n')

                # Find title (first heading of any level)
                title = None
                for line in lines:
                    if line.startswith('#'):
                        # Remove all # symbols and extract title
                        title = re.sub(r'^#+\s*', '', line).strip()
                        # Remove leading emoji if present
                        title = re.sub(r'^[^\w\s]+\s*', '', title)
                        break

                if not title:
                    logger.warning(f"Skipping {theme_dir.name}/{lesson_id}: no title found in lesson.md")
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
                    'duration': duration,
                    'theme_id': theme_meta['id']
                })

            # Add theme with its lessons
            themes.append({
                'id': theme_meta['id'],
                'name': theme_meta['name'],
                'description': theme_meta['description'],
                'icon': theme_meta.get('icon', '📚'),
                'lessons': lessons
            })

        return {'themes': themes}

    def load_lesson_content(self, theme_id: str, lesson_id: str):
        """Load lesson markdown, starter code, and optional help."""
        lesson_dir = self.themes_dir / theme_id / lesson_id

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


def copy_js_with_timestamp(static_dir: Path, output_dir: Path, timestamp: str):
    """
    Copy JavaScript files from static/js/ to output/static/js/ with timestamp.

    Replaces .dev.js with .{timestamp}.js in:
    - Filenames
    - Import statements inside files

    Returns mapping of original to timestamped filenames for logging.
    """
    js_source = static_dir / 'js'
    js_output = output_dir / 'js'

    if not js_source.exists():
        logger.warning("No static/js directory found")
        return {}

    # Clean old timestamped JS files to prevent accumulation
    if js_output.exists():
        logger.info(f"  Cleaning old JavaScript files from output/static/js/")
        shutil.rmtree(js_output)
    js_output.mkdir(parents=True, exist_ok=True)

    mapping = {}

    # Find all .dev.js files
    for js_file in js_source.rglob('*.dev.js'):
        # Calculate relative path from js_source
        rel_path = js_file.relative_to(js_source)

        # Create timestamped filename
        new_name = js_file.name.replace('.dev.js', f'.{timestamp}.js')
        dest_file = js_output / rel_path.parent / new_name

        # Ensure destination directory exists
        dest_file.parent.mkdir(parents=True, exist_ok=True)

        # Read file content
        content = js_file.read_text()

        # Replace all .dev.js references with timestamped version
        content = content.replace('.dev.js', f'.{timestamp}.js')

        # Write to destination
        dest_file.write_text(content)

        # Track mapping for logging
        mapping[str(rel_path)] = new_name

    return mapping


def build_lessons(project_root: Path, shapes_code: str):
    """Build individual lesson pages for all themes."""
    loader = LessonLoader(project_root)
    themes_config = loader.load_themes_config()

    templates_dir = project_root / 'templates'
    output_dir = project_root / 'output'

    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(templates_dir))

    # Build each lesson across all themes
    all_lessons = []
    all_themes_metadata = []

    for theme in themes_config['themes']:
        theme_id = theme['id']
        logger.info(f"  Building theme: {theme['name']} ({theme_id})")

        # Save theme metadata (without lessons to avoid duplication)
        all_themes_metadata.append({
            'id': theme['id'],
            'name': theme['name'],
            'description': theme['description'],
            'icon': theme['icon']
        })

        for lesson_meta in theme['lessons']:
            lesson_id = lesson_meta['id']
            logger.info(f"    Building lesson: {theme_id}/{lesson_id}")

            # Load lesson content
            content = loader.load_lesson_content(theme_id, lesson_id)

            # Merge metadata and content
            lesson_data = {**lesson_meta, **content}
            all_lessons.append(lesson_data)

            # Render lesson page
            template = env.get_template('lesson.html.jinja')
            html = template.render(
                lesson=lesson_data,
                current_theme=theme,
                all_themes=themes_config['themes'],
                shapes_code=shapes_code,
                base_path=BASE_PATH,
                build_version=BUILD_VERSION
            )

            # Write output to theme-specific directory
            lesson_path = output_dir / 'lessons' / theme_id / f"{lesson_id}.html"
            lesson_path.parent.mkdir(parents=True, exist_ok=True)
            lesson_path.write_text(html)
            logger.info(f"      → lessons/{theme_id}/{lesson_id}.html ({len(html)} bytes)")

    # Write lessons.json for client-side use
    lessons_json_path = output_dir / 'static' / 'data' / 'lessons.json'
    lessons_json_path.parent.mkdir(parents=True, exist_ok=True)
    lessons_json_path.write_text(json.dumps(all_lessons, indent=2))
    logger.info(f"  → static/data/lessons.json")

    # Write themes.json for client-side use
    themes_json_path = output_dir / 'static' / 'data' / 'themes.json'
    themes_json_path.parent.mkdir(parents=True, exist_ok=True)
    themes_json_path.write_text(json.dumps(themes_config['themes'], indent=2))
    logger.info(f"  → static/data/themes.json")

    # Copy static files (js, css, etc.) to output
    static_src = project_root / 'static'
    static_dest = output_dir / 'static'
    if static_src.exists():
        # Copy static files, but skip the data directory (we just created it)
        # and skip js directory (we'll handle that separately with timestamps)
        for item in static_src.iterdir():
            if item.name not in ('data', 'js'):
                dest = static_dest / item.name
                if item.is_dir():
                    shutil.copytree(item, dest, dirs_exist_ok=True)
                else:
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest)
        logger.info(f"  → static/ files copied")

        # Copy JS files with timestamp
        logger.info(f"  Copying JavaScript with timestamp: {BUILD_VERSION}")
        js_mapping = copy_js_with_timestamp(static_src, static_dest, BUILD_VERSION)
        for orig, timestamped in js_mapping.items():
            logger.info(f"    {orig} → {timestamped}")

    return themes_config


def main():
    """Generate index.html from template."""
    # Setup paths
    project_root = Path(__file__).parent.parent
    sketchpy_dir = project_root / 'sketchpy'
    templates_dir = project_root / 'templates'
    output_dir = project_root / 'output'

    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)

    # Combine modular sketchpy code for browser
    shapes_code = process_shapes_code(sketchpy_dir)

    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(templates_dir))

    # Build old single-page version (keep as fallback for now)
    # template = env.get_template('index.html.jinja')
    # html_content = template.render(shapes_code=shapes_code)
    # output_file = output_dir / 'index.html'
    # output_file.write_text(html_content)
    # logger.info(f"🔨 Built output/index.html ({len(html_content)} bytes)")

    # Build new multi-theme lesson version
    themes_config = build_lessons(project_root, shapes_code)

    # Load and execute snippets
    logger.info("Loading snippets...")
    snippets = load_snippets(project_root)
    logger.info(f"  Loaded {len(snippets)} snippets")

    # Build landing page
    logger.info("Building landing page...")
    index_template = env.get_template('index.html.jinja')
    index_html = index_template.render(
        all_themes=themes_config['themes'],
        snippets=snippets,
        base_path=BASE_PATH,
        build_version=BUILD_VERSION
    )
    index_path = output_dir / 'index.html'
    index_path.write_text(index_html)
    logger.info(f"  → index.html ({len(index_html)} bytes)")

    logger.info("✅ Build complete!")


if __name__ == '__main__':
    main()
