#!/usr/bin/env python3
"""
preflight.py — GitHub setup verification for AI Storefront Benchmark.

Checks that the target repo and token meet all requirements for the
specified scenario before starting a Digiswarm session. Run this before
delivering the prompt to Paul.

Usage:
    python preflight.py --token ghp_xxx --repo cindy-pi/ai-storefront-anthropic --scenario 2

Requirements:
    pip install requests
"""

import argparse
import sys

try:
    import requests
except ImportError:
    print("Error: 'requests' is not installed.  Run: pip install requests")
    sys.exit(1)

API = "https://api.github.com"

# ANSI colours — work in Windows Terminal, macOS Terminal, and most Linux terminals.
# Pass --no-color to disable if your terminal doesn't support them.
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

_color = True  # toggled by --no-color

def _c(code):
    return code if _color else ""

# Running counters
_passes = 0
_warns  = 0
_fails  = 0


def ok(msg):
    global _passes
    _passes += 1
    print(f"  {_c(GREEN)}PASS{_c(RESET)}  {msg}")


def warn(msg, fix=None):
    global _warns
    _warns += 1
    print(f"  {_c(YELLOW)}WARN{_c(RESET)}  {msg}")
    if fix:
        print(f"         → {fix}")


def fail(msg, fix=None):
    global _fails
    _fails += 1
    print(f"  {_c(RED)}FAIL{_c(RESET)}  {msg}")
    if fix:
        print(f"         → {fix}")


def gh(path, token):
    """GET from the GitHub REST API with the provided token."""
    return requests.get(
        f"{API}{path}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        timeout=10,
    )


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_token(token):
    """Validate the token and confirm it has the required scopes."""
    print(f"\n{_c(BOLD)}Token{_c(RESET)}")

    try:
        resp = gh("/", token)
    except requests.exceptions.ConnectionError:
        fail("Could not reach api.github.com — check your internet connection")
        return False

    if resp.status_code == 401:
        fail(
            "Token is invalid or expired",
            "Generate a new Classic PAT at GitHub → Settings → Developer Settings → Personal Access Tokens",
        )
        return False

    ok("Token is accepted by GitHub")

    # Classic PATs return scopes in a header; fine-grained tokens do not.
    raw_scopes = resp.headers.get("X-OAuth-Scopes", "")
    if not raw_scopes:
        warn(
            "Could not read token scopes — this may be a fine-grained token",
            "The benchmark recommends a Classic PAT with 'repo' and 'workflow' scopes (see setup/GITHUB_SETUP.md)",
        )
        return True  # can't verify, but don't hard-fail

    scopes = [s.strip() for s in raw_scopes.split(",") if s.strip()]

    if "repo" in scopes:
        ok("Token has 'repo' scope")
    else:
        fail(
            "Token is missing 'repo' scope",
            "Regenerate the token and check the full 'repo' checkbox",
        )

    if "workflow" in scopes:
        ok("Token has 'workflow' scope")
    else:
        fail(
            "Token is missing 'workflow' scope",
            "Regenerate the token and check the 'workflow' checkbox",
        )

    return "repo" in scopes and "workflow" in scopes


def check_repo(token, owner, repo):
    """Confirm the repo exists and the token can push to it."""
    print(f"\n{_c(BOLD)}Repository — {owner}/{repo}{_c(RESET)}")

    resp = gh(f"/repos/{owner}/{repo}", token)

    if resp.status_code == 404:
        fail(
            f"Repo '{owner}/{repo}' not found or token cannot see it",
            "Create the repo on GitHub, or verify the token has access to it",
        )
        return None

    if resp.status_code != 200:
        fail(f"Unexpected response from GitHub ({resp.status_code})")
        return None

    data = resp.json()
    ok(f"Repo '{owner}/{repo}' found")

    perms = data.get("permissions", {})
    if perms.get("push"):
        ok("Token has push (write) access")
    else:
        fail(
            "Token does not have push access to this repo",
            "Check the token's repo scope and the repo's collaborator settings",
        )

    return data


