---

layout: default
title: "New York Gritty"
station_id: "R23"
station_slug: canal-st
panel_id: the-mixtape-cardigan
order: 1
routes: ["N","W","R"] # keep J/Z only if you intend the larger complex
borough: "Manhattan"
neighborhood: "SoHo"
zip_code: "10013"

playlist_ref: "/assets/playlists/brooklyn-bridge-city-hall.json"

tracks:

- title: "Echoes Under the Arches"
  artist: "StudioRich"
  url: "/assets/audio/playtracks/echoes-under-the-arches.mp3"

# image paths — keep them consistent to your assets

image_base: "/assets/stations/640-brooklyn-bridge-city-hall/panels/new-york-gritty-canal-st"
hero_width: 1536
available_widths: [512,1024,1536]

# canonical URL for this panel (use the same slug as station_slug)

permalink: "/stations/brooklyn-bridge-city-hall/new-york-gritty-canal-st/"

# panel meta carried over from playground

description: "At Canal St., a t-shirt slouches across the railing like leftover thought — soft, creased, and quietly defiant. This subway pause becomes a loop: fluorescent flicker, overhead echo, a beat stitched from urban hush. Our accompanying lo-fi playlist hums beneath the station's grime and rhythm, weaving field recordings, Rhodes chords, and tape-warped drum textures into a soft transit drift — a memory carried in cotton and delay."
eyebrow: "Canal St."

# render controls

fit: cover # cover | contain
pos: center bottom # CSS object-position
text_style: overlay # overlay | below | cap
focus: graphic # graphic | model
zoom: 1.08

# pins

tags:

- x: 39
  y: 39
  href: https://goods.studiorich.shop/products/unisex-t-shirt
  label: New York Gritty Premium Tee
  icon: /assets/ui/tshirt.svg

- x: 81.1
  y: 59.4
  ref: /assets/playlists/canal-st.json
  label: Canal St Playlist
  icon: /assets/ui/star.svg
  cover: /assets/img/icons/peace-token-256.webp
