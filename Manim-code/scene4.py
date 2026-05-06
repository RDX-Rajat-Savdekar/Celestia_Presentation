from manim import *
import numpy as np

# =====================================================================
# CLIP 1: The Temperature Scale (No-LaTeX Version)
# Run: manim --renderer=opengl -pql --write_to_movie scene4.py S4_Clip1_Temperature
# =====================================================================
class S4_Clip1_Temperature(Scene):
    def construct(self):
        self.camera.background_color = "#000000"
        
        title = Text("Stellar Color & Temperature", font_size=36).to_corner(UL)
        self.add(title)

        # 1. Create a Gradient Color Bar (Planckian Locus)
        # From Class M (Red) to Class O (Blue)
        colors = ["#ff3800", "#ffcc6f", "#ffffff", "#cad7ff", "#5d7eff"]
        bar = Rectangle(width=8, height=0.5, grid_xstep=1.0).set_fill(
            color=colors, opacity=1
        ).set_stroke(WHITE, width=1)
        bar.shift(DOWN * 1)

        # 2. Labels using simple Text (No LaTeX)
        temp_labels = VGroup(
            Text("3,000K", font_size=18).next_to(bar.get_left(), UP),
            Text("6,000K", font_size=18).next_to(bar.get_center(), UP),
            Text("30,000K", font_size=18).next_to(bar.get_right(), UP)
        )
        
        class_labels = VGroup(
            Text("Class M", font_size=20, color="#ff3800").next_to(bar.get_left(), DOWN),
            Text("Class G (Our Sun)", font_size=20, color="#ffffff").next_to(bar.get_center(), DOWN),
            Text("Class O", font_size=20, color="#5d7eff").next_to(bar.get_right(), DOWN)
        )

        # 3. The Interactive Star
        target_star = Dot(radius=0.8, color="#ffffff").shift(UP * 1.5)
        glow = Dot(radius=1.2, color="#ffffff", fill_opacity=0.3).move_to(target_star)
        
        pointer = Triangle(fill_color=WHITE).scale(0.2).rotate(PI)
        pointer.next_to(bar.get_left(), DOWN, buff=0.1)

        # ANIMATION
        self.play(Create(bar), Write(temp_labels), FadeIn(target_star, glow))
        self.wait(1)
        self.play(Write(class_labels))
        
        # SLIDE: Move from Red to Blue
        # We animate the color of the star and the position of the pointer
        self.play(
            pointer.animate.move_to(bar.get_right() + DOWN*0.3),
            target_star.animate.set_color("#5d7eff"),
            glow.animate.set_color("#5d7eff"),
            run_time=4,
            rate_func=there_and_back
        )
        self.wait(2)

