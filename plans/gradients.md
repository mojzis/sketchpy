# Implementation Plan: Gradients and Named Objects for SketchPy

## Overview
Add two features to `shapes.py` while maintaining simplicity and backward compatibility:
1. **Gradient fills** - Define gradients separately, use like colors
2. **Named object groups** - Group shapes with context managers for manipulation

## Current Architecture
- `Canvas` class holds list of SVG shape strings in `self.shapes`
- Methods like `circle()`, `rect()` return `self` for chaining
- `to_svg()` generates final SVG by concatenating shapes
- No state tracking beyond the shapes list

---

## Feature 1: Gradient Support

### Requirements
- Define gradients separately from shapes
- Use gradients as fill values (like colors)
- Support linear and radial gradients
- Keep shape methods unchanged (no new parameters)
- SVG `<defs>` section must be added for gradient definitions

### Implementation Details

#### 1.1 Add gradient storage to Canvas.__init__
```python
def __init__(self, width: int = 800, height: int = 600, background: str = Color.WHITE):
    self.width = width
    self.height = height
    self.background = background
    self.shapes: List[str] = []
    self.gradients: Dict[str, str] = {}  # NEW: gradient_id -> SVG definition
```

#### 1.2 Add gradient definition methods
```python
def linear_gradient(self, name: str, 
                   start: Tuple[float, float] = (0, 0),
                   end: Tuple[float, float] = (100, 0),
                   colors: List[Tuple[str, float]] = None) -> 'Canvas':
    """
    Define a linear gradient for use in fills.
    
    Args:
        name: Identifier to use as fill="gradient:{name}"
        start: (x, y) start point in percentages (0-100)
        end: (x, y) end point in percentages (0-100)
        colors: List of (color, offset) tuples. Offset is 0.0-1.0
                If just colors provided, distribute evenly
    
    Example:
        canvas.linear_gradient("sunset", 
            start=(0, 0), end=(100, 0),
            colors=[("#FF6B6B", 0), ("#FFA500", 0.5), ("#FFD93D", 1.0)])
        
        # Then use as: canvas.circle(100, 100, 50, fill="gradient:sunset")
    """
    if colors is None:
        colors = [("#000000", 0), ("#FFFFFF", 1)]
    
    # Auto-distribute offsets if colors is list of strings
    if colors and isinstance(colors[0], str):
        n = len(colors)
        colors = [(color, i/(n-1) if n > 1 else 0) for i, color in enumerate(colors)]
    
    gradient_id = f"grad_{name}"
    stops = "".join(f'<stop offset="{offset*100}%" stop-color="{color}"/>' 
                    for color, offset in colors)
    
    svg_def = f'''<linearGradient id="{gradient_id}" x1="{start[0]}%" y1="{start[1]}%" x2="{end[0]}%" y2="{end[1]}%">
{stops}
</linearGradient>'''
    
    self.gradients[name] = svg_def
    return self


def radial_gradient(self, name: str,
                   center: Tuple[float, float] = (50, 50),
                   radius: float = 50,
                   colors: List[Tuple[str, float]] = None) -> 'Canvas':
    """
    Define a radial gradient for use in fills.
    
    Args:
        name: Identifier to use as fill="gradient:{name}"
        center: (x, y) center point in percentages (0-100)
        radius: Radius in percentages (0-100)
        colors: List of (color, offset) tuples or just colors
    """
    if colors is None:
        colors = [("#000000", 0), ("#FFFFFF", 1)]
    
    if colors and isinstance(colors[0], str):
        n = len(colors)
        colors = [(color, i/(n-1) if n > 1 else 0) for i, color in enumerate(colors)]
    
    gradient_id = f"grad_{name}"
    stops = "".join(f'<stop offset="{offset*100}%" stop-color="{color}"/>' 
                    for color, offset in colors)
    
    svg_def = f'''<radialGradient id="{gradient_id}" cx="{center[0]}%" cy="{center[1]}%" r="{radius}%">
{stops}
</radialGradient>'''
    
    self.gradients[name] = svg_def
    return self
```

#### 1.3 Helper function to convert fill values
```python
def _resolve_fill(self, fill: str) -> str:
    """Convert gradient:{name} to url(#grad_{name}), pass through regular colors."""
    if fill.startswith("gradient:"):
        gradient_name = fill[9:]  # Remove "gradient:" prefix
        return f"url(#grad_{gradient_name})"
    return fill
```

#### 1.4 Update all shape methods to use _resolve_fill
Modify each method (circle, rect, ellipse, polygon, rounded_rect) to process fill:
```python
# OLD:
fill: str = Color.BLACK

# NEW: 
fill: str = Color.BLACK

# In method body, change:
fill="{fill}"

# To:
fill="{self._resolve_fill(fill)}"
```

