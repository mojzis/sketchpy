from sketchpy import Canvas, Color
from sketchpy.helpers.cars import CarShapes

can = Canvas(800, 600)
cars = CarShapes()

# Draw road
cars.road(can, y=400, lane_width=80)

# Alternating car types and colors
for i in range(6):
    x = 50 + i * 120

    if i % 2 == 0:  # Even positions
        cars.rounded_car(can, x, 350, color=Color.BLUE)
    else:  # Odd positions
        cars.sports_car(can, x, 355, color=Color.RED)

# Traffic lights with different states
cars.traffic_light(can, 100, 100, active="red")
cars.traffic_light(can, 400, 100, active="yellow")
cars.traffic_light(can, 700, 100, active="green")

can
