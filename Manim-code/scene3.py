from manim import *
import numpy as np

# =====================================================================
# GLOBAL SETTINGS & HELPERS
# =====================================================================
# Use 600 for testing, bump to 6000 for final high-res render
OPTIMIZED_STARS = 600 
L = 2.5 # Must match Scene 1 & 2 for visual consistency

def get_random_stars():
    """Generates the unorganized, random stars before the math is applied."""
    np.random.seed(42) 
    stars = VGroup()
    for _ in range(OPTIMIZED_STARS):
        phi = np.arccos(np.random.uniform(-1, 1))
        theta = np.random.uniform(0, 2 * np.pi)
        x = L * np.sin(phi) * np.cos(theta)
        y = L * np.sin(phi) * np.sin(theta)
        z = L * np.cos(phi)
        stars.add(Square(side_length=0.003, color=np.random.choice(["#FFFFE0", "#FFFFFF"])).move_to([x, y, z]))
    return stars

def get_celestial_grid():
    """Generates an astronomical wireframe (RA/Dec)."""
    grid = VGroup()
    # Declination lines (Latitude equivalents)
    for phi in np.linspace(-PI/2 + PI/6, PI/2 - PI/6, 5):
        r = L * np.cos(phi)
        z = L * np.sin(phi)
        grid.add(Circle(radius=r, stroke_color="#34CF00", stroke_width=1, stroke_opacity=0.4).shift(OUT * z))
    
    # Right Ascension lines (Longitude equivalents)
    for theta in np.linspace(0, PI, 12):
        grid.add(Circle(radius=L, stroke_color="#34CF00", stroke_width=1, stroke_opacity=0.4).rotate(theta, UP).rotate(PI/2, RIGHT))
    
    # Highlight Equator (Dec = 0)
    equator = Circle(radius=L, stroke_color="#34CF00", stroke_width=3).shift(OUT * 0)
    
    # Highlight Prime Meridian (RA = 0)
    meridian = Circle(radius=L, stroke_color="#34CF00", stroke_width=3).rotate(PI/2, UP).rotate(PI/2, RIGHT)
    
    grid.add(equator, meridian)
    grid.z_index = 0 # Prevent 2D/3D render crashing
    return grid

# =====================================================================
# CLIP 1: The Celestial Grid
# Run: manim --renderer=opengl -pql --write_to_movie scene3.py S3_Clip1_CelestialGrid
# =====================================================================
class S3_Clip1_CelestialGrid(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#000000"
        
        # UI Setup
        title = Text("The Coordinate Pipeline", font_size=36, color=WHITE).to_corner(UL)
        ra_label = Text("Right Ascension (RA) = Longitude", font_size=20, color="#00ACC1").to_edge(DOWN).shift(UP * 0.5)
        dec_label = Text("Declination (Dec) = Latitude", font_size=20, color="#00ACC1").to_edge(DOWN).shift(DOWN * 0.2)
        self.add_fixed_in_frame_mobjects(title, ra_label, dec_label)

        # Scene Setup
        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)
        stars = get_random_stars()
        grid = get_celestial_grid()

        self.play(Write(title), FadeIn(stars), run_time=1.5)
        
        # Introduce the astronomical grid
        self.play(Create(grid), run_time=3)
        self.play(FadeIn(ra_label), FadeIn(dec_label), run_time=1)
        
        # Gentle orbit to show 3D volume
        self.move_camera(theta=75 * DEGREES, run_time=4, rate_func=smooth)
        self.wait(1)