#### 1.5 Update to_svg() to include gradients
```python
def to_svg(self) -> str:
    """Generate the complete SVG string."""
    svg_header = f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">'
    svg_background = f'<rect width="100%" height="100%" fill="{self.background}"/>'
    
    # NEW: Add defs section if gradients exist
    defs_section = ""
    if self.gradients:
        gradient_defs = "".join(self.gradients.values())
        defs_section = f"<defs>{gradient_defs}</defs>"
    
    svg_footer = '</svg>'
    
    return svg_header + svg_background + defs_section + ''.join(self.shapes) + svg_footer
```

---

## Feature 2: Named Object Groups

### Requirements
- Group shapes under named identifiers
- Use context manager syntax for intuitive grouping
- Support moving, hiding, showing, removing entire groups
- Maintain backward compatibility (ungrouped shapes still work)

### Implementation Details

#### 2.1 Add group storage to Canvas.__init__
```python
def __init__(self, width: int = 800, height: int = 600, background: str = Color.WHITE):
    self.width = width
    self.height = height
    self.background = background
    self.shapes: List[str] = []
    self.gradients: Dict[str, str] = {}
    self.groups: Dict[str, List[str]] = {}  # NEW: group_name -> list of shapes
    self.current_group: Optional[str] = None  # NEW: active group context
    self.group_transforms: Dict[str, str] = {}  # NEW: group_name -> transform attribute
    self.group_visibility: Dict[str, bool] = {}  # NEW: group_name -> visible
```

#### 2.2 Create context manager class
```python
class GroupContext:
    """Context manager for adding shapes to a named group."""
    
    def __init__(self, canvas: 'Canvas', name: str):
        self.canvas = canvas
        self.name = name
        
    def __enter__(self):
        if self.name not in self.canvas.groups:
            self.canvas.groups[self.name] = []
            self.canvas.group_visibility[self.name] = True
            self.canvas.group_transforms[self.name] = ""
        self.canvas.current_group = self.name
        return self.canvas
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.canvas.current_group = None
        return False
```

#### 2.3 Add group() method to Canvas
```python
def group(self, name: str) -> GroupContext:
    """
    Create a context manager for adding shapes to a named group.
    
    Example:
        with canvas.group("flower"):
            canvas.circle(100, 100, 20, fill=Color.YELLOW)
            canvas.circle(85, 90, 10, fill=Color.PINK)
        
        # Later manipulate as a unit
        canvas.move_group("flower", dx=50, dy=30)
        canvas.hide_group("flower")
    """
    return GroupContext(self, name)
```

#### 2.4 Update shape methods to respect groups
Modify ALL shape-adding methods (circle, rect, ellipse, line, polygon, text, rounded_rect):
```python
# At the END of each method, BEFORE return self:
# OLD:
self.shapes.append(svg)

# NEW:
if self.current_group:
    self.groups[self.current_group].append(svg)
else:
    self.shapes.append(svg)
```

#### 2.5 Add group manipulation methods
```python
def move_group(self, name: str, dx: float = 0, dy: float = 0) -> 'Canvas':
    """Move a group by offset (dx, dy)."""
    if name not in self.groups:
        return self
    
    # Parse existing transform or create new one
    existing = self.group_transforms.get(name, "")
    if existing and "translate" in existing:
        # Extract current translation and add to it
        # For simplicity, replace any existing translate
        import re
        existing = re.sub(r'translate\([^)]+\)', '', existing)
    
    self.group_transforms[name] = f"translate({dx}, {dy}) {existing}".strip()
    return self


def rotate_group(self, name: str, angle: float, cx: float = 0, cy: float = 0) -> 'Canvas':
    """Rotate a group by angle degrees around point (cx, cy)."""
    if name not in self.groups:
        return self
    
    existing = self.group_transforms[name]
    self.group_transforms[name] = f"{existing} rotate({angle}, {cx}, {cy})".strip()
    return self


def hide_group(self, name: str) -> 'Canvas':
    """Hide a group from rendering."""
    if name in self.group_visibility:
        self.group_visibility[name] = False
    return self


def show_group(self, name: str) -> 'Canvas':
    """Show a previously hidden group."""
    if name in self.group_visibility:
        self.group_visibility[name] = True
    return self


def remove_group(self, name: str) -> 'Canvas':
    """Permanently remove a group from the canvas."""
    if name in self.groups:
        del self.groups[name]
        del self.group_visibility[name]
        del self.group_transforms[name]
    return self
```

