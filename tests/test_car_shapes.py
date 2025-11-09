"""Tests for CarShapes helper class."""

import pytest
from sketchpy import Canvas, Color, CarShapes


class TestSimpleCar:
    """Test simple_car helper method."""

    def test_simple_car_renders(self):
        """simple_car draws without errors."""
        canvas = Canvas(600, 400)
        CarShapes.simple_car(canvas, x=100, y=200)
        svg = canvas.to_svg()

        # Should contain rectangles (body, roof parts)
        assert '<rect' in svg
        # Should contain circles (wheels)
        assert '<circle' in svg
        # Should contain polygon (roof/windshield)
        assert '<polygon' in svg

    def test_simple_car_default_color(self):
        """simple_car uses default RED color."""
        canvas = Canvas(600, 400)
        CarShapes.simple_car(canvas, x=100, y=200)
        svg = canvas.to_svg()

        assert Color.RED in svg
        assert Color.BLACK in svg  # Wheels

    def test_simple_car_custom_color(self):
        """simple_car accepts custom color."""
        canvas = Canvas(600, 400)
        CarShapes.simple_car(canvas, x=100, y=200, color=Color.BLUE)
        svg = canvas.to_svg()

        assert Color.BLUE in svg

    def test_simple_car_custom_dimensions(self):
        """simple_car accepts custom width and height."""
        canvas = Canvas(800, 600)
        CarShapes.simple_car(canvas, x=200, y=300, width=200, height=80, color=Color.GREEN)
        svg = canvas.to_svg()

        # Should render without error
        assert '<rect' in svg
        assert '<circle' in svg
        assert Color.GREEN in svg

    def test_simple_car_returns_canvas(self):
        """simple_car returns canvas for chaining."""
        canvas = Canvas(600, 400)
        result = CarShapes.simple_car(canvas, x=100, y=200)

        assert result is canvas

    def test_multiple_cars(self):
        """Can draw multiple cars on same canvas."""
        canvas = Canvas(800, 600)
        CarShapes.simple_car(canvas, x=100, y=200, color=Color.RED)
        CarShapes.simple_car(canvas, x=400, y=200, color=Color.BLUE)
        svg = canvas.to_svg()

        assert Color.RED in svg
        assert Color.BLUE in svg
        # Should have at least 4 circles (2 cars × 2 wheels)
        assert svg.count('<circle') >= 4


class TestWheel:
    """Test wheel helper method."""

    def test_wheel_renders(self):
        """wheel draws without errors."""
        canvas = Canvas(400, 400)
        CarShapes.wheel(canvas, x=200, y=200)
        svg = canvas.to_svg()

        # Should have 3 circles (tire, rim, hub)
        assert svg.count('<circle') == 3

    def test_wheel_default_colors(self):
        """wheel uses default colors."""
        canvas = Canvas(400, 400)
        CarShapes.wheel(canvas, x=200, y=200)
        svg = canvas.to_svg()

        assert Color.BLACK in svg  # Tire
        assert Color.SILVER in svg  # Rim

    def test_wheel_custom_colors(self):
        """wheel accepts custom colors."""
        canvas = Canvas(400, 400)
        CarShapes.wheel(canvas, x=200, y=200, tire_color=Color.GRAY, rim_color=Color.BLUE)
        svg = canvas.to_svg()

        assert Color.GRAY in svg
        assert Color.BLUE in svg

    def test_wheel_custom_radius(self):
        """wheel accepts custom radius."""
        canvas = Canvas(400, 400)
        CarShapes.wheel(canvas, x=200, y=200, radius=40)
        svg = canvas.to_svg()

        # Should have 3 circles
        assert svg.count('<circle') == 3

    def test_wheel_returns_canvas(self):
        """wheel returns canvas for chaining."""
        canvas = Canvas(400, 400)
        result = CarShapes.wheel(canvas, x=200, y=200)

        assert result is canvas

    def test_multiple_wheels(self):
        """Can draw multiple wheels."""
        canvas = Canvas(600, 400)
        CarShapes.wheel(canvas, x=150, y=300, radius=30)
        CarShapes.wheel(canvas, x=450, y=300, radius=30)
        svg = canvas.to_svg()

        # Should have 6 circles (2 wheels × 3 circles each)
        assert svg.count('<circle') == 6


class TestTrafficLight:
    """Test traffic_light helper method."""

    def test_traffic_light_renders(self):
        """traffic_light draws without errors."""
        canvas = Canvas(400, 600)
        CarShapes.traffic_light(canvas, x=150, y=50)
        svg = canvas.to_svg()

        # Should have housing (rounded rect)
        assert '<rect' in svg
        # Should have 3 circles (lights)
        assert svg.count('<circle') >= 3

    def test_traffic_light_default_red(self):
        """traffic_light defaults to red light active."""
        canvas = Canvas(400, 600)
        CarShapes.traffic_light(canvas, x=150, y=50)
        svg = canvas.to_svg()

        assert Color.RED in svg
        assert Color.GRAY in svg  # Inactive lights

    def test_traffic_light_yellow(self):
        """traffic_light can show yellow light."""
        canvas = Canvas(400, 600)
        CarShapes.traffic_light(canvas, x=150, y=50, active="yellow")
        svg = canvas.to_svg()

        assert Color.YELLOW in svg
        assert Color.GRAY in svg

    def test_traffic_light_green(self):
        """traffic_light can show green light."""
        canvas = Canvas(400, 600)
        CarShapes.traffic_light(canvas, x=150, y=50, active="green")
        svg = canvas.to_svg()

        assert Color.GREEN in svg
        assert Color.GRAY in svg

    def test_traffic_light_invalid_state(self):
        """traffic_light with invalid state defaults to red."""
        canvas = Canvas(400, 600)
        CarShapes.traffic_light(canvas, x=150, y=50, active="purple")
        svg = canvas.to_svg()

        # Should default to red
        assert Color.RED in svg

    def test_traffic_light_returns_canvas(self):
        """traffic_light returns canvas for chaining."""
        canvas = Canvas(400, 600)
        result = CarShapes.traffic_light(canvas, x=150, y=50)

        assert result is canvas

    def test_multiple_traffic_lights(self):
        """Can draw multiple traffic lights."""
        canvas = Canvas(800, 600)
        CarShapes.traffic_light(canvas, x=100, y=50, active="red")
        CarShapes.traffic_light(canvas, x=300, y=50, active="yellow")
        CarShapes.traffic_light(canvas, x=500, y=50, active="green")
        svg = canvas.to_svg()

        assert Color.RED in svg
        assert Color.YELLOW in svg
        assert Color.GREEN in svg


