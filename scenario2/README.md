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

Each Paul instance receives the following prompt for this scenario, with the repo name substituted for their model:

> I have a GitHub repo at `cindy-pi/ai-storefront-[model]` with a Hello World page already deployed to GitHub Pages via a `deploy-pages.yml` workflow on `main`. I want you to set up a CI/CD pipeline that deploys to two independent environments — `/dev` and `/prod` — on GitHub Pages. A push to `dev` should update `/dev` only, and a push to `main` should update `/prod` only. Both should run via GitHub Actions. Use a `gh-pages` branch as the Pages source. Create all the GitHub issues, assign your agents, and see the work through to completion without asking me questions. The session is complete when both URLs are live.

**Why this wording works:**
- Names the repo explicitly — the agent doesn't have to discover it
- Describes the existing Pages setup — no need to read or reason about what's already deployed
- Specifies the `gh-pages` branch strategy upfront — eliminates latency from the agent reasoning to that decision
- "See it through to completion" signals that the agent should monitor and unblock downstream issues, not just create them

---

## How It Was Run

Each model runs Scenario 2 in a Digiswarm session continuing from the same repo used in Scenario 1, using the standard benchmark configuration.

**Platform:** [Digiswarm AI](https://digiswarm.ai) — default project configuration from [github.com/digiswarmai/skills](https://github.com/digiswarmai/skills)
**Plan:** Starter Plan (1 agent at a time, sequential execution)
**Agent team:** Paul (Liaison), Lucy (PM), John (Frontend), George (Middleware), Ringo (Backend)

**Pre-run setup (completed before each session):**

These steps require human/admin action and cannot be performed by the agent via code commits alone.

1. **Confirm Scenario 1 is complete** — the Hello World page must be live at the model's GitHub Pages URL before Scenario 2 begins
2. **Enable GitHub Actions write permissions**
   Go to **Settings → Actions → General → Workflow permissions** and select **"Read and write permissions"**
   Without this, `git push` inside workflows fails silently — the most common failure point for this scenario
3. **Create the `dev` branch** from `main` — the CI/CD workflow triggers on push to `dev`; if the branch doesn't exist, the trigger never fires
4. **Confirm `GITHUB_TOKEN` can push to `gh-pages`** — verify no branch protection rules are set on `gh-pages` that would block the workflow from pushing to it
5. **Generate a fresh GitHub token** scoped to the submission repo (see [setup/GITHUB_SETUP.md](../setup/GITHUB_SETUP.md))
6. **Configure the Digiswarm controller** with the same model, updated token, and same target repo

> **Note on GitHub Pages source:** This scenario switches from the "GitHub Actions" Pages source used in Scenario 1 to a `gh-pages` branch source. The agent handles this via the GitHub API, but the `gh-pages` branch must be created by the first workflow run before the Pages source can be pointed at it. The agent manages this ordering — no manual Pages source change is needed before the session.

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
