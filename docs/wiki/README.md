# ASD3DP-DG public guide

Read the [dataset guide](index.md) and the [joint-shift benchmark](joint-benchmark.md). The [rendered guide](../../site/index.html) is generated from these Markdown pages.

## Publishing the guide

Edit the Markdown in this directory. From the repository root, build the HTML and include the changed files under `site/` in the same pull request.

```bash
python3 -m pip install 'Markdown==3.8.2'
python3 tools/build_site.py
```

After merging the pull request, run the [publisher](../../tools/publish_site.sh) from the repository root. It publishes the merged `site/` tree and keeps the history of the existing Pages branch.

```bash
bash tools/publish_site.sh
```

For the first deployment, set **Settings → Pages → Build and deployment → Source** to **Deploy from a branch**, and select `gh-pages` and `/ (root)`. The Pages branch contains the generated guide and its stylesheet.
