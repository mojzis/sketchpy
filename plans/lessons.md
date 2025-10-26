# Python Drawing Curriculum: Learn Programming Through Art

**Philosophy:** Every programming concept is hidden inside a visual project. Students choose their theme (cars, flowers, abstract art) but learn identical programming fundamentals. The theme provides motivation; the code provides skills.

## Curriculum Structure

**Duration:** 15 lessons, ~1 week each (60-90 minutes per session)
**Target:** High school beginners (ages 14-18)
**Approach:** Project-based, immediate visual feedback, progressive difficulty

---

## LEVEL 1: FOUNDATIONS (Lessons 1-5)
*Core concepts: Variables, basic types, simple operations, method calls*

### Lesson 1: First Shapes & Variables
**Programming Concepts:** Variables, numbers, strings, method calls
**Python Features:** Assignment (`=`), numeric types (int/float), calling methods with parameters

**Drawing Goal by Theme:**

| Theme | Project | Key Shapes |
|-------|---------|------------|
| **🚗 Cars** | Simple garage door | Rectangle |
| **🌸 Flowers** | Flower pot | Rectangle, circle |
| **🎨 Abstract** | Mondrian-style grid | Multiple rectangles |

**Code Pattern:**
```python
# Variables hold values
width = 200
height = 150
x_position = 100
y_position = 200

can = Canvas(800, 600)
can.rect(x_position, y_position, width, height, fill=Color.RED)
can
```

**Learning Objectives:**
- Understand that variables store values
- Change numbers to see different results
- Recognize that method calls need specific information (parameters)
- Experiment with different values

**Challenge:** Make your shape twice as big by changing the variables.

---

### Lesson 2: Colors & Expressions
**Programming Concepts:** Expressions, arithmetic operations, color values
**Python Features:** Math operators (`+`, `-`, `*`, `/`), expressions in parameters

**Drawing Goal by Theme:**

| Theme | Project | Concept |
|-------|---------|---------|
| **🚗 Cars** | Two-tone car body | Two rectangles, calculated positions |
| **🌸 Flowers** | Flower with stem | Rectangle stem, calculated circle position |
| **🎨 Abstract** | Color gradient blocks | Multiple rectangles with spacing |

**Code Pattern:**
```python
# Use math to calculate positions
body_width = 300
body_height = 100
body_x = 200
body_y = 300

# Calculate where roof should go (centered above body)
roof_x = body_x + 75  # Indent from body edges
roof_y = body_y - 60  # Above the body

can = Canvas(800, 600)
can.rect(body_x, body_y, body_width, body_height, fill=Color.RED)
can.rect(roof_x, roof_y, body_width / 2, 60, fill=Color.BLUE)
can
```

**Learning Objectives:**
- Use arithmetic to calculate positions
- Understand expressions evaluate to values
- See how changing one variable affects calculated values
- Use division to make proportional shapes

**Challenge:** Add a third shape positioned relative to the first two.

---

### Lesson 3: Multiple Shapes & Method Chaining
**Programming Concepts:** Method chaining, object-oriented basics, comments
**Python Features:** Dot notation, method chaining (`.method().method()`), `#` comments

**Drawing Goal by Theme:**

| Theme | Project | Concept |
|-------|---------|---------|
| **🚗 Cars** | Complete simple car | Body + 2 wheels + 2 windows |
| **🌸 Flowers** | Five-petal flower | Center circle + 5 petals |
| **🎨 Abstract** | Concentric circles | Multiple circles, same center |

**Code Pattern:**
```python
# Comments explain code
can = Canvas(800, 600)

# Method chaining - multiple shapes in sequence
can.rect(200, 300, 300, 100, fill=Color.RED)\
   .circle(250, 420, 40, fill=Color.BLACK)\
   .circle(450, 420, 40, fill=Color.BLACK)\
   .rect(250, 310, 60, 50, fill=Color.BLUE)\
   .rect(390, 310, 60, 50, fill=Color.BLUE)

can
```

**Learning Objectives:**
- Call multiple methods on the same object
- Understand that methods can return the object itself
- Use comments to document code
- Build complex drawings from simple shapes

**Challenge:** Add more details (headlights, door handles, extra petals).

---

### Lesson 4: String Operations & Text
**Programming Concepts:** Strings, concatenation, f-strings
**Python Features:** String type, `+` for concatenation, f-strings for formatting

**Drawing Goal by Theme:**

