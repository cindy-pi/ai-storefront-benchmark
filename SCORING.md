# Scoring Methodology

This document defines how the benchmark winner is determined across two categories: **operational metrics** and **site quality**.

---

## Category 1 — Operational Metrics (Objective)

These are recorded automatically during each model's build session.

| Metric | Description |
|---|---|
| **Build Time** | Wall-clock time from the moment the prompt is delivered to Paul until a passing `npm run build` is confirmed |
| **Token Cost** | Total API spend (USD) for cloud models; compute-equivalent cost estimate for the local Qwen3 model based on hardware cost amortization and inference time |

Operational metrics are informational — they do not feed into the final score that determines the winner. They provide context for understanding the cost/performance tradeoffs of each approach.

---

## Category 2 — Site Quality Score (Blind Peer Review)

This is the score that determines the winner.

### How It Works

Once all three sites are complete, each of the three competing models independently reviews **all three sites** — including its own — without being told which model built which site. This blind review eliminates bias and ensures the scoring reflects genuine quality assessment.

Each reviewer scores each site on three dimensions:

---

### Scoring Dimensions

#### Originality (1–100)
Does the design feel fresh, creative, and specific to the Fizban's Wands theme? Or does it feel generic, templated, or predictable?

| Score Range | Description |
|---|---|
| 90–100 | Exceptionally creative; distinctive visual identity; feels purpose-built |
| 70–89 | Clear creative effort; some memorable touches; generally non-generic |
| 50–69 | Functional and themed, but follows predictable patterns |
| 30–49 | Generic structure; minimal thematic effort |
| 1–29 | Could be any e-commerce site; no discernible creative intent |

#### Quality (1–100)
Is the implementation solid, complete, and functionally correct? Does it meet all the specified requirements?

| Score Range | Description |
|---|---|
| 90–100 | All features present and working; edge cases handled; clean, maintainable code |
| 70–89 | All major features present; minor gaps or rough edges |
| 50–69 | Core features work; some requirements missing or broken |
| 30–49 | Significant gaps; key features incomplete or non-functional |
| 1–29 | Fundamental functionality missing |

#### Elegance (1–100)
Is the UI polished, cohesive, and pleasant to use? Does it feel like something a real user would enjoy?

| Score Range | Description |
|---|---|
| 90–100 | Delightful UX; responsive; consistent visual language; no rough edges |
| 70–89 | Generally polished; a few minor inconsistencies or friction points |
| 50–69 | Functional and presentable; some visual roughness |
| 30–49 | Usable but visually unrefined; noticeable UX friction |
| 1–29 | Difficult or unpleasant to use; significant visual problems |

---

### Score Calculation

For each model's site:

```
Site Score (per reviewer) = (Originality + Quality + Elegance) / 3

Final Site Score = Average of all three reviewer Site Scores
```

The model with the **highest Final Site Score** wins the benchmark.

---

### Tie-Breaking

In the event of a tie in Final Site Score (within 0.5 points):

1. The site with the higher **Quality** sub-score wins
2. If still tied, the site with the faster **Build Time** wins

---

### Review Process

- Each [Digiswarm AI](https://digiswarm.ai) Paul instance conducts the review independently in a fresh session with no prior context
- The reviewer is shown each site (screenshots or live URLs) and asked to score it using the rubric above
- The reviewer is not told which model built which site
- Raw scores from each reviewer session are logged in the respective model's repo under `review/`

---

## Summary

| | Determines Winner? | Recorded |
|---|---|---|
| Build Time | No (informational) | Yes |
| Token Cost | No (informational) | Yes |
| Originality | Yes | Yes |
| Quality | Yes | Yes |
| Elegance | Yes | Yes |
| **Final Site Score** | **Yes — primary ranking** | Yes |
