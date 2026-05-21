# Scenario 3 — Full Project Brief (Paul's Run, AI-Judged)

## The Scenario

**Goal:** Give each model's Paul instance the full project brief and let the team build a complete product from start to finish.

Each Paul receives an identical brief — the same prompt, no cross-model visibility. Paul decomposes the brief into tasks, assigns them to agents, and the team delivers a complete, deployed product.

**This scenario is scored by AI.** Once all four models have submitted, each of the four models independently reviews all four submissions and scores them blind — no reviewer knows which model built which site.

**Success criteria:**
- The full application is deployed and live on GitHub Pages
- All required features from the brief are implemented and functional
- The site auto-deploys via GitHub Actions on every push to `main`
- All GitHub Issues and Pull Requests in the repo are closed

---

## The Prompt

The full brief delivered to each Paul instance is in [PROMPT.md](PROMPT.md). Every Paul received it identically, with no additional context about the other competitors.

**Project summary:** Build *Fizban's Wands* — a complete static e-commerce site for a whimsical magical wand shop inspired by Dragonlance. The site must include a wand catalog (36+ wands across 3 alignment categories), shopping cart, gold-balance checkout, order confirmation with a simulated receipt, and `localStorage` persistence. Built in React + Vite, auto-deployed to GitHub Pages via GitHub Actions.

---

## How It Was Run

Each model runs Scenario 3 in a Digiswarm session on its own dedicated repo, using the standard benchmark configuration.

**Platform:** [Digiswarm AI](https://digiswarm.ai) — default project configuration from [github.com/digiswarmai/skills](https://github.com/digiswarmai/skills)
**Plan:** Starter Plan (1 agent at a time, sequential execution)
**Agent team:** Paul (Liaison), Lucy (PM), John (Frontend), George (Middleware), Ringo (Backend)

**Pre-run setup (completed before each session):**
1. Create the model's submission repo on GitHub under `cindy-pi`
2. Initialize with a LICENSE — no source files pre-populated
3. Go to **Settings → Pages → Build and deployment → Source** and select **GitHub Actions**
4. Generate a scoped GitHub token for the session (see [setup/GITHUB_SETUP.md](../setup/GITHUB_SETUP.md))
5. Configure the Digiswarm controller: set the model, add the API key and GitHub token, set the target repo

Full setup procedure and session log template: [setup/SESSION_SETUP.md](../setup/SESSION_SETUP.md)
Required repo configuration: [setup/REPO_SETUP.md](../setup/REPO_SETUP.md)

**Timing:** Build time is measured from when the first issue with label `scenario3-start` is created in the submission repo to when the last issue with label `scenario3-end` is closed.

---

## Scoring

Scenario 3 is scored by AI in a blind peer review. Each of the four models independently reviews all four submissions without knowing which model built which site.

| Dimension | Description |
|---|---|
| **Originality** | Is the design fresh and creative, or generic and predictable? |
| **Quality** | Is the implementation solid, complete, and functionally correct? |
| **Elegance** | Is the UI polished, cohesive, and pleasant to use? |

Each dimension is scored 1–100. The four reviewer scores are averaged into the final site score. Full methodology: [SCORING.md](SCORING.md).

---

## Results

> Results will be published here once all four models have completed Scenario 3.

| Model | Build Time | Token Cost | Originality | Quality | Elegance | **Final Score** |
|---|---|---|---|---|---|---|
| Anthropic Claude | TBD | TBD | TBD | TBD | TBD | **TBD** |
| GPT | TBD | TBD | TBD | TBD | TBD | **TBD** |
| DeepSeek | TBD | TBD | TBD | TBD | TBD | **TBD** |
| Qwen3-Code | TBD | TBD | TBD | TBD | TBD | **TBD** |
