# AI Storefront Benchmark — Final Results

This document summarises the complete results of the AI Storefront Benchmark: two scenarios, four models, four independent judges, and the API cost incurred per model.

---

## Blind Mapping

All judging was conducted blind. Submissions were labeled A–D with model identity withheld from all judges until scoring was complete.

| Label | Model |
|-------|-------|
| **A** | Anthropic Claude |
| **B** | GPT |
| **C** | DeepSeek |
| **D** | Qwen3-Code |

---

## Scenario 1 — Hello World

Each judge scored each submission 1–100. Final scores are the mean of all four judges.

### Individual Judge Scores

| Submission | Lucy (Claude) | John (GPT) | George (DeepSeek) | Ringo (Qwen3) | **Final Avg** |
|------------|:---:|:---:|:---:|:---:|:---:|
| A — Anthropic Claude | 95 | 96 | 94 | 92 | **94.25** |
| B — GPT | 88 | 94 | 91 | 95 | **92.00** |
| C — DeepSeek | 72 | 88 | 84 | 88 | **83.00** |
| D — Qwen3-Code | 52 | 62 | 62 | 90 | **66.50** |

### Scenario 1 Rankings

| Rank | Model | Score |
|------|-------|-------|
| 1 | Anthropic Claude | 94.25 |
| 2 | GPT | 92.00 |
| 3 | DeepSeek | 83.00 |
| 4 | Qwen3-Code | 66.50 |

---

## Scenario 2 — Full Project (Fizban's Wands)

Each judge scored three dimensions (Originality, Quality, Elegance) per submission. A judge's site score is the mean of their three dimension scores. The final score is the mean of all four judges' site scores.

### Individual Judge Scores — Originality

| Submission | Lucy | John | George | Ringo |
|------------|:---:|:---:|:---:|:---:|
| A — Anthropic Claude | 91 | 88 | 90 | 82 |
| B — GPT | 89 | 86 | 85 | 85 |
| C — DeepSeek | 76 | 79 | 75 | 78 |
| D — Qwen3-Code | 67 | 38 | 35 | 35 |

### Individual Judge Scores — Quality

| Submission | Lucy | John | George | Ringo |
|------------|:---:|:---:|:---:|:---:|
| A — Anthropic Claude | 95 | 94 | 92 | 96 |
| B — GPT | 90 | 88 | 93 | 90 |
| C — DeepSeek | 72 | 82 | 82 | 82 |
| D — Qwen3-Code | 55 | 50 | 55 | 52 |

### Individual Judge Scores — Elegance

| Submission | Lucy | John | George | Ringo |
|------------|:---:|:---:|:---:|:---:|
| A — Anthropic Claude | 93 | 91 | 90 | 90 |
| B — GPT | 90 | 87 | 91 | 88 |
| C — DeepSeek | 70 | 80 | 78 | 80 |
| D — Qwen3-Code | 52 | 45 | 40 | 48 |

### Per-Judge Site Scores (mean of Originality + Quality + Elegance)

| Submission | Lucy | John | George | Ringo | **Final Avg** |
|------------|:---:|:---:|:---:|:---:|:---:|
| A — Anthropic Claude | 93.00 | 91.00 | 90.67 | 89.33 | **91.00** |
| B — GPT | 89.67 | 87.00 | 89.67 | 87.67 | **88.50** |
| C — DeepSeek | 72.67 | 80.33 | 78.33 | 80.00 | **77.83** |
| D — Qwen3-Code | 58.00 | 44.33 | 43.33 | 45.00 | **47.67** |

### Scenario 2 Rankings

| Rank | Model | Score |
|------|-------|-------|
| 1 | Anthropic Claude | 91.00 |
| 2 | GPT | 88.50 |
| 3 | DeepSeek | 77.83 |
| 4 | Qwen3-Code | 47.67 |

---

## API Cost

Cost incurred per model per scenario to produce all work (implementation + judging rounds).

| Model | Scenario 1 Cost | Scenario 2 Cost | Total |
|-------|:--------------:|:--------------:|:-----:|
| Anthropic Claude | $2.38 | $13.91 | **$16.29** |
| GPT | $1.24 | $10.56 | **$11.80** |
| DeepSeek | $0.01 | $0.09 | **$0.10** |
| Qwen3-Code | $0.00 | $0.00 | **$0.00** |

---

## Score vs Cost Analysis

A higher value ratio indicates more benchmark performance per dollar spent.

| Model | Scenario 1 Score | Scenario 2 Score | Total Cost | S1 Score/$ | S2 Score/$ | Notes |
|-------|:---:|:---:|:---:|:---:|:---:|-------|
| Anthropic Claude | 94.25 | 91.00 | $16.29 | 5.8 | 5.6 | Top scores in both scenarios; highest cost |
| GPT | 92.00 | 88.50 | $11.80 | 7.4 | 7.5 | Strong scores; notably lower cost than Claude |
| DeepSeek | 83.00 | 77.83 | $0.10 | 830 | 778 | Solid mid-tier scores at near-zero cost |
| Qwen3-Code | 66.50 | 47.67 | $0.00 | — | — | Lowest scores; free to run |

> **Note:** Score/$ ratios for DeepSeek are very high because the cost approaches zero. Qwen3-Code had no measurable cost, so a ratio is not defined. These ratios should be read as directional indicators rather than precise value metrics.

---

## Summary

- **Best overall performer:** Anthropic Claude (94.25 / 91.00)
- **Best value (cost-adjusted):** DeepSeek — competitive scores at a fraction of the cost of the frontier models
- **Most affordable frontier result:** GPT — second place in both scenarios at ~$12 total
- **Lowest cost:** Qwen3-Code ($0.00) — but also lowest scores in both scenarios

Full judge analysis is in [judging/](judging/).
