#!/usr/bin/env python3
"""
github_setup.py — Create and configure a GitHub repo for the AI Storefront
Benchmark, then guide you through generating a fine-grained Personal Access
Token scoped to that single repo.

The generated token will pass preflight.py for Scenario 1 or 2.

Usage:
    python tools/github_setup.py --repo owner/repo-name [--scenario 1|2] [--private]

Requirements:
    pip install requests
"""

import argparse
import os
import subprocess
import sys
import webbrowser
from getpass import getpass

try:
    import requests
except ImportError:
    print("Error: 'requests' is not installed.  Run: pip install requests")
    sys.exit(1)

API    = "https://api.github.com"
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"
RESET  = "\033[0m"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _gh(method, path, token, **kwargs):
    return getattr(requests, method)(
        f"{API}{path}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        timeout=15,
        **kwargs,
    )


def step(n, msg):
    print(f"\n{BOLD}Step {n}: {msg}{RESET}")


def ok(msg):
    print(f"  {GREEN}PASS{RESET}  {msg}")


def warn(msg, fix=None):
    print(f"  {YELLOW}WARN{RESET}  {msg}")
    if fix:
        print(f"         → {fix}")


def fail(msg, fix=None):
    print(f"  {RED}FAIL{RESET}  {msg}")
    if fix:
        print(f"         → {fix}")


# ---------------------------------------------------------------------------
# Step 1 — Obtain a setup token (admin rights to create/configure the repo)
# ---------------------------------------------------------------------------

