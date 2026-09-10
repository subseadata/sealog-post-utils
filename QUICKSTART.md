# Quick Start

This guide is for using the Sealog filter/export notebook — no Python experience needed, just follow the steps.

## 1. Install prerequisites

You need two tools, both one-time installs:

- **Git** — to download this repository. Check if you already have it: `git --version`. If not, install from [git-scm.com](https://git-scm.com/downloads).
- **uv** — runs Python and installs everything else for you. Install with:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
  (See [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/) for other install options, e.g. Windows.)

You do **not** need to separately install Python — `uv` takes care of that.

## 2. Get the code

```bash
git clone <REPO_URL>
cd sealog-post-utils
```

Replace `<REPO_URL>` with this repository's GitHub URL once it's up.

## 3. Install dependencies

From inside the `sealog-post-utils` folder:

```bash
uv sync
```

This sets up everything the notebook needs. You only need to run it again later if the project's dependencies change.

## 4. Add your data

Copy your Sealog export CSV into the `data/` folder in this project. That's it — no renaming needed.

## 5. Launch the notebook

```bash
uv run marimo edit notebooks/explore_events.py
```

This opens the notebook in your browser.

## 6. Use the notebook

Work through it top to bottom:

1. **Choose the sealog data file** — it defaults to the CSV you put in `data/`; change it if you have more than one.
2. **Choose the event value to filter the csv by** — pick from the event types found in your file.
3. **Choose the auxillary data to be kept** — pick which sensor/data groups (e.g. CTD, weather, navigation) to include alongside the event data.
4. **Preview of the data that will be exported** — a table shows exactly what the exported CSV will look like.
5. **Choose how to get your filtered CSV**:
   - **Save to disk** — writes the file into the `output/` folder (or a path you type in), then click **Export filtered CSV**.
   - **Download** — click **Download filtered CSV** to save it directly from your browser, no local file path needed.

If something's wrong (e.g. no CSV found), the notebook shows a plain-language message telling you what to fix rather than an error page.

## Next time

Once set up, coming back later just takes two commands from inside the `sealog-post-utils` folder:

```bash
uv sync
uv run marimo edit notebooks/explore_events.py
```