class TestRoad:
    """Test road helper method."""

    def test_road_renders(self):
        """road draws without errors."""
        canvas = Canvas(800, 600)
        CarShapes.road(canvas, y=400)
        svg = canvas.to_svg()

        # Should have rectangles (road surface + lane markers)
        assert '<rect' in svg
        assert Color.GRAY in svg  # Road surface

    def test_road_default_lanes(self):
        """road draws with default 2 lanes."""
        canvas = Canvas(800, 600)
        CarShapes.road(canvas, y=400)
        svg = canvas.to_svg()

        # Should have yellow lane markers
        assert Color.YELLOW in svg

    def test_road_custom_lanes(self):
        """road accepts custom number of lanes."""
        canvas = Canvas(800, 600)
        CarShapes.road(canvas, y=400, num_lanes=3)
        svg = canvas.to_svg()

        assert '<rect' in svg

    def test_road_single_lane(self):
        """road can draw single lane (no markers)."""
        canvas = Canvas(800, 600)
        CarShapes.road(canvas, y=400, num_lanes=1)
        svg = canvas.to_svg()

        # Should have road surface
        assert Color.GRAY in svg

    def test_road_custom_lane_width(self):
        """road accepts custom lane width."""
        canvas = Canvas(800, 600)
        CarShapes.road(canvas, y=400, lane_width=80, num_lanes=2)
        svg = canvas.to_svg()

        assert '<rect' in svg

    def test_road_returns_canvas(self):
        """road returns canvas for chaining."""
        canvas = Canvas(800, 600)
        result = CarShapes.road(canvas, y=400)

        assert result is canvas

    def test_road_full_width(self):
        """road spans full canvas width."""
        canvas = Canvas(1000, 600)
        CarShapes.road(canvas, y=400, num_lanes=2)
        svg = canvas.to_svg()

        # Road should use canvas width (1000 in this case)
        assert 'width="1000"' in svg or 'width="1000.0"' in svg


class TestCarSceneIntegration:
    """Test combining multiple CarShapes elements."""

    def test_complete_car_scene(self):
        """Build complete scene with road, cars, and traffic light."""
        canvas = Canvas(800, 600)

        # Draw road
        CarShapes.road(canvas, y=400, num_lanes=2)

        # Draw cars
        CarShapes.simple_car(canvas, x=100, y=380, color=Color.RED)
        CarShapes.simple_car(canvas, x=400, y=380, color=Color.BLUE)

        # Draw traffic light
        CarShapes.traffic_light(canvas, x=700, y=200, active="green")

        # Draw standalone wheels
        CarShapes.wheel(canvas, x=100, y=550, radius=25)

        svg = canvas.to_svg()

        # Verify all elements present
        assert Color.GRAY in svg  # Road
        assert Color.RED in svg  # Red car
        assert Color.BLUE in svg  # Blue car
        assert Color.GREEN in svg  # Traffic light
        assert Color.YELLOW in svg  # Lane markers
        assert '<circle' in svg  # Wheels
        assert '<rect' in svg  # Road and car bodies

    def test_car_shapes_method_chaining(self):
        """CarShapes methods return canvas for chaining with canvas methods."""
        canvas = Canvas(800, 600)

        # CarShapes methods return canvas, so we can chain with canvas methods
        result = (CarShapes.road(canvas, y=400)
                  .circle(100, 100, 20, fill=Color.RED)
                  .rect(200, 200, 50, 50, fill=Color.BLUE))

        assert result is canvas

        # We can also chain multiple CarShapes calls
        canvas2 = Canvas(800, 600)
        canvas2 = CarShapes.road(canvas2, y=400)
        canvas2 = CarShapes.simple_car(canvas2, x=200, y=380)
        canvas2 = CarShapes.traffic_light(canvas2, x=100, y=200, active="red")

        svg = canvas2.to_svg()
        assert '<rect' in svg  # Road and car
        assert '<circle' in svg  # Traffic light and wheels

    def test_car_shapes_are_static(self):
        """CarShapes methods are static (no instance needed)."""
        # Should not need to instantiate CarShapes
        canvas = Canvas(800, 600)

        # All methods should work as static methods
        CarShapes.simple_car(canvas, 100, 100)
        CarShapes.wheel(canvas, 200, 200)
        CarShapes.traffic_light(canvas, 300, 100)
        CarShapes.road(canvas, 400)

        svg = canvas.to_svg()
        assert len(svg) > 500  # Should have substantial content
