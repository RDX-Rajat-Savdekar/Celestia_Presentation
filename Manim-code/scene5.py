from manim import *
import numpy as np

# =====================================================================
# SCENE 5 - CLIP 1: The Adjacency List
# Run: manim --renderer=opengl -pql --write_to_movie scene5.py S5_Clip1_GraphData
# =====================================================================
from manim import *

class S5_Clip1_GraphData(Scene):
    def construct(self):
        self.camera.background_color = "#000000"

        # UI Setup
        title = Text("Constellations as Graphs", font_size=36, color=WHITE).to_corner(UL)
        subtitle = Text("Using Adjacency Lists to map connections", font_size=20, color=GRAY).next_to(title, DOWN, aligned_edge=LEFT)
        self.add(title, subtitle)

        # 1. THE DATA STRUCTURE (JSON Adjacency List)
        json_code = """{
    "Rigel": ["Saiph", "Mintaka"],
    "Betelgeuse": ["Bellatrix", "Alnitak"],
    "Bellatrix": ["Mintaka", "Betelgeuse"],
    "Saiph": ["Rigel", "Alnitak"]
}"""
        with open("adjacency_list.json", "w") as f:
            f.write(json_code)

        # Using standard styling to avoid Pygments/LaTeX conflicts
        code_block = Code(
            "adjacency_list.json",
            tab_width=4,
            background="window",
            language="json",
            paragraph_config={"font": "Monospace", "font_size": 22}
        ).to_edge(LEFT, buff=1).shift(DOWN * 0.5).scale(0.5)

        # 2. THE VISUAL NODES (Orion's core stars)
        # Manually plotted for a clean 2D diagram
        nodes = {
            "Betelgeuse": Dot(color="#ff3800", radius=0.15).move_to([1.5, 2, 0]),
            "Bellatrix": Dot(color="#cad7ff", radius=0.12).move_to([4.5, 2, 0]),
            "Rigel": Dot(color="#5d7eff", radius=0.15).move_to([4.5, -2, 0]),
            "Saiph": Dot(color="#cad7ff", radius=0.12).move_to([1.5, -2, 0]),
            "Alnitak": Dot(color="#ffffff", radius=0.1).move_to([2.5, 0, 0]),
            "Mintaka": Dot(color="#ffffff", radius=0.1).move_to([3.5, 0.5, 0])
        }

        # Create native Text labels for the nodes
        labels = VGroup(*[
            Text(name, font_size=16).next_to(dot, UP, buff=0.2)
            for name, dot in nodes.items()
        ])

        # 3. ANIMATION SEQUENCE
        self.play(FadeIn(code_block, shift=RIGHT), run_time=1.5)
        self.wait(0.5)
        
        # Pop in the stars and labels
        self.play(
            AnimationGroup(*[FadeIn(dot, scale=0.5) for dot in nodes.values()], lag_ratio=0.1),
            FadeIn(labels)
        )
        self.wait(1)

        # 4. DRAW THE EDGES (The lines connecting the graph)
        edges = [
            ("Rigel", "Saiph"), ("Rigel", "Mintaka"),
            ("Betelgeuse", "Bellatrix"), ("Betelgeuse", "Alnitak"),
            ("Bellatrix", "Mintaka"), ("Saiph", "Alnitak"),
            ("Alnitak", "Mintaka") # The belt
        ]

        lines = VGroup()
        for start, end in edges:
            line = Line(
                nodes[start].get_center(), 
                nodes[end].get_center(), 
                color=GRAY, 
                stroke_opacity=0.6,
                stroke_width=2
            )
            lines.add(line)

        # Draw the graph connections dynamically
        self.play(Create(lines, lag_ratio=0.2), run_time=3)
        self.wait(2)

