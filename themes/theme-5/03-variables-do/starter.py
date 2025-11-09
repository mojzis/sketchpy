from sketchpy import Canvas, Color
from sketchpy.helpers.cars import CarShapes

can = Canvas(800, 600)
cars = CarShapes()

# Draw your road here
cars.road(can, y=450, lane_width=80)

# Create your variables and draw vehicles here
# Example:
# my_car_x = 100
# my_car_y = 400
# my_car_color = Color.BLUE
# cars.rounded_car(can, my_car_x, my_car_y, color=my_car_color)

can
