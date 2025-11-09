# Curvy Cars Theme Plan

**Date:** 2025-11-09
**Status:** Planning Phase

## Overview

Create a new transportation-themed learning path (Theme 5) that teaches Python through drawing vehicles using the new curvy shape capabilities. Update CarShapes to use organic curves instead of rigid rectangles.

## Goals

1. **Improve CarShapes** - Leverage new Canvas methods (`blob()`, `tentacle()`, curves) for more organic car designs
2. **Create Theme 5** - "City Drivers" transportation theme following Theme 4's paired lesson approach
3. **Maintain Learning Focus** - Gradual concept introduction with "show/do" pattern

---

## Part 1: Enhanced CarShapes

### Current Implementation Issues
- Cars use basic rectangles and polygons (rigid, blocky)
- Limited visual appeal
- Doesn't showcase Canvas's new curve capabilities

### New Capabilities Available
- `blob()` - organic shapes with wobble (perfect for car bodies)
- `tentacle()` - smooth curves with curl/twist (not used for cars, but good reference)
- `wave()` - wavy lines
- `ellipse()` - already available
- `rounded_rect()` - already used but can enhance

### Proposed New CarShapes Methods

#### 1. `rounded_car()` - Modern curvy design
```python
def rounded_car(canvas, x, y, width=140, height=50, color=Color.BLUE):
    """Draw a modern car with smooth, curvy body"""
    # Main body: use blob() for organic shape
    # Use ellipse() for smoother roof/windshield
    # Circular/elliptical wheels
    # Smooth window shapes
```

**Features:**
- Blob-based body for organic feel
- Elliptical roof/windshield connection
- Larger rounded wheels
- Optional headlight/taillight circles

#### 2. `sports_car()` - Sleek, low-profile
```python
def sports_car(canvas, x, y, width=160, height=40, color=Color.RED):
    """Draw a sleek sports car with aerodynamic curves"""
    # Low, wide elliptical body
    # Curved windshield using polygon with more points
    # Small, wide wheels
    # Spoiler element
```

#### 3. `bus()` - Tall, boxy but with rounded corners
```python
def bus(canvas, x, y, width=200, height=120, color=Color.YELLOW):
    """Draw a city bus with rounded corners and windows"""
    # Large rounded_rect for body
    # Multiple windows (rounded_rect in loop)
    # Multiple wheels
    # Destination sign on top
```

#### 4. Keep Existing Methods
- `simple_car()` - Keep for backwards compatibility, maybe add slight curves
- `wheel()` - Keep as is (already good)
- `traffic_light()` - Keep as is
- `road()` - Keep as is

### Implementation Strategy
1. Keep original `simple_car()` for backwards compatibility (or enhance slightly)
2. Add new curvy car methods
3. Update method signatures to be consistent
4. Test in browser environment

---

## Part 2: Theme 5 - "City Drivers" 🚗

### Theme Metadata
```yaml
id: theme-5
name: City Drivers
icon: 🚗
description: Learn Python by creating traffic scenes with curvy cars and city streets
color_scheme: urban  # blues, grays, vibrant accent colors
```

### Lesson Structure (10 lessons)

Following Theme 4's pattern: intro → paired concepts (show/do) × 4 → final project

#### Lesson 01: Hello City (Introduction)
**Goal:** First canvas, first car, basic concepts
- Create canvas
- Draw a simple car using `rounded_car()`
- Draw a road using `road()`
- Learn about x/y coordinates

#### Lesson 02: Variables Show (Concept Introduction)
**Goal:** Show how variables control car properties
- Demo: Variables for color, size, position
- Show multiple cars with different variables
- Explain how changing one number changes everything

#### Lesson 03: Variables Do (Practice)
**Goal:** Student creates their own car with custom variables
- Create variables for car properties
- Draw custom car with their values
- Experiment with different values

#### Lesson 04: Loops Show (Concept Introduction)
**Goal:** Show how loops create patterns
- Demo: Row of cars using for loop
- Show how loop variable controls spacing
- Multiple lanes of traffic

#### Lesson 05: Loops Do (Practice)
**Goal:** Student creates traffic patterns with loops
- Create parking lot grid with loops
- Experiment with spacing
- Challenge: nested loops for rows/columns

#### Lesson 06: Functions Show (Concept Introduction)
**Goal:** Show how functions organize code
- Demo: Function to draw different car types
- Function parameters for customization
- Calling function multiple times

#### Lesson 07: Functions Do (Practice)
**Goal:** Student creates their own car drawing function
- Define function with parameters
- Call function to create scene
- Challenge: function that draws complete street scene

#### Lesson 08: Conditionals Show (Concept Introduction)
**Goal:** Show how if/else creates variety
- Demo: Traffic light that changes car behavior
- Different car types based on conditions
- Random colors/sizes with conditionals

