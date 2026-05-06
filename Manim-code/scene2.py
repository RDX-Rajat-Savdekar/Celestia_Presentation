from manim import *
import numpy as np

# =====================================================================
# SCENE 2: "6,000 out of 119,000"
# Topic: Apparent magnitude filter reducing the HYG catalog for VR perf
# Clips: S2_Clip1_DataOverload, S2_Clip2_ApparentMagnitude,
#        S2_Clip3_TheFilter, S2_Clip4_OptimizedSky
#
# RENDER NOTE: Change DISPLAY_STARS to 3000 for final high-res render.
# Keep at 400 for fast test previews.
# =====================================================================

DISPLAY_STARS = 400
MAG_THRESHOLD = 6.5
SPACE_BG = "#000000"
STAR_YELLOW = "#FFD700"
NEBULA_BLUE = "#4FC3F7"
ERROR_RED = "#EF5350"
SUCCESS_GREEN = "#66BB6A"

# Magnitude axis screen layout
AXIS_X = 4.8          # X position of the vertical magnitude axis
Y_AXIS_TOP = 3.2      # Screen Y for mag = -2 (brightest end)
Y_AXIS_BOT = -3.2     # Screen Y for mag = 10 (faintest end)

# =====================================================================
# HELPERS
# =====================================================================

def mag_to_y(mag):
    """Magnitude → screen Y.  Low (bright) mag = top, high (faint) mag = bottom."""
    return Y_AXIS_TOP + (mag - (-2)) / 12.0 * (Y_AXIS_BOT - Y_AXIS_TOP)


def get_star_data():
    """
    Returns a dict of star properties with a fixed seed for cross-clip consistency.
    ~82% faint stars (mag > threshold), ~18% bright — realistic catalog ratio.
    Stars are scattered in the left 75% of the screen (x ≤ 3.8).
    """
    np.random.seed(42)
    n = DISPLAY_STARS

    mask = np.random.uniform(0, 1, n) < 0.82
    mags = np.where(
        mask,
        np.random.uniform(MAG_THRESHOLD + 0.1, 9.5, n),
        np.random.uniform(-1.5, MAG_THRESHOLD, n)
    )
    xs = np.random.uniform(-6.2, 3.8, n)
    ys = np.random.uniform(-3.5, 3.5, n)
    sizes = np.clip(0.10 - mags * 0.007, 0.018, 0.09).astype(float)
    # Raise the opacity floor so faint stars are clearly visible before the filter removes them
    opacities = np.clip(1.0 - mags / 13.0, 0.45, 1.0).astype(float)

    colors = []
    for m in mags:
        if m < 0:
            colors.append("#9EC8FF")
        elif m < 2:
            colors.append("#FFFFFF")
        elif m < 4.5:
            colors.append("#FFFACC")
        else:
            colors.append("#AAAAAA")   # lighter gray — visible enough to notice disappearing

    return dict(
        n=n, mags=mags, xs=xs, ys=ys,
        sizes=sizes, opacities=opacities, colors=colors,
        above=mags > MAG_THRESHOLD
    )


def make_all_dots(data):
    """Single ordered VGroup of all star dots — index-stable for per-star FadeOut."""
    dots = VGroup()
    for i in range(data["n"]):
        dots.add(
            Dot(
                point=np.array([data["xs"][i], data["ys"][i], 0]),
                radius=float(data["sizes"][i]),
                color=data["colors"][i],
                fill_opacity=float(data["opacities"][i]),
            ).set_stroke(width=0)
        )
    return dots



def make_mag_axis():
    """Builds the vertical magnitude axis (axis line, ticks, labels, brightness arrow)."""
    grp = VGroup()

    # Main axis line
    grp.add(
        Line(
            np.array([AXIS_X, Y_AXIS_TOP, 0]),
            np.array([AXIS_X, Y_AXIS_BOT, 0]),
            color=NEBULA_BLUE,
            stroke_width=2.5,
        )
    )

    # Axis title
    title = Text("Vmag", font_size=20, color=NEBULA_BLUE)
    title.move_to(np.array([AXIS_X, Y_AXIS_TOP + 0.45, 0]))
    subtitle = Text("apparent magnitude", font_size=12, color=NEBULA_BLUE)
    subtitle.next_to(title, DOWN, buff=0.04)
    grp.add(title, subtitle)

    # Brightness direction indicator
    bright_arrow = Text("↑ Brighter", font_size=13, color=STAR_YELLOW)
    bright_arrow.move_to(np.array([AXIS_X, Y_AXIS_TOP + 1.0, 0]))
    grp.add(bright_arrow)

    # Tick marks and labels: (magnitude, display_text, color)
    ticks = [
        (-1.46, "Sirius  −1.46", STAR_YELLOW),
        (0.03,  "Vega   0.0",    WHITE),
        (2.0,   "2",             "#CCCCCC"),
        (4.0,   "4",             "#999999"),
        (6.5,   "6.5",           SUCCESS_GREEN),
        (8.5,   "8.5",           "#555555"),
    ]
    for mag, lbl, col in ticks:
        y = mag_to_y(mag)
        tick = Line(
            np.array([AXIS_X - 0.18, y, 0]),
            np.array([AXIS_X + 0.18, y, 0]),
            color=col,
            stroke_width=2,
        )
        t = Text(lbl, font_size=13, color=col)
        t.next_to(np.array([AXIS_X, y, 0]), LEFT, buff=0.28)
        grp.add(tick, t)

    return grp


