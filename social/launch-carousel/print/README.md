# Print → PDF (LinkedIn carousel)

`carousel-print.html` is the launch carousel with the web chrome removed — just
the five slides, all images embedded, ready to export as a PDF carousel.

## Export (use Chrome)
1. Open `carousel-print.html` in Chrome.
2. Ctrl + P.
3. Destination: **Save as PDF**.
4. **Margins: None**  ·  **Scale: 100 (Default)**  ·  Layout: Portrait.
5. More settings → **Background graphics: ON** (so the dark slides render).
6. Save → a 5-page PDF, each page 1080 × 1350 (4:5).

## Post to LinkedIn
New post → **Add a document** → upload the PDF → give it a title → post.
LinkedIn shows the pages as a swipeable carousel.

Regenerate after edits: `node ../build.mjs`
