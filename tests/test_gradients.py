"""Tests for gradient and named groups features."""

import pytest
from sketchpy import Canvas, Color


class TestGradients:
    """Test gradient fill functionality."""

    def test_linear_gradient_basic(self):
        """Test basic linear gradient creation."""
        canvas = Canvas(800, 600)
        canvas.linear_gradient("sunset", colors=["#FF6B6B", "#FFA500", "#FFD93D"])

        # Check gradient was stored
        assert "sunset" in canvas.gradients
        assert "linearGradient" in canvas.gradients["sunset"]
        assert 'id="grad_sunset"' in canvas.gradients["sunset"]

    def test_linear_gradient_with_offsets(self):
        """Test linear gradient with explicit offsets."""
        canvas = Canvas(800, 600)
        canvas.linear_gradient(
            "test",
            start=(0, 0),
            end=(100, 0),
            colors=[("#FF0000", 0), ("#00FF00", 0.5), ("#0000FF", 1.0)]
        )

        assert "test" in canvas.gradients
        assert 'offset="0%"' in canvas.gradients["test"] or 'offset="0.0%"' in canvas.gradients["test"]
        assert 'offset="50%"' in canvas.gradients["test"] or 'offset="50.0%"' in canvas.gradients["test"]
        assert 'offset="100%"' in canvas.gradients["test"] or 'offset="100.0%"' in canvas.gradients["test"]

    def test_radial_gradient_basic(self):
        """Test basic radial gradient creation."""
        canvas = Canvas(800, 600)
        canvas.radial_gradient("glow", colors=["#FFFF00", "#FF6B00"])

        assert "glow" in canvas.gradients
        assert "radialGradient" in canvas.gradients["glow"]
        assert 'id="grad_glow"' in canvas.gradients["glow"]

    def test_gradient_in_svg_output(self):
        """Test that gradients appear in SVG output."""
        canvas = Canvas(800, 600)
        canvas.linear_gradient("test", colors=["#FF0000", "#0000FF"])

        svg = canvas.to_svg()
        assert "<defs>" in svg
        assert "</defs>" in svg
        assert 'id="grad_test"' in svg
        assert "linearGradient" in svg

    def test_gradient_used_as_fill(self):
        """Test using gradient as fill in shapes."""
        canvas = Canvas(800, 600)
        canvas.linear_gradient("sunset", colors=["#FF6B6B", "#FFD93D"])
        canvas.circle(400, 300, 100, fill="gradient:sunset")

        svg = canvas.to_svg()
        assert 'fill="url(#grad_sunset)"' in svg

    def test_gradient_with_rect(self):
        """Test gradient fill on rectangle."""
        canvas = Canvas(800, 600)
        canvas.linear_gradient("sky", colors=["#87CEEB", "#FFFFFF"])
        canvas.rect(0, 0, 800, 300, fill="gradient:sky", stroke="none")

        svg = canvas.to_svg()
        assert 'fill="url(#grad_sky)"' in svg

    def test_multiple_gradients(self):
        """Test multiple gradients in one canvas."""
        canvas = Canvas(800, 600)
        canvas.linear_gradient("grad1", colors=["#FF0000", "#00FF00"])
        canvas.radial_gradient("grad2", colors=["#0000FF", "#FFFF00"])

        svg = canvas.to_svg()
        assert 'id="grad_grad1"' in svg
        assert 'id="grad_grad2"' in svg
        assert "linearGradient" in svg
        assert "radialGradient" in svg

    def test_gradient_method_chaining(self):
        """Test that gradient methods return self for chaining."""
        canvas = Canvas(800, 600)
        result = canvas.linear_gradient("test", colors=["#FF0000", "#0000FF"])
        assert result is canvas

        result2 = canvas.radial_gradient("test2", colors=["#00FF00", "#FFFF00"])
        assert result2 is canvas

    def test_normal_color_still_works(self):
        """Test that normal color fills still work alongside gradients."""
        canvas = Canvas(800, 600)
        canvas.linear_gradient("grad1", colors=["#FF0000", "#0000FF"])
        canvas.circle(200, 300, 50, fill=Color.RED)
        canvas.circle(400, 300, 50, fill="gradient:grad1")

        svg = canvas.to_svg()
        # Normal color should remain as-is
        assert f'fill="{Color.RED}"' in svg
        # Gradient should be converted
        assert 'fill="url(#grad_grad1)"' in svg


