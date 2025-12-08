---
layout: overlay
title: Moodline overlay for OBS
permalink: /moodline-overlay
---

<div id="overlay-root">

  <!-- BOTTOM MOODLINE -->
  <div id="moodbar-layer">
    <svg id="moodline" width="100%" height="120"
         viewBox="0 0 1000 120"
         preserveAspectRatio="none">
  
      <path id="mood-wave"
        d="M 0 60 Q 250 60 500 60 T 1000 60"
        stroke="#ffffff"        <!-- MotionEngine overwrites -->
        stroke-width="20"
        fill="none"
        stroke-linecap="round"
      />
  
    </svg>
  </div>

  <!-- TRACK INFO -->
  <div id="info-layer">
    <p id="nowplaying-label">Now Playing</p>
    <div id="track-line">
      <span id="track-title"></span>
      <span id="track-variant" class="variant-pill"></span>
    </div>
  </div>

</div>
