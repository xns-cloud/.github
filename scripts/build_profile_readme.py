#!/usr/bin/env python3
"""Regenerate profile/README.md from the org's actual public repositories.

The table is derived, not maintained. A new public repo appears in it because it
exists, using its own GitHub description as the text. profile/listing.json only
adds optional detail (install line, ordering); a repo missing from that file is
still listed, with a sane fallback.

Why this exists: relayer-quickstart was held out of the hand-written table in
5326bc3 ("hold ... until the repo has content"). The repo gained content on
2026-08-09 and nothing was watching the release condition, so a deliberate
temporary hold silently became a permanent omission, and the two repos published
after it were never added at all.
"""
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request

ORG = "xns-cloud"
GITLAB_GROUP = "scpcorp"
ROOT = pathlib.Path(__file__).resolve().parent.parent
TMPL = ROOT / "profile" / "README.tmpl.md"
OUT = ROOT / "profile" / "README.md"
CONF = ROOT / "profile" / "listing.json"


def get_json(url, token=None):
    req = urllib.request.Request(url, headers={"Accept": "application/json",
                                               "User-Agent": "xns-profile-readme"})
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def gitlab_source(name):
    """Return the GitLab URL if a public project of the same name exists, else None.

    Derived rather than configured, so a repo that gains or loses a GitLab source
    is reflected without anyone editing this file.
    """
    url = f"https://gitlab.com/api/v4/projects/{GITLAB_GROUP}%2F{name}"
    try:
        p = get_json(url)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    if p.get("visibility") != "public":
        return None
    return p.get("web_url")


def main():
    token = os.environ.get("GITHUB_TOKEN") or None
    conf = json.loads(CONF.read_text(encoding="utf-8"))
    over, exclude = conf.get("repos", {}), set(conf.get("exclude", []))

    repos = []
    page = 1
    while True:
        batch = get_json(
            f"https://api.github.com/orgs/{ORG}/repos?type=public&per_page=100&page={page}",
            token)
        if not batch:
            break
        repos += batch
        page += 1

    repos = [r for r in repos
             if not r["private"] and not r["archived"] and r["name"] not in exclude]
    if not repos:
        sys.exit("refusing to write an empty table — the repo listing came back empty")

    def sort_key(r):
        o = over.get(r["name"], {}).get("order")
        return (0, o, "") if o is not None else (1, 0, r["name"].lower())

    repos.sort(key=sort_key)

    rows = ["| Repository | What it is | Install / use | Source of truth |",
            "|------------|------------|---------------|-----------------|"]
    missing_desc, gh_issue_repos = [], []
    for r in repos:
        name = r["name"]
        o = over.get(name, {})
        desc = (r["description"] or "").strip()
        # The Source column already states the mirror relationship; the repo's own
        # description keeps saying it for GitHub search results, where no table exists.
        desc = re.sub(r"\s*Mirrored from GitLab\.?$", "", desc).strip()
        if not desc:
            # Surfaced rather than papered over: a blank description is a real
            # discoverability defect on the repo itself, and this is where it shows.
            missing_desc.append(name)
            desc = "_no description set on the repository_"
        gl = gitlab_source(name)
        if gl and o.get("gh_issues"):
            gh_issue_repos.append(name)
        rows.append("| [{n}](https://github.com/{o}/{n}) | {d} | {i} | {s} |".format(
            n=name, o=ORG, d=desc,
            i=o.get("install", "see the repo README"),
            s=f"[GitLab]({gl})" if gl else "here"))

    exc = ""
    if gh_issue_repos:
        links = ", ".join(
            f"[{n}](https://github.com/{ORG}/{n}/issues)" for n in gh_issue_repos)
        exc = ("  {} is the exception: its GitHub Issues are monitored too.\n".format(
            links if len(gh_issue_repos) > 1 else links))

    out = (TMPL.read_text(encoding="utf-8")
           .replace("<!-- REPO-TABLE -->", "\n".join(rows))
           .replace("<!-- GH-ISSUES-EXCEPTION -->\n", exc))

    changed = not OUT.exists() or OUT.read_text(encoding="utf-8") != out
    OUT.write_text(out, encoding="utf-8")
    for n in missing_desc:
        print(f"::warning::{n} has no GitHub description; the table says so out loud")
    print(f"{len(repos)} repos; README {'updated' if changed else 'unchanged'}")


if __name__ == "__main__":
    main()