| Theme | Project | Concept |
|-------|---------|---------|
| **🚗 Cars** | Labeled car parts | Car with text labels |
| **🌸 Flowers** | Flower name tags | Flowers with species names |
| **🎨 Abstract** | Titled artwork | Art piece with dynamic title |

**Code Pattern:**
```python
# Strings hold text
car_type = "Sports Car"
car_year = 2024
max_speed = 200

can = Canvas(800, 600)

# Draw car
can.rect(200, 300, 300, 100, fill=Color.RED)

# Add labels with f-strings
can.text(350, 280, f"{car_type} ({car_year})", size=20, fill=Color.BLACK)
can.text(350, 450, f"Top Speed: {max_speed} km/h", size=16, fill=Color.GRAY)

can
```

**Learning Objectives:**
- Store text in variables
- Combine strings with `+` and f-strings
- Display text on canvas
- Use f-strings to mix text and numbers

**Challenge:** Create a "specification sheet" with 5+ labeled details.

---

### Lesson 5: Boolean Logic & Conditionals (Part 1)
**Programming Concepts:** Booleans, comparison operators, simple if statements
**Python Features:** `True`/`False`, `==`, `>`, `<`, `if`/`else`

**Drawing Goal by Theme:**

| Theme | Project | Concept |
|-------|---------|---------|
| **🚗 Cars** | Day/night scene | Different sky color based on time |
| **🌸 Flowers** | Seasonal flowers | Different flower colors by season |
| **🎨 Abstract** | Mood-based colors | Color palette changes by mood |

**Code Pattern:**
```python
# Boolean variables
is_night = True
speed = 150

can = Canvas(800, 600)

# Conditional drawing - different results based on conditions
if is_night:
    can.rect(0, 0, 800, 600, fill="#001122")  # Dark sky
    can.circle(700, 100, 40, fill=Color.YELLOW)  # Moon
else:
    can.rect(0, 0, 800, 600, fill="#87CEEB")  # Blue sky
    can.circle(700, 100, 40, fill=Color.YELLOW)  # Sun

# Draw car (same either way)
can.rect(200, 400, 300, 100, fill=Color.RED)

# Show different message
if speed > 120:
    can.text(350, 550, "SPEEDING!", size=24, fill=Color.RED)
else:
    can.text(350, 550, "Safe speed", size=24, fill=Color.GREEN)

can
```

**Learning Objectives:**
- Understand True/False values
- Use comparison operators
- Make decisions with if/else
- See how code can produce different results

**Challenge:** Add three conditions (if/elif/else) for morning/afternoon/night.

---

## LEVEL 2: CONTROL FLOW (Lessons 6-10)
*Core concepts: Loops, lists, more conditionals, compound logic*

### Lesson 6: For Loops - Repetition
**Programming Concepts:** For loops, range(), iteration
**Python Features:** `for`, `range()`, loop variables, indentation

**Drawing Goal by Theme:**

| Theme | Project | Concept |
|-------|---------|---------|
| **🚗 Cars** | Parking lot | 5 cars in a row |
| **🌸 Flowers** | Garden row | 8 flowers in a line |
| **🎨 Abstract** | Pattern repetition | Repeating geometric pattern |

**Code Pattern:**
```python
can = Canvas(800, 600)

# Draw multiple cars without repeating code
for i in range(5):
    x_position = 50 + i * 150  # Each car 150 pixels apart
    
    # Draw car at calculated position
    can.rect(x_position, 300, 120, 80, fill=Color.RED)
    can.circle(x_position + 30, 390, 25, fill=Color.BLACK)
    can.circle(x_position + 90, 390, 25, fill=Color.BLACK)

can
```

**Learning Objectives:**
- Use loops to avoid repetitive code
- Understand loop variables (i)
- Calculate positions based on loop variable
- See power of repetition

**Challenge:** Create a 3x3 grid (nested loops preview).

---

### Lesson 7: Lists - Collections
**Programming Concepts:** Lists, indexing, iterating over lists
**Python Features:** `[]`, `list[index]`, `for item in list`, `len()`

**Drawing Goal by Theme:**

| Theme | Project | Concept |
|-------|---------|---------|
| **🚗 Cars** | Multi-colored car fleet | Each car different color from list |
| **🌸 Flowers** | Rainbow garden | Each flower different color |
| **🎨 Abstract** | Color palette showcase | Grid showing each color |

