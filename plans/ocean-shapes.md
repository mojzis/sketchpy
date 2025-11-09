# Implementation Plan: Ocean Shapes via Parametric Curves

## Overview

Add organic curve drawing capabilities to sketchpy through a layered approach:
1. **Parametric curve primitives** on Canvas (intuitive parameters, Bézier math hidden)
2. **OceanShapes helper class** built from primitives (instant gratification)
3. **OceanPalette** color constants

This lets kids engage at their skill level while maintaining the "clean, simple, powerful" philosophy.

## Design Philosophy

**Problem:** Raw Bézier curves (x1, y1, cx, cy, x2, y2) are mathematically intimidating. Kids need LLM to write them → no learning.

**Solution:** Abstract curves into meaningful operations:
- "Make a wave from here to there" not "Set control point at (234.7, 189.2)"
- Parameters describe *what* (curl, wobble) not *how* (control points)
- Graduation path: OceanShapes → Canvas primitives → (advanced: raw Bézier)

**Target audience:**
- Primary: Artistic 13-year-old who loves octopuses but is code-hesitant
- Secondary: Kids at different skill levels (composition vs. primitive use)

## Layer 1: Parametric Curve Primitives (Canvas methods)

Add to `Canvas` class in `sketchpy/shapes.py`:

### 1. `wave()` - Sine-like curve
```python
def wave(self, x1: float, y1: float, x2: float, y2: float,
         height: float = 20, waves: int = 1,
         stroke: Color = Color.BLACK, stroke_width: int = 2) -> 'Canvas':
    """
    Draw a wavy line from (x1, y1) to (x2, y2).

    Args:
        x1, y1: Start point
        x2, y2: End point
        height: Wave amplitude (peak-to-trough distance)
        waves: Number of complete wave cycles
        stroke: Line color
        stroke_width: Line thickness

    Returns:
        self (for method chaining)

    Examples:
        # Gentle ocean wave
        can.wave(0, 300, 800, 300, height=30, waves=3)

        # Choppy water
        can.wave(0, 400, 800, 420, height=10, waves=8)
    """
```

**Implementation:**
- Calculate angle from (x1,y1) to (x2,y2)
- Generate points along line with perpendicular sine displacement
- Use `polygon()` or line segments to draw (no fill, just stroke)
- Sample ~50 points per wave for smoothness

### 2. `tentacle()` - Tapered curved appendage
```python
def tentacle(self, x1: float, y1: float, x2: float, y2: float,
             curl: float = 0.0, thickness: float = 20,
             taper: float = 0.5, fill: Color = Color.PURPLE,
             stroke: Optional[Color] = None, stroke_width: int = 1) -> 'Canvas':
    """
    Draw an organic tentacle from (x1, y1) to (x2, y2).

    Args:
        x1, y1: Base/thick end
        x2, y2: Tip/thin end
        curl: How much it curves (-1 to 1, 0 = straight)
              Positive = curves right, negative = curves left
        thickness: Width at base
        taper: How much thinner at tip (0-1, where 1 = same width, 0 = point)
        fill: Tentacle color
        stroke: Optional outline color
        stroke_width: Outline thickness

    Returns:
        self (for method chaining)

    Examples:
        # Gentle curve to the right
        can.tentacle(400, 300, 300, 500, curl=0.3, thickness=30)

        # Tight curl to the left
        can.tentacle(400, 300, 500, 500, curl=-0.7, thickness=25)
    """
```

**Implementation:**
- Use cubic Bézier for centerline with control points offset perpendicular to line
- Curl parameter determines control point offset distance
- Generate outline by sampling centerline and offsetting perpendicular by thickness
- Thickness interpolates from base to tip (linear or cubic easing)
- Use `polygon()` to fill the shape
- Optionally stroke outline

### 3. `blob()` - Organic irregular circle
```python
def blob(self, x: float, y: float, radius: float = 50,
         wobble: float = 0.2, points: int = 8,
         fill: Color = Color.BLUE, stroke: Optional[Color] = None,
         stroke_width: int = 1) -> 'Canvas':
    """
    Draw an organic, irregular circle (like a cartoon cloud or octopus head).

    Args:
        x, y: Center point
        radius: Average radius
        wobble: How irregular (0-1, where 0 = perfect circle, 1 = very bumpy)
        points: Number of control points (more = smoother, fewer = bumpier)
        fill: Fill color
        stroke: Optional outline color
        stroke_width: Outline thickness

    Returns:
        self (for method chaining)

    Examples:
        # Smooth organic shape
        can.blob(400, 300, radius=100, wobble=0.2)

        # Very bumpy cloud
        can.blob(200, 150, radius=60, wobble=0.5, points=6)
    """
```

**Implementation:**
- Place `points` control points around circle at even angles
- Randomize each point's radius by ±(wobble * radius)
- Use quadratic Bézier curves between points (control point = midpoint of arc)
- Close the path
- Use `polygon()` for fill (or implement simple Path class if needed)

