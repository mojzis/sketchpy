"""Tests for ocean curve primitives and OceanShapes helpers."""

import pytest
from sketchpy import Canvas, Color, OceanPalette, OceanShapes


def test_wave_basic():
    """Wave draws from start to end point."""
    can = Canvas(400, 200)
    can.wave(50, 100, 350, 100, height=20, waves=2)
    svg = can.to_svg()

    # Should contain polyline
    assert 'polyline' in svg
    assert 'fill="none"' in svg  # Waves are strokes only, no fill


def test_wave_diagonal():
    """Wave works on diagonal lines."""
    can = Canvas(400, 400)
    can.wave(50, 50, 350, 350, height=30, waves=3, stroke=Color.BLUE)
    svg = can.to_svg()

    assert 'polyline' in svg
    assert Color.BLUE in svg


def test_wave_chaining():
    """Wave returns canvas for method chaining."""
    can = Canvas(400, 200)
    result = can.wave(50, 100, 350, 100, height=20, waves=2, stroke=Color.RED)
    assert result is can


def test_blob_basic():
    """Blob creates organic shape."""
    can = Canvas(200, 200)
    can.blob(100, 100, radius=50, wobble=0.2, points=12)
    svg = can.to_svg()

    # Should contain polygon
    assert 'polygon' in svg


def test_blob_wobble_zero():
    """Blob with wobble=0 creates roughly circular shape."""
    can = Canvas(200, 200)
    can.blob(100, 100, radius=50, wobble=0, points=12)
    svg = can.to_svg()

    # Still creates a polygon (though very regular)
    assert 'polygon' in svg


def test_blob_with_custom_colors():
    """Blob respects fill and stroke colors."""
    can = Canvas(200, 200)
    can.blob(100, 100, radius=50, wobble=0.3,
             fill=OceanPalette.CORAL, stroke=Color.BLACK)
    svg = can.to_svg()

    assert OceanPalette.CORAL in svg
    assert Color.BLACK in svg


def test_tentacle_straight():
    """Tentacle with curl=0 draws straight."""
    can = Canvas(400, 400)
    can.tentacle(200, 100, 200, 300, curl=0, thickness=20, taper=0.3)
    svg = can.to_svg()

    # Should contain polygon (filled shape)
    assert 'polygon' in svg


def test_tentacle_curl_positive():
    """Tentacle with positive curl curves right."""
    can = Canvas(400, 400)
    can.tentacle(200, 100, 200, 300, curl=0.5, thickness=20, taper=0.3,
                fill=OceanPalette.PURPLE_CORAL)
    svg = can.to_svg()

    assert 'polygon' in svg
    assert OceanPalette.PURPLE_CORAL in svg


def test_tentacle_curl_negative():
    """Tentacle with negative curl curves left."""
    can = Canvas(400, 400)
    can.tentacle(200, 100, 200, 300, curl=-0.5, thickness=20, taper=0.3)
    svg = can.to_svg()

    assert 'polygon' in svg


def test_tentacle_taper():
    """Tentacle respects taper parameter."""
    can = Canvas(400, 400)
    # High taper (thick tip)
    can.tentacle(150, 100, 150, 300, thickness=30, taper=0.9)
    # Low taper (thin tip)
    can.tentacle(250, 100, 250, 300, thickness=30, taper=0.1)
    svg = can.to_svg()

    # Should have two tentacles
    polygon_count = svg.count('<polygon')
    assert polygon_count == 2


def test_tentacle_twist():
    """Tentacle with twist creates S-curves."""
    can = Canvas(400, 400)
    # Simple curve (no twist)
    can.tentacle(100, 100, 100, 300, curl=0.5, twist=0, thickness=20)
    # S-curve (with twist)
    can.tentacle(200, 100, 200, 300, curl=0.5, twist=0.7, thickness=20)
    svg = can.to_svg()

    # Should have two tentacles
    polygon_count = svg.count('<polygon')
    assert polygon_count == 2


def test_tentacle_twist_maximum():
    """Tentacle with maximum twist."""
    can = Canvas(400, 400)
    can.tentacle(200, 100, 200, 300, curl=0.5, twist=1.0, thickness=25)
    svg = can.to_svg()

    assert 'polygon' in svg


def test_ocean_shapes_octopus():
    """Octopus renders without errors."""
    can = Canvas(600, 600)
    ocean = OceanShapes(can)
    ocean.octopus(300, 250, size=120)
    svg = can.to_svg()

    # Should contain blob (head) + 8 tentacles + eyes
    # At minimum: 1 head + 8 tentacles = 9 polygons
    polygon_count = svg.count('<polygon')
    assert polygon_count >= 9

    # Should have circles for eyes
    circle_count = svg.count('<circle')
    assert circle_count >= 4  # 2 white eyes + 2 black pupils


def test_ocean_shapes_octopus_custom_colors():
    """Octopus respects color parameters."""
    can = Canvas(600, 600)
    ocean = OceanShapes(can)
    ocean.octopus(300, 250, size=120,
                  body_color=OceanPalette.STARFISH_ORANGE,
                  eye_color=OceanPalette.SHELL_WHITE)
    svg = can.to_svg()

    assert OceanPalette.STARFISH_ORANGE in svg
    assert OceanPalette.SHELL_WHITE in svg


def test_ocean_shapes_jellyfish():
    """Jellyfish renders without errors."""
    can = Canvas(600, 600)
    ocean = OceanShapes(can)
    ocean.jellyfish(300, 200, size=80, tentacle_count=6)
    svg = can.to_svg()

    # Should contain bell + 6 tentacles = 7 polygons minimum
    polygon_count = svg.count('<polygon')
    assert polygon_count >= 7


