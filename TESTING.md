# Browser tests

The smoke tests use Playwright and pytest; they do not add dependencies to the
demo app itself.

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and
Python 3.10 or newer. From the repository root, sync the pinned test
dependencies and install the Chromium browser used by Playwright:

```sh
uv sync --locked --extra test
uv run playwright install chromium
```

## Run

```sh
uv run pytest
```

The test fixture starts a local HTTP server bound only to `127.0.0.1` on an
available port, then shuts it down when the test session ends. Each test gets
its own browser context so state cannot leak between tests.
