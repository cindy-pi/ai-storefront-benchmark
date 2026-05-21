# Scenario 1 — Hello World on GitHub Pages

## The Scenario

**Goal:** Deploy a Hello World webpage to the model's GitHub Pages URL.

The agent must create a minimal webpage and configure the repository to publish it live via GitHub Pages. This is the simplest possible deployment task — it tests whether the model can set up a basic deployment pipeline from scratch with no prior state in the repo.

**Success criteria:**
- A live webpage is accessible at the model's GitHub Pages URL
- The page content is functional and renders correctly in a browser
- The repository is correctly configured to publish via GitHub Actions

---

## The Prompt

Each Paul instance received the following prompt for this scenario:

> Deploy a Hello World webpage to this repository's GitHub Pages URL.
>
> Requirements:
> - Create a webpage with at least a heading and a short line of text
> - Configure the repository so the page is published live at this repo's GitHub Pages URL
> - Use a GitHub Actions workflow to build and deploy automatically on every push to `main`
> - In the repository settings, set the Pages source to **GitHub Actions** (not a branch)
> - The default branch is `main` — all work should be committed and merged to `main`
>
> The session is complete when the page is live and accessible in a browser. Do not ask for clarification — make all decisions independently.

---

## How It Was Run

Each model runs Scenario 1 in a fresh Digiswarm session using the standard benchmark configuration.

**Platform:** [Digiswarm AI](https://digiswarm.ai) — default project configuration from [github.com/digiswarmai/skills](https://github.com/digiswarmai/skills)
**Plan:** Starter Plan (1 agent at a time, sequential execution)
**Agent team:** Paul (Liaison), Lucy (PM), John (Frontend), George (Middleware), Ringo (Backend)

**Pre-run setup (completed before each session):**

Run the pre-flight script to verify token scopes, repo access, and Pages configuration before starting:

```bash
# Run from the ai-storefront-benchmark repo root
python setup/preflight.py --token ghp_xxx --repo cindy-pi/ai-storefront-[model] --scenario 1
```

1. Create the model's submission repo on GitHub under `cindy-pi`
2. Initialize with a LICENSE — no source files pre-populated
3. **Set default branch to `main`** — Settings → General → Default branch → click the pencil → select `main` → Update
4. Go to **Settings → Pages → Build and deployment → Source** and select **GitHub Actions**
5. Generate a scoped GitHub token for the session (see [setup/GITHUB_SETUP.md](../setup/GITHUB_SETUP.md))
6. Configure the Digiswarm controller: set the model, add the API key and GitHub token, set the target repo

**Timing:** Build time is measured from when the first issue with label `scenario1-start` is created in the submission repo to when the last issue with label `scenario1-end` is closed.

---

## Results

> Results will be published here once all four models have completed Scenario 1.

| Model | Build Time | Token Cost | Live URL | Status |
|---|---|---|---|---|
| Anthropic Claude | TBD | TBD | TBD | TBD |
| GPT | TBD | TBD | TBD | TBD |
| DeepSeek | TBD | TBD | TBD | TBD |
| Qwen3-Code | TBD | TBD | TBD | TBD |