# =====================================================================
# CLIP 2: The B-V Color Index
# Run: manim --renderer=opengl -pql --write_to_movie scene4.py S4_Clip2_BVIndex
# =====================================================================
# =====================================================================
# CLIP 2: The B-V Color Index (Strictly LaTeX-Free)
# Run: manim --renderer=opengl -pql --write_to_movie scene4.py S4_Clip2_BVIndex
# =====================================================================
class S4_Clip2_BVIndex(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # Using Text for the formula to avoid LaTeX dependency
        formula_parts = VGroup(
            Text("Color Index  =", font_size=32),
            Text("B", font_size=40, color=BLUE),
            Text("-", font_size=40),
            Text("V", font_size=40, color=YELLOW)
        ).arrange(RIGHT, buff=0.3)

        explanation = Text(
            "(Blue   Magnitude   minus   Visual   Magnitude)", 
            font_size=20, color=GRAY
        ).next_to(formula_parts, DOWN, buff=0.5)

        self.play(Write(formula_parts))
        self.play(FadeIn(explanation))
        self.wait(2)
        
        # THE FIX: Turn off auto-numbers to prevent LaTeX crash
        scale_line = NumberLine(x_range=[-0.5, 2.5, 0.5], length=6, include_numbers=False)
        scale_line.next_to(explanation, DOWN, buff=1)
        
        # THE FIX: Manually generate standard Text numbers
        labels = VGroup()
        for val in [-0.5, 0.0, 0.5, 1.0, 1.5, 2.0]:
            label = Text(f"{val:.1f}", font_size=16).next_to(scale_line.number_to_point(val), DOWN, buff=0.2)
            labels.add(label)
        
        blue_label = Text("Blue/Hot", font_size=18, color=BLUE).next_to(scale_line.number_to_point(-0.5), DOWN, buff=0.7)
        red_label = Text("Red/Cool", font_size=18, color=RED).next_to(scale_line.number_to_point(2.0), DOWN, buff=0.7)

        self.play(Create(scale_line), FadeIn(labels))
        self.play(FadeIn(blue_label, red_label))
        self.wait(2)

# =====================================================================
# CLIP 3: The Color Wash
# Run: manim --renderer=opengl -pql --write_to_movie scene4.py S4_Clip3_ColorWash
# =====================================================================
# =====================================================================
# CLIP 3: The Color Wash
# Run: manim --renderer=opengl -pql --write_to_movie scene4.py S4_Clip3_ColorWash
# =====================================================================
class S4_Clip3_ColorWash(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#000000"
        
        # Match cut camera angle from the end of Scene 3
        self.set_camera_orientation(phi=70 * DEGREES, theta=120 * DEGREES) 
        
        title = Text("Applying B-V Color Index", font_size=36, color=WHITE).to_corner(UL)
        
        # Safely lock the title to the 2D frame
        self.add_fixed_in_frame_mobjects(title)
        self.remove(title)
        self.add(title)

        # Generate the structured starfield (Matching Scene 3 Finale)
        np.random.seed(42)
        stars = VGroup()
        L = 2.5
        for _ in range(600): # Keep at 600 for rapid testing
            ra = np.random.uniform(0, 2 * PI)
            dec = np.random.uniform(-PI/2, PI/2)
            x = L * np.cos(dec) * np.cos(ra)
            y = L * np.cos(dec) * np.sin(ra)
            z = L * np.sin(dec)
            stars.add(Square(side_length=0.015, color=WHITE).move_to([x, y, z]))
        
        self.add(stars)
        self.wait(1)

        # THE COLOR WASH LOGIC
        # Real-world B-V colors: Blue, Light Blue, White, Yellow/Orange, Red
        star_colors = ["#5d7eff", "#cad7ff", "#ffffff", "#ffcc6f", "#ff3800"]
        
        color_animations = []
        for star in stars:
            # Weighted distribution: More red/orange stars, fewer blue supergiants
            chosen_color = np.random.choice(star_colors, p=[0.05, 0.1, 0.2, 0.3, 0.35])
            color_animations.append(star.animate.set_color(chosen_color))

        # Sweep the camera while the colors ripple across the stars
        self.move_camera(
            theta=160 * DEGREES,
            added_anims=[AnimationGroup(*color_animations, lag_ratio=0.005)],
            run_time=4
        )
        self.wait(2)

# =====================================================================
# CLIP 4: Atmospheric Scintillation (Twinkle)
# Run: manim --renderer=opengl -pql --write_to_movie scene4.py S4_Clip4_Twinkle
# =====================================================================
# =====================================================================
# CLIP 4: Atmospheric Scintillation (Twinkle) - Fly Inside
# Run: manim --renderer=opengl -pql --write_to_movie scene4.py S4_Clip4_Twinkle
# =====================================================================
# =====================================================================
# CLIP 4: Atmospheric Scintillation (Twinkle) - Fly Inside
# Run: manim --renderer=opengl -pql --write_to_movie scene4.py S4_Clip4_Twinkle
# =====================================================================
# =====================================================================
# CLIP 4: Atmospheric Scintillation (Twinkle) - Scale Up Immersion
# Run: manim --renderer=opengl -pql --write_to_movie scene4.py S4_Clip4_Twinkle
# =====================================================================
# =====================================================================
# CLIP 4: Atmospheric Scintillation (Twinkle) - Scale Up Immersion
# Run: manim --renderer=opengl -pql --write_to_movie scene4.py S4_Clip4_Twinkle
# =====================================================================
class S4_Clip4_Twinkle(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#000000"
        
        # Match cut camera angle from the EXACT end of Clip 3
        self.set_camera_orientation(phi=70 * DEGREES, theta=160 * DEGREES) 
        
        # UI Setup
        title = Text("Atmospheric Scintillation", font_size=36, color=WHITE).to_corner(UL)
        subtitle = Text("VR simulation of atmospheric turbulence", font_size=20, color=GRAY).next_to(title, DOWN, aligned_edge=LEFT)
        
        self.add_fixed_in_frame_mobjects(title, subtitle)
        self.remove(title, subtitle)
        self.add(title, subtitle)

        # 1. REBUILD THE EXACT STARFIELD FROM CLIP 3
        np.random.seed(42)
        stars = VGroup()
        L = 2.5
        star_colors = ["#5d7eff", "#cad7ff", "#ffffff", "#ffcc6f", "#ff3800"]
        
        for _ in range(600):
            ra = np.random.uniform(0, 2 * PI)
            dec = np.random.uniform(-PI/2, PI/2)
            x = L * np.cos(dec) * np.cos(ra)
            y = L * np.cos(dec) * np.sin(ra)
            z = L * np.sin(dec)
            
            chosen_color = np.random.choice(star_colors, p=[0.05, 0.1, 0.2, 0.3, 0.35])
            
            star = Square(side_length=0.015, color=chosen_color).move_to([x, y, z])
            star.phase = np.random.uniform(0, 2 * PI)
            star.base_opacity = np.random.uniform(0.5, 0.9)
            stars.add(star)
            
        self.add(stars)

        # 2. THE TWINKLE UPDATER FUNCTION
        stars.time = 0
        def twinkle_effect(mob, dt):
            mob.time += dt
            for s in mob:
                new_opacity = s.base_opacity + 0.4 * np.sin(4 * mob.time + s.phase)
                clamped_opacity = max(0.1, min(1.0, new_opacity))
                s.set_fill(opacity=clamped_opacity)
                s.set_stroke(opacity=clamped_opacity)

        # 3. ANIMATION SEQUENCE
        self.wait(1)
        
        stars.add_updater(twinkle_effect)
        
        # Swallows the camera while panning
        self.move_camera(
            theta=180 * DEGREES,
            added_anims=[stars.animate.scale(10)],
            run_time=4,
            rate_func=smooth
        )
        
        # Continue the twinkle and pan while fully immersed
        self.move_camera(
            theta=200 * DEGREES,
            run_time=3,
            rate_func=linear
        )
        
        stars.remove_updater(twinkle_effect)
        self.wait(1)