#### 2.6 Update to_svg() to render groups
```python
def to_svg(self) -> str:
    """Generate the complete SVG string."""
    svg_header = f'<svg width="{self.width}" height="{self.height}" xmlns="http://www.w3.org/2000/svg">'
    svg_background = f'<rect width="100%" height="100%" fill="{self.background}"/>'
    
    defs_section = ""
    if self.gradients:
        gradient_defs = "".join(self.gradients.values())
        defs_section = f"<defs>{gradient_defs}</defs>"
    
    # Ungrouped shapes
    ungrouped = ''.join(self.shapes)
    
    # NEW: Grouped shapes
    grouped = ""
    for group_name, shapes in self.groups.items():
        if not self.group_visibility.get(group_name, True):
            continue  # Skip hidden groups
        
        transform = self.group_transforms.get(group_name, "")
        transform_attr = f' transform="{transform}"' if transform else ""
        
        group_svg = f'<g id="{group_name}"{transform_attr}>{"".join(shapes)}</g>'
        grouped += group_svg
    
    svg_footer = '</svg>'
    
    return svg_header + svg_background + defs_section + ungrouped + grouped + svg_footer
```

#### 2.7 Update clear() method
```python
def clear(self) -> 'Canvas':
    """Clear all shapes and groups from the canvas."""
    self.shapes = []
    self.groups = {}
    self.group_transforms = {}
    self.group_visibility = {}
    self.current_group = None
    return self
```

---

## Testing Examples

### Example 1: Simple gradient usage
```python
canvas = Canvas(800, 600)

# Define gradients
canvas.linear_gradient("sunset", colors=["#FF6B6B", "#FFA500", "#FFD93D"])
canvas.radial_gradient("glow", center=(50, 50), colors=["#FFFF00", "#FF6B00"])

# Use like colors
canvas.circle(200, 200, 100, fill="gradient:sunset")
canvas.circle(500, 300, 80, fill="gradient:glow")
```

### Example 2: Named groups
```python
canvas = Canvas(800, 600)

# Create a flower as a group
with canvas.group("flower"):
    canvas.circle(400, 300, 30, fill=Color.YELLOW)
    canvas.circle(370, 280, 15, fill=Color.PINK)
    canvas.circle(430, 280, 15, fill=Color.PINK)
    canvas.circle(370, 320, 15, fill=Color.PINK)
    canvas.circle(430, 320, 15, fill=Color.PINK)

# Draw a car separately
with canvas.group("car"):
    canvas.rect(100, 400, 120, 50, fill=Color.RED)
    canvas.circle(130, 450, 15, fill=Color.BLACK)
    canvas.circle(190, 450, 15, fill=Color.BLACK)

# Manipulate groups
canvas.move_group("flower", dx=100, dy=-50)
canvas.hide_group("car")
canvas.show_group("car")
```

### Example 3: Combined features
```python
canvas = Canvas(800, 600)
canvas.linear_gradient("sky", start=(0, 0), end=(0, 100), 
                      colors=["#87CEEB", "#FFFFFF"])

# Background with gradient
canvas.rect(0, 0, 800, 600, fill="gradient:sky", stroke="none")

# Multiple flowers using groups
for i, x in enumerate([200, 400, 600]):
    with canvas.group(f"flower_{i}"):
        canvas.circle(x, 300, 30, fill=Color.YELLOW)
        for angle in range(0, 360, 60):
            import math
            px = x + 35 * math.cos(math.radians(angle))
            py = 300 + 35 * math.sin(math.radians(angle))
            canvas.circle(px, py, 15, fill=Color.PINK)
```

---

## Backward Compatibility Checklist
- [ ] All existing code without gradients/groups works unchanged
- [ ] Shape methods still return `self` for chaining
- [ ] Default parameters unchanged
- [ ] No breaking changes to method signatures
- [ ] `to_svg()` handles empty gradient and group dictionaries gracefully

## Implementation Order
1. Add gradient support first (simpler, fewer changes)
   - Add gradient storage to `__init__`
   - Implement `linear_gradient()` and `radial_gradient()`
   - Add `_resolve_fill()` helper
   - Update all shape methods to use `_resolve_fill()`
   - Update `to_svg()` for `<defs>` section
   - Test gradient functionality

2. Add group support second
   - Add group storage to `__init__`
   - Create `GroupContext` class
   - Add `group()` method
   - Update all shape methods to respect `current_group`
   - Implement group manipulation methods
   - Update `to_svg()` to render groups
   - Update `clear()` method
   - Test group functionality

3. Test combined usage

## Notes for Implementation
- Import `Dict` and `Optional` from `typing` at top
- Ensure SVG string formatting is clean (no extra spaces/newlines)
- Group transforms follow SVG transform syntax: `translate(x, y) rotate(angle, cx, cy)`
- Gradient colors can be hex strings or Color constants
- For simplicity, gradients use percentage coordinates (0-100) not pixels