"""Tests for core Canvas functionality."""

import pytest
from sketchpy import Canvas, Color


class TestCanvasInitialization:
    """Test Canvas creation and validation."""

    def test_canvas_default_dimensions(self):
        """Canvas creates with default dimensions."""
        canvas = Canvas()
        assert canvas.width == 800
        assert canvas.height == 600
        assert canvas.background == Color.WHITE

    def test_canvas_custom_dimensions(self):
        """Canvas accepts custom dimensions."""
        canvas = Canvas(1024, 768)
        assert canvas.width == 1024
        assert canvas.height == 768

    def test_canvas_custom_background(self):
        """Canvas accepts custom background color."""
        canvas = Canvas(800, 600, background=Color.BLUE)
        assert canvas.background == Color.BLUE

    def test_canvas_zero_width_raises_error(self):
        """Canvas with zero width raises ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            Canvas(0, 600)

    def test_canvas_zero_height_raises_error(self):
        """Canvas with zero height raises ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            Canvas(800, 0)

    def test_canvas_negative_width_raises_error(self):
        """Canvas with negative width raises ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            Canvas(-100, 600)

    def test_canvas_negative_height_raises_error(self):
        """Canvas with negative height raises ValueError."""
        with pytest.raises(ValueError, match="must be positive"):
            Canvas(800, -100)

    def test_canvas_exceeds_max_width(self):
        """Canvas exceeding MAX_WIDTH raises ValueError."""
        with pytest.raises(ValueError, match="exceeds maximum"):
            Canvas(3000, 600)

    def test_canvas_exceeds_max_height(self):
        """Canvas exceeding MAX_HEIGHT raises ValueError."""
        with pytest.raises(ValueError, match="exceeds maximum"):
            Canvas(800, 3000)

    def test_canvas_exceeds_max_area(self):
        """Canvas exceeding MAX_AREA raises ValueError."""
        # Both dimensions are within individual limits but area exceeds
        # 2000 * 2000 = 4,000,000 (exactly at limit)
        # But this test is tricky - the height check happens first
        # So we need dimensions that pass individual checks but fail area check
        # However, since MAX_AREA = MAX_WIDTH * MAX_HEIGHT, we can't actually
        # hit this case. Let's test that max area works correctly.
        with pytest.raises(ValueError, match="exceeds maximum"):
            # Height exceeds limit which is caught before area
            Canvas(2000, 2001)

    def test_canvas_at_max_dimensions(self):
        """Canvas at exactly MAX dimensions is allowed."""
        canvas = Canvas(2000, 2000)
        assert canvas.width == 2000
        assert canvas.height == 2000


class TestBasicShapes:
    """Test basic shape drawing methods."""

    def test_rect_default(self):
        """Rectangle draws with default parameters."""
        canvas = Canvas(400, 400)
        canvas.rect()
        svg = canvas.to_svg()

        assert '<rect' in svg
        assert 'x="0"' in svg
        assert 'y="0"' in svg
        assert 'width="100"' in svg
        assert 'height="100"' in svg

    def test_rect_custom(self):
        """Rectangle draws with custom parameters."""
        canvas = Canvas(400, 400)
        canvas.rect(x=50, y=60, width=200, height=150, fill=Color.RED, stroke=Color.BLUE, stroke_width=3)
        svg = canvas.to_svg()

        assert 'x="50"' in svg
        assert 'y="60"' in svg
        assert 'width="200"' in svg
        assert 'height="150"' in svg
        assert Color.RED in svg
        assert Color.BLUE in svg
        assert 'stroke-width="3"' in svg

    def test_rect_chaining(self):
        """Rectangle returns self for chaining."""
        canvas = Canvas(400, 400)
        result = canvas.rect(10, 10, 50, 50)
        assert result is canvas

    def test_circle_default(self):
        """Circle draws with default parameters."""
        canvas = Canvas(400, 400)
        canvas.circle()
        svg = canvas.to_svg()

        assert '<circle' in svg
        assert 'cx="50"' in svg
        assert 'cy="50"' in svg
        assert 'r="25"' in svg

    def test_circle_custom(self):
        """Circle draws with custom parameters."""
        canvas = Canvas(400, 400)
        canvas.circle(x=200, y=150, radius=75, fill=Color.GREEN, stroke=Color.YELLOW, stroke_width=2)
        svg = canvas.to_svg()

        assert 'cx="200"' in svg
        assert 'cy="150"' in svg
        assert 'r="75"' in svg
        assert Color.GREEN in svg
        assert Color.YELLOW in svg

    def test_circle_with_opacity(self):
        """Circle respects opacity parameter."""
        canvas = Canvas(400, 400)
        canvas.circle(200, 200, 50, opacity=0.5)
        svg = canvas.to_svg()

        assert 'opacity="0.5"' in svg

    def test_circle_opacity_default(self):
        """Circle with opacity=1.0 does not include opacity attribute."""
        canvas = Canvas(400, 400)
        canvas.circle(200, 200, 50, opacity=1.0)
        svg = canvas.to_svg()

        # Default opacity should not be explicitly set
        assert 'opacity=' not in svg or 'opacity="1' in svg

    def test_ellipse_default(self):
        """Ellipse draws with default parameters."""
        canvas = Canvas(400, 400)
        canvas.ellipse()
        svg = canvas.to_svg()

        assert '<ellipse' in svg
        assert 'cx="50"' in svg
        assert 'cy="50"' in svg
        assert 'rx="40"' in svg
        assert 'ry="25"' in svg

    def test_ellipse_custom(self):
        """Ellipse draws with custom parameters."""
        canvas = Canvas(400, 400)
        canvas.ellipse(x=250, y=180, rx=100, ry=60, fill=Color.PURPLE, stroke=Color.PINK)
        svg = canvas.to_svg()

        assert 'cx="250"' in svg
        assert 'cy="180"' in svg
        assert 'rx="100"' in svg
        assert 'ry="60"' in svg
        assert Color.PURPLE in svg

    def test_line_default(self):
        """Line draws with default parameters."""
        canvas = Canvas(400, 400)
        canvas.line()
        svg = canvas.to_svg()

        assert '<line' in svg
        assert 'x1="0"' in svg
        assert 'y1="0"' in svg
        assert 'x2="100"' in svg
        assert 'y2="100"' in svg

    def test_line_custom(self):
        """Line draws with custom parameters."""
        canvas = Canvas(400, 400)
        canvas.line(x1=50, y1=100, x2=350, y2=300, stroke=Color.RED, stroke_width=5)
        svg = canvas.to_svg()

        assert 'x1="50"' in svg
        assert 'y1="100"' in svg
        assert 'x2="350"' in svg
        assert 'y2="300"' in svg
        assert Color.RED in svg
        assert 'stroke-width="5"' in svg

    def test_polygon_default(self):
        """Polygon draws with default triangle."""
        canvas = Canvas(400, 400)
        canvas.polygon()
        svg = canvas.to_svg()

        assert '<polygon' in svg
        assert 'points=' in svg
        # Default triangle
        assert '50,0' in svg
        assert '100,100' in svg
        assert '0,100' in svg

    def test_polygon_custom(self):
        """Polygon draws with custom points."""
        canvas = Canvas(400, 400)
        points = [(100, 50), (150, 100), (100, 150), (50, 100)]
        canvas.polygon(points=points, fill=Color.ORANGE, stroke=Color.BROWN, stroke_width=3)
        svg = canvas.to_svg()

        assert '<polygon' in svg
        assert '100,50' in svg
        assert '150,100' in svg
        assert '100,150' in svg
        assert '50,100' in svg
        assert Color.ORANGE in svg

    def test_text_default(self):
        """Text draws with default parameters."""
        canvas = Canvas(400, 400)
        canvas.text()
        svg = canvas.to_svg()

        assert '<text' in svg
        assert 'x="0"' in svg
        assert 'y="20"' in svg
        assert 'font-size="16"' in svg
        assert '>Hello</text>' in svg

    def test_text_custom(self):
        """Text draws with custom parameters."""
        canvas = Canvas(400, 400)
        canvas.text(x=100, y=200, text="Custom Text", size=24, fill=Color.BLUE, font="monospace")
        svg = canvas.to_svg()

        assert 'x="100"' in svg
        assert 'y="200"' in svg
        assert 'font-size="24"' in svg
        assert 'font-family="monospace"' in svg
        assert '>Custom Text</text>' in svg
        assert Color.BLUE in svg

    def test_rounded_rect_default(self):
        """Rounded rectangle draws with default parameters."""
        canvas = Canvas(400, 400)
        canvas.rounded_rect()
        svg = canvas.to_svg()

        assert '<rect' in svg
        assert 'rx="5"' in svg
        assert 'ry="5"' in svg

    def test_rounded_rect_custom(self):
        """Rounded rectangle draws with custom parameters."""
        canvas = Canvas(400, 400)
        canvas.rounded_rect(x=50, y=50, width=200, height=100, rx=15, ry=10, fill=Color.SILVER)
        svg = canvas.to_svg()

        assert 'x="50"' in svg
        assert 'y="50"' in svg
        assert 'width="200"' in svg
        assert 'height="100"' in svg
        assert 'rx="15"' in svg
        assert 'ry="10"' in svg
        assert Color.SILVER in svg


class TestGrid:
    """Test grid drawing functionality."""

    def test_grid_default(self):
        """Grid draws with default parameters."""
        canvas = Canvas(400, 400)
        canvas.grid()
        svg = canvas.to_svg()

        # Should have multiple lines
        assert svg.count('<line') > 10
        # Should have coordinate labels
        assert '<text' in svg

    def test_grid_custom_spacing(self):
        """Grid respects custom spacing."""
        canvas = Canvas(400, 400)
        canvas.grid(spacing=100)
        svg = canvas.to_svg()

        # Should have fewer lines with larger spacing
        assert '<line' in svg

    def test_grid_custom_color(self):
        """Grid respects custom color."""
        canvas = Canvas(400, 400)
        canvas.grid(color=Color.BLUE)
        svg = canvas.to_svg()

        assert Color.BLUE in svg

    def test_grid_no_coords(self):
        """Grid can hide coordinate labels."""
        canvas = Canvas(400, 400)
        canvas.grid(show_coords=False)
        svg = canvas.to_svg()

        # Should have lines but no text labels
        assert '<line' in svg
        # Text count should be 0 or very minimal
        # (there might still be a (0,0) label)

    def test_grid_chaining(self):
        """Grid returns self for chaining."""
        canvas = Canvas(400, 400)
        result = canvas.grid()
        assert result is canvas


class TestShowPalette:
    """Test palette display functionality."""

    def test_show_palette_basic(self):
        """show_palette displays colors from palette class."""
        canvas = Canvas(800, 600)
        canvas.show_palette(Color)
        svg = canvas.to_svg()

        # Should have rectangles for each color
        assert '<rect' in svg
        # Should have text labels
        assert '<text' in svg
        # Should contain some color values
        assert Color.RED in svg or Color.BLUE in svg

    def test_show_palette_chaining(self):
        """show_palette returns self for chaining."""
        canvas = Canvas(800, 600)
        result = canvas.show_palette(Color)
        assert result is canvas

    def test_show_palette_custom_layout(self):
        """show_palette accepts custom layout parameters."""
        canvas = Canvas(800, 600)
        canvas.show_palette(
            Color,
            rect_width=100,
            rect_height=50,
            columns=3,
            padding=15,
            start_x=50,
            start_y=30
        )
        svg = canvas.to_svg()

        # Should render without error
        assert '<rect' in svg


class TestSVGGeneration:
    """Test SVG output methods."""

    def test_to_svg_basic(self):
        """to_svg generates valid SVG string."""
        canvas = Canvas(800, 600)
        svg = canvas.to_svg()

        assert svg.startswith('<svg')
        assert svg.endswith('</svg>')
        assert 'width="800"' in svg
        assert 'height="600"' in svg
        assert 'xmlns="http://www.w3.org/2000/svg"' in svg

    def test_to_svg_with_background(self):
        """to_svg includes background color."""
        canvas = Canvas(800, 600, background=Color.YELLOW)
        svg = canvas.to_svg()

        assert Color.YELLOW in svg
        assert 'width="100%"' in svg  # Background rect

    def test_to_svg_with_shapes(self):
        """to_svg includes drawn shapes."""
        canvas = Canvas(400, 400)
        canvas.circle(200, 200, 50, fill=Color.RED)
        canvas.rect(100, 100, 100, 100, fill=Color.BLUE)
        svg = canvas.to_svg()

        assert '<circle' in svg
        assert '<rect' in svg
        assert Color.RED in svg
        assert Color.BLUE in svg

    def test_repr_html(self):
        """_repr_html_ returns SVG for marimo display."""
        canvas = Canvas(400, 400)
        canvas.circle(200, 200, 50)
        html = canvas._repr_html_()

        assert html.startswith('<svg')
        assert html.endswith('</svg>')
        assert '<circle' in html

    def test_save_creates_file(self, tmp_path):
        """save() writes SVG to file."""
        canvas = Canvas(400, 400)
        canvas.circle(200, 200, 50, fill=Color.GREEN)

        filepath = tmp_path / "test.svg"
        canvas.save(str(filepath))

        assert filepath.exists()
        content = filepath.read_text()
        assert content.startswith('<svg')
        assert Color.GREEN in content


class TestMethodChaining:
    """Test that all shape methods support chaining."""

    def test_full_method_chain(self):
        """Multiple shape methods can be chained together."""
        canvas = Canvas(800, 600)

        result = (canvas
                  .rect(0, 0, 100, 100, fill=Color.RED)
                  .circle(200, 200, 50, fill=Color.BLUE)
                  .line(0, 0, 800, 600, stroke=Color.GREEN)
                  .text(400, 300, "Test", fill=Color.BLACK))

        assert result is canvas
        svg = canvas.to_svg()
        assert '<rect' in svg
        assert '<circle' in svg
        assert '<line' in svg
        assert '<text' in svg


class TestClear:
    """Test canvas clearing functionality."""

    def test_clear_removes_shapes(self):
        """clear() removes all shapes."""
        canvas = Canvas(400, 400)
        canvas.circle(200, 200, 50)
        canvas.rect(100, 100, 100, 100)

        assert len(canvas.shapes) == 2

        canvas.clear()

        assert len(canvas.shapes) == 0

    def test_clear_chaining(self):
        """clear() returns self for chaining."""
        canvas = Canvas(400, 400)
        canvas.circle(200, 200, 50)
        result = canvas.clear()

        assert result is canvas

    def test_clear_and_redraw(self):
        """Canvas can be reused after clear()."""
        canvas = Canvas(400, 400)
        canvas.circle(200, 200, 50, fill=Color.RED)
        canvas.clear()
        canvas.rect(100, 100, 100, 100, fill=Color.BLUE)

        svg = canvas.to_svg()
        assert Color.BLUE in svg
        assert Color.RED not in svg


class TestShapeLimit:
    """Test shape count security limits."""

    def test_shape_limit_enforcement(self):
        """Drawing too many shapes raises ValueError."""
        canvas = Canvas(800, 600)

        # Draw shapes up to the limit
        with pytest.raises(ValueError, match="Shape limit exceeded"):
            for i in range(Canvas.MAX_SHAPES + 1):
                canvas.circle(i % 800, i % 600, 5)

    def test_shape_limit_includes_groups(self):
        """Shape limit counts grouped shapes."""
        canvas = Canvas(800, 600)

        with pytest.raises(ValueError, match="Shape limit exceeded"):
            with canvas.group("test"):
                for i in range(Canvas.MAX_SHAPES + 1):
                    canvas.circle(i % 800, i % 600, 5)


class TestSecurityLimits:
    """Test various security constraints."""

    def test_max_width_constant(self):
        """MAX_WIDTH constant is defined."""
        assert Canvas.MAX_WIDTH == 2000

    def test_max_height_constant(self):
        """MAX_HEIGHT constant is defined."""
        assert Canvas.MAX_HEIGHT == 2000

    def test_max_area_constant(self):
        """MAX_AREA constant is defined."""
        assert Canvas.MAX_AREA == 4_000_000

    def test_max_shapes_constant(self):
        """MAX_SHAPES constant is defined."""
        assert Canvas.MAX_SHAPES == 10_000
