"""Tests for color palette classes."""

import pytest
from sketchpy import Color, CalmOasisPalette, CreativeGardenPalette, MathDoodlingPalette, OceanPalette


class TestColorPalette:
    """Test basic Color palette."""

    def test_color_red(self):
        """Color.RED is defined."""
        assert Color.RED == "#FF0000"

    def test_color_blue(self):
        """Color.BLUE is defined."""
        assert Color.BLUE == "#0000FF"

    def test_color_green(self):
        """Color.GREEN is defined."""
        assert Color.GREEN == "#00FF00"

    def test_color_yellow(self):
        """Color.YELLOW is defined."""
        assert Color.YELLOW == "#FFFF00"

    def test_color_black(self):
        """Color.BLACK is defined."""
        assert Color.BLACK == "#000000"

    def test_color_white(self):
        """Color.WHITE is defined."""
        assert Color.WHITE == "#FFFFFF"

    def test_color_gray(self):
        """Color.GRAY is defined."""
        assert Color.GRAY == "#808080"

    def test_color_orange(self):
        """Color.ORANGE is defined."""
        assert Color.ORANGE == "#FFA500"

    def test_color_purple(self):
        """Color.PURPLE is defined."""
        assert Color.PURPLE == "#800080"

    def test_color_pink(self):
        """Color.PINK is defined."""
        assert Color.PINK == "#FFC0CB"

    def test_color_brown(self):
        """Color.BROWN is defined."""
        assert Color.BROWN == "#8B4513"

    def test_color_silver(self):
        """Color.SILVER is defined."""
        assert Color.SILVER == "#C0C0C0"

    def test_all_colors_are_hex(self):
        """All Color constants are valid hex strings."""
        for attr_name in dir(Color):
            if not attr_name.startswith('_'):
                value = getattr(Color, attr_name)
                if isinstance(value, str):
                    assert value.startswith('#'), f"{attr_name} should start with #"
                    assert len(value) == 7, f"{attr_name} should be #RRGGBB format"


class TestCalmOasisPalette:
    """Test CalmOasisPalette colors."""

    def test_sky_blue(self):
        """SKY_BLUE is defined."""
        assert CalmOasisPalette.SKY_BLUE == "#A5C8E4"

    def test_mint_fresh(self):
        """MINT_FRESH is defined."""
        assert CalmOasisPalette.MINT_FRESH == "#B0E0A8"

    def test_lavender_mist(self):
        """LAVENDER_MIST is defined."""
        assert CalmOasisPalette.LAVENDER_MIST == "#E5DAFF"

    def test_powder_blue(self):
        """POWDER_BLUE is defined."""
        assert CalmOasisPalette.POWDER_BLUE == "#BFEFFF"

    def test_sage_green(self):
        """SAGE_GREEN is defined."""
        assert CalmOasisPalette.SAGE_GREEN == "#C0ECCC"

    def test_periwinkle(self):
        """PERIWINKLE is defined."""
        assert CalmOasisPalette.PERIWINKLE == "#CCCCFF"

    def test_cream(self):
        """CREAM is defined."""
        assert CalmOasisPalette.CREAM == "#FFF7D4"

    def test_soft_aqua(self):
        """SOFT_AQUA is defined."""
        assert CalmOasisPalette.SOFT_AQUA == "#AFDFE5"

    def test_pale_lilac(self):
        """PALE_LILAC is defined."""
        assert CalmOasisPalette.PALE_LILAC == "#E6D5FF"

    def test_cloud_white(self):
        """CLOUD_WHITE is defined."""
        assert CalmOasisPalette.CLOUD_WHITE == "#F5F5F5"

    def test_mist_gray(self):
        """MIST_GRAY is defined."""
        assert CalmOasisPalette.MIST_GRAY == "#D3D3D3"

    def test_seafoam(self):
        """SEAFOAM is defined."""
        assert CalmOasisPalette.SEAFOAM == "#C8FFE1"

    def test_all_colors_are_hex(self):
        """All CalmOasisPalette constants are valid hex strings."""
        for attr_name in dir(CalmOasisPalette):
            if not attr_name.startswith('_'):
                value = getattr(CalmOasisPalette, attr_name)
                if isinstance(value, str):
                    assert value.startswith('#'), f"{attr_name} should start with #"
                    assert len(value) == 7, f"{attr_name} should be #RRGGBB format"