def make_threshold_line():
    """Dashed threshold line at MAG_THRESHOLD with label."""
    y = mag_to_y(MAG_THRESHOLD)
    line = DashedLine(
        np.array([-7.2, y, 0]),
        np.array([AXIS_X + 0.18, y, 0]),
        color=SUCCESS_GREEN,
        dash_length=0.22,
        stroke_width=2.5,
    )
    label = Text(
        f"Naked-eye limit  Vmag ≤ {MAG_THRESHOLD}",
        font_size=15,
        color=SUCCESS_GREEN,
    )
    label.move_to(np.array([-1.2, y + 0.35, 0]))
    return VGroup(line, label)


def make_fps_hud(fps_value, good: bool):
    """Static FPS counter widget — safe for add/FadeIn/FadeOut (NOT Transform)."""
    col = SUCCESS_GREEN if good else ERROR_RED
    txt = Text(f"FPS: {fps_value}", font_size=18, color=col)
    bg  = Rectangle(
        width=txt.width + 0.28, height=txt.height + 0.28,
        fill_color="#0a0a1a", fill_opacity=0.85,
        stroke_color=col, stroke_width=1.5,
    ).move_to(txt)
    return VGroup(bg, txt).to_corner(UR, buff=0.3)


def get_sphere_stars(n=80):
    """Spherical star cloud for Clip 4 (the optimized 3D sky)."""
    np.random.seed(42)
    R = 2.5
    stars = VGroup()
    for _ in range(n):
        phi = np.arccos(np.random.uniform(-1, 1))
        theta = np.random.uniform(0, 2 * np.pi)
        pos = np.array([
            R * np.sin(phi) * np.cos(theta),
            R * np.sin(phi) * np.sin(theta),
            R * np.cos(phi),
        ])
        col = np.random.choice(["#FFFFE0", "#FFFFFF", "#9EC8FF"])
        stars.add(Square(side_length=0.015, color=col).move_to(pos))
    return stars


# =====================================================================
# CLIP 1: Data Overload
# manim --renderer=opengl -qh --write_to_movie scene2.py S2_Clip1_DataOverload
# =====================================================================
class S2_Clip1_DataOverload(Scene):
    def construct(self):
        self.camera.background_color = SPACE_BG

        title = Text("6,000 out of 119,000", font_size=34, color=WHITE).to_corner(UL)
        self.play(Write(title), run_time=0.8)

        catalog_label = Text(
            "HYG Star Catalog v4.2  —  119,000 stars",
            font_size=20, color=NEBULA_BLUE
        ).to_edge(DOWN, buff=0.55)

        # ValueTracker drives the smooth FPS countdown.
        # always_redraw rebuilds the widget each frame so the number AND
        # color (green → red) animate together without any Transform-on-Text bug.
        fps_val = ValueTracker(60)

        def build_fps_hud():
            val = int(fps_val.get_value())
            t   = max(0.0, (60 - val) / 46.0)   # 0 at FPS=60, 1 at FPS=14
            col = interpolate_color(ManimColor(SUCCESS_GREEN), ManimColor(ERROR_RED), t)
            txt = Text(f"FPS: {val}", font_size=18, color=col)
            bg  = Rectangle(
                width=txt.width + 0.28, height=txt.height + 0.28,
                fill_color="#0a0a1a", fill_opacity=0.85,
                stroke_color=col, stroke_width=1.5,
            ).move_to(txt)
            return VGroup(bg, txt).to_corner(UR, buff=0.3)

        fps_hud = always_redraw(build_fps_hud)

        data  = get_star_data()
        stars = make_all_dots(data)

        self.play(FadeIn(fps_hud), Write(catalog_label), run_time=0.6)
        self.play(FadeIn(stars), run_time=2)

        vr_warn = Text("VR minimum: 72 FPS", font_size=16, color=ERROR_RED)
        vr_warn.to_corner(UR, buff=0.3).shift(DOWN * 1.15)

        # Single play: FPS counts down AND warning fades in together
        self.play(
            fps_val.animate.set_value(14),
            FadeIn(vr_warn),
            run_time=2.0,
            rate_func=smooth,
        )
        self.wait(2.0)


