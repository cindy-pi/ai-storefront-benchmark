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
>
> The session is complete when the page is live and accessible in a browser. Do not ask for clarification — make all decisions independently.

---

## How It Was Run

Each model runs Scenario 1 in a fresh Digiswarm session using the standard benchmark configuration.

**Platform:** [Digiswarm AI](https://digiswarm.ai) — default project configuration from [github.com/digiswarmai/skills](https://github.com/digiswarmai/skills)
**Plan:** Starter Plan (1 agent at a time, sequential execution)
**Agent team:** Paul (Liaison), Lucy (PM), John (Frontend), George (Middleware), Ringo (Backend)

**Pre-run setup (completed before each session):**
1. Create the model's submission repo on GitHub under `cindy-pi`
2. Initialize with a LICENSE — no source files pre-populated
3. Go to **Settings → Pages → Build and deployment → Source** and select **GitHub Actions**
4. Generate a scoped GitHub token for the session (see [setup/GITHUB_SETUP.md](../setup/GITHUB_SETUP.md))
5. Configure the Digiswarm controller: set the model, add the API key and GitHub token, set the target repo

**Timing:** Starts when the prompt is submitted to Paul. Ends when the live page is confirmed accessible in a browser.

---

## Results

> Results will be published here once all four models have completed Scenario 1.

| Model | Build Time | Token Cost | Live URL | Status |
|---|---|---|---|---|
| Anthropic Claude | TBD | TBD | TBD | TBD |
| GPT | TBD | TBD | TBD | TBD |
| DeepSeek | TBD | TBD | TBD | TBD |
| Qwen3-Code | TBD | TBD | TBD | TBD |
