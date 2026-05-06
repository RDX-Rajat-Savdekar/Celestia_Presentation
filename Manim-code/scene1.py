from manim import *
import numpy as np

# =====================================================================
# GLOBAL SETTINGS & HELPERS
# =====================================================================
# Change to 1200 for the final high-res render. Keep at 120 for testing.
TOTAL_STARS = 120 
L = 2.5 # Size of the cube panels/sphere radius

def get_spherical_stars():
    """Generates the 3D spherical star cloud."""
    np.random.seed(42) # CRITICAL: Ensures random stars match perfectly across clips
    stars = VGroup()
    for _ in range(TOTAL_STARS):
        phi = np.arccos(np.random.uniform(-1, 1))
        theta = np.random.uniform(0, 2 * np.pi)
        x = L * np.sin(phi) * np.cos(theta)
        y = L * np.sin(phi) * np.sin(theta)
        z = L * np.cos(phi)
        stars.add(Square(side_length=0.01, color=np.random.choice(["#FFFFE0", "#FFFFFF"])).move_to([x, y, z]))
    return stars

def get_flat_panels():
    """Generates the 2D cross-net and maps stars onto the panels."""
    np.random.seed(42)
    panels = [
        Square(side_length=L, stroke_color="#4FC3F7", fill_opacity=0.1).move_to([0, L, 0]),   # 0: Top
        Square(side_length=L, stroke_color="#4FC3F7", fill_opacity=0.1).move_to([0, 0, 0]),   # 1: Center
        Square(side_length=L, stroke_color="#4FC3F7", fill_opacity=0.1).move_to([0, -L, 0]),  # 2: Bottom
        Square(side_length=L, stroke_color="#4FC3F7", fill_opacity=0.1).move_to([-L, 0, 0]),  # 3: Left
        Square(side_length=L, stroke_color="#4FC3F7", fill_opacity=0.1).move_to([L, 0, 0]),   # 4: Right
        Square(side_length=L, stroke_color="#4FC3F7", fill_opacity=0.1).move_to([2*L, 0, 0]), # 5: Far Right
    ]
    
    face_groups = VGroup()
    mapped_stars = VGroup()
    
    for panel in panels:
        face_group = VGroup(panel)
        panel_stars = VGroup()
        for _ in range(TOTAL_STARS // 6):
            target_dot = Square(side_length=0.01, color=np.random.choice(["#FFFFE0", "#FFFFFF"]))
            bound = (L / 2) - 0.05
            offset_x = np.random.uniform(-bound, bound)
            offset_y = np.random.uniform(-bound, bound)
            target_dot.move_to(panel.get_center() + np.array([offset_x, offset_y, 0]))
            panel_stars.add(target_dot)
        
        mapped_stars.add(panel_stars)
        face_group.add(panel_stars)
        face_groups.add(face_group)
        
    return panels, face_groups, mapped_stars

def get_folded_cube():
    """Returns the final folded 3D cube for match cutting into Clip 4."""
    panels, face_groups, mapped_stars = get_flat_panels()
    center_panel_ref = panels[1]
    
    # Pre-apply the folds so it spawns already closed
    face_groups[0].rotate(90 * DEGREES, axis=RIGHT, about_point=center_panel_ref.get_top())
    face_groups[2].rotate(-90 * DEGREES, axis=RIGHT, about_point=center_panel_ref.get_bottom())
    face_groups[3].rotate(90 * DEGREES, axis=UP, about_point=center_panel_ref.get_left())
    
    right_side_group = VGroup(face_groups[4], face_groups[5])
    right_side_group.rotate(-90 * DEGREES, axis=UP, about_point=center_panel_ref.get_right())
    
    lid_hinge = center_panel_ref.get_right() + OUT * L
    face_groups[5].rotate(-90 * DEGREES, axis=UP, about_point=lid_hinge)
    
    return face_groups

# =====================================================================
# CLIP 1: Immersion
# Run: manim --renderer=opengl -pql vr_scene.py S1_Clip1_Immersion
# =====================================================================
class S1_Clip1_Immersion(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#000000"
        
        title = Text("The Skybox Problem", font_size=36, color=WHITE).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title), run_time=1)

        self.star_field = get_spherical_stars()
        self.play(FadeIn(self.star_field), run_time=2)
        
        # Pan VR view
        self.set_camera_orientation(phi=90 * DEGREES, theta=0 * DEGREES)
        self.move_camera(theta=45 * DEGREES, phi=105 * DEGREES, run_time=4)

