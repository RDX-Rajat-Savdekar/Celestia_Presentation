/**
 * Single source of truth for Celestia presentation clips and scene metadata.
 * Loaded by index.html (homepage) and deck.html (player).
 */
window.CELESTIA = {
  scenes: [
    {
      id: 0,
      title: "Intro",
      description: "Celestia logo",
      poster: "posters/scene0.jpg",
      clips: ["scene0/S0_CelestiaLogo.mp4"],
    },
    {
      id: 1,
      title: "Sphere Projection",
      description:
        "Why the night sky is rendered on an inward-facing sphere",
      poster: "posters/scene1.jpg",
      clips: [
        "scene1/S1_Clip1_Immersion.mp4",
        "scene1/S1_Clip2_Abstraction.mp4",
        "scene1/S1_Clip3_Fold.mp4",
        "scene1/S1_Clip4_SphereSolution.mp4",
      ],
    },
    {
      id: 2,
      title: "Magnitude Filter",
      description:
        "Cutting 119k catalog stars down to ~9k naked-eye stars",
      poster: "posters/scene2.jpg",
      clips: [
        "scene2/S2_Clip1_DataOverload.mp4",
        "scene2/S2_Clip2_ApparentMagnitude.mp4",
        "scene2/S2_Clip3_TheFilter.mp4",
        "scene2/S2_Clip4_OptimizedSky.mp4",
      ],
    },
    {
      id: 3,
      title: "Great Migration",
      description: "RA/Dec → local sky coordinate pipeline",
      poster: "posters/scene3.jpg",
      clips: [
        "scene3/S3_Clip1_CelestialGrid.mp4",
        "scene3/S3_Clip2_ThePipeline.mp4",
        "scene3/S3_Clip3_GreatMigration.mp4",
      ],
    },
    {
      id: 4,
      title: "Color & Twinkle",
      description: "B-V index coloring and twinkle animation",
      poster: "posters/scene4.jpg",
      clips: [
        "scene4/S4_Clip1_Temperature.mp4",
        "scene4/S4_Clip2_BVIndex.mp4",
        "scene4/S4_Clip3_ColorWash.mp4",
        "scene4/S4_Clip4_Twinkle.mp4",
      ],
    },
    {
      id: 5,
      title: "Spatial Search",
      description:
        "Constellation graph and octree search concept (design exploration; shipped app uses O(1) hash map)",
      poster: "posters/scene5.jpg",
      clips: [
        "scene5/S5_Clip1_GraphData.mp4",
        "scene5/S5_Clip2_3DGraph.mp4",
        "scene5/S5_Clip3_Octree.mp4",
      ],
    },
  ],

  /** Flat list of all clip paths in presentation order. */
  getAllClips() {
    return this.scenes.flatMap((s) => s.clips);
  },

  /** Index in flat list of the first clip for a scene id. */
  getSceneStartIndex(sceneId) {
    let index = 0;
    for (const scene of this.scenes) {
      if (scene.id === sceneId) return index;
      index += scene.clips.length;
    }
    return 0;
  },

  getSceneById(sceneId) {
    return this.scenes.find((s) => s.id === sceneId);
  },

  /** Which scene owns this clip path. */
  getSceneForClip(clipPath) {
    return this.scenes.find((s) => s.clips.includes(clipPath));
  },

  /** Clip metadata parsed from filename conventions. */
  getClipMeta(clipPath) {
    const scene = this.getSceneForClip(clipPath);
    if (!scene) return null;

    const file = clipPath.split("/")[1];
    const parts = file.replace(".mp4", "").split("_");

    let clipNumber = 1;
    let clipName = "";

    if (parts.length >= 3) {
      clipNumber = parts[1].replace("Clip", "");
      clipName = parts.slice(2).join(" ");
    } else {
      clipName = parts.slice(1).join(" ");
    }

    return {
      sceneId: scene.id,
      sceneTitle: scene.title,
      clipNumber: parseInt(clipNumber, 10),
      totalClips: scene.clips.length,
      clipName,
    };
  },
};
