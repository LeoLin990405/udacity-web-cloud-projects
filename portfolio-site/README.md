# Portfolio Site

This submission implements a responsive portfolio homepage using BEM class names, organized SCSS partials, and a compiled `dist/main.css` stylesheet.

## Structure

- `src/index.html` contains the semantic HTML for the portfolio homepage.
- `src/img/` contains the profile and project images.
- `src/scss/base/` contains resets and global element styles.
- `src/scss/blocks/` contains component styles using BEM naming.
- `src/scss/utils/` contains variables and mixins.
- `dist/main.css` is the compiled stylesheet loaded by the page.

## Build

The project includes a `package.json` with a Sass build command:

```bash
npm install
npm run build
```

The compiled CSS is already included in `dist/main.css` for review.
