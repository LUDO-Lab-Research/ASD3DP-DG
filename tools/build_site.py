"""Build the GitHub Pages guide from the tracked Markdown guide."""

from pathlib import Path
import html
import re

import markdown


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/wiki"
DESTINATION = ROOT / "site"
PAGES = (
    ("index", "Overview"),
    ("collection", "Collection"),
    ("layout", "Files"),
    ("timebase", "Time coordinates"),
    ("selection", "Clip selection"),
    ("annotations", "Annotations"),
    ("schemas", "Schemas"),
    ("fields", "Field dictionary"),
    ("verification", "Verification"),
    ("joint-benchmark", "Joint shifts"),
    ("limits", "Limitations"),
    ("download", "Downloads"),
)


def main():
    for stem, label in PAGES:
        source = (SOURCE / f"{stem}.md").read_text()
        body = markdown.markdown(source, extensions=["tables", "fenced_code", "toc", "attr_list"])
        body = re.sub(
            r'href="([a-z-]+)\.md(#[^"]*)?"',
            lambda match: f'href="{match.group(1)}.html{match.group(2) or ""}"',
            body,
        )
        body = body.replace(
            'href="../../',
            'href="https://github.com/LUDO-Lab-Research/ASD3DP-DG/blob/main/',
        )
        links = "".join(
            f'<a href="{name}.html"{(" aria-current=" + chr(34) + "page" + chr(34)) if name == stem else ""}>{html.escape(title)}</a>'
            for name, title in PAGES
        )
        page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="ASD3DP-DG public dataset guide">
<title>{html.escape(label)} · ASD3DP-DG</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header><a class="brand" href="index.html">ASD3DP-DG</a><nav aria-label="Guide">{links}</nav></header>
<main id="content">{body}</main>
<footer><a href="https://github.com/LUDO-Lab-Research/ASD3DP-DG">ASD3DP-DG on GitHub</a></footer>
</body>
</html>
'''
        (DESTINATION / f"{stem}.html").write_text(page)
    print(f"Built {len(PAGES)} pages from {SOURCE}")


if __name__ == "__main__":
    main()
