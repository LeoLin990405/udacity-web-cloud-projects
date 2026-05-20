# Study Night: Preparing for Production

This submission prepares the Study Night flashcard application for production review.

## What Is Included

- `package.json` includes the required project metadata, `type: "module"`, MIT license, scripts, and required dev dependencies.
- `src/shuffle.js` and `src/utilityRenderFunctions.js` have been corrected and formatted for ESLint/Prettier readability.
- CSS selectors in `styles/` have been manually simplified from long descendant selectors to maintainable class selectors.
- `gulpfile.js` defines tasks for Parcel build/serve, Mocha unit tests, and Cypress end-to-end tests.
- `test/shuffle.js` contains focused Mocha/Chai unit tests for the shuffle function.
- `cypress/e2e/navigation.cy.js` covers navigation behavior.
- `cypress/e2e/form.cy.js` covers happy and unhappy paths for the create-set and add-card forms.
- `dist/` is included as the production build artifact directory.

## Commands

```bash
npm install
npm run test
npm run gulp test
npm run gulp
```

Run the Parcel server before Cypress:

```bash
npm run serve
npm run cypress:run
```
