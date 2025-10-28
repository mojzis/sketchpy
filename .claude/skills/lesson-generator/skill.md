---
name: lesson-generator
description: Generate new Python drawing lessons for sketchpy curriculum. Use when user wants to create lessons, add lessons, generate lesson content, or extend the curriculum with new programming concepts and drawing themes.
allowed_tools:
  - Read
  - Write
  - Edit
  - TodoWrite
  - AskUserQuestion
  - Bash
  - Glob
  - Grep
  - Task
---

# Lesson Generator for sketchpy

Generate new Python drawing lessons following the established 15-lesson curriculum structure.

## When This Skill Activates

- User says "create a lesson about {topic}"
- User provides a lesson specification list
- User says "generate lesson {number}"
- User wants to extend the curriculum

## Required Information

Get from user before starting:
1. **Lesson ID** (e.g., `06-parking-lot`)
2. **Theme** - User must provide or reference a theme document that defines:
   - Theme name and visual style
   - Typical shapes and elements
   - Recommended color palettes
   - Progression examples (simple → complex)
3. **Programming Concept** (e.g., "for loops and range()")
4. **Drawing Goal** (e.g., "5 objects in a row")
5. **Curriculum Level**:
   - Level 1 (Lessons 1-5): Foundations (variables, expressions, conditionals)
   - Level 2 (Lessons 6-10): Control Flow (loops, lists, compound conditions)
   - Level 3 (Lessons 11-15): Functions (parameters, return values, data structures)

**Note:** Theme documents are separate from this skill. User must provide theme guidance or reference an existing theme document.

## File Structure to Generate

```
themes/theme-1
└── {lesson-id}/
    ├── lesson.md                   # CREATE: Instructions
    ├── starter.py                  # CREATE: Initial code
    └── help.md                     # CREATE: Reference and troubleshooting
```

**Note:** lessons.yaml is generated automatically - don't create or modify it.

## Generation Steps

### Step 1: Verify Prerequisites

Check existing lessons:
```bash
view /mnt/project/ description:"Check lesson structure"
```

Identify:
- Last lesson number
- What concepts students already learned
- Which lessons this builds on

### Step 2: Generate lesson.md

**Structure:**
```markdown
# {Title}

## What You'll Learn
- **Programming:** {Concept list}
- **Drawing:** {Visual concepts}

## {Concept Introduction}
{Why this concept matters, with analogy or motivation}

## Instructions

### Step 1: {Basic Version}
{Clear explanation}

```python
{Complete working example with comments}
```

**Try it:** {Specific thing to modify}

### Step 2: {Add Complexity}
{Build on step 1}

```python
{Extended example}
```

**Try it:** {Experiment}

### Step 3: {Complete Version}
{Achieve the lesson goal}

**Challenge:** {Extension task that requires thinking}

## Common Issues

### Issue: {Typical problem}
**Solution:** {How to fix}
```

**Writing Guidelines:**
- 2nd person ("You'll learn...")
- Short paragraphs (2-4 sentences)
- Complete code examples (must run)
- Inline comments explaining WHY
- Specific "Try it" prompts
- Achievable challenges

**Code Examples Must:**
- Run without errors
- Show the concept clearly
- Build progressively
- Include helpful comments

### Step 3: Generate starter.py

**Template structure:**
```python
from sketchpy.shapes import Canvas, Color{, Palette if needed}


def main():
    # {Brief description of what to do}

    can = Canvas(800, 600)

    # Draw a coordinate grid to help with positioning
    can.grid(spacing=50, show_coords=True)

    # {Variable setup with comments}
    
    # {Working example code that demonstrates the concept}
    # Include multiple examples if teaching multiple things
    
    # {More code with inline comments explaining WHY}

    # Your turn! {Specific invitation to modify or extend}

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-{lesson-number}.svg')
```

**Rules:**
- Wrap everything in `main()` function that returns canvas
- Always include grid for positioning help
- Provide WORKING code that demonstrates the concept (not just TODOs)
- Use inline comments to explain the logic
- End with encouraging comment inviting modification
- Include debug block with correct lesson number
- Import ONLY what's needed for this lesson
- Use appropriate palette (CreativeGardenPalette for flowers, etc.)

**Example for Lesson 06 (For Loops):**
```python
from sketchpy.shapes import Canvas, Color


def main():
    # Draw multiple cars using a for loop

    can = Canvas(800, 600)
    can.grid(spacing=50, show_coords=True)

    # Draw 5 cars in a row
    for i in range(5):
        x = 50 + i * 150  # Each car is 150 pixels apart
        
        # Car body
        can.rect(x, 300, 120, 80, fill=Color.RED)
        
        # Wheels (positioned relative to car)
        can.circle(x + 30, 390, 25, fill=Color.BLACK)
        can.circle(x + 90, 390, 25, fill=Color.BLACK)

    # Your turn! Try changing the number of cars, spacing, or colors!
    # Challenge: Can you make each car a different color?

    return can


if __name__ == '__main__':
    from pathlib import Path
    Path('debug_out').mkdir(exist_ok=True)
    canvas = main()
    canvas.save('debug_out/output-06.svg')
```

### Step 4: Generate help.md

Always create a help file with:

**Content to include:**
- **Quick Reference**: Syntax reminders for the new concept
- **Common Errors**: Actual error messages with plain-English explanations
- **Debugging Tips**: How to troubleshoot when code doesn't work
- **Related Lessons**: What this builds on, what comes next
- **Extra Challenges**: Optional extensions for advanced students
- **Color Palette Reference**: If using special palettes, show available colors

**Structure:**