**Code Pattern:**
```python
# Lists hold multiple values
colors = [Color.RED, Color.BLUE, Color.GREEN, Color.YELLOW, Color.ORANGE]
sizes = [100, 120, 90, 110, 95]

can = Canvas(800, 600)

# Loop through list with enumerate to get index and value
for i, color in enumerate(colors):
    x = 50 + i * 150
    size = sizes[i]  # Access list by index
    
    can.circle(x, 300, size / 2, fill=color)

can
```

**Learning Objectives:**
- Store multiple values in a list
- Access items by index
- Loop through lists
- Understand list length with len()

**Challenge:** Create lists of car properties (width, height, color) and draw varied cars.

---

### Lesson 8: Nested Loops - Grids
**Programming Concepts:** Nested loops, 2D positioning
**Python Features:** Loop inside loop, calculating row/column positions

**Drawing Goal by Theme:**

| Theme | Project | Concept |
|-------|---------|---------|
| **🚗 Cars** | Multi-story parking garage | Grid of cars (3 rows × 4 cols) |
| **🌸 Flowers** | Flower field | Grid of flowers |
| **🎨 Abstract** | Checkerboard/tile pattern | Alternating colored squares |

**Code Pattern:**
```python
can = Canvas(800, 600)

# Nested loops create grids
for row in range(3):
    for col in range(4):
        x = 50 + col * 180
        y = 100 + row * 180
        
        # Alternating colors
        if (row + col) % 2 == 0:
            color = Color.RED
        else:
            color = Color.BLUE
        
        can.rect(x, y, 150, 100, fill=color)
        can.circle(x + 40, y + 110, 20, fill=Color.BLACK)
        can.circle(x + 110, y + 110, 20, fill=Color.BLACK)

can
```

**Learning Objectives:**
- Use nested loops for 2D patterns
- Calculate grid positions
- Combine loops with conditionals
- Create complex patterns from simple rules

**Challenge:** Make the pattern change based on position (gradient effect).

---

### Lesson 9: While Loops & Conditions
**Programming Concepts:** While loops, loop control, counters
**Python Features:** `while`, loop conditions, `break`, `continue`

**Drawing Goal by Theme:**

| Theme | Project | Concept |
|-------|---------|---------|
| **🚗 Cars** | Traffic jam (random spacing) | Cars until canvas full |
| **🌸 Flowers** | Growing vine | Flowers until reaching edge |
| **🎨 Abstract** | Spiral pattern | Drawing until size limit |

**Code Pattern:**
```python
can = Canvas(800, 600)

x = 50
y = 300

# Draw cars until we run out of space
while x < 750:
    can.rect(x, y, 100, 60, fill=Color.RED)
    can.circle(x + 25, y + 70, 15, fill=Color.BLACK)
    can.circle(x + 75, y + 70, 15, fill=Color.BLACK)
    
    # Variable spacing (could add randomness later)
    x = x + 120
    
    # Optional: vary the y position slightly
    if x > 400:
        y = y + 20

can
```

**Learning Objectives:**
- Use while for condition-based loops
- Update loop variables
- Understand loop exit conditions
- Compare while vs for loops

**Challenge:** Add a counter to stop after exactly 6 cars.

---

### Lesson 10: Compound Conditions
**Programming Concepts:** Logical operators, complex conditionals
**Python Features:** `and`, `or`, `not`, parentheses for grouping

**Drawing Goal by Theme:**

| Theme | Project | Concept |
|-------|---------|---------|
| **🚗 Cars** | Smart traffic system | Light color based on multiple factors |
| **🌸 Flowers** | Seasonal garden | Flowers that need specific conditions |
| **🎨 Abstract** | Rule-based art | Complex pattern rules |

**Code Pattern:**
```python
time_of_day = "morning"
is_weekend = True
traffic_level = 75

can = Canvas(800, 600)

# Complex conditions determine what to draw
if time_of_day == "morning" and is_weekend:
    can.text(400, 50, "Leisure Drive", size=24)
    car_color = Color.BLUE
elif traffic_level > 70 or time_of_day == "evening":
    can.text(400, 50, "Rush Hour!", size=24, fill=Color.RED)
    car_color = Color.GRAY
else:
    can.text(400, 50, "Normal Traffic", size=24)
    car_color = Color.GREEN

# Draw car with determined color
can.rect(300, 300, 200, 100, fill=car_color)

can
```

**Learning Objectives:**
- Combine multiple conditions with and/or
- Use not to invert conditions
- Build complex decision trees
- Model real-world logic in code

