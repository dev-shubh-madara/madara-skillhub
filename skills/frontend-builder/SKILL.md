---
name: frontend-builder
description: "Builds and fixes frontend work: landing pages, dashboards, animated or 3D scroll sites, responsive layouts, and UI cleanups. Use when the user asks for a website, page, UI, component, animation, or says the design looks plain or broken."
---

# Frontend builder

## Before you start

Ask only what you cannot guess: who the page is for, what action it should drive, and any brand colors or references. If the user already gave a reference site or style, use it and skip the questions.

## Workflow

1. **Pick a direction in one line.** Example: "dark, high contrast, one accent color, large type, slow scroll reveals". Stick to it for the whole build.
2. **Structure first.** Write the section list (hero, proof, features, pricing, call to action) before any styling.
3. **Build in one pass, then refine.** Semantic HTML, CSS variables for color and spacing, a type scale, and a small set of reusable components.
4. **Add motion with purpose.** Reveal on scroll, hover feedback, and one signature effect. Respect `prefers-reduced-motion`.
5. **Check it.** Resize to phone, tablet and desktop widths. Tab through the page. Check contrast on text over images.
6. **Fix what the check finds** before handing it over.

## Quality bar

- Works at 360px wide without horizontal scroll.
- Buttons and links have visible hover and focus states.
- Images have alt text and sizes. Fonts are limited to two families.
- No layout shift when images or fonts load.
- Heavy effects (3D, particles) have a lighter fallback on weak devices.
- Text contrast meets WCAG AA.

## Output

- For a single page, deliver one self-contained HTML file unless the user wants a framework.
- For an app, give the folder structure first, then the files.
- End with a short note: how to run it, what to change first, and anything you left out.

## Avoid

- Default gradients and stock layouts that make every site look the same.
- Libraries added for one small effect.
- Giant inline blocks of repeated code. Use variables and small helpers.
- Fake testimonials, fake logos, or invented statistics.

## Reference

Read `references/checklist.md` when starting a build, picking tokens, or fixing a layout bug. It has the checklists, templates and worked examples for this skill.

## Self-check before replying

Run through these before you send the answer. Fix anything that fails.

- Did I test at 360px and at desktop width, at least by reading the CSS for fixed widths and `100vw`?
- Does every interactive element have hover and focus styles?
- Is there exactly one signature effect, and does it respect reduced motion?
- Did I invent any testimonials, logos or numbers? If so, replace them with clear placeholders.
- Can the user run it with the steps I gave, without guessing a missing file?
- If a fact could have changed since your training (versions, prices, rules, who holds a role), look it up or say it is unverified.
