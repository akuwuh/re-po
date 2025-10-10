# re-po

Reusable GitHub statistics cards. The project provides a shared Python core, a GitHub Action wrapper, an HTTP API, and a tiny web builder.

## Quickstart

### 1. GitHub Action

Add the reusable workflow to your repository:

```yaml
name: Update re-po card
on:
  schedule:
    - cron: "0 * * * *"
  workflow_dispatch:

jobs:
  card:
    uses: akuwuh/re-po/.github/workflows/reusable.yml@main
    with:
      user: your-github-handle
      format: svg
      theme: terminal
      output: re-po.svg
```

Or use the composite Action directly:

```yaml
- uses: akuwuh/re-po/actions/re-po-action@main
  with:
    user: your-github-handle
    format: svg
    theme: terminal
    out: re-po.svg
```

### 2. API

Run locally with Uvicorn:

```bash
pip install ./packages/py-core
uvicorn apps.api.main:app --reload
```

Then request a card:

```
curl "http://127.0.0.1:8000/v1/card?user=akuwuh&format=svg"
```

### 3. Web builder

The Next.js builder consumes the same API and outputs an embed URL or workflow YAML.

```bash
cd apps/web
npm install
npm run dev
```

Visit `http://localhost:3000/builder` to experiment and copy the generated URLs.

## Repository layout

- `packages/py-core` – shared Python package and CLI (`re-po render ...`).
- `actions/re-po-action` – composite GitHub Action wrapping the CLI.
- `apps/api` – FastAPI app serving the same render pipeline.
- `apps/web` – Next.js builder for embeds and workflows.
- `.github/workflows` – CI and reusable workflow definitions.

## Configuration

The root `re-po.config.yml` file defines themes and default limits. Override with `RE_PO_CONFIG_PATH` if you need a custom location. Both the CLI and API load the same configuration.

Set `GITHUB_TOKEN` to increase GitHub API rate limits in local runs, Actions, or the API server.
