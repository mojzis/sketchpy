"""Tests for CarShapes helper class."""

import pytest
from sketchpy import Canvas, Color, CarShapes


class TestSimpleCar:
    """Test simple_car helper method."""

    def test_simple_car_renders(self):
        """simple_car draws without errors."""
        canvas = Canvas(600, 400)
        cars = CarShapes(canvas)
        cars.simple_car(x=100, y=200)
        svg = canvas.to_svg()

        # Should contain rectangles (body, roof parts)
        assert '<rect' in svg
        # Should contain circles (wheels)
        assert '<circle' in svg
        # Should contain polygon (roof/windshield)
        assert '<polygon' in svg

    def test_simple_car_default_gradient(self):
        """simple_car uses gradient by default."""
        canvas = Canvas(600, 400)
        cars = CarShapes(canvas)
        cars.simple_car(x=100, y=200)
        svg = canvas.to_svg()

        assert "grad_car_metallic_shine" in svg
        assert Color.BLACK in svg  # Wheels

    def test_simple_car_custom_color(self):
        """simple_car accepts custom color."""
        canvas = Canvas(600, 400)
        cars = CarShapes(canvas)
        cars.simple_car(x=100, y=200, color=Color.BLUE)
        svg = canvas.to_svg()

        assert Color.BLUE in svg

    def test_simple_car_custom_dimensions(self):
        """simple_car accepts custom width and height."""
        canvas = Canvas(800, 600)
        cars = CarShapes(canvas)
        cars.simple_car(x=200, y=300, width=200, height=80, color=Color.GREEN)
        svg = canvas.to_svg()

        # Should render without error
        assert '<rect' in svg
        assert '<circle' in svg
        assert Color.GREEN in svg

    def test_simple_car_returns_self(self):
        """simple_car returns self for chaining."""
        canvas = Canvas(600, 400)
        cars = CarShapes(canvas)
        result = cars.simple_car(x=100, y=200)

        assert result is cars

    def test_multiple_cars(self):
        """Can draw multiple cars on same canvas."""
        canvas = Canvas(800, 600)
        cars = CarShapes(canvas)
        cars.simple_car(x=100, y=200, color=Color.RED)
        cars.simple_car(x=400, y=200, color=Color.BLUE)
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
        cars = CarShapes(canvas)
        cars.wheel(x=200, y=200)
        svg = canvas.to_svg()

        # Should have 3 circles (tire, rim, hub)
        assert svg.count('<circle') == 3

    def test_wheel_default_gradients(self):
        """wheel uses gradients by default."""
        canvas = Canvas(400, 400)
        cars = CarShapes(canvas)
        cars.wheel(x=200, y=200)
        svg = canvas.to_svg()

        assert "grad_car_tire_rubber" in svg
        assert "grad_car_chrome_rim" in svg

    def test_wheel_custom_colors(self):
        """wheel accepts custom colors."""
        canvas = Canvas(400, 400)
        cars = CarShapes(canvas)
        cars.wheel(x=200, y=200, tire_color=Color.GRAY, rim_color=Color.BLUE)
        svg = canvas.to_svg()

        assert Color.GRAY in svg
        assert Color.BLUE in svg

    def test_wheel_custom_radius(self):
        """wheel accepts custom radius."""
        canvas = Canvas(400, 400)
        cars = CarShapes(canvas)
        cars.wheel(x=200, y=200, radius=40)
        svg = canvas.to_svg()

        # Should have 3 circles
        assert svg.count('<circle') == 3

    def test_wheel_returns_self(self):
        """wheel returns self for chaining."""
        canvas = Canvas(400, 400)
        cars = CarShapes(canvas)
        result = cars.wheel(x=200, y=200)

        assert result is cars

    def test_multiple_wheels(self):
        """Can draw multiple wheels."""
        canvas = Canvas(600, 400)
        cars = CarShapes(canvas)
        cars.wheel(x=150, y=300, radius=30)
        cars.wheel(x=450, y=300, radius=30)
        svg = canvas.to_svg()

        # Should have 6 circles (2 wheels × 3 circles each)
        assert svg.count('<circle') == 6


