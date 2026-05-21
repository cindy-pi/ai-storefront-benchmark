# Repo Setup — GitHub Pages Deployment

Each competing model's repo must be configured to automatically build and deploy to GitHub Pages on every push to `main`. This is a benchmark requirement — the live site must always reflect the latest committed code so judges can review it at any time.

This document covers the exact configuration each submission repo must include.

---

## 1. Vite Config — Set the Base Path

In `vite.config.js` (or `vite.config.ts`), set `base` to the repo name. This ensures asset paths resolve correctly on GitHub Pages.

```js
// vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/ai-storefront-anthropic/',  // replace with this repo's name
})
```

Each repo uses its own name:

| Repo | base value |
|---|---|
| ai-storefront-anthropic | `/ai-storefront-anthropic/` |
| ai-storefront-gpt | `/ai-storefront-gpt/` |
| ai-storefront-deepseek | `/ai-storefront-deepseek/` |
| ai-storefront-qwen3 | `/ai-storefront-qwen3/` |

---

## 2. GitHub Actions Workflow

Create the file `.github/workflows/deploy.yml` in the repo with the following content. This workflow builds the Vite app and deploys the output to GitHub Pages automatically on every push to `main`.

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Node
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - name: Install dependencies
        run: npm install

      - name: Build
        run: npm run build

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: ./dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## 3. Enable GitHub Pages in Repository Settings

After pushing the workflow file, enable Pages in the GitHub repository settings:

1. Go to the repo on GitHub
2. Click **Settings** → **Pages** (left sidebar)
3. Under **Build and deployment**, set **Source** to **GitHub Actions**
4. Save

The first successful workflow run will publish the site. Subsequent pushes to `main` redeploy automatically.

---

## 4. React Router — Handle Client-Side Routing (if used)

If the app uses React Router with `BrowserRouter`, GitHub Pages will return 404 on direct URL access to any route other than `/`. Use `HashRouter` instead for full static-site compatibility:

```jsx
// main.jsx
import { HashRouter } from 'react-router-dom'

<HashRouter>
  <App />
</HashRouter>
```

Or, alternatively, add a `public/404.html` redirect trick — but `HashRouter` is simpler and more reliable on GitHub Pages.

---

## 5. Verify the Deployment

Once the Actions workflow has run successfully:

- The live site will be at `https://cindy-pi.github.io/<repo-name>/`
- Workflow status is visible under the repo's **Actions** tab
- The deployed URL also appears in **Settings → Pages**

| Repo | Expected Live URL |
|---|---|
| ai-storefront-anthropic | `https://cindy-pi.github.io/ai-storefront-anthropic/` |
| ai-storefront-gpt | `https://cindy-pi.github.io/ai-storefront-gpt/` |
| ai-storefront-deepseek | `https://cindy-pi.github.io/ai-storefront-deepseek/` |
| ai-storefront-qwen3 | `https://cindy-pi.github.io/ai-storefront-qwen3/` |

---

## Summary Checklist

- [ ] `vite.config.js` has `base` set to the correct repo name
- [ ] `.github/workflows/deploy.yml` exists and matches the template above
- [ ] GitHub Pages source is set to **GitHub Actions** in repo settings
- [ ] First workflow run completed successfully
- [ ] Live site is accessible at the expected URL