```markdown
# Help: {Title}

## Quick Reference

### {Concept}
{Brief syntax reminder}

## Common Errors

### Error: {Actual error message}
**What it means:** {Plain English}
**How to fix:** {Steps}

## Debugging Tips
1. {Strategy}
2. {Strategy}

## Related Lessons
- Lesson {X}: {Builds on this}
```

**Example help.md for Lesson 06 (For Loops):**

````markdown
# Help: Drawing a Parking Lot with For Loops

## Quick Reference

### For Loop Syntax
```python
for i in range(5):  # Runs 5 times: i = 0, 1, 2, 3, 4
    # Code here runs each time
    # Use i to calculate positions
```

### Calculating Positions
```python
x = start_position + i * spacing
# Example: x = 50 + i * 150
# Loop 0: x = 50, Loop 1: x = 200, Loop 2: x = 350
```

## Common Errors

### Error: "NameError: name 'i' is not defined"
**What it means:** You're trying to use `i` outside the for loop
**How to fix:** Make sure `i` is only used inside the indented block

### Error: All cars appear in the same spot
**What it means:** You're not using `i` to change the position
**How to fix:** Use `i` in your position calculation: `x = 50 + i * 150`

## Debugging Tips
1. Print the loop variable to see values: `print(f"i = {i}, x = {50 + i * 150}")`
2. Start with 2 or 3 loops instead of 5 to make testing faster
3. Use `can.grid()` to verify positions visually

## Related Lessons
- **Lesson 2:** Expressions and arithmetic - the math used here
- **Next:** Lesson 7 uses lists to store different values for each iteration

## Extra Challenges
- Make each car a different color using a list
- Create a two-row parking lot with nested loops
- Vary the car sizes as they progress
````

## Using Theme Documents

Each theme should be documented separately (e.g., `themes/cars.md`, `themes/flowers.md`). When generating a lesson, reference the appropriate theme document to understand:

**What a theme document should include:**
- **Visual Style**: Overall aesthetic and drawing approach
- **Core Elements**: Basic shapes and objects for this theme
- **Color Palettes**: Recommended Color and Palette classes to use
- **Progression Pattern**: How complexity builds (L1-5 → L6-10 → L11-15)
- **Example Shapes**: Code patterns for common theme elements
- **Terminology**: Theme-specific vocabulary

**How to use theme documents:**
1. Ask user which theme or check if theme document exists
2. Read theme document if available: `view /mnt/project/themes/{theme-name}.md`
3. Use theme's visual style, colors, and progression in generated lessons
4. Follow theme's example patterns for starter.py code
5. Use theme-appropriate terminology in lesson.md

**If no theme document exists:**
- Ask user to provide theme guidance (visual style, typical shapes, colors)
- Or suggest creating a theme document first before generating lessons

**Example theme document structure:**
```markdown
# Theme Name

## Visual Style
{Description of aesthetic}

## Core Elements
- Element 1: {Description and code pattern}
- Element 2: {Description and code pattern}

## Recommended Colors
- Palette: {CreativeGardenPalette, CalmOasisPalette, Color}
- Typical colors: {List}

## Progression
- L1-5: {Simple shapes}
- L6-10: {Multiple objects, patterns}
- L11-15: {Functions, complex scenes}

## Example Code Patterns
{Common code snippets for this theme}
```

## Quality Checklist

Before completing:
- [ ] starter.py runs without errors
- [ ] lesson.md has clear objectives
- [ ] Code examples are complete and commented
- [ ] "Try it" prompts are specific
- [ ] Challenge is achievable but requires thought
- [ ] Theme is consistent
- [ ] Builds on previous lessons
- [ ] Programming concept is clear
- [ ] Visual goal is interesting

## Validation (Required)

**Lesson generation is not complete until starter.py runs successfully.**

After generating files, automatically test:
1. **Syntax check:** Run `uv run python lessons/{id}/starter.py`
   - Must execute without errors
   - If errors found: Fix and regenerate the file
2. **Concept check:** Verify programming concept is demonstrated
3. **Theme check:** Verify visual output matches theme
4. **Progression check:** Ensure it builds on prior lessons

Do not mark work as complete until starter.py executes successfully.

## Example Workflow

**User Request:**
"Create a lesson about while loops using the cars theme"

**Your Response:**
1. Check for theme document and ask clarifying questions:
   - "Let me check if themes/cars.md exists..." (use view tool)
   - If found: "I found the cars theme document. What should the while loop draw? (e.g., objects until canvas full, until reaching edge)"
   - If not found: "I don't see a theme document for 'cars'. Can you provide theme guidance (visual style, typical shapes, colors) or would you like to create a theme document first?"
   - "This would be Lesson 9 (Level 2: Control Flow). Should I proceed?"

2. Generate files:
   - Create lessons/09-traffic-jam/lesson.md
   - Create lessons/09-traffic-jam/starter.py
   - Create lessons/09-traffic-jam/help.md

3. Show summary:
   ```
   ✓ Generated Lesson 9: Traffic Jam (While Loops)
   ✓ Created 3 files in lessons/09-traffic-jam/
   
   Concept: While loops with condition-based drawing
   Goal: Draw objects until x reaches edge
   Theme: Cars (from themes/cars.md)
   ```

4. Test starter.py automatically:
   - Run `python lessons/09-traffic-jam/starter.py` to verify it works
   - If errors: Fix them and regenerate
   - Only complete once starter.py runs successfully

## Notes

- Follow established patterns from curriculum
- Balance teaching programming with creating art
- Keep visual output achievable in 60-90 minutes
- Progressive complexity within each lesson
- Clear error messages and debugging guidance