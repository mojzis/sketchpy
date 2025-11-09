# Helper Class Gradient Support Plan

**Goal**: Enable helper classes (OceanShapes, CarShapes) to define and use predefined gradients for more visually appealing default shapes.

**Status**: Planning
**Date**: 2025-11-09

---

## Problem Statement

Currently, helper classes use flat colors for shapes:
- `ocean.octopus()` uses solid `OceanPalette.CORAL`
- `ocean.jellyfish()` uses solid `OceanPalette.TRANSLUCENT_BLUE`
- `cars.simple_car()` uses solid `Color.RED`

Canvas already supports gradients via:
- `canvas.linear_gradient(name, start, end, colors)`
- `canvas.radial_gradient(name, center, radius, colors)`
- Usage: `fill="gradient:name"`

**Issue**: Helper classes can't easily define their own gradients without polluting user code or manually registering them each time.

---

## Proposed Solution

### 1. Architecture

**Gradient Registration System**:
- Each helper class defines a `_setup_gradients()` method
- Called automatically in `__init__` to register gradients with canvas
- Gradients use namespaced IDs to avoid conflicts: `{helper_class}_{gradient_name}`
- Example: `"ocean_octopus_body"`, `"ocean_jellyfish_glow"`, `"car_metallic"`

**Benefits**:
- Clean separation of concerns (helpers manage their own visual presets)
- No global state pollution
- Automatic registration (zero user setup)
- Backward compatible (users can override with solid colors)

### 2. Implementation Plan

#### Phase 1: Core Infrastructure (Helper Base Pattern)

**Add `_setup_gradients()` method to each helper class**:

```python
class OceanShapes:
    def __init__(self, canvas: 'Canvas'):
        self.canvas = canvas
        self._setup_gradients()

    def _setup_gradients(self):
        """Register predefined gradients for ocean shapes."""
        # Octopus body: coral with darker edges for depth
        self.canvas.radial_gradient(
            "ocean_octopus_body",
            center=(50, 30),  # Top-lit effect
            radius=70,
            colors=[
                ("#FF9B8A", 0),      # Light coral (highlight)
                (OceanPalette.CORAL, 0.5),  # Base coral
                ("#C84B3D", 1.0)     # Dark coral (shadow)
            ]
        )

        # Jellyfish bell: translucent glow effect
        self.canvas.radial_gradient(
            "ocean_jellyfish_glow",
            center=(50, 40),
            radius=60,
            colors=[
                ("#FFFFFF", 0),      # Bright center (bioluminescence)
                (OceanPalette.TRANSLUCENT_BLUE, 0.6),
                ("#6EA8C8", 1.0)     # Darker edges
            ]
        )

        # Seaweed: gradient from dark roots to light tips
        self.canvas.linear_gradient(
            "ocean_seaweed_depth",
            start=(0, 100),  # Bottom (dark)
            end=(0, 0),      # Top (light)
            colors=[
                (OceanPalette.KELP_GREEN, 0),   # Dark base
                (OceanPalette.SEA_GREEN, 1.0)   # Lighter tips
            ]
        )

        # Tentacle shading (works for both octopus and jellyfish)
        self.canvas.linear_gradient(
            "ocean_tentacle_shading",
            start=(0, 0),    # Left
            end=(100, 0),    # Right
            colors=[
                ("#D8685C", 0),      # Shadow side
                (OceanPalette.CORAL, 0.5),  # Middle
                ("#FF9B8A", 1.0)     # Highlight side
            ]
        )
```

**Similar pattern for CarShapes**:

```python
class CarShapes:
    def __init__(self, canvas: 'Canvas'):
        self.canvas = canvas
        self._setup_gradients()

    def _setup_gradients(self):
        """Register predefined gradients for car shapes."""
        # Metallic car body paint
        self.canvas.linear_gradient(
            "car_metallic_shine",
            start=(0, 0),    # Top
            end=(0, 100),    # Bottom
            colors=[
                ("#FFB3B3", 0),      # Highlight (sky reflection)
                ("#FF6B6B", 0.3),    # Upper body
                ("#E04040", 0.7),    # Lower body (darker)
                ("#A03030", 1.0)     # Shadow/undercarriage
            ]
        )

        # Tire rubber shading
        self.canvas.radial_gradient(
            "car_tire_rubber",
            center=(30, 30),  # Light source from upper-left
            radius=70,
            colors=[
                ("#3A3A3A", 0),      # Lighter rubber
                (Color.BLACK, 1.0)   # Deep black
            ]
        )

        # Chrome/silver rim shine
        self.canvas.radial_gradient(
            "car_chrome_rim",
            center=(40, 40),
            radius=60,
            colors=[
                ("#FFFFFF", 0),      # Bright reflection
                (Color.SILVER, 0.5),
                ("#808080", 1.0)     # Darker metal edge
            ]
        )

        # Traffic light glow effect
        self.canvas.radial_gradient(
            "car_light_glow_red",
            center=(50, 50),
            radius=70,
            colors=[
                ("#FFCCCC", 0),      # Bright center
                (Color.RED, 0.6),
                ("#AA0000", 1.0)     # Dark edge
            ]
        )

        # Similar for yellow and green lights
        self.canvas.radial_gradient(
            "car_light_glow_yellow",
            center=(50, 50),
            radius=70,
            colors=[("#FFFFCC", 0), (Color.YELLOW, 0.6), ("#CCAA00", 1.0)]
        )

        self.canvas.radial_gradient(
            "car_light_glow_green",
            center=(50, 50),
            radius=70,
            colors=[("#CCFFCC", 0), (Color.GREEN, 0.6), ("#00AA00", 1.0)]
        )
```