class TestTrafficLight:
    """Test traffic_light helper method."""

    def test_traffic_light_renders(self):
        """traffic_light draws without errors."""
        canvas = Canvas(400, 600)
        cars = CarShapes(canvas)
        cars.traffic_light(x=150, y=50)
        svg = canvas.to_svg()

        # Should have housing (rounded rect)
        assert '<rect' in svg
        # Should have 3 circles (lights)
        assert svg.count('<circle') >= 3

    def test_traffic_light_default_red_gradient(self):
        """traffic_light defaults to red light with gradient glow."""
        canvas = Canvas(400, 600)
        cars = CarShapes(canvas)
        cars.traffic_light(x=150, y=50)
        svg = canvas.to_svg()

        assert "grad_car_light_glow_red" in svg
        assert Color.GRAY in svg  # Inactive lights

    def test_traffic_light_yellow(self):
        """traffic_light can show yellow light with gradient."""
        canvas = Canvas(400, 600)
        cars = CarShapes(canvas)
        cars.traffic_light(x=150, y=50, active="yellow")
        svg = canvas.to_svg()

        assert "grad_car_light_glow_yellow" in svg
        assert Color.GRAY in svg

    def test_traffic_light_green(self):
        """traffic_light can show green light with gradient."""
        canvas = Canvas(400, 600)
        cars = CarShapes(canvas)
        cars.traffic_light(x=150, y=50, active="green")
        svg = canvas.to_svg()

        assert "grad_car_light_glow_green" in svg
        assert Color.GRAY in svg

    def test_traffic_light_invalid_state(self):
        """traffic_light with invalid state defaults to red."""
        canvas = Canvas(400, 600)
        cars = CarShapes(canvas)
        cars.traffic_light(x=150, y=50, active="purple")
        svg = canvas.to_svg()

        # Should default to red
        assert "grad_car_light_glow_red" in svg

    def test_traffic_light_returns_self(self):
        """traffic_light returns self for chaining."""
        canvas = Canvas(400, 600)
        cars = CarShapes(canvas)
        result = cars.traffic_light(x=150, y=50)

        assert result is cars

    def test_multiple_traffic_lights(self):
        """Can draw multiple traffic lights."""
        canvas = Canvas(800, 600)
        cars = CarShapes(canvas)
        cars.traffic_light(x=100, y=50, active="red")
        cars.traffic_light(x=300, y=50, active="yellow")
        cars.traffic_light(x=500, y=50, active="green")
        svg = canvas.to_svg()

        assert "grad_car_light_glow_red" in svg
        assert "grad_car_light_glow_yellow" in svg
        assert "grad_car_light_glow_green" in svg


class TestRoad:
    """Test road helper method."""

    def test_road_renders(self):
        """road draws without errors."""
        canvas = Canvas(800, 600)
        cars = CarShapes(canvas)
        cars.road(y=400)
        svg = canvas.to_svg()

        # Should have rectangles (road surface + lane markers)
        assert '<rect' in svg
        assert Color.GRAY in svg  # Road surface

    def test_road_default_lanes(self):
        """road draws with default 2 lanes."""
        canvas = Canvas(800, 600)
        cars = CarShapes(canvas)
        cars.road(y=400)
        svg = canvas.to_svg()

        # Should have yellow lane markers
        assert Color.YELLOW in svg

    def test_road_custom_lanes(self):
        """road accepts custom number of lanes."""
        canvas = Canvas(800, 600)
        cars = CarShapes(canvas)
        cars.road(y=400, num_lanes=3)
        svg = canvas.to_svg()

        assert '<rect' in svg

    def test_road_single_lane(self):
        """road can draw single lane (no markers)."""
        canvas = Canvas(800, 600)
        cars = CarShapes(canvas)
        cars.road(y=400, num_lanes=1)
        svg = canvas.to_svg()

        # Should have road surface
        assert Color.GRAY in svg

    def test_road_custom_lane_width(self):
        """road accepts custom lane width."""
        canvas = Canvas(800, 600)
        cars = CarShapes(canvas)
        cars.road(y=400, lane_width=80, num_lanes=2)
        svg = canvas.to_svg()

        assert '<rect' in svg

    def test_road_returns_self(self):
        """road returns self for chaining."""
        canvas = Canvas(800, 600)
        cars = CarShapes(canvas)
        result = cars.road(y=400)

        assert result is cars

    def test_road_full_width(self):
        """road spans full canvas width."""
        canvas = Canvas(1000, 600)
        cars = CarShapes(canvas)
        cars.road(y=400, num_lanes=2)
        svg = canvas.to_svg()

        # Road should use canvas width (1000 in this case)
        assert 'width="1000"' in svg or 'width="1000.0"' in svg