class TestNamedGroups:
    """Test named object groups functionality."""

    def test_group_context_manager(self):
        """Test basic group creation with context manager."""
        canvas = Canvas(800, 600)

        with canvas.group("test_group"):
            canvas.circle(100, 100, 50, fill=Color.RED)
            canvas.rect(200, 200, 100, 100, fill=Color.BLUE)

        # Check shapes are in group, not main shapes list
        assert "test_group" in canvas.groups
        assert len(canvas.groups["test_group"]) == 2
        assert len(canvas.shapes) == 0  # No ungrouped shapes

    def test_group_appears_in_svg(self):
        """Test that groups render as SVG <g> elements."""
        canvas = Canvas(800, 600)

        with canvas.group("flower"):
            canvas.circle(400, 300, 30, fill=Color.YELLOW)

        svg = canvas.to_svg()
        assert '<g id="flower"' in svg
        assert '</g>' in svg

    def test_move_group(self):
        """Test moving a group."""
        canvas = Canvas(800, 600)

        with canvas.group("car"):
            canvas.rect(100, 100, 200, 100, fill=Color.RED)

        canvas.move_group("car", dx=50, dy=30)

        svg = canvas.to_svg()
        assert 'transform="translate(50, 30)' in svg

    def test_hide_group(self):
        """Test hiding a group."""
        canvas = Canvas(800, 600)

        with canvas.group("hidden_group"):
            canvas.circle(100, 100, 50, fill=Color.RED)

        canvas.hide_group("hidden_group")

        svg = canvas.to_svg()
        # Hidden group should not appear in output
        assert 'id="hidden_group"' not in svg

    def test_show_group(self):
        """Test showing a previously hidden group."""
        canvas = Canvas(800, 600)

        with canvas.group("toggle_group"):
            canvas.circle(100, 100, 50, fill=Color.RED)

        canvas.hide_group("toggle_group")
        canvas.show_group("toggle_group")

        svg = canvas.to_svg()
        # Should appear after show
        assert 'id="toggle_group"' in svg

    def test_remove_group(self):
        """Test permanently removing a group."""
        canvas = Canvas(800, 600)

        with canvas.group("temp_group"):
            canvas.circle(100, 100, 50, fill=Color.RED)

        canvas.remove_group("temp_group")

        assert "temp_group" not in canvas.groups
        svg = canvas.to_svg()
        assert 'id="temp_group"' not in svg

    def test_ungrouped_shapes_still_work(self):
        """Test that ungrouped shapes work alongside groups."""
        canvas = Canvas(800, 600)

        # Ungrouped shape
        canvas.circle(100, 100, 50, fill=Color.RED)

        # Grouped shape
        with canvas.group("test"):
            canvas.circle(200, 200, 50, fill=Color.BLUE)

        assert len(canvas.shapes) == 1  # One ungrouped
        assert len(canvas.groups["test"]) == 1  # One grouped

        svg = canvas.to_svg()
        assert 'fill="#FF0000"' in svg  # Red circle
        assert 'fill="#0000FF"' in svg  # Blue circle

    def test_clear_removes_groups(self):
        """Test that clear() removes groups."""
        canvas = Canvas(800, 600)

        with canvas.group("test"):
            canvas.circle(100, 100, 50, fill=Color.RED)

        canvas.clear()

        assert len(canvas.groups) == 0
        assert canvas.current_group is None

    def test_group_method_chaining(self):
        """Test that group manipulation methods return self."""
        canvas = Canvas(800, 600)

        with canvas.group("test"):
            canvas.circle(100, 100, 50, fill=Color.RED)

        result = canvas.move_group("test", dx=10, dy=20)
        assert result is canvas

        result2 = canvas.hide_group("test")
        assert result2 is canvas


class TestCombinedFeatures:
    """Test gradients and groups working together."""

    def test_gradient_in_group(self):
        """Test using gradients on shapes within groups."""
        canvas = Canvas(800, 600)
        canvas.linear_gradient("sunset", colors=["#FF6B6B", "#FFD93D"])

        with canvas.group("flower"):
            canvas.circle(400, 300, 50, fill="gradient:sunset")

        svg = canvas.to_svg()
        assert 'id="grad_sunset"' in svg
        assert '<g id="flower"' in svg
        assert 'fill="url(#grad_sunset)"' in svg
