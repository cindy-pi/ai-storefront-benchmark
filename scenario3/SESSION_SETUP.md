# Session Setup — Scenario 3 Run Configuration

This document defines the exact steps followed for each model's Scenario 3 benchmark run. The process is identical across all four runs. **The only thing that changes between runs is the model selected in the Digiswarm controller.**

This standardization is a core part of the methodology — it ensures that differences in output reflect model capability, not differences in tooling, context, agent skills, or prompt delivery.

---

## Why Digiswarm AI

[Digiswarm AI](https://digiswarm.ai) was chosen as the orchestration platform specifically because it allows the underlying model to be swapped without changing anything else. The agent framework, tool access, project context, and skill set remain constant across all four runs. This makes the comparison as close to apples-to-apples as possible and removes platform bias as a confounding variable.

## Plan Tier and Agent Concurrency

This benchmark runs on the **Digiswarm Starter Plan**, which supports **1 agent running at a time**. Each model session has 4 agents configured, but they execute sequentially — one finishes before the next begins. This means build time measurements reflect sequential single-agent execution, not parallelized work.

Digiswarm's higher-tier plans support up to 5 agents running in parallel, which would significantly reduce wall-clock build time. That tradeoff — plan cost vs. speed — is an interesting variable on its own and will be explored in a follow-up paper. For this benchmark, all four model runs use the same Starter Plan to keep the agent concurrency constraint identical across competitors.

---

## What Changes Per Run

| Setting | Anthropic Run | GPT Run | DeepSeek Run | Qwen3 Run |
|---|---|---|---|---|
| Model | Claude (Anthropic) | GPT | DeepSeek | Qwen3-Code |
| Model API Key | Anthropic key | OpenAI key | DeepSeek key | N/A (local) |
| GitHub Token | Scoped to `ai-storefront-anthropic` | Scoped to `ai-storefront-gpt` | Scoped to `ai-storefront-deepseek` | Scoped to `ai-storefront-qwen3` |
| Target Repo | `cindy-pi/ai-storefront-anthropic` | `cindy-pi/ai-storefront-gpt` | `cindy-pi/ai-storefront-deepseek` | `cindy-pi/ai-storefront-qwen3` |

## What Stays the Same Per Run

| Setting | Value |
|---|---|
| Digiswarm Project | `digiswarm` (default) |
| Agent Context | Identical — same skills, tools, and knowledge |
| Prompt Delivered to Paul | Identical — see [PROMPT.md](PROMPT.md) |
| Repo Setup Requirements | Identical — see [REPO_SETUP.md](../REPO_SETUP.md) |
| Timing Start | Moment the prompt is submitted to Paul |
| Timing End | First successful `npm run build` confirmed in session |

---

## Pre-Run Checklist (Complete Before Each Session)

### Step 1 — Create the GitHub Repo and Enable GitHub Pages

- [ ] Create the repo on GitHub under `cindy-pi` (e.g. `ai-storefront-anthropic`)
- [ ] Initialize with a LICENSE (MIT recommended)
- [ ] Do **not** pre-populate with any source files — Paul's agents build from scratch
- [ ] Enable Issues (optional, for session notes)
- [ ] Go to **Settings → Pages** in the new repo
- [ ] Under **Build and deployment → Source**, select **GitHub Actions**
- [ ] Save

> **Why this must be done before the run:** The GitHub Actions deploy workflow the AI generates uses `actions/deploy-pages`, which only works when the Pages source is set to "GitHub Actions." If the source is left on the default ("Deploy from a branch"), the workflow will appear to run but will silently fail to publish the site. This is a one-time manual UI step — it cannot be set by the AI via code commits alone.

### Step 2 — Generate a Fresh Model API Key

- [ ] Create a **new, dedicated API key** for this run in the model provider's console
- [ ] This key is used only for this benchmark run — it provides a clean cost baseline with no prior usage
- [ ] Record the key's starting balance or spend baseline in the session log

### Step 3 — Generate a GitHub Token

See [GITHUB_SETUP.md](../GITHUB_SETUP.md) for the full token setup guide.

- [ ] Go to GitHub → Settings → Developer Settings → Personal Access Tokens
- [ ] Generate a **Classic PAT** with `repo` (full) and `workflow` scopes
- [ ] Set an expiration appropriate for the run duration

### Step 4 — Configure the Digiswarm Controller

- [ ] Open the [Digiswarm AI](https://digiswarm.ai) controller
- [ ] Select project: **`digiswarm`** (the default project — do not create a custom project)
- [ ] Set the model to the one for this run
- [ ] Add the model API key to the controller credentials
- [ ] Add the GitHub token to the controller credentials
- [ ] Set the target repo URL (e.g. `https://github.com/cindy-pi/ai-storefront-anthropic`)
- [ ] Verify the controller shows the correct model, token, and repo before proceeding

### Step 5 — Deliver the Prompt and Start Timing

- [ ] Record the session start timestamp (wall clock)
- [ ] Submit the prompt from [PROMPT.md](PROMPT.md) to Paul — deliver it exactly as written, no additions or clarifications
- [ ] Do not interact with Paul during the session unless the agent is completely stuck (log any intervention)

### Step 6 — End the Session

- [ ] Record the session end timestamp when a successful `npm run build` is confirmed
- [ ] Verify the GitHub Actions workflow has deployed the site to GitHub Pages
- [ ] Pull the final token usage / API cost from the model provider console
- [ ] Save the session log (see template below)

---

## Session Log Template

Create a file called `session-log.md` in each submission repo at the end of the run. Fill in all fields.

```markdown
# Session Log — [Model Name]

## Run Info
- **Model:** 
- **Digiswarm Project:** digiswarm (default)
- **Target Repo:** https://github.com/cindy-pi/[repo-name]
- **Live Site:** https://cindy-pi.github.io/[repo-name]/

## Timing
- **Session Start:** YYYY-MM-DD HH:MM (timezone)
- **Session End:** YYYY-MM-DD HH:MM (timezone)
- **Total Build Time:** X hours Y minutes

## Token / Cost
- **API Key Created:** YYYY-MM-DD
- **Total Tokens Used:** 
- **Total Cost (USD):** 
- **Cost Notes:** (e.g. cache hits, batch discounts, local compute estimate)

## Session Notes
- Any interventions made (if none, write "None")
- Anything unexpected that happened during the run
- Any manual corrections required after the session

## Scoring (filled in after blind review)
- **Originality:** TBD
- **Quality:** TBD
- **Elegance:** TBD
- **Final Score:** TBD
```

---

## Intervention Policy

The goal is fully autonomous execution. However, if Paul's agents become completely blocked (e.g. a tool failure, an unrecoverable error state), a minimal unblocking intervention is allowed under these conditions:

- The intervention must be logged in the session log with the exact time and what was done
- The intervention must be limited to unblocking — no guidance on implementation choices
- The clock keeps running through any intervention

If an intervention meaningfully influenced the output, note it in the final paper.