### 4. `curve()` - Simple arc (optional, for learning progression)
```python
def curve(self, x1: float, y1: float, x2: float, y2: float,
          bend: float = 0.0, stroke: Color = Color.BLACK,
          stroke_width: int = 2) -> 'Canvas':
    """
    Draw a smooth curve from (x1, y1) to (x2, y2).

    Args:
        x1, y1: Start point
        x2, y2: End point
        bend: How much to curve (-1 to 1, 0 = straight line)
              Positive = curves "outward", negative = curves "inward"
        stroke: Line color
        stroke_width: Line thickness

    Returns:
        self (for method chaining)

    Examples:
        # Gentle arc
        can.curve(100, 100, 300, 100, bend=0.3)

        # S-curve (use two curves)
        can.curve(100, 100, 200, 200, bend=0.5)
        can.curve(200, 200, 300, 100, bend=-0.5)
    """
```

**Implementation:**
- Quadratic Bézier with control point perpendicular to midpoint
- Bend parameter determines control point offset distance
- Simpler than tentacle (no taper, just stroke)

## Layer 2: OceanShapes Helper Class

Add after `Canvas` class in `sketchpy/shapes.py`:

```python
class OceanShapes:
    """Pre-built ocean creature helpers for educational use."""

    def __init__(self, canvas: Canvas):
        """Initialize with a Canvas instance."""
        self.canvas = canvas

    def octopus(self, x: float, y: float, size: float = 100,
                body_color: Color = OceanPalette.CORAL,
                eye_color: Color = Color.WHITE) -> 'OceanShapes':
        """
        Draw a cute octopus.

        Args:
            x, y: Center position
            size: Approximate size
            body_color: Main body color
            eye_color: Eye color

        Returns:
            self (for method chaining)

        Example:
            ocean = OceanShapes(can)
            ocean.octopus(400, 200, size=120, body_color=OceanPalette.PURPLE_CORAL)
        """
        # Implementation:
        # - blob() for head
        # - 8 tentacle() calls radiating from bottom
        # - 2 circles for eyes (white + black pupil)
        # - Maybe small circles for suction cups

    def jellyfish(self, x: float, y: float, size: float = 80,
                  body_color: Color = OceanPalette.TRANSLUCENT_BLUE,
                  tentacle_count: int = 6) -> 'OceanShapes':
        """
        Draw a jellyfish.

        Args:
            x, y: Center of bell (top)
            size: Bell diameter
            body_color: Bell color
            tentacle_count: Number of trailing tentacles

        Returns:
            self (for method chaining)
        """
        # Implementation:
        # - blob() for bell (slightly flattened)
        # - Multiple thin tentacle() calls hanging down with varying curl

    def seaweed(self, x: float, y: float, height: float = 150,
                sway: float = 0.3, color: Color = OceanPalette.KELP_GREEN) -> 'OceanShapes':
        """
        Draw swaying seaweed.

        Args:
            x, y: Base position (ocean floor)
            height: How tall
            sway: How much it curves (0-1)
            color: Seaweed color

        Returns:
            self (for method chaining)
        """
        # Implementation:
        # - tentacle() or curve() going upward with some curl
        # - Maybe add small leaf-like shapes along the stem

    def coral(self, x: float, y: float, size: float = 60,
              branches: int = 5, color: Color = OceanPalette.CORAL) -> 'OceanShapes':
        """
        Draw branching coral.

        Args:
            x, y: Base position
            size: Approximate size
            branches: Number of main branches
            color: Coral color

        Returns:
            self (for method chaining)
        """
        # Implementation:
        # - Recursive or iterative branching using tentacle()
        # - Each branch splits into 2-3 smaller branches
```

## Layer 3: OceanPalette

Add after other palette classes:

```python
class OceanPalette:
    """Ocean-themed color palette for sea creatures and underwater scenes."""

    # Blues and greens (water, seaweed)
    DEEP_OCEAN = "#0A2E4D"      # Dark blue depths
    OCEAN_BLUE = "#1E5A8E"      # Medium ocean blue
    SHALLOW_WATER = "#4A90C8"   # Light blue shallows
    SEAFOAM = "#88C7DC"         # Pale blue-green foam
    KELP_GREEN = "#2D5C3F"      # Dark seaweed green
    SEA_GREEN = "#4A8B6F"       # Medium aqua green

    # Creature colors (octopus, fish, coral)
    CORAL = "#E8695C"           # Coral/salmon pink
    PURPLE_CORAL = "#A27BA2"    # Purple octopus
    STARFISH_ORANGE = "#F4A460" # Sandy orange
    TROPICAL_YELLOW = "#FFD966" # Bright yellow fish

    # Accents
    SAND = "#D4C5A9"            # Sandy ocean floor
    SHELL_WHITE = "#F5F1E8"     # Pale shell/pearl

    # Special (semi-transparent concept, rendered as light version)
    TRANSLUCENT_BLUE = "#A8D8EA"  # Light blue for jellyfish
```

## Implementation Strategy

