#!/usr/bin/env python3
"""Build script to generate index.html from template with embedded shapes.py code."""

import re
import logging
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Use parent logger from srv.py when imported, or configure if run standalone
logger = logging.getLogger(__name__)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S')


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

    # Remove type hints from function signatures for cleaner browser code
    # Handle nested brackets properly (e.g., List[Tuple[float, float]])
    # Using a regex that handles one level of nesting
    processed_code = re.sub(r': (List|Tuple|Optional)\[([^\[\]]+|\[[^\]]*\])*\]', '', processed_code)
    # Remove simple type hints
    processed_code = re.sub(r': (float|int|str|bool)', '', processed_code)
    # Remove return type annotations
    processed_code = re.sub(r' -> [\'"]?Canvas[\'"]?', '', processed_code)
    processed_code = re.sub(r' -> (str|None)', '', processed_code)

    return processed_code.strip()


def main():
    """Generate index.html from template."""
    # Setup paths
    project_root = Path(__file__).parent.parent
    shapes_path = project_root / 'sketchpy' / 'shapes.py'
    templates_dir = project_root / 'templates'
    output_dir = project_root / 'output'
    output_file = output_dir / 'index.html'

    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)

    # Process shapes.py code
    shapes_code = process_shapes_code(shapes_path)

    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template('index.html.jinja')

    # Render template
    html_content = template.render(shapes_code=shapes_code)

    # Write output
    output_file.write_text(html_content)

    logger.info(f"🔨 Built output/index.html ({len(html_content)} bytes)")


if __name__ == '__main__':
    main()