def check_pages(token, owner, repo, expected_source):
    """
    Check GitHub Pages configuration.

    expected_source: "actions" (deploy-pages workflow) | "gh-pages" (branch)
    """
    resp = gh(f"/repos/{owner}/{repo}/pages", token)

    if resp.status_code == 404:
        fail(
            "GitHub Pages is not enabled on this repo",
            "Go to Settings → Pages and configure the Pages source before starting the session",
        )
        return None

    if resp.status_code != 200:
        warn(f"Could not read Pages configuration ({resp.status_code})")
        return None

    data = resp.json()
    ok("GitHub Pages is enabled")

    build_type = data.get("build_type", "")       # "workflow" = GitHub Actions
    source     = data.get("source", {})
    branch     = source.get("branch", "")

    if expected_source == "actions":
        if build_type == "workflow":
            ok("Pages source is 'GitHub Actions' ✓")
        else:
            fail(
                f"Pages source is '{build_type or branch}' — expected 'GitHub Actions'",
                "Go to Settings → Pages → Source and select 'GitHub Actions'",
            )

    elif expected_source == "gh-pages":
        if branch == "gh-pages":
            ok("Pages source is 'gh-pages' branch ✓")
        else:
            warn(
                f"Pages source branch is '{branch or 'not configured'}' — Scenario 2 uses the 'gh-pages' branch",
                "The agent configures this via the API once the gh-pages branch exists — no manual action needed",
            )

    return data


def check_actions_write_permissions(token, owner, repo):
    """Check that Actions workflow permissions allow write (not read-only)."""
    resp = gh(f"/repos/{owner}/{repo}/actions/permissions/workflow", token)

    if resp.status_code == 403:
        warn(
            "Could not read Actions workflow permissions — admin access may be required",
            "Manually verify: Settings → Actions → General → Workflow permissions → 'Read and write permissions'",
        )
        return None

    if resp.status_code != 200:
        warn(f"Could not read Actions workflow permissions ({resp.status_code})")
        return None

    data  = resp.json()
    perms = data.get("default_workflow_permissions", "unknown")

    if perms == "write":
        ok("Actions workflow permissions: 'read and write' ✓")
    else:
        fail(
            f"Actions workflow permissions are '{perms}' — workflows cannot push to branches",
            "Go to Settings → Actions → General → Workflow permissions → select 'Read and write permissions'",
        )

    return perms


def check_branch_exists(token, owner, repo, branch):
    """Return True if the branch exists."""
    resp = gh(f"/repos/{owner}/{repo}/branches/{branch}", token)
    return resp.status_code == 200


def check_branch_protection(token, owner, repo, branch):
    """Return True if the branch has protection rules (which block workflow pushes)."""
    resp = gh(f"/repos/{owner}/{repo}/branches/{branch}/protection", token)
    return resp.status_code == 200  # 404 = no protection = good


def check_repo_is_empty(token, owner, repo):
    """Warn if the repo contains files beyond a LICENSE (Scenario 3 expects a clean slate)."""
    resp = gh(f"/repos/{owner}/{repo}/contents/", token)
    if resp.status_code != 200:
        warn(f"Could not list repo contents ({resp.status_code})")
        return

    contents = resp.json()
    if not isinstance(contents, list):
        return

    names = [f["name"] for f in contents]
    extra = [n for n in names if n.upper() not in ("LICENSE", "LICENSE.MD", "LICENSE.TXT")]

    if extra:
        warn(
            f"Repo contains files beyond LICENSE: {', '.join(extra)}",
            "Scenario 3 expects agents to build from scratch — unexpected files may confuse the agent",
        )
    else:
        ok("Repo contains only LICENSE — clean slate for agents ✓")


# ---------------------------------------------------------------------------
# Per-scenario check suites
# ---------------------------------------------------------------------------

def scenario_1(token, owner, repo):
    print(f"\n{_c(BOLD)}Scenario 1 — Hello World{_c(RESET)}")
    check_pages(token, owner, repo, expected_source="actions")


