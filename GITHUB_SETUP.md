# GitHub Setup Guide

This document is for anyone running or replicating this benchmark. It covers exactly what GitHub token permissions are required for each model's session, why each permission is needed, and how to generate the token correctly.

---

## Token Type — Classic PAT

Use a **Classic Personal Access Token**. It covers everything the agent needs with just two scope selections and is the simplest option to set up.

---

## How to Create the Token

1. Go to **GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)**
2. Click **Generate new token (classic)**
3. Set a **Note** that identifies the run — e.g. `digiswarm-anthropic-run`
4. Set an **Expiration** — 30 days is a safe choice; enough time to complete the run with buffer
5. Select the two scopes below
6. Click **Generate token** and save it immediately — GitHub will not show it again

---

## Required Scopes

Only two scopes are needed:

| Scope | Why It's Needed |
|---|---|
| **`repo`** (full) | Covers everything in the submission repo — pushing code, reading/writing branches, Issues, Pull Requests, deployments, Pages configuration, secrets, variables, and environments |
| **`workflow`** | Allows the agent to create and modify `.github/workflows/` files — required to set up the GitHub Actions CI/CD pipeline that deploys to GitHub Pages |

Check both boxes and nothing else.

---

## What `repo` Covers

Selecting `repo` grants access to all of the following for any repo the token can see:

- Code — push commits, create and delete branches, read contents
- Issues — create, comment on, and close issues
- Pull Requests — open, review, merge, and close PRs
- Deployments — create and manage deployments (used by GitHub Pages)
- Pages — enable GitHub Pages and configure the Pages source
- Environments — manage deployment environments (e.g. the `github-pages` environment)
- Secrets — add and manage repository secrets
- Variables — add and manage repository variables
- Commit statuses — report pass/fail status on commits

---

## Security Recommendations

- **One token per run.** Generate a separate token for each model's repo. If a token is ever exposed, it only affects one submission.
- **Set an expiration.** 30 days is practical; revoke manually once the run is done.
- **Never commit the token.** Add it to the Digiswarm controller only — it should never appear in the repo, `.env` files, or any logs.
- **Revoke after the run.** Once the site is live and all Issues and PRs are closed, revoke the token under GitHub → Settings → Developer Settings → Personal Access Tokens. The GitHub Pages site stays live without it.

---

## Verifying the Token Works

After generating the token, run a quick check with the GitHub CLI before handing it to the Digiswarm controller:

```bash
# Set the token temporarily
export GITHUB_TOKEN=your_token_here

# Confirm it can see the repo
gh repo view cindy-pi/ai-storefront-anthropic

# Confirm it can see Actions
gh run list --repo cindy-pi/ai-storefront-anthropic
```

Both commands should return results without a permissions error.

---

## One-Page Summary

> **Token type:** Classic PAT
>
> **Scopes needed:** `repo` (full) + `workflow`
>
> **Expiration:** 30 days
>
> **One token per repo. Revoke after the run.**