def test_ocean_shapes_seaweed():
    """Seaweed renders without errors."""
    can = Canvas(600, 600)
    ocean = OceanShapes(can)
    ocean.seaweed(300, 500, height=150, sway=0.3)
    svg = can.to_svg()

    # Should contain main stem + leaf blobs
    polygon_count = svg.count('<polygon')
    assert polygon_count >= 4  # 1 stem + at least 3 leaves


def test_ocean_shapes_chaining():
    """OceanShapes methods support chaining."""
    can = Canvas(800, 600)
    ocean = OceanShapes(can)

    result = (ocean
              .octopus(200, 200, size=80)
              .jellyfish(500, 150, size=60)
              .seaweed(100, 600, height=120))

    assert result is ocean


def test_ocean_palette_exists():
    """OceanPalette has expected colors."""
    assert hasattr(OceanPalette, 'DEEP_OCEAN')
    assert hasattr(OceanPalette, 'CORAL')
    assert hasattr(OceanPalette, 'PURPLE_CORAL')
    assert hasattr(OceanPalette, 'KELP_GREEN')
    assert hasattr(OceanPalette, 'TRANSLUCENT_BLUE')

    # Colors should be hex strings
    assert OceanPalette.DEEP_OCEAN.startswith('#')
    assert len(OceanPalette.CORAL) == 7  # #RRGGBB format


def test_complete_ocean_scene():
    """Integration test: build complete ocean scene."""
    can = Canvas(800, 600, background=OceanPalette.SHALLOW_WATER)
    ocean = OceanShapes(can)

    # Add various ocean elements
    ocean.octopus(400, 300, size=150, body_color=OceanPalette.PURPLE_CORAL)
    ocean.jellyfish(200, 150, size=80, tentacle_count=6)
    ocean.seaweed(100, 600, height=150)
    ocean.seaweed(700, 600, height=120)

    # Add waves
    can.wave(0, 50, 800, 50, height=20, waves=5, stroke=OceanPalette.SEAFOAM)

    # Add some blobs for rocks or coral
    can.blob(150, 550, radius=30, wobble=0.4, fill=OceanPalette.SAND)

    svg = can.to_svg()

    # Verify scene has substantial content
    assert len(svg) > 1000  # Should be a rich SVG
    assert OceanPalette.PURPLE_CORAL in svg
    assert OceanPalette.SEAFOAM in svg
    assert 'polygon' in svg
    assert 'polyline' in svg


def test_ocean_gradients_registered():
    """OceanShapes automatically registers gradients on init."""
    can = Canvas(800, 600)
    ocean = OceanShapes(can)

    # Verify gradients exist in canvas
    assert "ocean_octopus_body" in can.gradients
    assert "ocean_jellyfish_glow" in can.gradients
    assert "ocean_seaweed_depth" in can.gradients
    assert "ocean_tentacle_shading" in can.gradients


def test_octopus_uses_gradient_by_default():
    """Octopus uses gradient fill by default."""
    can = Canvas(800, 600)
    ocean = OceanShapes(can)
    ocean.octopus(400, 300)

    svg = can.to_svg()

    # Should contain gradient definition
    assert "grad_ocean_octopus_body" in svg
    # Should reference gradient in shapes
    assert "url(#grad_ocean_octopus_body)" in svg


def test_jellyfish_uses_gradient_by_default():
    """Jellyfish uses gradient fill by default."""
    can = Canvas(800, 600)
    ocean = OceanShapes(can)
    ocean.jellyfish(400, 300)

    svg = can.to_svg()

    # Should contain gradient definition
    assert "grad_ocean_jellyfish_glow" in svg
    # Should reference gradient in shapes
    assert "url(#grad_ocean_jellyfish_glow)" in svg


def test_seaweed_uses_gradient_by_default():
    """Seaweed uses gradient fill by default."""
    can = Canvas(800, 600)
    ocean = OceanShapes(can)
    ocean.seaweed(400, 500)

    svg = can.to_svg()

    # Should contain gradient definition
    assert "grad_ocean_seaweed_depth" in svg
    # Should reference gradient in shapes
    assert "url(#grad_ocean_seaweed_depth)" in svg


def test_octopus_can_override_with_solid_color():
    """Octopus can use solid color instead of gradient."""
    can = Canvas(800, 600)
    ocean = OceanShapes(can)
    ocean.octopus(400, 300, body_color=Color.PURPLE)

    svg = can.to_svg()

    # Should use solid color
    assert Color.PURPLE in svg
    # Should NOT reference octopus body gradient in shapes
    # (gradient def exists but isn't used)
    assert "url(#grad_ocean_octopus_body)" not in svg


def test_jellyfish_can_override_with_solid_color():
    """Jellyfish can use solid color instead of gradient."""
    can = Canvas(800, 600)
    ocean = OceanShapes(can)
    ocean.jellyfish(400, 300, body_color=OceanPalette.PURPLE_CORAL)

    svg = can.to_svg()

    # Should use solid color
    assert OceanPalette.PURPLE_CORAL in svg
    # Should NOT reference jellyfish gradient in shapes
    assert "url(#grad_ocean_jellyfish_glow)" not in svg


def test_seaweed_can_override_with_solid_color():
    """Seaweed can use solid color instead of gradient."""
    can = Canvas(800, 600)
    ocean = OceanShapes(can)
    ocean.seaweed(400, 500, color=OceanPalette.SEA_GREEN)

    svg = can.to_svg()

    # Should use solid color
    assert OceanPalette.SEA_GREEN in svg
    # Should NOT reference seaweed gradient in shapes
    assert "url(#grad_ocean_seaweed_depth)" not in svg