**Challenge:** Create a weather + season + time system with 8+ conditions.

---

## LEVEL 3: FUNCTIONS & MODULARITY (Lessons 11-15)
*Core concepts: Functions, parameters, return values, code organization*

### Lesson 11: Basic Functions
**Programming Concepts:** Function definition, calling functions, code reuse
**Python Features:** `def`, function names, calling with `()`

**Drawing Goal by Theme:**

| Theme | Project | Concept |
|-------|---------|---------|
| **🚗 Cars** | Draw different car types | Functions: sedan(), truck(), sports_car() |
| **🌸 Flowers** | Draw flower types | Functions: rose(), tulip(), sunflower() |
| **🎨 Abstract** | Reusable patterns | Functions: star(), spiral(), grid_square() |

**Code Pattern:**
```python
can = Canvas(800, 600)

# Define a function - recipe for drawing a car
def draw_simple_car(canvas):
    canvas.rect(200, 300, 200, 80, fill=Color.RED)
    canvas.circle(250, 390, 25, fill=Color.BLACK)
    canvas.circle(350, 390, 25, fill=Color.BLACK)

def draw_truck(canvas):
    canvas.rect(200, 280, 250, 120, fill=Color.BLUE)
    canvas.rect(400, 250, 80, 150, fill=Color.BLUE)
    canvas.circle(250, 410, 30, fill=Color.BLACK)
    canvas.circle(380, 410, 30, fill=Color.BLACK)

# Call functions to use them
draw_simple_car(can)

can
```

**Learning Objectives:**
- Define functions with `def`
- Understand functions as reusable code blocks
- Call functions to execute them
- Pass canvas as parameter

**Challenge:** Create 3 unique vehicle functions.

---

### Lesson 12: Functions with Parameters
**Programming Concepts:** Parameters, arguments, function flexibility
**Python Features:** Parameters in definition, passing arguments, default values

**Drawing Goal by Theme:**

| Theme | Project | Concept |
|-------|---------|---------|
| **🚗 Cars** | Customizable car | draw_car(x, y, color, size) |
| **🌸 Flowers** | Variable flowers | draw_flower(x, y, petals, color) |
| **🎨 Abstract** | Parameterized patterns | draw_pattern(x, y, size, rotation) |

**Code Pattern:**
```python
can = Canvas(800, 600)

def draw_car(canvas, x, y, width, color):
    """Draw a car at position (x, y) with given width and color."""
    height = width * 0.5  # Proportional height
    
    # Body
    canvas.rect(x, y, width, height, fill=color, stroke=Color.BLACK, stroke_width=2)
    
    # Wheels (positioned relative to car size)
    wheel_radius = height * 0.3
    canvas.circle(x + width * 0.25, y + height + wheel_radius, wheel_radius, fill=Color.BLACK)
    canvas.circle(x + width * 0.75, y + height + wheel_radius, wheel_radius, fill=Color.BLACK)

# Now we can draw many different cars!
draw_car(can, 50, 200, 150, Color.RED)
draw_car(can, 250, 250, 200, Color.BLUE)
draw_car(can, 500, 180, 100, Color.GREEN)

can
```

**Learning Objectives:**
- Add parameters to make functions flexible
- Pass different arguments for different results
- Use default parameter values
- Calculate proportional measurements

**Challenge:** Add more parameters (wheel_color, has_windows, etc.).

---

### Lesson 13: Return Values
**Programming Concepts:** Return statements, using function results
**Python Features:** `return`, capturing return values, function composition

**Drawing Goal by Theme:**

| Theme | Project | Concept |
|-------|---------|---------|
| **🚗 Cars** | Car factory | Function returns car specifications |
| **🌸 Flowers** | Flower calculator | Function returns petal positions |
| **🎨 Abstract** | Pattern generator | Function returns color/size calculations |

**Code Pattern:**
```python
can = Canvas(800, 600)

def calculate_wheel_positions(car_x, car_y, car_width):
    """Calculate where wheels should be placed.
    Returns a list of (x, y) tuples."""
    wheel_y = car_y + 80
    front_wheel_x = car_x + car_width * 0.25
    rear_wheel_x = car_x + car_width * 0.75
    
    return [(front_wheel_x, wheel_y), (rear_wheel_x, wheel_y)]

def get_car_color(speed):
    """Return appropriate color based on speed."""
    if speed > 150:
        return Color.RED
    elif speed > 100:
        return Color.ORANGE
    else:
        return Color.BLUE

# Use returned values
speed = 180
car_color = get_car_color(speed)
car_x = 200
car_width = 250

can.rect(car_x, 300, car_width, 80, fill=car_color)

# Get wheel positions and draw them
wheel_positions = calculate_wheel_positions(car_x, 300, car_width)
for x, y in wheel_positions:
    can.circle(x, y, 25, fill=Color.BLACK)

can
```

