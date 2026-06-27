(function () {
  const params = new URLSearchParams(window.location.search);
  const fullMode = params.has("full");
  const autoplayOnLoad = params.get("autoplay") === "1" || fullMode;
  const sceneParam = params.get("scene");
  const startSceneId =
    sceneParam !== null && !fullMode
      ? parseInt(sceneParam, 10)
      : null;

  const videos = window.CELESTIA.getAllClips();
  let index = 0;
  let autoplay = autoplayOnLoad;

  const player = document.getElementById("player");
  const sceneTitleEl = document.getElementById("sceneTitle");
  const clipCounterEl = document.getElementById("clipCounter");
  const bottomLabel = document.getElementById("bottomLabel");
  const progress = document.getElementById("progress");
  const autoplayBtn = document.getElementById("autoplayBtn");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");

  function canGoPrev() {
    if (fullMode) return index > 0;

    const scene = getCurrentScene();
    if (!scene) return false;
    if (getSceneClipIndex() > 0) return true;

    return !!window.CELESTIA.scenes.find(function (s) {
      return s.id === scene.id - 1;
    });
  }

  function canGoNext() {
    if (fullMode) return index < videos.length - 1;

    const scene = getCurrentScene();
    if (!scene) return false;
    if (getSceneClipIndex() < scene.clips.length - 1) return true;

    return !!window.CELESTIA.scenes.find(function (s) {
      return s.id === scene.id + 1;
    });
  }

  function updateNavButtons() {
    prevBtn.disabled = !canGoPrev();
    nextBtn.disabled = !canGoNext();
  }

  function getCurrentScene() {
    return window.CELESTIA.getSceneForClip(videos[index]);
  }

  function getSceneClipIndex() {
    const scene = getCurrentScene();
    if (!scene) return 0;
    const clipPath = videos[index];
    return scene.clips.indexOf(clipPath);
  }

  function resolveStartIndex() {
    if (fullMode || startSceneId === null || Number.isNaN(startSceneId)) {
      return 0;
    }
    const scene = window.CELESTIA.getSceneById(startSceneId);
    if (!scene) return 0;
    return window.CELESTIA.getSceneStartIndex(startSceneId);
  }

  function updateLabels() {
    const meta = window.CELESTIA.getClipMeta(videos[index]);
    if (!meta) return;

    sceneTitleEl.textContent = meta.sceneTitle;
    clipCounterEl.textContent = fullMode
      ? `${index + 1} / ${videos.length}`
      : `Clip ${meta.clipNumber} / ${meta.totalClips}`;

    bottomLabel.textContent = meta.clipName;
    updateNavButtons();
  }

  function loadVideo(i, shouldPlay) {
    index = i;
    player.src = videos[index];
    updateLabels();

    if (shouldPlay !== false) {
      player.play().catch(function () {
        /* autoplay may be blocked until user interaction */
      });
    }
  }

  function goNext() {
    if (fullMode) {
      if (index < videos.length - 1) {
        loadVideo(index + 1);
      }
      return;
    }

    const scene = getCurrentScene();
    if (!scene) return;

    const clipIdx = getSceneClipIndex();
    if (clipIdx < scene.clips.length - 1) {
      loadVideo(index + 1);
      return;
    }

    // Last clip of scene — advance to next scene's first clip
    const nextScene = window.CELESTIA.scenes.find(function (s) {
      return s.id === scene.id + 1;
    });
    if (nextScene) {
      loadVideo(window.CELESTIA.getSceneStartIndex(nextScene.id));
    }
  }

  function goPrev() {
    if (fullMode) {
      if (index > 0) {
        loadVideo(index - 1);
      }
      return;
    }

    const scene = getCurrentScene();
    if (!scene) return;

    const clipIdx = getSceneClipIndex();
    if (clipIdx > 0) {
      loadVideo(index - 1);
      return;
    }

    // First clip of scene — go to previous scene's last clip
    const prevScene = window.CELESTIA.scenes.find(function (s) {
      return s.id === scene.id - 1;
    });
    if (prevScene) {
      const prevStart = window.CELESTIA.getSceneStartIndex(prevScene.id);
      loadVideo(prevStart + prevScene.clips.length - 1);
    }
  }

  document.addEventListener("keydown", function (e) {
    if (e.key === "ArrowRight") {
      e.preventDefault();
      goNext();
    } else if (e.key === "ArrowLeft") {
      e.preventDefault();
      goPrev();
    } else if (e.key === " ") {
      e.preventDefault();
      if (player.paused) {
        player.play();
      } else {
        player.pause();
      }
    }
  });

  player.addEventListener("timeupdate", function () {
    if (player.duration) {
      progress.style.width =
        (player.currentTime / player.duration) * 100 + "%";
    }
  });

  player.addEventListener("ended", function () {
    if (!autoplay) return;

    if (fullMode) {
      if (index < videos.length - 1) {
        loadVideo(index + 1);
      }
      return;
    }

    goNext();
  });

  autoplayBtn.addEventListener("click", function () {
    autoplay = !autoplay;
    autoplayBtn.textContent = "Autoplay: " + (autoplay ? "ON" : "OFF");
  });

  prevBtn.addEventListener("click", goPrev);
  nextBtn.addEventListener("click", goNext);

  index = resolveStartIndex();
  autoplayBtn.textContent = "Autoplay: " + (autoplay ? "ON" : "OFF");
  loadVideo(index);
})();