#### Lesson 09: Conditionals Do (Practice)
**Goal:** Student creates intelligent traffic scene
- Use if/else for traffic patterns
- Alternate colors or types
- Challenge: traffic light system

#### Lesson 10: City Scene (Final Project)
**Goal:** Combine all concepts into complete city scene
- Multiple streets with cars
- Traffic lights
- Different car types
- Parking areas
- Student creativity encouraged

### Helper Class Requirements

Theme 5 will use the updated `CarShapes` class with new methods:
- `rounded_car()`
- `sports_car()`
- `bus()`
- `simple_car()` (kept/enhanced)
- `wheel()`
- `traffic_light()`
- `road()`

---

## Part 3: Implementation Plan

### Phase 1: Update CarShapes (Priority 1)
1. Read existing `sketchpy/helpers/cars.py`
2. Design new curvy methods using Canvas capabilities
3. Implement new methods
4. Keep backwards compatibility
5. Test in marimo notebook
6. Test in browser (via srv)

### Phase 2: Create Theme 5 Structure (Priority 2)
1. Create `themes/theme-5/` directory
2. Create `theme.yaml` file
3. Create lesson directories (01-10)
4. Write lesson.md for each lesson
5. Write starter.py for each lesson
6. Optional: Add help.md hints

### Phase 3: Content Development (Priority 3)
1. Write clear, beginner-friendly instructions
2. Create progressive examples
3. Test each lesson in browser
4. Ensure concepts build naturally
5. Add challenges for advanced students

### Phase 4: Testing & Refinement (Priority 4)
1. Run pytest (all tests should pass)
2. Test browser loading
3. Test lesson progression
4. Verify code examples work
5. Check theme switching
6. Get user feedback

---

## Design Principles

### Curvy Car Design
- Use organic shapes (blob, ellipse) for modern aesthetic
- Smooth transitions between body parts
- Circular/elliptical wheels (not just circles)
- Subtle details (headlights, windows) enhance without complexity

### Theme 5 Pedagogy
- **Show/Do Pattern**: Demonstrate concept, then practice
- **Gradual Complexity**: Start simple, add one concept at a time
- **Visual Feedback**: Every lesson produces visual output
- **Creative Freedom**: Final project encourages experimentation
- **Real-World Connection**: Cars and traffic are familiar to students

### Code Quality
- Keep methods simple and well-documented
- Use default parameters for ease of use
- Maintain method chaining support
- Browser-compatible (no local-only features)

---

## Success Criteria

### CarShapes Enhancement
- [ ] At least 2 new curvy car methods implemented
- [ ] Backwards compatible with existing code
- [ ] Works in browser environment
- [ ] Visually appealing and modern

### Theme 5 Creation
- [ ] 10 lessons following show/do pattern
- [ ] Clear progression from basics to complex
- [ ] All starter code runs without errors
- [ ] Lessons are engaging and age-appropriate
- [ ] Final project combines all learned concepts

### Technical Requirements
- [ ] All pytest tests pass
- [ ] Browser tests pass
- [ ] Theme appears in theme selector
- [ ] Lessons load correctly
- [ ] Code examples are syntactically correct

---

## Timeline Estimate

1. **CarShapes Enhancement**: 2-3 hours
   - Design: 30 min
   - Implementation: 1 hour
   - Testing: 30-60 min

2. **Theme Structure**: 1 hour
   - Directory setup: 15 min
   - Theme metadata: 15 min
   - Lesson scaffolding: 30 min

3. **Content Creation**: 4-5 hours
   - Lesson 01 (intro): 30 min
   - Lessons 02-09 (4 pairs): 3 hours
   - Lesson 10 (project): 1 hour

4. **Testing & Polish**: 1-2 hours
   - Technical testing: 30 min
   - Content review: 30 min
   - Refinement: 30-60 min

**Total: 8-11 hours**

---

## Open Questions

1. Should `simple_car()` be updated or left as-is for backwards compatibility?
   - **Recommendation:** Add slight curves but keep signature identical

2. How many car types are needed?
   - **Recommendation:** 3 new types (rounded, sports, bus) + keep simple

3. Should theme 5 introduce any new concepts beyond theme 4?
   - **Recommendation:** Stick with same concepts (variables, loops, functions, conditionals) but different context

4. Color scheme for theme 5?
   - **Recommendation:** Urban palette (asphalt gray, street yellow, car colors: red, blue, silver, black)

---

## Next Steps

1. Get approval on plan
2. Start with CarShapes implementation
3. Test curvy cars in isolation
4. Create theme structure
5. Write lesson content iteratively
6. Test and refine

## Notes

- Theme 4 (Ocean Explorers) is a good reference for lesson structure
- New Canvas methods (blob, wave, tentacle) open creative possibilities
- Focus on visual appeal to engage learners
- Keep code simple - this is for beginners
