# Themes Directory

This directory contains different themed learning paths for sketchpy. Each theme provides a unique set of lessons organized around a central motif or concept.

## Structure

```
themes/
├── theme-1/          # Creative Garden theme
│   ├── theme.yaml    # Theme metadata
│   └── 01-*/         # Lesson directories
├── theme-2/          # Space Explorer theme
│   ├── theme.yaml    # Theme metadata
│   └── 01-*/         # Lesson directories (when created)
└── README.md         # This file
```

## Theme Metadata (theme.yaml)

Each theme directory must contain a `theme.yaml` file with the following structure:

```yaml
id: theme-1                    # Unique identifier (must match directory name)
name: Creative Garden          # Display name shown in UI
description: Learn Python...   # Brief description of theme's learning approach
icon: "🌸"                     # Emoji icon for theme selector
colors:                        # Optional: Theme color scheme
  primary: "#2C5F7C"
  accent: "#FF6B6B"
```

## Lesson Organization

Within each theme, lessons follow the same structure as before:

```
01-lesson-name/
├── lesson.md       # Lesson instructions
├── starter.py      # Starting code
└── help.md         # Optional hints
```

The build script automatically discovers all lessons in each theme and groups them by theme in the UI.

## Creating a New Theme

1. Create a new directory: `themes/theme-N/`
2. Add a `theme.yaml` file with metadata
3. Create lesson directories following the `NN-lesson-name/` pattern
4. Run `uv run build` to regenerate the site

## Current Themes

### Theme 1: Creative Garden 🌸
Learn Python through drawing colorful flowers, gardens, and geometric patterns. This theme uses nature-inspired visuals to teach fundamental programming concepts.

**Lessons:** 15 lessons covering variables, loops, functions, and more.

### Theme 2: Space Explorer 🚀
Discover Python by creating rockets, planets, and cosmic adventures. (Coming soon - ready for content)

**Lessons:** To be created.

## Design Notes

- Each theme should maintain consistent difficulty progression (beginner → intermediate → advanced)
- Themes can have different numbers of lessons
- The theme selector appears before the lesson selector in the UI
- Lessons within a theme are numbered independently (01, 02, 03...)
- Theme colors in `theme.yaml` are reserved for future UI customization
