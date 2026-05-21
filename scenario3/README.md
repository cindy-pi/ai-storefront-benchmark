# Scenario 3 — Full Project Brief (Paul's Run, AI-Judged)

## The Scenario

**Goal:** Give each model's Paul instance the full project brief and let the team build a complete product from start to finish.

Each Paul receives an identical brief — the same prompt, no cross-model visibility. Paul decomposes the brief into tasks, assigns them to agents, and the team delivers a complete, deployed product.

**This scenario is scored by AI.** Once all four models have submitted, each of the four models independently reviews all four submissions and scores them blind — no reviewer knows which model built which site.

**Success criteria:**
- The full application is deployed and live on GitHub Pages
- All required features from the brief are implemented and functional
- The site auto-deploys via GitHub Actions on every push to `main`
- All GitHub Issues and Pull Requests in the repo are closed (the completion signal to the organizer)

---

## The Prompt

The full prompt delivered to each Paul instance is in [PROMPT.md](PROMPT.md).

Every Paul received this brief identically, with no additional context about the other competitors.

---

## How It Was Run

Each model runs Scenario 3 in a Digiswarm session on its own dedicated repo, using the standard benchmark configuration.

**Platform:** [Digiswarm AI](https://digiswarm.ai) — default project configuration from [github.com/digiswarmai/skills](https://github.com/digiswarmai/skills)
**Plan:** Starter Plan (1 agent at a time, sequential execution)
**Agent team:** Paul (Liaison), Lucy (PM), John (Frontend), George (Middleware), Ringo (Backend)

**Full setup procedure:** [SESSION_SETUP.md](SESSION_SETUP.md)
**Required repo configuration:** [REPO_SETUP.md](../REPO_SETUP.md)
**GitHub token setup:** [GITHUB_SETUP.md](../GITHUB_SETUP.md)

**Timing:** Starts when the prompt is submitted to Paul. Ends when the first successful `npm run build` is confirmed in the session.

---

## Scoring

Scenario 3 is scored across three dimensions: **Originality**, **Quality**, and **Elegance**. Each dimension is scored 1–100 by each of the four models in a blind review session.

Full scoring methodology and rubric: [SCORING.md](SCORING.md)

| Dimension | Description |
|---|---|
| **Originality** | Is the design fresh and creative, or generic and predictable? |
| **Quality** | Is the implementation solid, complete, and functionally correct? |
| **Elegance** | Is the UI polished, cohesive, and pleasant to use? |

---

## Results

> Results will be published here once all four models have completed Scenario 3.

| Model | Build Time | Token Cost | Originality | Quality | Elegance | **Final Score** |
|---|---|---|---|---|---|---|
| Anthropic Claude | TBD | TBD | TBD | TBD | TBD | **TBD** |
| GPT | TBD | TBD | TBD | TBD | TBD | **TBD** |
| DeepSeek | TBD | TBD | TBD | TBD | TBD | **TBD** |
| Qwen3-Code | TBD | TBD | TBD | TBD | TBD | **TBD** |