**Learning Objectives:**
- Return values from functions
- Use returned values in other code
- Understand functions as calculations
- Compose functions together

**Challenge:** Create a function that returns a dictionary of car properties.

---

### Lesson 14: Lists + Functions - Building Scenes
**Programming Concepts:** Combining lists and functions, data structures
**Python Features:** List comprehensions (intro), dictionaries (intro)

**Drawing Goal by Theme:**

| Theme | Project | Concept |
|-------|---------|---------|
| **🚗 Cars** | Dynamic traffic scene | List of car data, draw all |
| **🌸 Flowers** | Garden from plan | List of flower specs, create garden |
| **🎨 Abstract** | Generative art | List of pattern rules, apply all |

**Code Pattern:**
```python
can = Canvas(800, 600)

def draw_car(canvas, car_data):
    """Draw a car from a dictionary of properties."""
    canvas.rect(
        car_data['x'], 
        car_data['y'], 
        car_data['width'], 
        car_data['height'],
        fill=car_data['color']
    )
    
    # Wheels
    wheel_y = car_data['y'] + car_data['height'] + 15
    canvas.circle(car_data['x'] + 30, wheel_y, 20, fill=Color.BLACK)
    canvas.circle(car_data['x'] + car_data['width'] - 30, wheel_y, 20, fill=Color.BLACK)

# Data-driven drawing - separate data from display logic
cars_in_scene = [
    {'x': 50, 'y': 300, 'width': 150, 'height': 80, 'color': Color.RED},
    {'x': 250, 'y': 320, 'width': 180, 'height': 90, 'color': Color.BLUE},
    {'x': 480, 'y': 290, 'width': 140, 'height': 75, 'color': Color.GREEN},
]

# Draw all cars from data
for car in cars_in_scene:
    draw_car(can, car)

can
```

**Learning Objectives:**
- Separate data from logic
- Use dictionaries for structured data
- Process lists of complex objects
- Build scalable programs

**Challenge:** Add a function that generates random car data.

---

### Lesson 15: Final Project - Complete Scene
**Programming Concepts:** Integration, project planning, all previous concepts
**Python Features:** Everything learned, organized code, comments

**Drawing Goal by Theme:**

| Theme | Project | Complexity |
|-------|---------|------------|
| **🚗 Cars** | City traffic simulation | Multiple car types, roads, buildings, traffic lights |
| **🌸 Flowers** | Complete garden landscape | Different flower types, varying sizes, background |
| **🎨 Abstract** | Algorithmic art piece | Multiple pattern types, color schemes, composition |

**Success criteria:** Student creates a complete scene using at least 5 functions, 2 loops, conditionals, and lists/dictionaries. Code is well-commented and organized.

---

## Cross-Theme Skills Matrix

Every lesson teaches identical programming concepts regardless of theme choice:

| Lesson | Core Skill | All Themes Learn |
|--------|-----------|------------------|
| 1-5 | Foundations | Variables, expressions, conditionals |
| 6-10 | Control Flow | Loops, lists, compound logic |
| 11-15 | Functions | Organization, parameters, data structures |

---

## Implementation Guide

**Session Structure (60-90 min):**
1. Concept intro (10 min)
2. Guided practice (20 min)
3. Independent work (30 min)
4. Share & reflect (10 min)

**Scaffolding:**
- Lessons 1-5: Complete starter code, modify values
- Lessons 6-10: Structure provided, fill in logic
- Lessons 11-15: Requirements only, write from scratch

**Assessment:**
- ✅ MVP: Code runs, uses target concept, produces output
- ⭐ Proficiency: Clean code, handles edge cases
- 🏆 Mastery: Completes challenge, adds creative elements

---

## Learning Outcomes

By lesson 15, students will:
- Write Python programs from scratch
- Use all fundamental programming constructs
- Organize code with functions
- Work with data structures
- Debug programs independently
- Have a portfolio of 15+ visual projects
- **Think computationally** - break problems into steps