# =====================================================================
# CLIP 2: Apparent Magnitude
# manim --renderer=opengl -qh --write_to_movie scene2.py S2_Clip2_ApparentMagnitude
# =====================================================================
class S2_Clip2_ApparentMagnitude(Scene):
    def construct(self):
        self.camera.background_color = SPACE_BG

        # MATCH CUT: Reproduce Clip 1 end state exactly
        title = Text("6,000 out of 119,000", font_size=34, color=WHITE).to_corner(UL)
        catalog_label = Text(
            "HYG Star Catalog v4.2  —  119,000 stars",
            font_size=20, color=NEBULA_BLUE
        ).to_edge(DOWN, buff=0.55)
        fps_hud = make_fps_hud(14, good=False)
        vr_warn = Text("VR minimum: 72 FPS", font_size=16, color=ERROR_RED)
        vr_warn.to_corner(UR, buff=0.3).shift(DOWN * 1.15)

        data = get_star_data()
        stars = make_all_dots(data)

        self.add(title, catalog_label, fps_hud, vr_warn, stars)
        self.wait(0.3)

        # Reveal magnitude axis
        mag_axis = make_mag_axis()
        self.play(Create(mag_axis), run_time=2.2)

        # Callout: lower = brighter (the counter-intuitive part)
        # Positioned mid-left in the open star field, away from title and axis
        lower_note = Text("lower number = brighter star", font_size=14, color=STAR_YELLOW)
        lower_note.move_to(np.array([0.0, 0.0, 0]))
        lower_bg = SurroundingRectangle(
            lower_note, fill_color="#1a1500",
            fill_opacity=0.8, stroke_color=STAR_YELLOW, buff=0.14
        )
        callout = VGroup(lower_bg, lower_note)
        self.play(FadeIn(callout), run_time=0.8)

        # Highlight Sirius and Vega — dots sit ON the axis tick line
        sirius_pos = np.array([AXIS_X, mag_to_y(-1.46), 0])
        vega_pos   = np.array([AXIS_X, mag_to_y(0.03),  0])

        sirius_dot  = Dot(sirius_pos, radius=0.16, color=STAR_YELLOW)
        sirius_ring = Circle(radius=0.30, color=STAR_YELLOW,
                             stroke_width=1.5, stroke_opacity=0.6).move_to(sirius_pos)
        vega_dot    = Dot(vega_pos, radius=0.12, color=WHITE)

        self.play(
            FadeIn(sirius_dot), Create(sirius_ring),
            FadeIn(vega_dot),
            run_time=1.2
        )
        self.wait(2.5)


# =====================================================================
# CLIP 3: The Filter
# manim --renderer=opengl -qh --write_to_movie scene2.py S2_Clip3_TheFilter
# =====================================================================
class S2_Clip3_TheFilter(Scene):
    def construct(self):
        self.camera.background_color = SPACE_BG

        # MATCH CUT: Reproduce Clip 2 end state
        title = Text("6,000 out of 119,000", font_size=34, color=WHITE).to_corner(UL)
        fps_hud = make_fps_hud(14, good=False)
        vr_warn = Text("VR minimum: 72 FPS", font_size=16, color=ERROR_RED)
        vr_warn.to_corner(UR, buff=0.3).shift(DOWN * 1.15)

        data = get_star_data()
        stars = make_all_dots(data)
        mag_axis = make_mag_axis()

        sirius_pos = np.array([AXIS_X, mag_to_y(-1.46), 0])
        vega_pos   = np.array([AXIS_X, mag_to_y(0.03),  0])
        sirius_dot  = Dot(sirius_pos, radius=0.16, color=STAR_YELLOW)
        sirius_ring = Circle(radius=0.30, color=STAR_YELLOW,
                             stroke_width=1.5, stroke_opacity=0.6).move_to(sirius_pos)
        vega_dot    = Dot(vega_pos, radius=0.12, color=WHITE)
        lower_note  = Text("lower number = brighter star", font_size=14, color=STAR_YELLOW)
        lower_note.move_to(np.array([0.0, 0.0, 0]))
        lower_bg = SurroundingRectangle(
            lower_note, fill_color="#1a1500",
            fill_opacity=0.8, stroke_color=STAR_YELLOW, buff=0.14
        )
        callout = VGroup(lower_bg, lower_note)

        self.add(title, fps_hud, vr_warn, stars, mag_axis,
                 sirius_dot, sirius_ring, vega_dot, callout)

        # Draw the threshold cut-off line
        threshold = make_threshold_line()
        self.play(Create(threshold), run_time=1.5)
        self.wait(0.4)

        # Separate faint (to remove) and kept (to keep) dots
        faint_group  = VGroup(*[stars[i] for i in range(data["n"]) if     data["above"][i]])
        bright_group = VGroup(*[stars[i] for i in range(data["n"]) if not data["above"][i]])

        # Catalog label present during match cut — swap it out after filter
        catalog_label = Text(
            "HYG Star Catalog v4.2  —  119,000 stars",
            font_size=20, color=NEBULA_BLUE
        ).to_edge(DOWN, buff=0.55)
        self.add(catalog_label)

        count_after = Text(
            "HYG Star Catalog v4.2  —  ~6,000 stars",
            font_size=20, color=SUCCESS_GREEN
        ).to_edge(DOWN, buff=0.55)

        # Faint stars fade out; then label swaps — FadeOut/FadeIn avoids Transform-on-Text bug
        self.play(FadeOut(faint_group), run_time=1.5)
        self.play(FadeOut(catalog_label), FadeIn(count_after), run_time=0.6)

        # Bright stars pulse once to confirm they survived
        self.play(bright_group.animate.scale(1.35), run_time=0.4)
        self.play(bright_group.animate.scale(1 / 1.35), run_time=0.4)

        # Final summary line
        summary = Text(
            "Magnitude ≤ 6.5  —  the human naked-eye limit under dark skies",
            font_size=15, color=SUCCESS_GREEN
        ).to_edge(DOWN, buff=0.22)
        self.play(FadeIn(summary), run_time=0.8)
        self.wait(2.2)


