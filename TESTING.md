# Browser tests

The browser smoke tests use Playwright and do not add dependencies to the demo app.

## Setup

Install Node.js 20 or newer and npm, then install the test dependencies and
Chromium:

```sh
npm ci
npx playwright install chromium
```

## Run

```sh
npm test
```

Playwright starts and stops a local HTTP server bound to `127.0.0.1`. Each test
uses an isolated browser context.