#### Phase 2: Update Helper Methods to Use Gradients

**OceanShapes Changes**:

```python
def octopus(self, x: float, y: float, size: float = 100,
            body_color: str = "gradient:ocean_octopus_body",  # Changed default
            eye_color: str = Color.WHITE) -> 'OceanShapes':
    """Draw a cute octopus with gradient shading."""
    # Method body stays the same - gradients work automatically
    # Users can still override: .octopus(400, 200, body_color=Color.PURPLE)
    ...

def jellyfish(self, x: float, y: float, size: float = 80,
              body_color: str = "gradient:ocean_jellyfish_glow",  # Changed default
              tentacle_count: int = 6) -> 'OceanShapes':
    """Draw a glowing jellyfish."""
    ...

def seaweed(self, x: float, y: float, height: float = 150,
            sway: float = 0.3,
            color: str = "gradient:ocean_seaweed_depth") -> 'OceanShapes':  # Changed default
    """Draw gradient seaweed from dark roots to light tips."""
    ...
```

**CarShapes Changes**:

```python
@staticmethod
def simple_car(canvas: 'Canvas', x: float, y: float,
               width: float = 120, height: float = 50,
               color: str = "gradient:car_metallic_shine") -> 'Canvas':  # Changed default
    """Draw a car with metallic paint gradient."""
    # CarShapes is static, so we need to rethink this...
    # DECISION: Convert CarShapes to instance-based like OceanShapes
    ...
```

**⚠️ CarShapes Refactor Required**:
- Current: Static methods (no `__init__`, no instance)
- Needed: Instance-based like OceanShapes to call `_setup_gradients()`
- **Breaking change** but more consistent API

#### Phase 3: Backward Compatibility

**Ensure users can override gradients**:
- Keep `color` parameter flexible
- Accept both solid colors and gradient references
- Example: `.octopus(x, y, body_color=Color.PURPLE)` still works

**Migration path**:
- Old code using solid colors continues to work
- New code gets gradients by default
- Users can opt-out by passing solid colors

---

## Implementation Details

### 3.1 OceanShapes Gradient Definitions

**Octopus** (3D depth effect):
- **Body gradient**: Radial from light coral center to darker edges
- **Tentacle gradient**: Linear across width for cylindrical shading
- **Visual goal**: Soft, rounded, 3D appearance

**Jellyfish** (bioluminescent glow):
- **Bell gradient**: Radial from bright white center to translucent blue edges
- **Tentacle gradient**: Same as octopus but lighter colors
- **Visual goal**: Ethereal, glowing, translucent effect

**Seaweed** (underwater depth):
- **Stem gradient**: Linear from dark green base to lighter tips
- **Leaves**: Use same gradient as stem
- **Visual goal**: Natural shading from murky depths to sunlit water

### 3.2 CarShapes Gradient Definitions

**Car Body** (metallic paint):
- **Linear gradient**: Top-to-bottom simulating sky reflection
- **Colors**: Light on top (sky), darker on bottom (shadow)
- **Visual goal**: Shiny car paint with realistic lighting

**Wheels**:
- **Tire**: Radial from gray to black (rubber texture)
- **Rim**: Radial from white to silver (chrome reflection)
- **Hub**: Small radial gradient (metallic center)

**Traffic Light** (LED/bulb glow):
- **Active light**: Radial from bright center to darker edge
- **Inactive lights**: Use flat gray (no gradient)
- **Visual goal**: Realistic light emission

### 3.3 Technical Considerations

**Gradient Coordinate System**:
- Canvas gradients use percentage-based coordinates (0-100)
- Independent of shape size/position
- Works well for reusable gradients

**Performance**:
- Gradients are SVG `<defs>` (minimal overhead)
- One gradient definition can be reused by multiple shapes
- No impact on render performance

**Browser Compatibility**:
- SVG gradients supported in all modern browsers
- Already tested in current Canvas implementation
- No special polyfills needed

---

## Testing Strategy

### 4.1 Unit Tests (Python)

**Test gradient registration**:
```python
def test_ocean_gradients_registered():
    can = Canvas(800, 600)
    ocean = OceanShapes(can)

    # Verify gradients exist
    assert "ocean_octopus_body" in can.gradients
    assert "ocean_jellyfish_glow" in can.gradients
    assert "ocean_seaweed_depth" in can.gradients
```

**Test default gradient usage**:
```python
def test_octopus_uses_gradient_by_default():
    can = Canvas(800, 600)
    ocean = OceanShapes(can)
    ocean.octopus(400, 300)

    svg = can.to_svg()
    assert "url(#grad_ocean_octopus_body)" in svg
```

