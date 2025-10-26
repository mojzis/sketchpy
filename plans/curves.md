# Implementation Plan: Bézier Curves and Path API for Canvas

## Overview

Add Bézier curve drawing capabilities and a path builder API to support organic shapes (tentacles, leaves, waves, etc.) while maintaining the simple, beginner-friendly API style.

## New Canvas Methods

### 1. Quadratic Bézier Curve
```python
def curve(self, x1: float, y1: float, cx: float, cy: float, 
          x2: float, y2: float, stroke: Color = Color.BLACK, 
          stroke_width: int = 1, fill: Optional[Color] = None) -> 'Canvas':
    """
    Draw a quadratic Bézier curve.
    
    Args:
        x1, y1: Start point
        cx, cy: Control point (pulls curve toward this point)
        x2, y2: End point
        stroke: Line color
        stroke_width: Line thickness
        fill: Optional fill color (fills area under curve to baseline)
    
    Returns:
        self (for method chaining)
    """
```

**Implementation:** Use PIL's `ImageDraw.line()` with calculated points. Sample the curve at ~50 points for smooth rendering.

**Math:** Point at t ∈ [0,1]: 
- x = (1-t)²·x1 + 2(1-t)t·cx + t²·x2
- y = (1-t)²·y1 + 2(1-t)t·cy + t²·y2

### 2. Cubic Bézier Curve
```python
def bezier(self, x1: float, y1: float, cx1: float, cy1: float,
           cx2: float, cy2: float, x2: float, y2: float,
           stroke: Color = Color.BLACK, stroke_width: int = 1,
           fill: Optional[Color] = None) -> 'Canvas':
    """
    Draw a cubic Bézier curve.
    
    Args:
        x1, y1: Start point
        cx1, cy1: First control point
        cx2, cy2: Second control point
        x2, y2: End point
        stroke: Line color
        stroke_width: Line thickness
        fill: Optional fill color
    
    Returns:
        self (for method chaining)
    """
```

**Math:** Point at t ∈ [0,1]:
- x = (1-t)³·x1 + 3(1-t)²t·cx1 + 3(1-t)t²·cx2 + t³·x2
- y = (1-t)³·y1 + 3(1-t)²t·cy1 + 3(1-t)t²·cy2 + t³·y2

### 3. Path Builder (for filled shapes)
```python
class Path:
    """Builder for complex filled shapes."""
    
    def __init__(self, canvas: 'Canvas'):
        self._canvas = canvas
        self._points = []
        self._closed = False
    
    def move_to(self, x: float, y: float) -> 'Path':
        """Start a new subpath at (x, y)."""
        
    def line_to(self, x: float, y: float) -> 'Path':
        """Draw line to (x, y)."""
        
    def curve_to(self, cx: float, cy: float, x: float, y: float) -> 'Path':
        """Draw quadratic curve to (x, y) with control point (cx, cy)."""
        
    def bezier_to(self, cx1: float, cy1: float, cx2: float, cy2: float,
                  x: float, y: float) -> 'Path':
        """Draw cubic Bézier curve to (x, y)."""
        
    def close(self) -> 'Path':
        """Close path by connecting back to start point."""
        
    def fill(self, color: Color) -> None:
        """Fill the path with given color."""
        
    def stroke(self, color: Color, width: int = 1) -> None:
        """Draw the path outline."""

# Canvas method to create path
def path(self) -> Path:
    """Create a new path builder."""
    return Path(self)
```

**Implementation:** Use PIL's `ImageDraw.polygon()` for filled paths. Convert all curves to line segments, store as list of (x,y) tuples.

## Implementation Details

### File Structure

Add to existing `canvas.py`:
- Helper function `_bezier_points(p0, p1, p2, p3=None, steps=50)` for curve sampling
- Path class (can be inner class or separate)
- New canvas methods

### Curve Sampling Resolution

Use adaptive sampling based on curve length:
- Short curves (<100px): 20 points
- Medium curves (100-300px): 50 points  
- Long curves (>300px): 100 points

