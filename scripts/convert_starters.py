#!/usr/bin/env python3
"""Convert all starter.py files to include imports, main function, and if __name__ block."""

import re
from pathlib import Path


def get_required_imports(code: str) -> list[str]:
    """Detect which imports are needed based on the code content."""
    imports = ['Canvas']

    # Check for Color usage
    if 'Color.' in code or 'fill=Color' in code:
        imports.append('Color')

    # Check for CreativeGardenPalette usage
    if 'CreativeGardenPalette.' in code:
        imports.append('CreativeGardenPalette')

    # Check for CalmOasisPalette usage
    if 'CalmOasisPalette.' in code:
        imports.append('CalmOasisPalette')

    return imports


def convert_starter_file(file_path: Path):
    """Convert a starter.py file to the new format."""
    code = file_path.read_text()

    # Skip if already converted
    if 'def main():' in code:
        print(f"  Skipping {file_path.name} (already converted)")
        return

    # Remove trailing 'can' if present (last line)
    lines = code.strip().split('\n')
    if lines and lines[-1].strip() == 'can':
        lines = lines[:-1]
    code = '\n'.join(lines).strip()

    # Detect required imports
    imports = get_required_imports(code)
    import_line = f"from sketchpy.shapes import {', '.join(imports)}"

    # Indent all code by 4 spaces
    indented_code = '\n'.join('    ' + line if line.strip() else '' for line in code.split('\n'))

    # Build new file content
    new_content = f"""{import_line}


def main():
{indented_code}

    return can


if __name__ == '__main__':
    canvas = main()
    canvas.save('output.svg')
    print("Saved to output.svg")
"""

    # Write the new content
    file_path.write_text(new_content)
    print(f"  ✓ Converted {file_path.name}")


def main():
    """Convert all starter.py files in the lessons directory."""
    project_root = Path(__file__).parent.parent
    lessons_dir = project_root / 'lessons'

    starter_files = sorted(lessons_dir.glob('*/starter.py'))

    print(f"Found {len(starter_files)} starter.py files to convert\n")

    for starter_file in starter_files:
        convert_starter_file(starter_file)

    print(f"\n✅ Conversion complete!")


if __name__ == '__main__':
    main()
