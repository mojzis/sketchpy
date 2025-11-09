# Changelog

All notable changes to sketchpy will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-11-09

### Added
- Initial release of sketchpy
- Core `Canvas` class with SVG rendering
- Basic shapes: `circle()`, `rect()`, `ellipse()`, `line()`, `polygon()`, `text()`, `rounded_rect()`
- Organic shapes: `blob()`, `tentacle()`, `wave()`
- Gradient support: `linear_gradient()`, `radial_gradient()`
- Shape grouping with transformations: `group()`, `move_group()`, `rotate_group()`, `hide_group()`
- Security limits for browser safety (max dimensions, max shapes)
- Color palettes:
  - `Color`: Basic 12-color palette
  - `CalmOasisPalette`: 12 calming blues/greens
  - `CreativeGardenPalette`: 12 pastel creative colors
  - `MathDoodlingPalette`: Triadic palette for geometric patterns
  - `OceanPalette`: Ocean-themed colors
- Helper classes:
  - `CarShapes`: Pre-built car, wheel, traffic light, road shapes
  - `OceanShapes`: Pre-built octopus, jellyfish, seaweed shapes
- Utility functions:
  - `grid()`: Coordinate grid overlay for learning
  - `show_palette()`: Visual palette display
  - `quick_draw()`: Fast canvas creation
- Browser compatibility via Pyodide
- Marimo/Jupyter notebook support via `_repr_html_()`
- Method chaining for fluent API
- Zero external dependencies (pure Python)
- Examples:
  - Basic shapes (house scene)
  - Organic shapes demo
  - Ocean scene with helpers
  - Math doodling patterns
  - Convex blobs demo
  - Ocean primitives

### Technical
- Python 3.9+ support
- MIT License
- Modular architecture (canvas, palettes, helpers, utils)
- Comprehensive test suite (Python + JavaScript)

[0.1.0]: https://github.com/mojzis/sketchpy/releases/tag/v0.1.0