# =====================================================================
# CLIP 4: The Optimized Sky
# manim --renderer=opengl -qh --write_to_movie scene2.py S2_Clip4_OptimizedSky
# =====================================================================
class S2_Clip4_OptimizedSky(ThreeDScene):
    def construct(self):
        self.camera.background_color = SPACE_BG

        # Fixed-frame UI (survives 3D camera moves)
        title = Text("6,000 out of 119,000", font_size=34, color=WHITE).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        self.add(title)

        # MATCH CUT: FPS still bad — about to fix it
        fps_hud = make_fps_hud(14, good=False)
        self.add_fixed_in_frame_mobjects(fps_hud)
        self.add(fps_hud)

        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        # Optimized 3D star sphere (represents the filtered 6k catalog)
        opt_stars = get_sphere_stars(n=80)

        # Thin wireframe sphere (green = healthy)
        R = 2.5
        sky_sphere = VGroup()
        for t in np.linspace(0, PI, 12):
            sky_sphere.add(
                Circle(radius=R, stroke_color=SUCCESS_GREEN,
                       stroke_width=1.0, stroke_opacity=0.35
                       ).rotate(t, UP).rotate(PI / 2, RIGHT)
            )
        for p in np.linspace(-PI / 2 + 0.2, PI / 2 - 0.2, 8):
            r = R * np.cos(p)
            z = R * np.sin(p)
            sky_sphere.add(
                Circle(radius=r, stroke_color=SUCCESS_GREEN,
                       stroke_width=1.0, stroke_opacity=0.35).shift(OUT * z)
            )
        sky_sphere.z_index = 0

        self.play(Create(sky_sphere), FadeIn(opt_stars), run_time=2.0)

        # FPS jumps to VR-ready — FadeOut/FadeIn avoids the Transform-on-Text bug
        fps_hud_good = make_fps_hud(90, good=True)
        self.add_fixed_in_frame_mobjects(fps_hud_good)
        self.play(FadeOut(fps_hud), FadeIn(fps_hud_good), run_time=1.0)

        # Performance breakdown label
        perf = Text(
            "6,000 stars  ·  ~6 GPU draw calls  ·  Graphics.DrawMeshInstanced()",
            font_size=16, color=SUCCESS_GREEN
        ).to_edge(DOWN, buff=0.5)
        self.add_fixed_in_frame_mobjects(perf)
        self.play(FadeIn(perf), run_time=0.7)

        # Gentle skybox rotation to prove it still looks great
        self.play(
            Rotate(sky_sphere, angle=65 * DEGREES, axis=UP + OUT * 0.15),
            Rotate(opt_stars,  angle=65 * DEGREES, axis=UP + OUT * 0.15),
            run_time=4.0,
            rate_func=smooth,
        )

        # Closing line
        closing = Text(
            "Indistinguishable from the full catalog to the human eye",
            font_size=20, color=GREEN
        ).to_corner(UR, buff=1).shift(RIGHT * 0.5)
        self.add_fixed_in_frame_mobjects(closing)
        self.play(FadeIn(closing), run_time=0.7)
        self.wait(2.0)