# =====================================================================
# CLIP 2: The Data Drop
# Run: manim --renderer=opengl -pql --write_to_movie scene3.py S3_Clip2_DataDrop
# =====================================================================
# =====================================================================
# CLIP 2: The Data Drop
# Run: manim --renderer=opengl -pql --write_to_movie scene3.py S3_Clip2_DataDrop
# =====================================================================
# =====================================================================
# CLIP 2: The Data Drop
# Run: manim --renderer=opengl -pql --write_to_movie scene3.py S3_Clip2_DataDrop
# =====================================================================
# =====================================================================
# COMBINED CLIP 2 & 3: The Data Pipeline
# Run: manim --renderer=opengl -pql --write_to_movie scene3.py S3_Clip2_ThePipeline
# =====================================================================
# =====================================================================
# COMBINED CLIP 2 & 3: The Data Pipeline
# Run: manim --renderer=opengl -pql --write_to_movie scene3.py S3_Clip2_ThePipeline
# =====================================================================
# =====================================================================
# COMBINED CLIP 2 & 3: The Data Pipeline (LaTeX-Free)
# Run: manim --renderer=opengl -pql --write_to_movie scene3.py S3_Clip2_ThePipeline
# =====================================================================
class S3_Clip2_ThePipeline(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#000000"
        
        # UI Setup
        title = Text("The Coordinate Pipeline", font_size=36, color=WHITE).to_corner(UL)
        ra_label = Text("Right Ascension (RA) = Longitude", font_size=20, color="#00ACC1").to_edge(DOWN).shift(UP * 0.5)
        dec_label = Text("Declination (Dec) = Latitude", font_size=20, color="#00ACC1").to_edge(DOWN).shift(DOWN * 0.2)
        self.add_fixed_in_frame_mobjects(title, ra_label, dec_label)
        self.add(title, ra_label, dec_label)

        # 3D Geometry Match Cut
        self.set_camera_orientation(phi=70 * DEGREES, theta=75 * DEGREES)
        stars = get_random_stars()
        grid = get_celestial_grid()
        self.add(stars, grid)

        # 1. JSON DATA SETUP
        json_code = """{
    "star": "Sirius",
    "vmag": -1.46,
    "ra": 101.28,
    "dec": -16.71
}"""
        with open("sirius_data.json", "w") as f:
            f.write(json_code)

        data_text = Code(
            "sirius_data.json",
            tab_width=4,
            background="window",
            language="json",
            paragraph_config={"font": "Monospace", "font_size": 24} 
        ).scale(0.8).to_edge(LEFT).shift(DOWN * 0.5)
        
        self.add_fixed_in_frame_mobjects(data_text)
        self.remove(data_text)

        # 2. MATH FORMULA SETUP (NO LATEX)
        math_header = Text("Spherical to Cartesian", font_size=26, color=BLUE_B)
        
        formula = VGroup(
            Text("x = R • cos(Dec) • cos(RA)", font_size=24, font="Monospace"),
            Text("y = R • cos(Dec) • sin(RA)", font_size=24, font="Monospace"),
            Text("z = R • sin(Dec)", font_size=24, font="Monospace")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        
        # Center the formula right under the header
        formula.next_to(math_header, DOWN, buff=0.8)

        formula_box = SurroundingRectangle(formula, color=WHITE, buff=0.4, stroke_width=1)
        formula_group = VGroup(math_header, formula, formula_box)
        
        # THE FIX: Scale the entire group down by 25% so it clears the sphere, 
        # then lock it to the right edge.
        formula_group.scale(0.75).to_edge(RIGHT, buff=0.3).shift(UP * 0.5)

        self.add_fixed_in_frame_mobjects(formula_group)
        self.remove(formula_group)

        # ANIMATION SEQUENCE
        self.play(FadeIn(data_text, scale=0.5), run_time=1.5)
        self.wait(1)

        self.play(
            data_text.animate.scale(0.7).to_edge(LEFT).shift(UP * 0.5),
            Write(math_header),
            run_time=1.5
        )
        
        self.play(
            Create(formula_box),
            Write(formula),
            run_time=2
        )
        
        # Highlight the formula box instead of specific LaTeX strings
        self.play(formula_box.animate.set_color(YELLOW), run_time=1)
        self.wait(2)



# =====================================================================
# CLIP 3: The Great Migration
# Run: manim --renderer=opengl -pql --write_to_movie scene3.py S3_Clip3_GreatMigration
# =====================================================================
class S3_Clip3_GreatMigration(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.set_camera_orientation(phi=70 * DEGREES, theta=75 * DEGREES)
        
        # UI Setup
        title = Text("The Coordinate Pipeline", font_size=36, color=WHITE).to_corner(UL)
        
        # Lock title to 2D frame (using the safe method)
        self.add_fixed_in_frame_mobjects(title)
        self.remove(title)
        self.add(title)

        stars = get_random_stars()
        grid = get_celestial_grid()
        self.add(stars, grid)

        # Prepare the target positions (the conversion logic)
        np.random.seed(42) # KEEP SEED FOR MATCH CUT
        animations = []
        
        for star in stars:
            # Simulate real RA/Dec data (normally this would be from your dataset)
            ra = np.random.uniform(0, 2 * PI)
            dec = np.random.uniform(-PI/2, PI/2)
            
            # Apply the formulas from the previous clip
            target_x = L * np.cos(dec) * np.cos(ra)
            target_y = L * np.cos(dec) * np.sin(ra)
            target_z = L * np.sin(dec)
            
            animations.append(star.animate.move_to([target_x, target_y, target_z]))

        # THE PAYOFF
        self.wait(1)
        
        # Animate the fade and the swarm simultaneously over 4 seconds
        self.play(
            FadeOut(grid), 
            AnimationGroup(*animations, lag_ratio=0.001), 
            run_time=4
        )
        
        # Rotate to show the new accurate constellations
        self.move_camera(theta=120 * DEGREES, run_time=5, rate_func=sigmoid)
        self.wait(2)

