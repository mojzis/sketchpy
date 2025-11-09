from sketchpy import Canvas, Color
from sketchpy.helpers.cars import CarShapes

can = Canvas(800, 600)
cars = CarShapes()

# Draw your road
cars.road(can, y=400, lane_width=80)

# Create your loop with conditionals here
# for i in range(???):
#     x = ??? + i * ???
#
#     if ???:
#         # Draw one thing
#     else:
#         # Draw another thing

can
