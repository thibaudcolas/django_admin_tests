"""Map source branches to stable, DNS-safe Pages output branches."""

import hashlib
import os
import re


def deployment_branch(source, django_pr=""):
    if django_pr:
        if not re.fullmatch(r"[1-9][0-9]*", django_pr) or len(django_pr) > 20:
            raise ValueError("The Django PR number must be a positive integer.")
        return f"preview-{django_pr}"
    if source == "main":
        return "gh-pages"
    if not source or source == "gh-pages" or source.startswith("preview-"):
        raise ValueError("Generated output branches cannot be used as source branches.")
    slug = re.sub(r"[^a-z0-9-]+", "-", source.lower()).strip("-") or "branch"
    # Keep ordinary names readable. Use a separate namespace and a stable hash
    # for lossy normalization, so fix/api and fix-api cannot share a deployment.
    if slug != source or len(slug) > 48:
        digest = hashlib.sha256(source.encode()).hexdigest()[:12]
        return f"preview-ref-{slug[:38].rstrip('-')}-{digest}"
    return f"preview-branch-{slug}"


if __name__ == "__main__":
    branch = deployment_branch(os.environ["SOURCE_BRANCH"], os.environ.get("DJANGO_PR", ""))
    host = "django-admin-tests.pages.dev"
    if branch != "gh-pages":
        host = f"{branch}.{host}"
    url = f"https://{host}/django_admin_tests/latest/english/admin/"
    with open(os.environ["GITHUB_OUTPUT"], "a") as output:
        output.write(f"branch={branch}\nurl={url}\n")
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as summary:
        summary.write(f"Pages output branch: `{branch}`\n\nPreview URL after Cloudflare finishes deploying: {url}\n")
        if os.environ.get("DJANGO_PR"):
            summary.write(f"\n[Automated code review](https://{host}/review.txt)\n")
