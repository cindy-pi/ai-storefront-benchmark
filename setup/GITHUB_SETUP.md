# GitHub Setup Guide

This guide covers creating the target repo, enabling GitHub Pages, and generating a GitHub token for a benchmark run. The token is **fine-grained and scoped to a single repo**, so a leaked or expired token cannot affect any other repository.

---

## Recommended: Use the Setup Script

`github_setup.py` (in this directory) automates the repo creation, Pages configuration, and token generation in one guided flow.

**Prerequisites:** Python 3 + `pip install requests`

```powershell
cd ai-storefront-benchmark\setup
python github_setup.py --repo cindy-pi/ai-storefront-anthropic --scenario 2
```

The script will:

1. Use your existing admin token (from `GH_TOKEN`, `gh auth token`, or a prompt) to create the repo
2. Initialize it with a MIT LICENSE so the `main` branch exists immediately
3. Enable GitHub Pages with **GitHub Actions** as the source
4. Open your browser to the fine-grained token creation page with exact instructions
5. Accept the new token, validate it against all preflight checks, and print it for copying

### Re-validating a token without re-running setup

If you need to re-check a token you already have:

```powershell
python github_setup.py --repo cindy-pi/ai-storefront-anthropic --scenario 2 --token github_pat_xxx...
```

---

## Token Type — Fine-Grained PAT (Recommended)

Each run uses a **fine-grained Personal Access Token scoped to a single repository**. If the token is ever exposed, it cannot be used to access any other repo.

### Required Repository Permissions

When the script opens the token creation page, set these under **Permissions → Repository permissions**:

| Permission | Level |
|---|---|
| **Actions** | Read and write |
| **Contents** | Read and write |
| **Issues** | Read and write |
| **Metadata** | Read-only *(auto-selected, required)* |
| **Pages** | Read and write |
| **Pull requests** | Read and write |
| **Workflows** | Read and write |

Set **Repository access** to **Only select repositories** and choose only the target repo for this run.

### Why fine-grained over Classic PAT?

A Classic PAT with `repo` scope grants write access to **every repository you own**. A fine-grained token scoped to one repo means:

- A compromised token affects only that run's submission repo
- You can revoke per-run without touching other tokens
- The permission surface is exactly what the agent needs — nothing more

---

## Manual Setup (Fallback)

If you prefer not to use the script, follow these steps manually.

### 1 — Create the repo

- Go to GitHub and create a new public repo under `cindy-pi`
- Initialize with a **MIT License** (this creates the `main` branch)
- Do **not** add any other files — agents build from scratch

### 2 — Enable GitHub Pages

- Go to **Settings → Pages** in the new repo
- Under **Build and deployment → Source**, select **GitHub Actions**
- Save

> **Why this must be done before the run:** The deploy workflow uses `actions/deploy-pages`, which only publishes when the source is set to "GitHub Actions." If left on the default ("Deploy from a branch"), the workflow appears to succeed but the site never goes live.

### 3 — Generate a Fine-Grained Token

1. Go to **GitHub → Settings → Developer Settings → Personal Access Tokens → Fine-grained tokens**
2. Click **Generate new token**
3. Set a **Token name** — e.g. `ai-storefront-anthropic`
4. Set **Expiration** — 90 days is a safe default
5. Under **Resource owner**, select `cindy-pi`
6. Under **Repository access**, choose **Only select repositories** → select the target repo
7. Under **Permissions → Repository permissions**, set the seven permissions in the table above
8. Click **Generate token** and copy it immediately — it is shown only once

---

## Verifying the Token

Run `preflight.py` to confirm everything is configured correctly before starting the session:

```powershell
python preflight.py --token github_pat_xxx... --repo cindy-pi/ai-storefront-anthropic --scenario 2
```

Expected output: all checks **PASS**, with one **WARN** on the scope header (fine-grained tokens don't expose scopes in that header — this is expected and does not cause a failure).

---

## Security Recommendations

- **One token per repo.** Generate a separate token for each model's run — the script enforces this by design.
- **Set an expiration.** 90 days gives buffer; revoke manually once the run is complete.
- **Never commit the token.** Add it to the Digiswarm controller only — it must never appear in the repo, `.env` files, or any logs.
- **Revoke after the run.** Once the site is live and all Issues and PRs are closed, revoke the token under GitHub → Settings → Developer Settings → Personal Access Tokens. The GitHub Pages site stays live without it.
