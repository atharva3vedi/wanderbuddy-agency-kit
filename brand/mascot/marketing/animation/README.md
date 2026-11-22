# WanderBuddy clip pipeline

Fixed short actions for the two buddies, made without an animator or a rig.

1. **Start frame.** Seedream, text only (the connector errors on reference images): one
   character, standing, arms at sides, solid black on pure white, lots of margin, portrait.
   Reuse the SAME start frame for every clip of that character so they all begin and end alike.
2. **Animate.** Seedance image-to-video via the `seedance` MCP: 3 to 4s, 720p, no audio, no
   watermark, do not pass `camera_fixed` (rejected for i2v). Prompt pattern: "Flat 2D vector
   animation. The black silhouette gentleman <ACTION>, then returns to the exact starting
   standing pose. Solid flat pure black silhouette, crisp edges. Background stays pure white and
   empty. Static locked camera, no zoom, no shadows, no new objects, no colour, no 3D shading."
3. **Make it transparent.** Black on white means luminance is the matte:

   ```bash
   A="split[a][b];[a]format=gray,negate,lut=y='clip((val-40)*1.35,0,255)'[al];[b]lutrgb=r=0:g=0:b=0[k];[k][al]alphamerge"
   ffmpeg -i clip.mp4 -filter_complex "[0]fps=24,scale=-2:480,$A" -loop 1 -c:v libwebp_anim -lossless 0 -q:v 60 clip.webp
   ```

   `-loop 1` plays once and holds the last frame. Output is black + alpha: tint with the ink
   colour in Flutter (`color:` + `BlendMode.srcIn`) so dark mode is free.
4. **Check.** First and last frame match the start pose; no grey haze (raise the 40 threshold);
   silhouette stays solid (no interior detail appearing); under about 250KB.

Action list per character (about 10): hat tip / curtsy, wave, point, pocket the passport,
hold up ticket, check watch, celebrate, reassuring palm, small nod (AI chat), lean in (AI chat).
