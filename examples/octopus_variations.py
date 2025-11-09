"""
Octopus Variations Demo - Testing three different octopus styles
"""

import marimo

__generated_with = "0.10.13"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    from sketchpy import Canvas, Color, OceanShapes
    from sketchpy.palettes import OceanPalette
    return Canvas, Color, OceanPalette, OceanShapes


@app.cell
def _(mo):
    mo.md(
        """
        # Octopus Variations Demo

        Testing three different octopus styles with improved anatomy:

        1. **Classic** - Pear-shaped head, evenly spread tentacles
        2. **Realistic** - Grouped tentacles (4 per side)
        3. **Cartoon** - Exaggerated features with curly tentacles

        All three styles now have:
        - Tentacles drawn **behind** the head (not on top)
        - Pear-shaped head (wide top, narrow bottom)
        - Better tentacle attachment points
        - Visible tentacle curvatures when gradients are applied
        """
    )
    return


@app.cell
def _(Canvas, OceanShapes, OceanPalette):
    # Classic style octopus
    can_classic = Canvas(800, 600, background=OceanPalette.OCEAN_FLOOR)

    # Add gradient to show tentacle placement
    can_classic.radial_gradient(
        "octopus_gradient",
        center=(50, 30),
        radius=80,
        colors=[OceanPalette.CORAL, OceanPalette.PURPLE_CORAL]
    )

    ocean_classic = OceanShapes(can_classic)
    ocean_classic.octopus(
        400, 150, size=150,
        body_color="gradient:octopus_gradient"
    )

    can_classic
    return can_classic, ocean_classic


@app.cell
def _(Canvas, OceanShapes, OceanPalette):
    # Realistic style octopus
    can_realistic = Canvas(800, 600, background=OceanPalette.OCEAN_FLOOR)

    # Gradient to highlight anatomy
    can_realistic.radial_gradient(
        "octopus_gradient2",
        center=(50, 30),
        radius=80,
        colors=[OceanPalette.SUNSET_ORANGE, OceanPalette.CORAL_REEF]
    )

    ocean_realistic = OceanShapes(can_realistic)
    ocean_realistic.octopus(
        400, 150, size=150,
        body_color="gradient:octopus_gradient2",
        style="realistic"
    )

    can_realistic
    return can_realistic, ocean_realistic


@app.cell
def _(Canvas, OceanShapes, OceanPalette):
    # Cartoon style octopus
    can_cartoon = Canvas(800, 600, background=OceanPalette.OCEAN_FLOOR)

    # Fun gradient for cartoon
    can_cartoon.radial_gradient(
        "octopus_gradient3",
        center=(50, 30),
        radius=80,
        colors=[OceanPalette.PINK_CORAL, OceanPalette.PURPLE_CORAL]
    )

    ocean_cartoon = OceanShapes(can_cartoon)
    ocean_cartoon.octopus(
        400, 150, size=150,
        body_color="gradient:octopus_gradient3",
        style="cartoon"
    )

    can_cartoon
    return can_cartoon, ocean_cartoon


@app.cell
def _(Canvas, OceanShapes, OceanPalette, Color):
    # Comparison view - all three side by side
    can_compare = Canvas(1200, 400, background=OceanPalette.DEEP_OCEAN)

    # Add some underwater ambiance
    can_compare.circle(200, 100, 80, fill=OceanPalette.SEAFOAM_GREEN, opacity=0.3)
    can_compare.circle(1000, 150, 100, fill=OceanPalette.SEAFOAM_GREEN, opacity=0.3)

    ocean_compare = OceanShapes(can_compare)

    # Classic
    can_compare.radial_gradient("grad1", colors=[OceanPalette.CORAL, OceanPalette.SUNSET_ORANGE])
    ocean_compare.octopus(200, 100, size=120, body_color="gradient:grad1", style="classic")

    # Realistic
    can_compare.radial_gradient("grad2", colors=[OceanPalette.PURPLE_CORAL, OceanPalette.PINK_CORAL])
    ocean_compare.octopus(600, 100, size=120, body_color="gradient:grad2", style="realistic")

    # Cartoon
    can_compare.radial_gradient("grad3", colors=[OceanPalette.SUNSET_ORANGE, OceanPalette.CORAL_REEF])
    ocean_compare.octopus(1000, 100, size=120, body_color="gradient:grad3", style="cartoon")

    # Labels
    can_compare.text(155, 380, "CLASSIC", size=18, fill=Color.WHITE)
    can_compare.text(545, 380, "REALISTIC", size=18, fill=Color.WHITE)
    can_compare.text(950, 380, "CARTOON", size=18, fill=Color.WHITE)

    can_compare
    return can_compare, ocean_compare


@app.cell
def _(Canvas, Color):
    # Test the new pear primitive on its own
    can_pear = Canvas(800, 400, background="#F0F0F0")

    # Show pears in different sizes and orientations
    can_pear.pear(150, 50, width=80, height=120, fill=Color.GREEN, stroke=Color.DARKGREEN, stroke_width=2)
    can_pear.pear(350, 50, width=120, height=100, fill=Color.YELLOW, stroke=Color.ORANGE, stroke_width=2)
    can_pear.pear(600, 50, width=100, height=140, fill=Color.RED, stroke=Color.DARKRED, stroke_width=2)

    # Labels
    can_pear.text(100, 200, "Tall & Narrow", size=14, fill=Color.BLACK)
    can_pear.text(290, 180, "Short & Wide", size=14, fill=Color.BLACK)
    can_pear.text(550, 220, "Classic Pear", size=14, fill=Color.BLACK)

    can_pear
    return (can_pear,)


@app.cell
def _(mo):
    mo.md(
        """
        ## Key Improvements

        ### Drawing Order
        - Tentacles are now drawn **before** the head
        - This makes them appear behind, creating depth
        - The head overlaps the tentacle bases naturally

        ### Pear-Shaped Head
        - New `pear()` primitive method added to Canvas
        - Wide at top (mantle), narrow at bottom
        - Provides better attachment points for tentacles
        - More anatomically correct for octopus/cephalopod shape

        ### Tentacle Placement
        - **Classic**: Evenly spread across bottom edge
        - **Realistic**: Grouped (4 left, 4 right) for natural look
        - **Cartoon**: Wide spread with exaggerated curves

        ### Gradient Visibility
        - With gradients applied, tentacle curvatures are now visible
        - No penetration into head
        - Clean attachment at the narrow bottom of pear shape
        """
    )
    return


if __name__ == "__main__":
    app.run()