class TestCreativeGardenPalette:
    """Test CreativeGardenPalette colors."""

    def test_peach_whisper(self):
        """PEACH_WHISPER is defined."""
        assert CreativeGardenPalette.PEACH_WHISPER == "#FFDAC1"

    def test_rose_quartz(self):
        """ROSE_QUARTZ is defined."""
        assert CreativeGardenPalette.ROSE_QUARTZ == "#F6A8A6"

    def test_butter_yellow(self):
        """BUTTER_YELLOW is defined."""
        assert CreativeGardenPalette.BUTTER_YELLOW == "#FFF0A3"

    def test_mint_cream(self):
        """MINT_CREAM is defined."""
        assert CreativeGardenPalette.MINT_CREAM == "#C0ECCC"

    def test_sky_breeze(self):
        """SKY_BREEZE is defined."""
        assert CreativeGardenPalette.SKY_BREEZE == "#A5C8E4"

    def test_lilac_dream(self):
        """LILAC_DREAM is defined."""
        assert CreativeGardenPalette.LILAC_DREAM == "#D5C3E0"

    def test_coral_blush(self):
        """CORAL_BLUSH is defined."""
        assert CreativeGardenPalette.CORAL_BLUSH == "#FFB3B3"

    def test_lemon_chiffon(self):
        """LEMON_CHIFFON is defined."""
        assert CreativeGardenPalette.LEMON_CHIFFON == "#F9F0C1"

    def test_misty_mauve(self):
        """MISTY_MAUVE is defined."""
        assert CreativeGardenPalette.MISTY_MAUVE == "#E8D4E8"

    def test_honeydew(self):
        """HONEYDEW is defined."""
        assert CreativeGardenPalette.HONEYDEW == "#E8F5E3"

    def test_vanilla_cream(self):
        """VANILLA_CREAM is defined."""
        assert CreativeGardenPalette.VANILLA_CREAM == "#FAF0E6"

    def test_dove_gray(self):
        """DOVE_GRAY is defined."""
        assert CreativeGardenPalette.DOVE_GRAY == "#D5D5D5"

    def test_all_colors_are_hex(self):
        """All CreativeGardenPalette constants are valid hex strings."""
        for attr_name in dir(CreativeGardenPalette):
            if not attr_name.startswith('_'):
                value = getattr(CreativeGardenPalette, attr_name)
                if isinstance(value, str):
                    assert value.startswith('#'), f"{attr_name} should start with #"
                    assert len(value) == 7, f"{attr_name} should be #RRGGBB format"


class TestMathDoodlingPalette:
    """Test MathDoodlingPalette colors."""

    def test_mist_blue(self):
        """MIST_BLUE is defined."""
        assert MathDoodlingPalette.MIST_BLUE == "#93C5FD"

    def test_mist_rose(self):
        """MIST_ROSE is defined."""
        assert MathDoodlingPalette.MIST_ROSE == "#FCA5A5"

    def test_mist_mint(self):
        """MIST_MINT is defined."""
        assert MathDoodlingPalette.MIST_MINT == "#86EFAC"

    def test_deep_blue(self):
        """DEEP_BLUE is defined."""
        assert MathDoodlingPalette.DEEP_BLUE == "#3B82F6"

    def test_warm_coral(self):
        """WARM_CORAL is defined."""
        assert MathDoodlingPalette.WARM_CORAL == "#F87171"

    def test_fresh_green(self):
        """FRESH_GREEN is defined."""
        assert MathDoodlingPalette.FRESH_GREEN == "#4ADE80"

    def test_paper_white(self):
        """PAPER_WHITE is defined."""
        assert MathDoodlingPalette.PAPER_WHITE == "#FAFAFA"

    def test_pencil_grey(self):
        """PENCIL_GREY is defined."""
        assert MathDoodlingPalette.PENCIL_GREY == "#E5E7EB"

    def test_all_colors_are_hex(self):
        """All MathDoodlingPalette constants are valid hex strings."""
        for attr_name in dir(MathDoodlingPalette):
            if not attr_name.startswith('_'):
                value = getattr(MathDoodlingPalette, attr_name)
                if isinstance(value, str):
                    assert value.startswith('#'), f"{attr_name} should start with #"
                    assert len(value) == 7, f"{attr_name} should be #RRGGBB format"


