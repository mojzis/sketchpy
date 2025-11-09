from sketchpy import Canvas, Color
from sketchpy.helpers.cars import CarShapes

# Create a canvas (800 pixels wide, 600 pixels tall)
can = Canvas(800, 600)

# Create car drawing helper
cars = CarShapes()

# Draw a road
cars.road(can, y=400, lane_width=80)

# Draw a modern curvy car
cars.rounded_car(can, x=200, y=350, width=140, height=50, color=Color.BLUE)

can
