# Scenario 2 — CI/CD Pipeline with `/dev` and `/prod` Environments

## The Scenario

**Goal:** Extend the repository with an automated CI/CD pipeline that deploys to two separate paths — `/dev` for staging and `/prod` for production — both driven entirely from the `main` branch, with a GitHub issue-based promotion gate between them.

The agent must implement two GitHub Actions workflows: one that auto-deploys to `/dev` on every push to `main`, and one that deploys to `/prod` when a GitHub issue labeled `promote-to-prod` is created. This gives a controlled promotion path — `/dev` gets every commit, `/prod` only gets promoted builds. All workflow files and configuration end up committed to `main`.

**Success criteria:**
- Two GitHub Actions workflows exist in the repository on `main`
- Pushing to `main` automatically deploys to `/dev`
- Creating a GitHub issue with the label `promote-to-prod` triggers a deploy to `/prod`
- Both environments deploy independently
- The webpage is accessible at both `/dev` and `/prod` paths on the repo's GitHub Pages URL

---

## The Prompt

Each Paul instance receives the following prompt for this scenario, with the repo name substituted for their model:

> I have a GitHub repo at `cindy-pi/ai-storefront-[model]` with a Hello World page already deployed to GitHub Pages via a `deploy-pages.yml` workflow on `main`. I want you to set up a CI/CD pipeline that deploys to two independent environments — `/dev` and `/prod` — both driven from `main`. Every push to `main` should automatically deploy to `/dev`. When `/dev` is verified and ready to promote, creating a GitHub issue with the label `promote-to-prod` should automatically trigger a deployment to `/prod`. Use a `gh-pages` branch as the Pages source. All workflow files should be committed to `main`. Create all the GitHub issues, assign your agents, and see the work through to completion without asking me questions. The session is complete when both URLs are live and the promote workflow has been successfully triggered at least once.

**Why this wording works:**
- Names the repo explicitly — the agent doesn't have to discover it
- Describes the existing Pages setup — no need to read or reason about what's already deployed
- Specifies the `gh-pages` branch strategy and both trigger mechanisms upfront — eliminates latency from the agent reasoning to those decisions
- Issue-label promotion gate mirrors how agents already work — they create and label issues naturally
- Both environments driven from `main` — no permanent `dev` branch, clean final state
- "See it through to completion" signals that the agent should monitor and unblock downstream issues, not just create them

---

## How It Was Run

Each model runs Scenario 2 in a Digiswarm session continuing from the same repo used in Scenario 1, using the standard benchmark configuration.

**Platform:** [Digiswarm AI](https://digiswarm.ai) — default project configuration from [github.com/digiswarmai/skills](https://github.com/digiswarmai/skills)
**Plan:** Starter Plan (1 agent at a time, sequential execution)
**Agent team:** Paul (Liaison), Lucy (PM), John (Frontend), George (Middleware), Ringo (Backend)

**Pre-run setup (completed before each session):**

Run the pre-flight script first — it checks all of the below automatically and reports what needs fixing:

```bash
# Run from the ai-storefront-benchmark repo root
python setup/preflight.py --token ghp_xxx --repo cindy-pi/ai-storefront-[model] --scenario 2
```

The following items require human/admin action and cannot be performed by the agent via code commits alone:

1. **Confirm Scenario 1 is complete** — the Hello World page must be live at the model's GitHub Pages URL before Scenario 2 begins
2. **Set default branch to `main`**
   Go to **Settings → General → Default branch** → click the pencil → select `main` → Update
3. **Enable GitHub Actions write permissions**
   Go to **Settings → Actions → General → Workflow permissions** and select **"Read and write permissions"**
   Without this, `git push` inside workflows fails silently — the most common failure point for this scenario
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