**Test color override**:
```python
def test_octopus_can_use_solid_color():
    can = Canvas(800, 600)
    ocean = OceanShapes(can)
    ocean.octopus(400, 300, body_color=Color.PURPLE)

    svg = can.to_svg()
    assert Color.PURPLE in svg
    assert "grad_ocean_octopus_body" not in svg  # Gradient not used
```

### 4.2 Browser Tests (Playwright)

**Test visual rendering**:
- Verify gradients render correctly in browser
- Check that colors interpolate smoothly
- Ensure no visual regressions

**Test lesson integration**:
- Ocean lesson should show gradient shapes by default
- Car lesson should show metallic cars
- Performance should remain acceptable

---

## Migration Plan

### 5.1 CarShapes Refactor (Breaking Change)

**Current API**:
```python
from sketchpy import Canvas, CarShapes

can = Canvas(800, 600)
CarShapes.simple_car(can, 100, 300)  # Static method
```

**New API**:
```python
from sketchpy import Canvas, CarShapes

can = Canvas(800, 600)
cars = CarShapes(can)  # Create instance
cars.simple_car(100, 300)  # Instance method
```

**Migration Steps**:
1. Convert all `@staticmethod` to instance methods
2. Remove `canvas` parameter from methods (use `self.canvas`)
3. Add `__init__` and `_setup_gradients()` methods
4. Update documentation and examples
5. Update car lesson to use new API

**Backward Compatibility**:
- Old static API will break (intentional)
- Update all examples in one PR
- Document breaking change in CHANGELOG
- Users get better API + gradients in one upgrade

### 5.2 Lesson Updates

**Update `themes/ocean/lesson.md`**:
- Show off new gradient effects
- Explain how to override with solid colors
- Add section on customizing gradients

**Update `themes/cars/lesson.md`**:
- Update examples to use new instance-based API
- Show metallic car effects
- Demonstrate gradient overrides

---

## Future Enhancements

### 6.1 Custom Gradient Builder

**Helper method for easy gradient creation**:
```python
class OceanShapes:
    def create_gradient(self, name: str, colors: list, type: str = "radial"):
        """Easy gradient creation for advanced users."""
        if type == "radial":
            self.canvas.radial_gradient(f"ocean_{name}", colors=colors)
        else:
            self.canvas.linear_gradient(f"ocean_{name}", colors=colors)
```

### 6.2 Gradient Presets Library

**Expand gradient collection**:
- Metallic effects (gold, silver, copper)
- Sunset/sunrise gradients
- Underwater light rays
- Glass/transparency effects

### 6.3 Helper Base Class

**Abstract base class for all helpers**:
```python
class ShapeHelper:
    """Base class for all shape helpers."""

    def __init__(self, canvas: 'Canvas'):
        self.canvas = canvas
        self._namespace = self.__class__.__name__.lower()
        self._setup_gradients()

    def _setup_gradients(self):
        """Override in subclasses to define gradients."""
        pass

    def _gradient_name(self, name: str) -> str:
        """Generate namespaced gradient ID."""
        return f"{self._namespace}_{name}"
```

Benefits:
- Consistent API across all helpers
- Automatic namespace management
- Less boilerplate in helper implementations

---

## Open Questions

1. **Should we provide a way to disable gradients globally?**
   - Use case: Users who prefer flat design
   - Possible solution: `OceanShapes(canvas, use_gradients=False)`

2. **Should gradients be lazy-loaded?**
   - Current plan: Register all gradients in `__init__`
   - Alternative: Register only when first shape is drawn
   - Trade-off: Simplicity vs. minor memory savings

3. **How to handle gradient customization?**
   - Should users be able to modify predefined gradients?
   - Provide `modify_gradient(name, colors)` method?

4. **Naming convention for gradients?**
   - Current: `{helper}_{shape}_{variant}` (e.g., `ocean_octopus_body`)
   - Alternative: Shorter names? (e.g., `oct_body`)

---

## Success Criteria

1. ✅ OceanShapes uses gradients by default
2. ✅ CarShapes uses gradients by default
3. ✅ All existing tests pass
4. ✅ New gradient tests added
5. ✅ Browser tests verify visual rendering
6. ✅ Documentation updated with gradient examples
7. ✅ Lessons showcase gradient effects
8. ✅ Backward compatible for color overrides
9. ✅ No performance regression

---

## Timeline Estimate

- **Phase 1** (Core Infrastructure): 2-3 hours
- **Phase 2** (Helper Updates): 2-3 hours
- **Phase 3** (Testing): 2-3 hours
- **Documentation**: 1-2 hours

**Total**: 7-11 hours of development time

---

## References

- Canvas gradient implementation: `sketchpy/canvas.py:127-196`
- OceanShapes current implementation: `sketchpy/helpers/ocean.py`
- CarShapes current implementation: `sketchpy/helpers/cars.py`
- SVG gradient spec: https://www.w3.org/TR/SVG11/pservers.html