class TestOceanPalette:
    """Test OceanPalette colors."""

    def test_deep_ocean(self):
        """DEEP_OCEAN is defined."""
        assert OceanPalette.DEEP_OCEAN == "#0A2E4D"

    def test_ocean_blue(self):
        """OCEAN_BLUE is defined."""
        assert OceanPalette.OCEAN_BLUE == "#1E5A8E"

    def test_shallow_water(self):
        """SHALLOW_WATER is defined."""
        assert OceanPalette.SHALLOW_WATER == "#4A90C8"

    def test_seafoam(self):
        """SEAFOAM is defined."""
        assert OceanPalette.SEAFOAM == "#88C7DC"

    def test_kelp_green(self):
        """KELP_GREEN is defined."""
        assert OceanPalette.KELP_GREEN == "#2D5C3F"

    def test_sea_green(self):
        """SEA_GREEN is defined."""
        assert OceanPalette.SEA_GREEN == "#4A8B6F"

    def test_coral(self):
        """CORAL is defined."""
        assert OceanPalette.CORAL == "#E8695C"

    def test_purple_coral(self):
        """PURPLE_CORAL is defined."""
        assert OceanPalette.PURPLE_CORAL == "#A27BA2"

    def test_starfish_orange(self):
        """STARFISH_ORANGE is defined."""
        assert OceanPalette.STARFISH_ORANGE == "#F4A460"

    def test_tropical_yellow(self):
        """TROPICAL_YELLOW is defined."""
        assert OceanPalette.TROPICAL_YELLOW == "#FFD966"

    def test_sand(self):
        """SAND is defined."""
        assert OceanPalette.SAND == "#D4C5A9"

    def test_shell_white(self):
        """SHELL_WHITE is defined."""
        assert OceanPalette.SHELL_WHITE == "#F5F1E8"

    def test_translucent_blue(self):
        """TRANSLUCENT_BLUE is defined."""
        assert OceanPalette.TRANSLUCENT_BLUE == "#A8D8EA"

    def test_all_colors_are_hex(self):
        """All OceanPalette constants are valid hex strings."""
        for attr_name in dir(OceanPalette):
            if not attr_name.startswith('_'):
                value = getattr(OceanPalette, attr_name)
                if isinstance(value, str):
                    assert value.startswith('#'), f"{attr_name} should start with #"
                    assert len(value) == 7, f"{attr_name} should be #RRGGBB format"


class TestPaletteUsage:
    """Test that palette colors work in Canvas methods."""

    def test_basic_color_in_canvas(self):
        """Basic Color constants work in canvas shapes."""
        from sketchpy import Canvas

        canvas = Canvas(400, 400)
        canvas.circle(200, 200, 50, fill=Color.RED, stroke=Color.BLUE)
        svg = canvas.to_svg()

        assert Color.RED in svg
        assert Color.BLUE in svg

    def test_calm_oasis_in_canvas(self):
        """CalmOasisPalette colors work in canvas shapes."""
        from sketchpy import Canvas

        canvas = Canvas(400, 400, background=CalmOasisPalette.SKY_BLUE)
        canvas.rect(100, 100, 200, 200, fill=CalmOasisPalette.MINT_FRESH)
        svg = canvas.to_svg()

        assert CalmOasisPalette.SKY_BLUE in svg
        assert CalmOasisPalette.MINT_FRESH in svg

    def test_creative_garden_in_canvas(self):
        """CreativeGardenPalette colors work in canvas shapes."""
        from sketchpy import Canvas

        canvas = Canvas(400, 400)
        canvas.circle(200, 200, 50, fill=CreativeGardenPalette.PEACH_WHISPER)
        svg = canvas.to_svg()

        assert CreativeGardenPalette.PEACH_WHISPER in svg

    def test_math_doodling_in_canvas(self):
        """MathDoodlingPalette colors work in canvas shapes."""
        from sketchpy import Canvas

        canvas = Canvas(400, 400)
        canvas.ellipse(200, 200, 100, 50, fill=MathDoodlingPalette.MIST_BLUE)
        svg = canvas.to_svg()

        assert MathDoodlingPalette.MIST_BLUE in svg

    def test_ocean_palette_in_canvas(self):
        """OceanPalette colors work in canvas shapes."""
        from sketchpy import Canvas

        canvas = Canvas(400, 400, background=OceanPalette.DEEP_OCEAN)
        canvas.polygon(
            points=[(100, 50), (150, 100), (100, 150), (50, 100)],
            fill=OceanPalette.CORAL
        )
        svg = canvas.to_svg()

        assert OceanPalette.DEEP_OCEAN in svg
        assert OceanPalette.CORAL in svg
