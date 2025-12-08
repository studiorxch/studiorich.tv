---
layout: default
title: Music Library
permalink: /library/
redirect_from:
  - /tracks/
description: "Browse over 360 StudioRich tracks by mood, genre, and visual aesthetic."
image: /assets/img/hero/music-library-record-room-hero.webp
hero: false
compact_header: true
subtitle: "360+ tracks — filter by mood & genre, or ask Genie."
show_rxch: true
scripts:
  - /assets/js/rxch/rxch-genie.js
  - /assets/js/library/filters.js
---


<!-- Filter Bar -->
<div class="filter-bar">
  <button type="button" data-filter="all" data-type="all" class="active">All</button>

  {% assign all_moods  = "" | split: "" %}
  {% assign all_genres = "" | split: "" %}
  {% for track in site.data.library %}
    {% assign mood_array  = track.mood  %}
    {% if mood_array == nil or mood_array == blank %}{% assign mood_array  = "" | split: "" %}{% endif %}
    {% assign genre_array = track.genre %}
    {% if genre_array == nil or genre_array == blank %}{% assign genre_array = "" | split: "" %}{% endif %}
    {% assign all_moods  = all_moods  | concat: mood_array  %}
    {% assign all_genres = all_genres | concat: genre_array %}
  {% endfor %}

  {% assign unique_moods  = all_moods  | uniq | sort %}
  {% assign unique_genres = all_genres | uniq | sort %}

  <!-- Moods -->
  {% for mood in unique_moods %}
    {% unless mood == "nan" or mood == "" %}
      <button type="button" data-filter="{{ mood | downcase | strip }}" data-type="mood">
        {{ mood | strip }}
      </button>
    {% endunless %}
  {% endfor %}

  <!-- Genres -->
  {% for genre in unique_genres %}
    {% unless genre == "nan" or genre == "" %}
      <button type="button" data-filter="{{ genre | downcase | strip }}" data-type="genre">
        {{ genre | strip }}
      </button>
    {% endunless %}
  {% endfor %}
</div>

<!-- Track Grid -->
<section class="track-grid">
  {% for track in site.data.library %}
    {% if track.has_cover and track.has_loop %}
      {% assign mood_array = track.mood %}
      {% if mood_array == nil or mood_array.size < 3 %}
        {% assign mood_array = track.mood_suggested %}
        {% assign filtered_mood = false %}
      {% else %}
        {% assign filtered_mood = true %}
      {% endif %}

      {% assign genre_array = track.genre | default: "" | split: "" %}

      <a class="track-card {% unless filtered_mood %}no-filter{% endunless %}"
         href="/tracks/{{ track.slug }}/?autoplay=1"
         data-mood="{{ mood_array | join: ' ' | downcase }}"
         data-genre="{{ genre_array | join: ' ' | downcase }}">
        <img src="/assets/img/covers/{{ track.slug }}.webp" alt="{{ track.title }} cover" class="track-cover">
        <div class="track-title">{{ track.title }}</div>
      </a>
    {% endif %}
  {% endfor %}
</section>
