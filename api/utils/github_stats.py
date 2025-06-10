import requests as req
from functools import lru_cache
from datetime import datetime, timedelta
import markdown

GITHUB_RELEASES_URL = "https://api.github.com/repos/Arian-Ott/storify/releases"
RATE_LIMIT = 60


FIRST_REQUEST_MADE = None
REQS = 0


def get_all_github_releases():
    """
    Fetch all GitHub releases from the Storify repository.
    """
    global FIRST_REQUEST_MADE, REQS
    try:
        if FIRST_REQUEST_MADE is None:
            FIRST_REQUEST_MADE = datetime.now()
            REQS = 1
        else:
            elapsed = datetime.now() - FIRST_REQUEST_MADE
            if elapsed > timedelta(hours=1):
                # Reset count after 1 hour
                FIRST_REQUEST_MADE = datetime.now()
                REQS = 1
            elif REQS >= RATE_LIMIT:
                raise RuntimeError(
                    "GitHub API rate limit exceeded (unauthenticated: 60/hr)"
                )

            else:
                REQS += 1

        response = req.get(GITHUB_RELEASES_URL)
        response.raise_for_status()
        return response.json()
    except req.RequestException as e:
        print(f"Error fetching GitHub releases: {e}")
        return []


@lru_cache(maxsize=64)
def all_releases():
    return get_all_github_releases()


def format_releases():
    """
    Format GitHub releases into a list of dictionaries with title, version, and date.
    """
    releases = all_releases()
    formatted_releases = []

    for release in releases:
        if "tag_name" in release and "published_at" in release:
            formatted_releases.append(
                {
                    "title": release.get("name", "No title"),
                    "version": release["tag_name"],
                    "date": release["published_at"],
                    "description": convert_markdown_to_html(
                        release.get("body", "No description")
                    ),
                    "author": release.get("author", {}).get("login", "Unknown"),
                }
            )

    return formatted_releases


def convert_markdown_to_html(markdown_text):
    """
    Convert Markdown text to HTML.
    """

    out = markdown.markdown(
        text=markdown_text,
        extensions=["fenced_code", "tables", "codehilite", "nl2br", "sane_lists"],
    )
    out = out.replace(
        "<ul>", "<ul class='list-disc list-inside bg-slate-700 p-4 rounded'>"
    )
    out.replace("<h1>", "<h1 class='text-2xl font-bold'>")
    out = out.replace("<h2>", "<h2 class='text-xl font-semibold'>")
    out = out.replace("<strong>", "<strong class='font-monospace'>")
    return out
