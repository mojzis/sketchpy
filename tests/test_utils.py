"""Tests for utility functions and classes."""

import pytest
from sketchpy import Point, quick_draw, Canvas, Color


class TestPoint:
    """Test Point dataclass."""

    def test_point_creation(self):
        """Point can be created with x and y."""
        point = Point(10, 20)
        assert point.x == 10
        assert point.y == 20

    def test_point_float_coordinates(self):
        """Point accepts float coordinates."""
        point = Point(10.5, 20.75)
        assert point.x == 10.5
        assert point.y == 20.75

    def test_point_negative_coordinates(self):
        """Point accepts negative coordinates."""
        point = Point(-50, -100)
        assert point.x == -50
        assert point.y == -100

    def test_point_zero_coordinates(self):
        """Point accepts zero coordinates."""
        point = Point(0, 0)
        assert point.x == 0
        assert point.y == 0

    def test_point_equality(self):
        """Points with same coordinates are equal."""
        p1 = Point(10, 20)
        p2 = Point(10, 20)
        assert p1 == p2

    def test_point_inequality(self):
        """Points with different coordinates are not equal."""
        p1 = Point(10, 20)
        p2 = Point(10, 30)
        p3 = Point(20, 20)
        assert p1 != p2
        assert p1 != p3

    def test_point_repr(self):
        """Point has meaningful repr."""
        point = Point(10, 20)
        repr_str = repr(point)
        assert "Point" in repr_str
        assert "10" in repr_str
        assert "20" in repr_str


class TestQuickDraw:
    """Test quick_draw convenience function."""

    def test_quick_draw_default(self):
        """quick_draw creates canvas with default dimensions."""
        canvas = quick_draw()
        assert isinstance(canvas, Canvas)
        assert canvas.width == 800
        assert canvas.height == 600

    def test_quick_draw_custom_dimensions(self):
        """quick_draw accepts custom dimensions."""
        canvas = quick_draw(1024, 768)
        assert canvas.width == 1024
        assert canvas.height == 768

    def test_quick_draw_returns_canvas(self):
        """quick_draw returns a Canvas instance."""
        canvas = quick_draw()
        assert isinstance(canvas, Canvas)

    def test_quick_draw_canvas_is_usable(self):
        """Canvas from quick_draw can draw shapes."""
        canvas = quick_draw(400, 400)
        canvas.circle(200, 200, 50, fill=Color.RED)
        svg = canvas.to_svg()

        assert '<circle' in svg
        assert Color.RED in svg

    def test_quick_draw_small_canvas(self):
        """quick_draw can create small canvas."""
        canvas = quick_draw(200, 150)
        assert canvas.width == 200
        assert canvas.height == 150

    def test_quick_draw_large_canvas(self):
        """quick_draw can create large canvas (within limits)."""
        canvas = quick_draw(1920, 1080)
        assert canvas.width == 1920
        assert canvas.height == 1080

    def test_quick_draw_respects_canvas_limits(self):
        """quick_draw respects Canvas security limits."""
        # Should raise error for canvas exceeding limits
        with pytest.raises(ValueError):
            quick_draw(3000, 3000)

    def test_quick_draw_method_chaining(self):
        """Canvas from quick_draw supports method chaining."""
        svg = (quick_draw(400, 400)
               .circle(200, 200, 50, fill=Color.BLUE)
               .rect(100, 100, 100, 100, fill=Color.RED)
               .to_svg())

        assert '<circle' in svg
        assert '<rect' in svg
        assert Color.BLUE in svg
        assert Color.RED in svg


class TestUtilsIntegration:
    """Test utilities working together."""

    def test_point_with_quick_draw(self):
        """Point coordinates can be used with quick_draw canvas."""
        canvas = quick_draw(400, 400)
        p1 = Point(100, 100)
        p2 = Point(300, 300)

        # Use point coordinates to draw
        canvas.circle(p1.x, p1.y, 20, fill=Color.RED)
        canvas.circle(p2.x, p2.y, 20, fill=Color.BLUE)

        svg = canvas.to_svg()
        assert Color.RED in svg
        assert Color.BLUE in svg

    def test_point_for_line_endpoints(self):
        """Points can define line endpoints."""
        canvas = quick_draw(400, 400)
        start = Point(50, 50)
        end = Point(350, 350)

        canvas.line(start.x, start.y, end.x, end.y, stroke=Color.GREEN)

        svg = canvas.to_svg()
        assert '<line' in svg
        assert Color.GREEN in svg

    def test_point_for_polygon_vertices(self):
        """Points can define polygon vertices."""
        canvas = quick_draw(400, 400)
        vertices = [
            Point(200, 100),
            Point(300, 200),
            Point(200, 300),
            Point(100, 200)
        ]

        # Convert points to tuples for polygon
        points_list = [(p.x, p.y) for p in vertices]
        canvas.polygon(points=points_list, fill=Color.PURPLE)

        svg = canvas.to_svg()
        assert '<polygon' in svg
        assert Color.PURPLE in svg
