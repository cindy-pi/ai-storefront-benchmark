# Judging — AI Peer Review Setup

## Overview

Once all four models have completed the three scenarios, the results are scored by AI in a blind peer review. A separate Digiswarm project called **judges** is used for this — it has four agents, each running a different model, each acting as an independent judge.

No judge is told which model built which submission. All four judges review all four submissions independently and write their analysis to their own directory in this repo.

---

## The Judges Project

### Agent → Model Assignment

| Agent | Model | Analysis Directory |
|---|---|---|
| **Lucy** | Anthropic Claude | [judging/lucy/](lucy/) |
| **John** | GPT | [judging/john/](john/) |
| **George** | DeepSeek | [judging/george/](george/) |
| **Ringo** | Qwen3-Code | [judging/ringo/](ringo/) |

**Paul** (Liaison) orchestrates the judging sessions — Paul's model can be any cloud model. Paul receives each judging prompt, assigns the task to all four judges, and confirms all findings are written before closing the session.

### Digiswarm Project Setup

1. Open the [Digiswarm AI](https://digiswarm.ai) controller
2. Create a new project — name it **`judges`**
3. Assign each agent their model (see table above)
4. Set the target repo to: `https://github.com/cindy-pi/ai-storefront-benchmark`
5. Add a GitHub token with write access to `ai-storefront-benchmark` (see [setup/GITHUB_SETUP.md](../setup/GITHUB_SETUP.md))
6. Do **not** use the default `digiswarm` project — create a dedicated `judges` project so model assignments are persistent across all three judging sessions

### What the Judges Have Access To

The judges project points to this repo (`ai-storefront-benchmark`). The agents can read the scenario READMEs for live URLs and submission details, and they write their analysis back to their own directories in `judging/`.

The judges do **not** have write access to the competitor repos (`ai-storefront-anthropic`, `ai-storefront-gpt`, etc.) — read-only access via public GitHub Pages URLs is sufficient.

---

## Scoring

All scores are **1–100** (1 = poor, 100 = excellent).

For **Scenarios 1 and 2**, each judge gives a single overall score per submission plus written notes.

For **Scenario 3**, each judge scores three dimensions per submission:

| Dimension | Description |
|---|---|
| **Originality** | Is the design fresh and creative, or generic and predictable? |
| **Quality** | Is the implementation solid, complete, and functionally correct? |
| **Elegance** | Is the UI polished, cohesive, and pleasant to use? |

The final site score for Scenario 3 is the average of all four judges' averaged dimension scores. Full methodology is in [scenario3/SCORING.md](../scenario3/SCORING.md).

---

## The Judging Prompts

Three prompts are delivered to Paul in sequence — one per scenario. Deliver each prompt only after the previous scenario's judging session is complete.

---

### Judging Prompt 1 — Scenario 1 (Hello World)

> All four models have completed Scenario 1. Each attempted to deploy a Hello World webpage to their GitHub Pages URL.
>
> Your task is to coordinate a blind peer review of the four submissions. Do not tell any judge which model built which submission — refer to them only as Submission A, B, C, and D.
>
> The live URLs for each submission are listed in [scenario1/README.md](../scenario1/README.md). Map them to Submission A–D before beginning.
>
> Each judge (Lucy, John, George, Ringo) must independently review all four submissions and score each one 1–100 using the following criteria:
>
> | Score | Criteria |
> |---|---|
> | 90–100 | Page is live, loads correctly, renders well, and the GitHub Actions workflow is clean and correct |
> | 70–89 | Page is live and functional with minor workflow or implementation issues |
> | 50–69 | Page is partially live or has notable problems |
> | 30–49 | Page is inconsistently accessible or has significant issues |
> | 1–29 | Submission failed to deploy or the page is not live |
>
> Each judge must write their scores and analysis to their directory:
> - Lucy → `judging/lucy/README.md`
> - John → `judging/john/README.md`
> - George → `judging/george/README.md`
> - Ringo → `judging/ringo/README.md`
>
> Judges must not share or read each other's analysis until all four have committed their findings. Work independently.
>
> The session is complete when all four judges have written and committed their Scenario 1 findings.

---

### Judging Prompt 2 — Scenario 2 (CI/CD Pipeline)

> All four models have completed Scenario 2. Each attempted to implement a CI/CD pipeline deploying to `/dev` and `/prod` paths on GitHub Pages.
>
> Your task is to coordinate a blind peer review. Use the same Submission A–D mapping from Scenario 1 so the blind is consistent across all three judging sessions.
>
> The live `/dev` and `/prod` URLs for each submission are listed in [scenario2/README.md](../scenario2/README.md).
>
> Each judge (Lucy, John, George, Ringo) must independently review all four submissions and score each one 1–100 using the following criteria:
>
> | Score | Criteria |
> |---|---|
> | 90–100 | Both `/dev` and `/prod` are live; environments deploy independently; workflow is well-structured and correct |
> | 70–89 | Both environments are live with minor issues in the workflow or independence |
> | 50–69 | One environment works reliably; the other has problems |
> | 30–49 | Both environments have significant issues or the CI/CD logic is broken |
> | 1–29 | Submission failed to implement the pipeline or neither environment is live |
>
> Each judge must add their Scenario 2 scores and analysis to their existing directory file:
> - Lucy → `judging/lucy/README.md`
> - John → `judging/john/README.md`
> - George → `judging/george/README.md`
> - Ringo → `judging/ringo/README.md`
>
> Judges must work independently. The session is complete when all four judges have committed their Scenario 2 findings.

---

### Judging Prompt 3 — Scenario 3 (Full Project)

> All four models have completed Scenario 3. Each built a complete static e-commerce site called Fizban's Wands and deployed it to GitHub Pages.
>
> Your task is to coordinate a blind peer review. Use the same Submission A–D mapping from the previous scenarios.
>
> The live site URLs for each submission are listed in [scenario3/README.md](../scenario3/README.md).
>
> Each judge (Lucy, John, George, Ringo) must independently review all four sites and score each one across three dimensions (1–100 each):
>
> - **Originality** — Is the design fresh and creative, or generic and predictable?
> - **Quality** — Is the implementation solid, complete, and functionally correct?
> - **Elegance** — Is the UI polished, cohesive, and pleasant to use?
>
> Full scoring rubric: [scenario3/SCORING.md](../scenario3/SCORING.md)
>
> Each judge must add their Scenario 3 scores and analysis to their existing directory file:
> - Lucy → `judging/lucy/README.md`
> - John → `judging/john/README.md`
> - George → `judging/george/README.md`
> - Ringo → `judging/ringo/README.md`
>
> Judges must work independently. The session is complete when all four judges have committed their Scenario 3 findings.

---

## How Final Scores Are Calculated

**Scenarios 1 and 2:** The four judges' scores for each submission are averaged into a single final score per submission.

**Scenario 3:** Each judge averages their three dimension scores (Originality + Quality + Elegance / 3) into a site score. The four site scores are then averaged into the final score. See [scenario3/SCORING.md](../scenario3/SCORING.md) for the full formula.

Results are published in each scenario's README once all four judges have submitted.