# =====================================================================
# CLIP 2: Abstraction
# Run: manim --renderer=opengl -pql vr_scene.py S1_Clip2_Abstraction
# =====================================================================
class S1_Clip2_Abstraction(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#000000"
        
        title = Text("The Skybox Problem", font_size=36, color=WHITE).to_corner(UL)
        self.add_fixed_in_frame_mobjects(title)
        self.add(title)

        # MATCH CUT: Start exactly where Clip 1 ended
        self.star_field = get_spherical_stars()
        self.add(self.star_field)
        self.set_camera_orientation(phi=105 * DEGREES, theta=45 * DEGREES)
        
        # Pull back
        self.move_camera(phi=75 * DEGREES, theta=30 * DEGREES, run_time=2)

        self.panels, self.face_groups, self.mapped_stars = get_flat_panels()
        
        net_label = Text("6-sided Cubemap Net", font_size=24).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(net_label)

        self.play(FadeIn(VGroup(*self.panels)), FadeIn(net_label), run_time=1)
        self.play(ReplacementTransform(self.star_field, self.mapped_stars), run_time=3)
        self.wait(1)

# =====================================================================
# CLIP 3: The Fold
# Run: manim --renderer=opengl -pql vr_scene.py S1_Clip3_Fold
# =====================================================================
class S1_Clip3_Fold(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#000000"
        
        title = Text("The Skybox Problem", font_size=36, color=WHITE).to_corner(UL)
        label2 = Text("Folded Cube (Pole Distortion)", font_size=24, color="#EF5350").to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(title, label2)
        self.add(title, label2)

        # MATCH CUT: Start with the flat net
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.panels, self.face_groups, self.mapped_stars = get_flat_panels()
        self.add(self.face_groups)

        center_panel_ref = self.panels[1]
        
        # Folding sequence
        self.play(
            Rotate(self.face_groups[0], angle=90 * DEGREES, axis=RIGHT, about_point=center_panel_ref.get_top()),
            Rotate(self.face_groups[2], angle=-90 * DEGREES, axis=RIGHT, about_point=center_panel_ref.get_bottom()),
            Rotate(self.face_groups[3], angle=90 * DEGREES, axis=UP, about_point=center_panel_ref.get_left()),
            run_time=2
        )

        right_side_group = VGroup(self.face_groups[4], self.face_groups[5])
        self.play(Rotate(right_side_group, angle=-90 * DEGREES, axis=UP, about_point=center_panel_ref.get_right()), run_time=1.5)

        lid_hinge = center_panel_ref.get_right() + OUT * L
        self.play(Rotate(self.face_groups[5], angle=-90 * DEGREES, axis=UP, about_point=lid_hinge), run_time=1.5)
        
        # Orbit closed box
        self.move_camera(phi=60 * DEGREES, theta=60 * DEGREES, run_time=2)
        self.wait(1)

# =====================================================================
# CLIP 4: Sphere Solution
# Run: manim --renderer=opengl -pql vr_scene.py S1_Clip4_SphereSolution
# =====================================================================
# =====================================================================
# CLIP 4: Sphere Solution
# Run: manim --renderer=opengl -pql --write_to_movie vr_scene.py S1_Clip4_SphereSolution
# =====================================================================
# =====================================================================
# CLIP 4: Sphere Solution
# Run: manim --renderer=opengl -pql --write_to_movie vr_scene.py S1_Clip4_SphereSolution
# =====================================================================
# =====================================================================
# CLIP 4: Sphere Solution
# Run: manim --renderer=opengl -pql --write_to_movie vr_scene.py S1_Clip4_SphereSolution
# =====================================================================
class S1_Clip4_SphereSolution(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#000000"
        
        # Setup common UI (Fixed in Frame)
        title = Text("The Skybox Problem", font_size=36, color=WHITE).to_corner(UL)
        label2 = Text("Folded Cube (Pole Distortion)", font_size=24, color="#EF5350").to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(title, label2)
        self.add(title, label2)

        # MATCH CUT: Start with the folded cube
        self.set_camera_orientation(phi=60 * DEGREES, theta=60 * DEGREES)
        self.folded_cube = get_folded_cube()
        self.add(self.folded_cube)

        label3 = Text("Inverted Sphere (No Distortion)", font_size=24, color="#66BB6A").to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(label3)

        # 1. Generate hollow wireframe and stars
        sky_sphere = VGroup()
        for theta in np.linspace(0, PI, 16):
            sky_sphere.add(Circle(radius=L, stroke_color="#66BB6A", stroke_width=1.5, stroke_opacity=0.5).rotate(theta, UP).rotate(PI/2, RIGHT))
        for phi in np.linspace(-PI/2 + 0.2, PI/2 - 0.2, 12):
            r = L * np.cos(phi)
            z = L * np.sin(phi)
            sky_sphere.add(Circle(radius=r, stroke_color="#66BB6A", stroke_width=1.5, stroke_opacity=0.5).shift(OUT * z))
        
        # Z-INDEX PROOF FIX: Manually inject a z_index for Cairo/OpenGL safety
        sky_sphere.z_index = 0
        spherical_stars = get_spherical_stars()

        # CROSSFADE: Cube -> Sphere
        self.play(
            FadeOut(label2), FadeIn(label3),
            FadeOut(self.folded_cube), 
            Create(sky_sphere), FadeIn(spherical_stars),
            run_time=2.5
        )
        self.remove(self.folded_cube)
        self.wait(1)

        # Add "Inside View" context text in UR corner, keep it there.
        cross_section_label = Text("View from Inside", font_size=24).to_corner(UR)
        self.add_fixed_in_frame_mobjects(cross_section_label)

        # 2. THE FLY-IN: Enter the volume
        self.play(
            sky_sphere.animate.scale(8),
            spherical_stars.animate.scale(8),
            FadeOut(label3), FadeIn(cross_section_label),
            run_time=3
        )

        # 3. VR PAN: Distinct sweeps at eye level
        

        # 4. FIXED GAME MECHANIC: Dynamic Sky Rotation (Sine Wave Motion)

        # THE FIX (Label): Create a new, prominent, correct label at the bottom centered.
        label4 = Text("Dynamic Sky Rotation", font_size=24, color=YELLOW).to_edge(DOWN)
        self.add_fixed_in_frame_mobjects(label4)

        # Cleanly Transform context text into prominent new label
        # self.play(Transform(cross_section_label, label4), run_time=1)
        
        # THE FIX (Look Up): Stop move_camera, rotate the geometry instead.
        # Use a "diagonal" axis: Rotate on RIGHT + OUT. 
        # rate_func='there_and_back' creates the smooth oscillating sine motion, 
        # making the sky seamlessly loop.
        self.play(
            Rotate(sky_sphere, angle=-90 * DEGREES, axis=RIGHT + OUT),
            Rotate(spherical_stars, angle=-90 * DEGREES, axis=RIGHT + OUT),
            run_time=5,
            rate_func=there_and_back
        )
        self.wait(2)