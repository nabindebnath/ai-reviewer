import os
import requests
from openai import OpenAI

# Setup OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# GitHub environment variables (injected by GitHub Actions)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPOSITORY")   # e.g. "user/repo"
PR_NUMBER = os.getenv("PR_NUMBER")


def get_pr_diff() -> str:
    """Fetch the actual PR diff from GitHub API"""
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3.diff",
    }
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.text


def review_code(diff: str) -> str:
    """Send diff to OpenAI for code review"""
    prompt = f"""
    You are a senior software engineer reviewing a pull request.

    Here is the code diff:

    {diff}

    Please:
    1. Group feedback by file name.
    2. Flag potential bugs or logic issues.
    3. Suggest improvements in readability, naming, and best practices.
    4. Keep comments concise and actionable.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",   # or gpt-4o for stronger reasoning
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content.strip()


def post_comment(body: str):
    """Post review feedback as a PR comment"""
    url = f"https://api.github.com/repos/{REPO}/issues/{PR_NUMBER}/comments"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }
    payload = {"body": body}
    r = requests.post(url, headers=headers, json=payload)
    r.raise_for_status()


if __name__ == "__main__":
    print("📥 Fetching PR diff...")
    diff = get_pr_diff()

    print("🤖 Running AI code review...")
    feedback = review_code(diff)

    print("💬 Posting comment to PR...")
    post_comment(f"### 🤖 AI Review Feedback\n\n{feedback}")

    print("✅ Review posted successfully!")