class TestCarSceneIntegration:
    """Test combining multiple CarShapes elements."""

    def test_complete_car_scene(self):
        """Build complete scene with road, cars, and traffic light."""
        canvas = Canvas(800, 600)
        cars = CarShapes(canvas)

        # Draw road
        cars.road(y=400, num_lanes=2)

        # Draw cars
        cars.simple_car(x=100, y=380, color=Color.RED)
        cars.simple_car(x=400, y=380, color=Color.BLUE)

        # Draw traffic light
        cars.traffic_light(x=700, y=200, active="green")

        # Draw standalone wheels
        cars.wheel(x=100, y=550, radius=25)

        svg = canvas.to_svg()

        # Verify all elements present
        assert Color.GRAY in svg  # Road
        assert Color.RED in svg  # Red car
        assert Color.BLUE in svg  # Blue car
        assert "grad_car_light_glow_green" in svg  # Traffic light
        assert Color.YELLOW in svg  # Lane markers
        assert '<circle' in svg  # Wheels
        assert '<rect' in svg  # Road and car bodies

    def test_car_shapes_method_chaining(self):
        """CarShapes methods return self for chaining."""
        canvas = Canvas(800, 600)
        cars = CarShapes(canvas)

        # CarShapes methods return self for chaining
        result = (cars.road(y=400)
                  .simple_car(x=200, y=380)
                  .traffic_light(x=100, y=200, active="red"))

        assert result is cars

        svg = canvas.to_svg()
        assert '<rect' in svg  # Road and car
        assert '<circle' in svg  # Traffic light and wheels

    def test_car_shapes_require_instance(self):
        """CarShapes methods require instance (instance-based API)."""
        canvas = Canvas(800, 600)
        cars = CarShapes(canvas)

        # All methods should work via instance
        cars.simple_car(100, 100)
        cars.wheel(200, 200)
        cars.traffic_light(300, 100)
        cars.road(400)

        svg = canvas.to_svg()
        assert len(svg) > 500  # Should have substantial content


class TestCarGradients:
    """Test CarShapes gradient functionality."""

    def test_car_gradients_registered(self):
        """CarShapes automatically registers gradients on init."""
        canvas = Canvas(800, 600)
        cars = CarShapes(canvas)

        # Verify gradients exist in canvas
        assert "car_metallic_shine" in canvas.gradients
        assert "car_tire_rubber" in canvas.gradients
        assert "car_chrome_rim" in canvas.gradients
        assert "car_light_glow_red" in canvas.gradients
        assert "car_light_glow_yellow" in canvas.gradients
        assert "car_light_glow_green" in canvas.gradients

    def test_car_uses_gradient_by_default(self):
        """Car uses metallic gradient by default."""
        canvas = Canvas(800, 600)
        cars = CarShapes(canvas)
        cars.simple_car(400, 300)

        svg = canvas.to_svg()

        # Should contain gradient definition
        assert "grad_car_metallic_shine" in svg
        # Should reference gradient in shapes
        assert "url(#grad_car_metallic_shine)" in svg

    def test_car_can_override_with_solid_color(self):
        """Car can use solid color instead of gradient."""
        canvas = Canvas(800, 600)
        cars = CarShapes(canvas)
        cars.simple_car(400, 300, color=Color.GREEN)

        svg = canvas.to_svg()

        # Should use solid color
        assert Color.GREEN in svg
        # Should NOT reference metallic gradient in shapes
        assert "url(#grad_car_metallic_shine)" not in svg
