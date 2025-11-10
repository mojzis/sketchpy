## 🎁 Functions: Package Code for Reuse

### Goal
Learn how functions let you name and reuse chunks of code.

### What You'll Learn
- Functions are named blocks of code
- Parameters let you customize each use
- Functions make code organized and reusable
- Call a function many times with different values

### What's a Function?
A function is like a recipe. You write it once, then use it many times:

```python
def draw_traffic_light_scene(x, y):
    """Draw a traffic light with a waiting car"""
    cars.traffic_light(can, x, y, active="red")
    cars.simple_car(can, x + 100, y + 140, width=100)
```

Now you can call it:
```python
draw_traffic_light_scene(100, 50)  # First intersection
draw_traffic_light_scene(500, 50)  # Second intersection
```

### The Demo Shows
- A function that draws a complete intersection
- Parameters for customization (position, car color)
- Calling the function multiple times
- Building complex scenes from simple functions

### Try This
1. Run the code - see the intersections
2. Add a third intersection by calling the function again
3. Change the car_color parameter
4. Change what's inside the function

### Challenge
Create your own function that draws a car with traffic cones around it.
