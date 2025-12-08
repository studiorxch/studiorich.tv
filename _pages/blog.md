---
layout: blog
kicker: 2025
title: StudioRich Blog
subtitle: Archives of Lo-Fi Memory, Weird Internet, and Beat Culture
permalink: /blog/
description: "Explore lo-fi articles, thoughts, and release commentary by StudioRich."
---

<div class="blog-feed">
  {% for post in site.posts %}
    <a href="{{ post.url | relative_url }}" class="blog-card">
      <div class="blog-thumb">
        {% if post.published == false %}
          <div class="unpublished-flag">UNPUBLISHED</div>
        {% endif %}
        <img src="{{ post.image | default: '/assets/img/blog/default.jpg' }}" alt="{{ post.title }}">
        <div class="blog-date">{{ post.date | date: "%d" }}<br>{{ post.date | date: "%b" }}</div>
        <div class="blog-text-overlay">
          <div class="blog-title">{{ post.title }}</div>
          <div class="blog-desc">{{ post.description | default: post.excerpt | strip_html | truncate: 90 }}</div>
        </div>
      </div>
    </a>
  {% endfor %}
</div>
