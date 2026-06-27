(function () {
  const grid = document.getElementById("sceneGrid");
  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;
  const canHover = window.matchMedia("(hover: hover)").matches;
  const enableHoverPreview = canHover && !prefersReducedMotion;

  window.CELESTIA.scenes.forEach(function (scene) {
    const card = document.createElement("a");
    card.className = "scene-card";
    card.href = "deck.html?scene=" + scene.id;
    card.setAttribute("aria-label", "Watch scene " + scene.id + ": " + scene.title);

    const thumb = document.createElement("div");
    thumb.className = "scene-thumb";

    const num = document.createElement("span");
    num.className = "scene-thumb-num";
    num.textContent = "Scene " + scene.id;

    const thumbTitle = document.createElement("span");
    thumbTitle.className = "scene-thumb-title";
    thumbTitle.textContent = scene.title;

    const poster = document.createElement("img");
    poster.className = "scene-poster";
    poster.src = scene.poster;
    poster.alt = "";
    poster.loading = "lazy";
    poster.decoding = "async";

    const previewVideo = document.createElement("video");
    previewVideo.muted = true;
    previewVideo.loop = true;
    previewVideo.playsInline = true;
    previewVideo.preload = "none";
    previewVideo.setAttribute("aria-hidden", "true");

    thumb.appendChild(poster);
    thumb.appendChild(previewVideo);
    thumb.appendChild(num);
    thumb.appendChild(thumbTitle);

    const body = document.createElement("div");
    body.className = "scene-body";

    const desc = document.createElement("p");
    desc.textContent = scene.description;

    const meta = document.createElement("div");
    meta.className = "scene-meta";
    const clipLabel = scene.clips.length === 1 ? "clip" : "clips";
    meta.textContent = scene.clips.length + " " + clipLabel;

    const actionHint = document.createElement("div");
    actionHint.className = "card-action-hint";
    actionHint.innerHTML =
      '<span class="hint-hover">Hover to preview</span>' +
      '<span class="hint-tap">Tap to watch</span>';

    body.appendChild(desc);
    body.appendChild(meta);
    body.appendChild(actionHint);

    card.appendChild(thumb);
    card.appendChild(body);
    grid.appendChild(card);

    if (!enableHoverPreview) return;

    var previewLoaded = false;

    card.addEventListener("mouseenter", function () {
      if (!previewLoaded) {
        previewVideo.src = scene.clips[0];
        previewLoaded = true;
      }
      card.classList.add("is-previewing");
      previewVideo.play().catch(function () {});
    });

    card.addEventListener("mouseleave", function () {
      card.classList.remove("is-previewing");
      previewVideo.pause();
      previewVideo.currentTime = 0;
    });

    card.addEventListener("focus", function () {
      if (!previewLoaded) {
        previewVideo.src = scene.clips[0];
        previewLoaded = true;
      }
    });
  });
})();
