## 🎯 Your Turn: Custom Vehicles

### Goal
Use variables to create your own custom vehicle scene.

### Your Mission
Create variables and draw at least 3 different vehicles on the road.

### Steps
1. Create variables for each vehicle:
   - Position (x, y)
   - Size (width, height)
   - Color
2. Use CarShapes methods:
   - `cars.simple_car()` - classic car
   - `cars.rounded_car()` - modern sedan
   - `cars.sports_car()` - sleek sports car
   - `cars.bus()` - city bus
3. Draw the road and vehicles

### Example Pattern
```python
# Variables for first car
car1_x = ???
car1_y = ???
car1_color = Color.???

# Draw it
cars.rounded_car(can, car1_x, car1_y, color=car1_color)
```

### Tips
- Road position: y=400 or y=450
- Car y positions: about 50 pixels above road
- Spacing: Leave 100-200 pixels between vehicles
- Available colors: RED, BLUE, GREEN, YELLOW, PURPLE, ORANGE

### Challenge
- Use 5 different vehicles
- Create a two-lane road with cars on both lanes
- Make vehicles different sizes using width/height variables
