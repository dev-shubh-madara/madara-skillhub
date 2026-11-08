# Frontend checklist and fixes

## Starter tokens

```css
:root {
  --bg: #0b0d12; --surface: #141821; --text: #e8eaf0; --muted: #9aa3b2;
  --accent: #7c5cff; --accent-2: #22d3ee; --danger: #ef4444;
  --radius: 14px; --gap: clamp(16px, 2.5vw, 32px);
  --step-0: clamp(1rem, 0.95rem + 0.3vw, 1.125rem);
  --step-1: clamp(1.25rem, 1.1rem + 0.8vw, 1.6rem);
  --step-2: clamp(1.6rem, 1.3rem + 1.6vw, 2.4rem);
  --step-3: clamp(2.2rem, 1.6rem + 3vw, 4rem);
  --ease: cubic-bezier(.2,.7,.2,1);
}
*, *::before, *::after { box-sizing: border-box; }
img, video, canvas, svg { max-width: 100%; display: block; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; scroll-behavior: auto !important; }
}
```

Swap the colors for the brand. Keep every color and size in a variable so a restyle is a one-place change.

## Widths to test

360, 390, 768, 1024, 1280, 1920. Rotate the phone sizes to landscape once.

## Bugs that come up again and again

| Symptom | Usual cause | Fix |
|---|---|---|
| Sideways scroll on phone | `width: 100vw` (includes scrollbar) or a wide child | Use `width: 100%`; find the culprit with `* { outline: 1px solid red }` |
| Hero cut off on mobile | `height: 100vh` with the browser bar | `min-height: 100svh` (fall back to `100vh`) |
| Flex item overflows | Flex children default to `min-width: auto` | `min-width: 0` on the child |
| `position: sticky` does nothing | A parent has `overflow: hidden/auto` | Remove it or move sticky element up |
| Modal under the header | New stacking context from `transform` or `filter` | Put the modal at the end of `body`, set one z-index scale |
| Layout jumps when images load | No size on images | Set `width`/`height` or `aspect-ratio` |
| Font flash | Web font blocks text | `font-display: swap`, preload the main weight only |
| Janky scroll effect | Animating `top/left/height` or listening to scroll | Animate `transform`/`opacity`; use `IntersectionObserver` |

## Performance budget

- Main image under 200 KB, served as WebP or AVIF, with `loading="lazy"` below the fold.
- At most two font families, two to three weights.
- No library for something CSS can do (fades, slides, sticky, smooth scroll).
- 3D or particle scenes: cap device pixel ratio at 2, pause when the tab is hidden or the canvas is off screen, give a static image fallback on low-end devices.

## Accessibility pass

- One `h1`, headings in order, landmarks (`header`, `nav`, `main`, `footer`).
- Every interactive element reachable by Tab, with a visible `:focus-visible` style.
- Buttons are `<button>`, links are `<a href>`. No click handlers on `div`.
- Text contrast 4.5:1 (3:1 for large text). Check text placed over images.
- Form inputs have labels. Errors are in text, not color alone.

## Motion with purpose

Pick one signature effect for the page (a hero reveal, a 3D tilt, a scroll-linked scene) and keep everything else quiet: 150 to 300 ms transitions, one easing curve, reveals that run once.
