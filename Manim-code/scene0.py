from manim import *
import numpy as np
import random

class S6_CelestiaLogo(Scene):
    def construct(self):
        # Deep night sky background
        self.camera.background_color = "#010409"

        # 1. THE ISLAND & OCEAN HORIZON
        ocean = Rectangle(width=15, height=2, color="#020813", fill_opacity=1, stroke_width=0).to_edge(DOWN, buff=0)
        island = Ellipse(width=10, height=2, color="#040b17", fill_opacity=1, stroke_width=0).move_to([0, -3.5, 0])
        horizon = VGroup(ocean, island)

        # 2. THE CONSTELLATION "FONT"
        font_map = {
            'C': {'pts': [[1,2], [0,2], [0,0], [1,0]], 'edges': [(0,1), (1,2), (2,3)]},
            'E': {'pts': [[1,2], [0,2], [0,1], [0.8,1], [0,0], [1,0]], 'edges': [(0,1), (1,2), (2,3), (2,4), (4,5)]},
            'L': {'pts': [[0,2], [0,0], [1,0]], 'edges': [(0,1), (1,2)]},
            'S': {'pts': [[1,2], [0,2], [0,1], [1,1], [1,0], [0,0]], 'edges': [(0,1), (1,2), (2,3), (3,4), (4,5)]},
            'T': {'pts': [[0,2], [1,2], [0.5,2], [0.5,0]], 'edges': [(0,1), (2,3)]},
            'I': {'pts': [[0,2], [1,2], [0.5,2], [0.5,0], [0,0], [1,0]], 'edges': [(0,1), (2,3), (4,5)]},
            'A': {'pts': [[0,0], [0.5,2], [1,0], [0.25,1], [0.75,1]], 'edges': [(0,1), (1,2), (3,4)]}
        }

        word = "CELESTIA"
        spacing = 1.4
        x_offset = -4.9  
        y_offset = 0.5   

        stars = VGroup()
        lines = VGroup()
        
        np.random.seed(42)

        # Build the Graph
        for char in word:
            char_data = font_map[char]
            char_nodes = []
            
            for p in char_data['pts']:
                jx = p[0] + x_offset + np.random.uniform(-0.15, 0.15)
                jy = p[1] + y_offset + np.random.uniform(-0.15, 0.15) 
                
                star = Dot(point=[jx, jy, 0], radius=np.random.uniform(0.04, 0.07), color=WHITE, fill_opacity=0)
                char_nodes.append(star)
                stars.add(star)
            
            for e in char_data['edges']:
                line = Line(
                    char_nodes[e[0]].get_center(), 
                    char_nodes[e[1]].get_center(), 
                    stroke_width=2, 
                    color="#00ACC1", 
                    stroke_opacity=0
                )
                lines.add(line)
                
            x_offset += spacing

        # 3. BACKGROUND STARS
        bg_stars = VGroup()
        for _ in range(100):
            sx = np.random.uniform(-7, 7)
            sy = np.random.uniform(-2.5, 4) 
            bg_stars.add(Dot(point=[sx, sy, 0], radius=np.random.uniform(0.01, 0.03), color=WHITE, fill_opacity=0))

        # 4. TAGLINE
        tagline = Text("STEREOSCOPIC STELLAR ENGINE", font_size=20, color=GRAY)
        platform = Text("BUILT FOR META QUEST", font_size=14, color="#00ACC1")
        text_group = VGroup(tagline, platform).arrange(DOWN, buff=0.2).move_to([0, -2, 0])

        # 5. TWINKLE UPDATER FUNCTION
        def twinkle_updater(mob, dt):
            for s in mob:
                if not hasattr(s, "twinkle_phase"):
                    s.twinkle_phase = np.random.uniform(0, 2 * PI)
                    s.twinkle_speed = np.random.uniform(2, 5) 
                    s.time_tracker = 0
                    
                s.time_tracker += dt
                new_opacity = 0.65 + 0.35 * np.sin(s.twinkle_speed * s.time_tracker + s.twinkle_phase)
                s.set_style(fill_opacity=new_opacity)

        # 6. ANIMATION SEQUENCE
        self.add(horizon)
        # CHANGED: run_time from 1 to 0.5
        self.play(FadeIn(horizon), run_time=0.5)

        # Phase 1: Background stars fade in
        for s in bg_stars:
            s.set_style(fill_opacity=np.random.uniform(0.2, 0.8))
        # CHANGED: run_time from 1 to 0.5
        self.play(FadeIn(bg_stars), run_time=0.5)

        # Phase 2: Main Constellation Stars appear randomly
        stars_list = list(stars)
        random.shuffle(stars_list)
        for s in stars_list:
            s.set_style(fill_opacity=1)
        
        stars.add_updater(twinkle_updater)
        bg_stars.add_updater(twinkle_updater)

        # CHANGED: lag_ratio from 0.05 to 0.02, run_time from 2.5 to 1.0
        self.play(
            LaggedStart(*[FadeIn(s, scale=0.5) for s in stars_list], lag_ratio=0.02),
            run_time=1.0
        )

        # Phase 3: Connect the Graph
        # CHANGED: run_time from 2 to 0.75
        self.play(
            lines.animate.set_stroke(opacity=0.6),
            run_time=2,
            rate_func=smooth
        )

        # Phase 4: Final Glow, Tagline, and Activate Twinkle
        # CHANGED: run_time from 2 to 1.0
        self.play(
            stars.animate.set_color("#cad7ff"), 
            lines.animate.set_stroke(opacity=1, width=3),
            FadeIn(text_group, shift=UP*0.3),
            run_time=1.0
        )
        
        self.wait(3)