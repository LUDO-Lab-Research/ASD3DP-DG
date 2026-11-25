#!/usr/bin/env bash
set -euo pipefail

git fetch origin \
    refs/heads/main:refs/remotes/origin/main \
    refs/heads/gh-pages:refs/remotes/origin/gh-pages

main=$(git rev-parse refs/remotes/origin/main)
pages=$(git rev-parse refs/remotes/origin/gh-pages)
site_tree=$(git rev-parse "$main:site")

if [[ "$site_tree" == "$(git rev-parse "$pages^{tree}")" ]]; then
    printf 'The gh-pages branch already matches site/ on main.\n'
    exit 0
fi

commit=$(git commit-tree "$site_tree" -p "$pages" -m "Publish dataset guide from ${main:0:12}")
git push origin "$commit:refs/heads/gh-pages"