def scenario_2(token, owner, repo):
    print(f"\n{_c(BOLD)}Scenario 2 — CI/CD Pipeline{_c(RESET)}")

    check_actions_write_permissions(token, owner, repo)

    if check_branch_exists(token, owner, repo, "dev"):
        ok("'dev' branch exists ✓")
    else:
        fail(
            "'dev' branch does not exist",
            "Create the 'dev' branch from main before starting the session (git checkout -b dev && git push origin dev)",
        )

    if check_branch_exists(token, owner, repo, "gh-pages"):
        ok("'gh-pages' branch exists")
        if check_branch_protection(token, owner, repo, "gh-pages"):
            fail(
                "'gh-pages' branch has protection rules — workflow pushes will be blocked",
                "Go to Settings → Branches, find 'gh-pages', and remove all protection rules",
            )
        else:
            ok("'gh-pages' branch has no protection rules ✓")
    else:
        warn(
            "'gh-pages' branch does not exist yet",
            "The agent creates it during the session — no action needed unless it fails to appear",
        )

    check_pages(token, owner, repo, expected_source="gh-pages")


def scenario_3(token, owner, repo):
    print(f"\n{_c(BOLD)}Scenario 3 — Full Project{_c(RESET)}")
    check_pages(token, owner, repo, expected_source="actions")
    check_repo_is_empty(token, owner, repo)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Pre-flight GitHub check for AI Storefront Benchmark",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python preflight.py --token ghp_xxx --repo cindy-pi/ai-storefront-anthropic --scenario 1
  python preflight.py --token ghp_xxx --repo cindy-pi/ai-storefront-gpt       --scenario 2
  python preflight.py --token ghp_xxx --repo cindy-pi/ai-storefront-deepseek  --scenario 3
        """,
    )
    parser.add_argument("--token",    required=True,                          help="GitHub Personal Access Token (Classic PAT)")
    parser.add_argument("--repo",     required=True,                          help="Target repo in owner/name format")
    parser.add_argument("--scenario", required=True, choices=["1", "2", "3"], help="Scenario to check")
    parser.add_argument("--no-color", action="store_true",                    help="Disable ANSI colour output")
    args = parser.parse_args()

    global _color
    if args.no_color:
        _color = False

    if "/" not in args.repo:
        print("Error: --repo must be in owner/name format (e.g. cindy-pi/ai-storefront-anthropic)")
        sys.exit(1)

    owner, repo = args.repo.split("/", 1)

    print(f"\n{_c(BOLD)}AI Storefront Benchmark — Pre-flight Check{_c(RESET)}")
    print(f"Repo:     {owner}/{repo}")
    print(f"Scenario: {args.scenario}")

    token_ok = check_token(args.token)
    if not token_ok:
        print(f"\n{_c(RED)}Token checks failed — fix the token before continuing.{_c(RESET)}")
        sys.exit(1)

    repo_data = check_repo(args.token, owner, repo)
    if repo_data is None:
        print(f"\n{_c(RED)}Repo checks failed — fix repo access before continuing.{_c(RESET)}")
        sys.exit(1)

    if args.scenario == "1":
        scenario_1(args.token, owner, repo)
    elif args.scenario == "2":
        scenario_2(args.token, owner, repo)
    elif args.scenario == "3":
        scenario_3(args.token, owner, repo)

    # Summary
    total = _passes + _warns + _fails
    print(f"\n{'─' * 48}")
    print(f"  {_c(GREEN)}{_passes} passed{_c(RESET)}  "
          f"{_c(YELLOW)}{_warns} warnings{_c(RESET)}  "
          f"{_c(RED)}{_fails} failed{_c(RESET)}  "
          f"({total} checks)")

    if _fails > 0:
        print(f"\n  {_c(RED)}Fix the failures above before starting the session.{_c(RESET)}")
        sys.exit(1)
    elif _warns > 0:
        print(f"\n  {_c(YELLOW)}Warnings present — review them, but the session can proceed.{_c(RESET)}")
    else:
        print(f"\n  {_c(GREEN)}All checks passed — ready to start the session.{_c(RESET)}")


if __name__ == "__main__":
    main()