def get_admin_token():
    for var in ("GH_TOKEN", "GITHUB_TOKEN"):
        tok = os.environ.get(var, "")
        if tok:
            print(f"  Using token from ${var}")
            return tok

    try:
        result = subprocess.run(
            ["gh", "auth", "token"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0 and result.stdout.strip():
            print("  Using token from 'gh auth token'")
            return result.stdout.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    print(
        "\n  Enter a GitHub token with permission to CREATE repos under the target owner."
        "\n  A Classic PAT with 'repo' scope works. This token is only used for setup —"
        "\n  it is NOT the token you will use for the benchmark."
    )
    return getpass("  Setup token: ").strip()


# ---------------------------------------------------------------------------
# Step 2 — Create or confirm the target repository
# ---------------------------------------------------------------------------

def create_or_confirm_repo(token, owner, repo_name, private):
    resp = _gh("get", f"/repos/{owner}/{repo_name}", token)
    if resp.status_code == 200:
        warn(f"Repo '{owner}/{repo_name}' already exists — skipping creation")
        return resp.json()

    # Detect whether owner is the authenticated user or an org
    me = _gh("get", "/user", token).json().get("login", "")
    payload = {
        "name": repo_name,
        "description": "AI Storefront Benchmark target repository",
        "private": private,
        "auto_init": True,          # creates first commit + main branch
        "license_template": "mit",  # adds LICENSE so the repo isn't empty
    }

    if me.lower() == owner.lower():
        resp = _gh("post", "/user/repos", token, json=payload)
    else:
        resp = _gh("post", f"/orgs/{owner}/repos", token, json=payload)

    if resp.status_code in (200, 201):
        ok(f"Repo '{owner}/{repo_name}' created")
        return resp.json()

    fail(
        f"Could not create repo ({resp.status_code})",
        resp.text[:200],
    )
    sys.exit(1)


# ---------------------------------------------------------------------------
# Step 3 — Ensure default branch is 'main'
# ---------------------------------------------------------------------------

def ensure_main_branch(token, owner, repo_name):
    data   = _gh("get", f"/repos/{owner}/{repo_name}", token).json()
    current = data.get("default_branch", "")

    if current == "main":
        ok("Default branch is 'main'")
        return

    if not current:
        warn("Repository has no commits yet — cannot rename branch")
        return

    warn(f"Default branch is '{current}', renaming to 'main' …")
    r = _gh(
        "post",
        f"/repos/{owner}/{repo_name}/branches/{current}/rename",
        token,
        json={"new_name": "main"},
    )
    if r.status_code == 201:
        _gh("patch", f"/repos/{owner}/{repo_name}", token, json={"default_branch": "main"})
        ok("Branch renamed to 'main'")
    else:
        fail(
            f"Could not rename branch ({r.status_code})",
            "Rename it manually: Settings → General → Default branch",
        )


# ---------------------------------------------------------------------------
# Step 4 — Enable GitHub Pages with 'GitHub Actions' as the source
# ---------------------------------------------------------------------------

def enable_pages(token, owner, repo_name):
    resp = _gh("get", f"/repos/{owner}/{repo_name}/pages", token)

    if resp.status_code == 200 and resp.json().get("build_type") == "workflow":
        ok("GitHub Pages already enabled with 'GitHub Actions' source")
        return

    # Try to create Pages with workflow (Actions) source
    r = _gh("post", f"/repos/{owner}/{repo_name}/pages", token, json={"build_type": "workflow"})

    if r.status_code in (200, 201):
        ok("GitHub Pages enabled with 'GitHub Actions' source")
        return

    if r.status_code == 409:
        # Pages exists but with wrong source — update it
        r2 = _gh("put", f"/repos/{owner}/{repo_name}/pages", token, json={"build_type": "workflow"})
        if r2.status_code in (200, 204):
            ok("GitHub Pages updated to 'GitHub Actions' source")
            return
        warn(
            f"Could not update Pages source ({r2.status_code})",
            f"Go to https://github.com/{owner}/{repo_name}/settings/pages and select 'GitHub Actions'",
        )
        return

    warn(
        f"Could not enable GitHub Pages automatically ({r.status_code})",
        f"Go to https://github.com/{owner}/{repo_name}/settings/pages and select 'GitHub Actions'",
    )


# ---------------------------------------------------------------------------
# Step 5 — Guide the user through fine-grained token creation
# ---------------------------------------------------------------------------

def print_fine_grained_token_guide(owner, repo_name):
    url = "https://github.com/settings/personal-access-tokens/new"
    print(f"""
{BOLD}{'━' * 56}{RESET}
{BOLD}  Create a Fine-Grained Personal Access Token{RESET}
{BOLD}{'━' * 56}{RESET}

  Opening: {url}

  Fill in the form:
    • Token name        →  ai-storefront-benchmark
    • Expiration        →  90 days (or your preference)
    • Resource owner    →  {owner}

  Under "Repository access":
    ● Only select repositories  →  select "{repo_name}"

  Under "Permissions → Repository permissions":
    • Actions        →  Read and write
    • Contents       →  Read and write
    • Issues         →  Read and write
    • Metadata       →  Read-only   (auto-selected, required)
    • Pages          →  Read and write
    • Pull requests  →  Read and write
    • Workflows      →  Read and write

  Click "Generate token", then copy the value shown.

  {YELLOW}The token is displayed only once — copy it before leaving the page.{RESET}
{BOLD}{'━' * 56}{RESET}""")

    try:
        webbrowser.open(url)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Step 6 — Collect & validate the fine-grained token (mirrors preflight.py)
# ---------------------------------------------------------------------------

def collect_and_validate(owner, repo_name, prefilled=None):
    print()
    if prefilled:
        token = prefilled
    else:
        token = getpass("  Paste your fine-grained token (hidden): ").strip()
    if not token:
        fail("No token entered.")
        sys.exit(1)

    print(f"\n{BOLD}Validating token …{RESET}")
    passes = warns = fails = 0

    # --- Token validity & scope ---
    try:
        resp = requests.get(
            f"{API}/",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=10,
        )
    except requests.exceptions.ConnectionError:
        fail("Could not reach api.github.com")
        sys.exit(1)

    if resp.status_code == 401:
        fail(
            "Token is invalid or expired",
            "Generate a new token and re-run this script",
        )
        sys.exit(1)

    ok("Token accepted by GitHub")
    passes += 1

    raw_scopes = resp.headers.get("X-OAuth-Scopes", "")
    if not raw_scopes:
        # Fine-grained tokens never expose scopes in this header — that's expected.
        warn(
            "Fine-grained token detected — scope header absent (expected behaviour)",
            "preflight.py will show a WARN here but will NOT fail",
        )
        warns += 1
    else:
        scopes = [s.strip() for s in raw_scopes.split(",")]
        for scope in ("repo", "workflow"):
            if scope in scopes:
                ok(f"Token has '{scope}' scope")
                passes += 1
            else:
                fail(f"Token is missing '{scope}' scope")
                fails += 1

    # --- Repo access & push permission ---
    resp2 = requests.get(
        f"{API}/repos/{owner}/{repo_name}",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        timeout=10,
    )

    if resp2.status_code != 200:
        fail(
            f"Cannot access repo '{owner}/{repo_name}' ({resp2.status_code})",
            "Ensure the token is scoped to this repository",
        )
        fails += 1
    else:
        ok(f"Repo '{owner}/{repo_name}' accessible")
        passes += 1
        data = resp2.json()

        if data.get("permissions", {}).get("push"):
            ok("Token has push (write) access")
            passes += 1
        else:
            fail(
                "Token does not have push access",
                "Set Contents → Read and write when creating the token",
            )
            fails += 1

        if data.get("default_branch") == "main":
            ok("Default branch is 'main'")
            passes += 1
        else:
            fail(
                f"Default branch is '{data.get('default_branch')}' — expected 'main'",
                "Settings → General → Default branch → rename to main",
            )
            fails += 1

    # --- GitHub Pages ---
    resp3 = requests.get(
        f"{API}/repos/{owner}/{repo_name}/pages",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        timeout=10,
    )

    if resp3.status_code == 404:
        fail(
            "GitHub Pages is not enabled",
            f"Go to https://github.com/{owner}/{repo_name}/settings/pages and enable it",
        )
        fails += 1
    elif resp3.status_code == 200:
        ok("GitHub Pages is enabled")
        passes += 1
        if resp3.json().get("build_type") == "workflow":
            ok("Pages source is 'GitHub Actions'")
            passes += 1
        else:
            fail(
                "Pages source is not 'GitHub Actions'",
                f"Go to https://github.com/{owner}/{repo_name}/settings/pages → Source → GitHub Actions",
            )
            fails += 1
    else:
        warn(f"Could not read Pages configuration ({resp3.status_code})")
        warns += 1

    # --- Summary ---
    total = passes + warns + fails
    print(f"\n{'─' * 48}")
    print(
        f"  {GREEN}{passes} passed{RESET}  "
        f"{YELLOW}{warns} warnings{RESET}  "
        f"{RED}{fails} failed{RESET}  "
        f"({total} checks)"
    )

    if fails > 0:
        print(f"\n  {RED}Fix the failures above, then re-run this script or preflight.py.{RESET}")
        sys.exit(1)
    elif warns > 0:
        print(f"\n  {YELLOW}Warnings present — preflight.py will WARN but NOT fail for fine-grained tokens.{RESET}")
    else:
        print(f"\n  {GREEN}All checks passed!{RESET}")

    return token


# ---------------------------------------------------------------------------
# Step 7 — Print the token and the preflight command to copy
# ---------------------------------------------------------------------------

def print_summary(token, owner, repo_name, scenario):
    print(f"""
{BOLD}{'═' * 56}{RESET}
{BOLD}  Your fine-grained token (copy this){RESET}
{BOLD}{'═' * 56}{RESET}

  {GREEN}{token}{RESET}

{BOLD}  Preflight command to verify:{RESET}

  python preflight.py `
      --token {token} `
      --repo {owner}/{repo_name} `
      --scenario {scenario}
{BOLD}{'═' * 56}{RESET}
""")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Set up a GitHub repo for the AI Storefront Benchmark and generate a fine-grained PAT.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python github_setup.py --repo cindy-pi/ai-storefront-anthropic --scenario 1
  python github_setup.py --repo cindy-pi/ai-storefront-anthropic --scenario 2 --private
  python github_setup.py --repo cindy-pi/ai-storefront-anthropic --scenario 2 --token github_pat_xxx
        """,
    )
    parser.add_argument("--repo",     required=True,             help="Target repo in owner/name format")
    parser.add_argument("--scenario", default="1", choices=["1", "2"], help="Benchmark scenario to configure (default: 1)")
    parser.add_argument("--private",  action="store_true",       help="Create the repo as private (default: public)")
    parser.add_argument("--token",                               help="Skip setup; validate this token and print the preflight command")
    args = parser.parse_args()

    if "/" not in args.repo:
        print("Error: --repo must be in owner/name format (e.g. cindy-pi/ai-storefront-anthropic)")
        sys.exit(1)

    owner, repo_name = args.repo.split("/", 1)

    # Validate-only mode: skip repo setup, just check the supplied token.
    if args.token:
        print(f"\n{BOLD}AI Storefront Benchmark — Token Validation{RESET}")
        print(f"  Repo:     {owner}/{repo_name}")
        print(f"  Scenario: {args.scenario}")
        validated = collect_and_validate(owner, repo_name, prefilled=args.token)
        print_summary(validated, owner, repo_name, args.scenario)
        return

    print(f"\n{BOLD}AI Storefront Benchmark — GitHub Setup{RESET}")
    print(f"  Repo:     {owner}/{repo_name}")
    print(f"  Scenario: {args.scenario}")

    step(1, "Setup token (used only to create and configure the repo)")
    admin_token = get_admin_token()

    resp = requests.get(
        f"{API}/user",
        headers={
            "Authorization": f"Bearer {admin_token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        timeout=10,
    )
    if resp.status_code != 200:
        fail(f"Setup token is invalid ({resp.status_code})")
        sys.exit(1)
    ok(f"Authenticated as '{resp.json().get('login', '?')}'")

    step(2, f"Create repository '{owner}/{repo_name}'")
    create_or_confirm_repo(admin_token, owner, repo_name, args.private)

    step(3, "Verify default branch is 'main'")
    ensure_main_branch(admin_token, owner, repo_name)

    step(4, "Enable GitHub Pages (GitHub Actions source)")
    enable_pages(admin_token, owner, repo_name)

    step(5, "Create a fine-grained PAT scoped to this repo only")
    print_fine_grained_token_guide(owner, repo_name)

    step(6, "Paste and validate your new fine-grained token")
    fg_token = collect_and_validate(owner, repo_name, prefilled=None)

    print_summary(fg_token, owner, repo_name, args.scenario)


if __name__ == "__main__":
    main()
