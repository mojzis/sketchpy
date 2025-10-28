#!/usr/bin/env python3
"""Update the if __name__ block in all starter.py files."""

from pathlib import Path
import re


def update_starter_file(file_path: Path):
    """Update the if __name__ block to use debug_out directory and lesson number."""
    code = file_path.read_text()

    # Extract lesson number from directory name (e.g., "01" from "01-first-flower")
    lesson_dir = file_path.parent.name
    lesson_num = lesson_dir.split('-')[0]

    # Find and replace the if __name__ block
    # Match the entire block including any following lines
    pattern = r"if __name__ == '__main__':\n    canvas = main\(\)\n(?:.*\n)*"
    replacement = f"""if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-{lesson_num}.svg')
"""

    new_code = re.sub(pattern, replacement, code)

    # Write back
    file_path.write_text(new_code)
    print(f"  ✓ Updated {file_path.parent.name}")


def main():
    """Update all starter.py files."""
    project_root = Path(__file__).parent.parent
    lessons_dir = project_root / 'lessons'

    starter_files = sorted(lessons_dir.glob('*/starter.py'))

    print(f"Updating {len(starter_files)} starter.py files\n")

    for starter_file in starter_files:
        update_starter_file(starter_file)

    print(f"\n✅ Update complete!")


if __name__ == '__main__':
    main()
