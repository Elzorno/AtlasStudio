from __future__ import annotations

import subprocess

from .models import GithubUnavailableError, NetworkError


REPO_SLUGS = {
    "TheLastSwordProtocol-Atlas": "Elzorno/TheLastSwordProtocol-Atlas",
    "TheLastSwordProtocol-Game": "Elzorno/TheLastSwordProtocol-Game",
}


def check_reachable(repo: str) -> bool:
    slug = _slug(repo)
    try:
        result = subprocess.run(
            ["gh", "repo", "view", slug],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0


def open_issue(repo: str, title: str, body: str, labels: list[str]) -> str:
    slug = _slug(repo)
    try:
        result = subprocess.run(
            [
                "gh",
                "issue",
                "create",
                "--repo",
                slug,
                "--title",
                title,
                "--body",
                body,
                "--label",
                ",".join(labels),
            ],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise NetworkError("network error contacting GitHub") from error
    except OSError as error:
        raise GithubUnavailableError("gh CLI is unavailable") from error
    if result.returncode != 0:
        message = (result.stderr or result.stdout or "GitHub issue creation failed").strip()
        raise GithubUnavailableError(message)
    return result.stdout.strip().splitlines()[-1]


def _slug(repo: str) -> str:
    if repo not in REPO_SLUGS:
        raise GithubUnavailableError(f"unapproved GitHub target repository: {repo}")
    return REPO_SLUGS[repo]
