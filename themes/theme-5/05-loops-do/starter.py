from sketchpy import Canvas, Color
from sketchpy.helpers.cars import CarShapes

can = Canvas(800, 600)
cars = CarShapes()

# Draw your road
cars.road(can, y=400, lane_width=80)

# Create your loop here
# Example:
# for i in range(???):
#     x = ??? + i * ???
#     cars.rounded_car(can, x, 350, color=Color.BLUE)

can
