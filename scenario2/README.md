# Scenario 2 — CI/CD Pipeline with `/dev` and `/prod` Environments

## The Scenario

**Goal:** Extend the repository with an automated CI/CD pipeline that deploys to two separate paths — `/dev` for the staging environment and `/prod` for production.

The agent must design and implement a GitHub Actions workflow that deploys to different paths based on branch or trigger, making the site accessible at both a `/dev` and a `/prod` URL on GitHub Pages.

**Success criteria:**
- A working GitHub Actions workflow exists in the repository
- Pushing to the designated branch triggers an automated deploy
- The webpage is accessible at both `/dev` and `/prod` paths on the repo's GitHub Pages URL
- Both environments deploy independently — a push to one does not affect the other

---

## The Prompt

Each Paul instance received the following prompt for this scenario:

> Extend this repository's deployment with a CI/CD pipeline that publishes to two separate environments on GitHub Pages.
>
> Requirements:
> - The site must be accessible at both a `/dev` path and a `/prod` path on this repo's GitHub Pages URL
> - The `/dev` environment must deploy automatically when commits are pushed to the `dev` branch
> - The `/prod` environment must deploy automatically when commits are pushed to `main`
> - Both pipelines must run via GitHub Actions
> - Both environments must deploy independently — a push to `dev` must not affect `/prod`, and vice versa
> - The existing Hello World page from Scenario 1 can serve as the content for both environments
>
> The session is complete when both `/dev` and `/prod` paths are live and accessible in a browser. Do not ask for clarification — make all decisions independently.

---

## How It Was Run

Each model runs Scenario 2 in a Digiswarm session continuing from the same repo used in Scenario 1, using the standard benchmark configuration.

**Platform:** [Digiswarm AI](https://digiswarm.ai) — default project configuration from [github.com/digiswarmai/skills](https://github.com/digiswarmai/skills)
**Plan:** Starter Plan (1 agent at a time, sequential execution)
**Agent team:** Paul (Liaison), Lucy (PM), John (Frontend), George (Middleware), Ringo (Backend)

**Pre-run setup (completed before each session):**
1. Confirm Scenario 1 is complete — live page must be accessible before Scenario 2 begins
2. Generate a fresh GitHub token scoped to the same submission repo (see [setup/GITHUB_SETUP.md](../setup/GITHUB_SETUP.md))
3. Configure the Digiswarm controller with the same model, updated token, and same target repo

**Timing:** Build time is measured from when the first issue with label `scenario2-start` is created in the submission repo to when the last issue with label `scenario2-end` is closed.

---

## Results

> Results will be published here once all four models have completed Scenario 2.

| Model | Build Time | Token Cost | `/dev` URL | `/prod` URL | Status |
|---|---|---|---|---|---|
| Anthropic Claude | TBD | TBD | TBD | TBD | TBD |
| GPT | TBD | TBD | TBD | TBD | TBD |
| DeepSeek | TBD | TBD | TBD | TBD | TBD |
| Qwen3-Code | TBD | TBD | TBD | TBD | TBD |