# =====================================================================
# SCENE 5 - CLIP 2: Constructing the Graph in 3D
# Run: manim --renderer=opengl -pql --write_to_movie scene5.py S5_Clip2_3DGraph
# =====================================================================
# =====================================================================
# SCENE 5 - CLIP 2: Constructing the Graph in 3D
# Run: manim --renderer=opengl -pql --write_to_movie scene5.py S5_Clip2_3DGraph
# =====================================================================
# =====================================================================
# SCENE 5 - CLIP 2: Constructing the Graph in 3D (Type-Safe Version)
# Run: manim --renderer=opengl -pql --write_to_movie scene5.py S5_Clip2_3DGraph
# =====================================================================
# =====================================================================
# SCENE 5 - CLIP 2: Constructing the Graph in 3D (Stabilized)
# Run: manim --renderer=opengl -pql --write_to_movie scene5.py S5_Clip2_3DGraph
# =====================================================================
class S5_Clip2_3DGraph(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.set_camera_orientation(phi=80 * DEGREES, theta=45 * DEGREES)
        
        # UI Setup
        title = Text("Constructing Constellations", font_size=36, color=WHITE).to_corner(UL)
        subtitle = Text("Mapping edges in 3D space", font_size=20, color=GRAY).next_to(title, DOWN, aligned_edge=LEFT)
        
        self.add_fixed_in_frame_mobjects(title, subtitle)
        self.remove(title, subtitle)
        self.add(title, subtitle)

        # 1. BACKGROUND STARS (Using standard Dot to avoid z_index errors)
        np.random.seed(42)
        bg_stars = VGroup()
        for _ in range(150):
            pt = [np.random.uniform(-6, 6), np.random.uniform(-6, 6), np.random.uniform(-4, 0)]
            bg_stars.add(Dot(point=pt, color=WHITE, radius=0.02, fill_opacity=0.6))
        self.add(bg_stars)

        # 2. ORION STARS IN 3D SPACE
        # Swapped Dot3D -> Dot (Still works in 3D, but more stable)
        nodes = {
            "Betelgeuse": Dot(point=[1.5, 2.0, 2.0], color="#ff3800", radius=0.08),
            "Bellatrix": Dot(point=[3.5, 2.0, 1.8], color="#cad7ff", radius=0.06),
            "Rigel": Dot(point=[4.0, -2.0, 1.5], color="#5d7eff", radius=0.08),
            "Saiph": Dot(point=[1.0, -2.0, 1.7], color="#cad7ff", radius=0.06),
            "Alnitak": Dot(point=[2.0, 0.0, 1.9], color="#ffffff", radius=0.05),
            "Mintaka": Dot(point=[3.0, 0.5, 1.8], color="#ffffff", radius=0.05)
        }
        
        node_group = VGroup(*nodes.values())
        self.play(AnimationGroup(*[FadeIn(dot) for dot in node_group], lag_ratio=0.1))
        self.wait(1)

        # 3. THE EDGES
        edges = [
            ("Rigel", "Saiph"), ("Rigel", "Mintaka"),
            ("Betelgeuse", "Bellatrix"), ("Betelgeuse", "Alnitak"),
            ("Bellatrix", "Mintaka"), ("Saiph", "Alnitak"),
            ("Alnitak", "Mintaka")
        ]

        lines = VGroup()
        for start, end in edges:
            start_pt = nodes[start].get_center()
            end_pt = nodes[end].get_center()
            line = Line(start_pt, end_pt, color="#00ACC1", stroke_width=4, stroke_opacity=0.8)
            lines.add(line)

        # 4. ANIMATE DRAWING + CAMERA PAN
        self.move_camera(
            theta=85 * DEGREES,
            phi=70 * DEGREES,
            added_anims=[Create(lines, lag_ratio=0.2)],
            run_time=4,
            rate_func=smooth
        )
        self.wait(2)

# =====================================================================
# SCENE 5 - CLIP 3: Spatial Partitioning (Octree Visualization)
# Run: manim --renderer=opengl -pql --write_to_movie scene5.py S5_Clip3_Octree
# =====================================================================
# =====================================================================
# SCENE 5 - CLIP 3: Spatial Partitioning (Octree Visualization)
# Run: manim --renderer=opengl -pql --write_to_movie scene5.py S5_Clip3_Octree
# =====================================================================
# =====================================================================
# SCENE 5 - CLIP 3: Spatial Partitioning (Octree Visualization) - FIXED MOTION
# Run: manim --renderer=opengl -pql --write_to_movie scene5.py S5_Clip3_Octree
# =====================================================================
class S5_Clip3_Octree(ThreeDScene):
    def construct(self):
        self.camera.background_color = "#000000"
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        # UI Setup
        title = Text("Optimizing the Search", font_size=36)
        status = Text("Complexity: O(N log N)", font_size=24, color="#00ACC1")
        ui_group = VGroup(title, status).arrange(DOWN, aligned_edge=LEFT).to_corner(UL)
        
        self.add_fixed_in_frame_mobjects(ui_group)
        self.remove(ui_group)
        self.add(ui_group)

        # 1. GENERATE STARFIELD
        np.random.seed(10)
        stars = VGroup(*[
            Dot(point=[np.random.uniform(-3, 3), np.random.uniform(-3, 3), np.random.uniform(-3, 3)], 
                radius=0.03, color=WHITE,opacity=0.3)
            for _ in range(400)
        ])
        self.add(stars)

        # 2. CREATE THE OCTREE GRID
        box_size = 3.1
        cube_params = {"color": BLUE_D, "stroke_width": 1, "fill_opacity": 0.05}
        octants = VGroup(*[
            Cube(side_length=box_size, **cube_params).move_to([x, y, z])
            for x in [-box_size/2, box_size/2]
            for y in [-box_size/2, box_size/2]
            for z in [-box_size/2, box_size/2]
        ])

        # 3. SEARCH RADIUS (The Yellow Sphere)
        # We'll use a wireframe sphere to keep the stars visible inside
        center_star = stars[150].copy().set_color(YELLOW)
        search_radius = Sphere(radius=1.2, color=YELLOW, stroke_width=1, fill_opacity=0.1)
        search_radius.move_to(center_star)
        
        # 4. ANIMATION SEQUENCE
        self.wait(1)
        
        # MOTION FIX: We move the camera over a long duration 
        # and nest the other animations inside it.
        self.move_camera(
            theta=45 * DEGREES,
            phi=65 * DEGREES,
            added_anims=[
                Create(octants, lag_ratio=0.1),
                FadeIn(search_radius),
                center_star.animate.scale(3)
            ],
            run_time=4
        )

        # Transition: Highlight the relevant "Bucket"
        # Front-top-right octant is index 7
        self.move_camera(
            theta=90 * DEGREES,
            added_anims=[
                octants[7].animate.set_fill(BLUE_B, opacity=0.4).set_stroke(BLUE_B, 4),
                stars.animate.set_opacity(0.4),
                search_radius.animate.set_opacity(0.05)
            ],
            run_time=2
        )
        
        # Identify stars inside the Partition
        relevant_stars = [s for s in stars if s.get_center()[0] > 0 and s.get_center()[1] > 0 and s.get_center()[2] > 0]
        
        self.play(
            *[s.animate.set_color(BLUE_B).set_opacity(1) for s in relevant_stars], 
            run_time=1
        )
        
        # Final slow rotation to show the 3D volume
        self.move_camera(theta=140 * DEGREES, run_time=5, rate_func=linear)
        self.wait(2)