Calculate approximate length: `sqrt((x2-x1)² + (y2-y1)²)`

### Path Storage
```python
class Path:
    def __init__(self, canvas):
        self._canvas = canvas
        self._segments = []  # List of ('line'|'curve'|'bezier', params)
        self._points = None  # Cached flattened points
        
    def _flatten(self):
        """Convert all segments to line points."""
        if self._points is not None:
            return self._points
            
        points = []
        current = (0, 0)
        
        for seg_type, params in self._segments:
            if seg_type == 'move':
                current = params
                points.append(current)
            elif seg_type == 'line':
                points.append(params)
                current = params
            elif seg_type == 'curve':
                curve_points = _bezier_points(current, *params)
                points.extend(curve_points[1:])
                current = params[-2:]
            # ... etc
        
        self._points = points
        return points
```

### Error Handling

- Validate all numeric inputs (must be finite numbers)
- Require at least 2 points for paths
- Warn if path not closed before fill() but auto-close
- Handle degenerate cases (all points identical)

## Testing Strategy

### Unit Tests
```python
def test_curve_basic():
    """Curve draws from start to end."""
    can = Canvas(100, 100)
    can.curve(10, 10, 50, 50, 90, 10)
    # Verify pixels exist along expected curve

def test_path_closed_shape():
    """Filled path creates closed polygon."""
    can = Canvas(100, 100)
    p = can.path()
    p.move_to(50, 10)
    p.line_to(90, 90)
    p.line_to(10, 90)
    p.close()
    p.fill(Color.RED)
    # Verify interior pixels are red

def test_method_chaining():
    """Curve returns canvas for chaining."""
    can = Canvas(100, 100)
    result = can.curve(10, 10, 50, 50, 90, 10, stroke=Color.RED)
    assert result is can
```

### Visual Tests

Create example scripts in `examples/`:
- `curves_basic.py` - Simple S-curve
- `tentacle.py` - Octopus tentacle using path
- `leaf.py` - Organic leaf shape
- `wave.py` - Sine-like wave using multiple curves

## Documentation

### Docstrings

Each method needs:
- Clear description of what it draws
- Parameter meanings (especially control points)
- Visual diagram in docstring (ASCII art)
- Example usage

Example:
```python
def curve(self, x1, y1, cx, cy, x2, y2, ...):
    """
    Draw a smooth quadratic Bézier curve.
    
    The curve starts at (x1, y1), ends at (x2, y2), and is pulled
    toward the control point (cx, cy).
    
    Visual representation:
        
        (x1,y1) •
                 \
                  \  ← pulled toward (cx,cy)
                   \
                    • (x2,y2)
    
    Examples:
        # Simple arc
        can.curve(100, 100, 200, 50, 300, 100)
        
        # S-curve
        can.curve(100, 100, 150, 200, 300, 100)
    """
```

### Tutorial Addition

Add new section to README:
- "Drawing Organic Shapes"
- When to use curve vs bezier
- Path builder walkthrough with tentacle example

## Migration Path

1. Implement curve() and bezier() first (simpler, standalone)
2. Add visual tests to verify rendering
3. Implement Path class
4. Add to curriculum document (lessons 8-13)
5. Create octopus theme examples

## Performance Considerations

- Cache flattened path points (don't recalculate on each draw)
- For animation, pre-compute curve points if curve parameters don't change
- Consider adding `steps` parameter for user control of smoothness vs speed

## Open Questions

1. Should curves support dashed lines? (defer to v2)
2. Should Path support holes (subtract regions)? (defer to v2)
3. Should we add arc() method for circular arcs? (yes, useful for wheels)

## Success Criteria

- [ ] All three methods work with method chaining
- [ ] Visual output matches expectations (smooth curves, no jagged edges)
- [ ] Path fill() creates properly closed shapes
- [ ] Documentation includes visual examples
- [ ] At least one complete "octopus" example in examples/
- [ ] Integration with existing Color and Canvas APIs is seamless