### Phase 1: Parametric Primitives (Focus: `wave`, `tentacle`, `blob`)
1. Add helper function `_bezier_points()` to generate curve sample points
2. Implement `wave()` - simplest, good for testing rendering pipeline
3. Implement `blob()` - tests closed shapes and randomness
4. Implement `tentacle()` - most complex, tests tapering and fills
5. Add unit tests (verify output has expected shape characteristics)
6. Create `examples/primitives_demo.py` showing all three

### Phase 2: OceanShapes Class
1. Add `OceanPalette` colors
2. Implement `OceanShapes.octopus()` using primitives
3. Implement one more helper (jellyfish or seaweed)
4. Create `examples/ocean_scene.py` - full underwater scene
5. Add to browser interface as example lesson (optional)

### Phase 3: Documentation & Polish
1. Update README with "Drawing Organic Shapes" section
2. Add docstring examples for each method
3. Consider adding to lesson curriculum (advanced topic)

## Testing Strategy

### Unit Tests (pytest)
```python
def test_wave_basic():
    """Wave draws from start to end point."""
    can = Canvas(400, 200)
    can.wave(50, 100, 350, 100, height=20, waves=2)
    svg = can.to_svg()
    assert 'polyline' in svg or 'path' in svg
    # Verify rough bounding box

def test_tentacle_taper():
    """Tentacle gets thinner toward tip."""
    can = Canvas(400, 400)
    can.tentacle(200, 100, 200, 300, thickness=40, taper=0.2)
    svg = can.to_svg()
    assert 'polygon' in svg
    # Could verify point count or approximate area

def test_blob_wobble():
    """Blob with wobble=0 is roughly circular."""
    can = Canvas(200, 200)
    can.blob(100, 100, radius=50, wobble=0, points=12)
    svg = can.to_svg()
    assert 'polygon' in svg

def test_ocean_shapes_octopus():
    """Octopus renders without errors."""
    can = Canvas(600, 600)
    ocean = OceanShapes(can)
    ocean.octopus(300, 250, size=120)
    svg = can.to_svg()
    # Should contain blob (head) + 8 tentacles
    assert svg.count('polygon') >= 9
```

### Visual Tests
Create example scripts in `examples/`:
- `ocean_primitives.py` - Demo each primitive method
- `ocean_scene.py` - Full scene with OceanShapes
- `tentacle_gallery.py` - Show different curl values
- `wave_patterns.py` - Different wave configurations

## Math Reference

### Bézier Curve Formulas

**Quadratic Bézier** (3 points: start, control, end):
```
B(t) = (1-t)²·P₀ + 2(1-t)t·P₁ + t²·P₂,  t ∈ [0,1]
```

**Cubic Bézier** (4 points: start, control1, control2, end):
```
B(t) = (1-t)³·P₀ + 3(1-t)²t·P₁ + 3(1-t)t²·P₂ + t³·P₃,  t ∈ [0,1]
```

### Helper Function
```python
def _bezier_points(p0, p1, p2, p3=None, steps=50):
    """
    Generate points along a Bézier curve.

    Args:
        p0: Start point (x, y)
        p1: First control point (x, y)
        p2: Second control point (x, y) [or end point if quadratic]
        p3: End point (x, y) [None for quadratic]
        steps: Number of sample points

    Returns:
        List of (x, y) tuples along the curve
    """
    points = []
    for i in range(steps + 1):
        t = i / steps
        if p3 is None:  # Quadratic
            x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
            y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
        else:  # Cubic
            x = (1-t)**3 * p0[0] + 3*(1-t)**2*t * p1[0] + 3*(1-t)*t**2 * p2[0] + t**3 * p3[0]
            y = (1-t)**3 * p0[1] + 3*(1-t)**2*t * p1[1] + 3*(1-t)*t**2 * p2[1] + t**3 * p3[1]
        points.append((x, y))
    return points
```

## Open Questions

1. **Randomness in `blob()`**: Should it be deterministic (same wobble = same shape)?
   - **Proposal**: Add optional `seed` parameter, default to random

2. **Tentacle suction cups**: Auto-add or separate method?
   - **Proposal**: Separate `tentacle_with_suckers()` or param `suckers=True`

3. **SVG path vs polygon**: Use native SVG curves or sample to polygons?
   - **Proposal**: Start with polygons (simpler), consider SVG paths later for smaller file size

4. **Browser compatibility**: Does Pyodide SVG rendering handle complex polygons?
   - **Test**: Include in browser tests after Phase 1

## Success Criteria

- [ ] All parametric methods work with method chaining
- [ ] Tentacle looks organic (smooth taper, natural curl)
- [ ] Wave looks like water (smooth sine-like motion)
- [ ] Blob looks blobby (irregular but not jagged)
- [ ] Octopus is recognizable and cute
- [ ] OceanPalette colors are aesthetically pleasing
- [ ] All examples render correctly in browser (Pyodide)
- [ ] Tests pass (both unit and visual)
- [ ] 13-year-old draws an octopus without frustration :)

## Future Extensions (v2)

- Animation helpers (waving tentacles, swimming fish)
- More creatures (fish, crab, seahorse, whale)
- Particle effects (bubbles rising)
- Interactive parameters (slider to adjust curl in browser)
- Raw Bézier API for advanced users (defer from original plan)
