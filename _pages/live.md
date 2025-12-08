---
layout: default
title: StudioRich | Lo-Fi Radio Chill Beats
description: 'Stream lo-fi chill beats 24/7 from StudioRich – live music therapy, cozy visuals, and relaxed vibes direct from Twitch.'
permalink: /live/
image: /assets/img/covers/live-stream.webp
---

<div class="live-layout">
  <div class="video-container">
    <iframe
      src="https://player.twitch.tv/?channel=studiorich&parent=studiorich.shop"
      allowfullscreen
      frameborder="0">
    </iframe>
  </div>

  <div class="chat-container" id="chatBox">
    <iframe
      src="https://www.twitch.tv/embed/studiorich/chat?parent=studiorich.shop&darkpopout"
      frameborder="0">
    </iframe>
  </div>
</div>

<button id="toggleChat">🗨️ Hide Chat</button>

{% include youtube-carousel.html video_urls="
https://www.youtube.com/embed/3_U9pLLI6Tk,
https://www.youtube.com/embed/u5tCaLsFW-M,
https://www.youtube.com/embed/d_ERqZwROAk,
https://www.youtube.com/embed/vKIr3HJiAVo
" %}

<div class="offline-message">
  <h1><img src="/assets/ui/radio.svg" alt="Radio icon" class="icon-sm"> StudioRich Radio is Offline</h1>
  <p>We stream live every Monday to Thursday from 8–10PM EST.</p>
  <p>
    Catch Stranger Vibes, lo-fi chill, and ambient hip hop here or on
    <a href="https://twitch.tv/studiorich" target="_blank">Twitch</a>.
  </p>
</div>
<script src="/assets/js/live.js"></script>
