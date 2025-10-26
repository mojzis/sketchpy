## 🌸 Project 1: Draw Your First Flower

### Goal
Draw a simple stylized flower using circles and ellipses.

### What you'll learn
- Creating a canvas
- Drawing circles and ellipses
- Using the CreativeGardenPalette
- Positioning shapes with coordinates

### Autocomplete Tip
Type `can.` to see Canvas methods! Press **Tab** or **Enter** to insert working example code with all parameters. Then customize the values!

### Steps
1. Create a canvas: `can = Canvas(800, 600)`
2. Draw petals using circles or ellipses
3. Add a center circle for the flower
4. Draw a stem and leaves

### Coordinate System
The canvas coordinates start at the top-left (0, 0). X increases to the right, Y increases downward.

### Available Methods
- `can.circle(x, y, radius, fill=...)`
- `can.ellipse(x, y, rx, ry, fill=...)`
- `can.rect(x, y, width, height, fill=...)`
- `can.line(x1, y1, x2, y2, stroke=...)`
- `can.grid(spacing=50)` - Show coordinate grid
- `can.show_palette(PaletteClass)` - Display palette colors

### Creative Garden Palette
`CreativeGardenPalette.ROSE_QUARTZ`, `BUTTER_YELLOW`, `MINT_CREAM`, `SKY_BREEZE`, `LILAC_DREAM`, `CORAL_BLUSH`

### Tip
Try `can.show_palette(CreativeGardenPalette)` to see all available colors! Also available: `CalmOasisPalette` and `Color` (basic colors).

### Challenge
Can you add more petals or change colors? Try experimenting with different positions and sizes!
