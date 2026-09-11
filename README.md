# sealog-post-utils

Utilities for post-processing Sealog expedition event export CSVs.

## Scope

The current focus is the CSV event export produced by Schmidt Ocean Institute's [sealog-fkt](https://github.com/schmidtocean/sealog-server/tree/master/misc) instance, but nothing here is tied to that specifically — it could be generalized and expanded to other Sealog deployments or export shapes. The goal is to let you filter that export down to one event type and restructure it (dropping unpopulated columns, folding in units, choosing which sensor data groups to keep) so the output is simple and matches what you actually need, rather than handing you the full raw export every time.

> Just want to use the notebook? See [QUICKSTART.md](QUICKSTART.md) for a no-Python-experience-needed walkthrough.

## Requirements

- Python 3.13+ (see `.python-version`)
- [uv](https://docs.astral.sh/uv/)

## Setup

Install dependencies into a local virtual environment managed by uv:

```bash
uv sync
```

This creates/updates `.venv` and installs everything pinned in `uv.lock`.

## Running

Run the console script defined in `pyproject.toml` (`sealog-post-utils = "sealog_post_utils:main"`):

```bash
uv run sealog-post-utils
```

Run a module directly instead of the console script, e.g. the utils module's `__main__` block:

```bash
uv run python -m sealog_post_utils.sealog_post_utils
```

Run an arbitrary script or one-off command inside the project's environment:

```bash
uv run python your_script.py
```

## Local data

Put your own copy of a Sealog export CSV in `data/` (it's gitignored, so nothing there gets committed). The
notebook's "Sealog export CSV path" field defaults to the first `*.csv` it finds in `data/` automatically, so
just drop your file in there and open the notebook. You can still point it (or the `csv_path` argument of any
function below) at any other path, e.g. `data/FKt260806_sealog_export.csv`.

Filtered/exported CSVs go in `output/` (also gitignored) when using the "Save to disk" option in the notebook,
or calling `export_event_csv` directly. Its output path field defaults to `output`, and `export_event_csv`
auto-names the file inside it (`<event_value>_filtered.csv`) whenever `output_path` is a directory — pass a
full file path instead if you want to control the name yourself.

## Using the utility functions

The functions in `src/sealog_post_utils/sealog_post_utils.py` operate on a Sealog event export CSV. If you
omit `csv_path`, they default to the first `*.csv` file found in `data/` (raising an error if none exists),
or you can pass any path explicitly:

```bash
uv run python -c "
from sealog_post_utils.sealog_post_utils import get_event_value_types
print(get_event_value_types('/path/to/export.csv'))
"
```

Available functions:

- `get_event_value_types(csv_path)` — list all distinct `event_value` types in the export.
- `get_populated_event_option_columns(event_value, csv_path)` — counts of populated `event_option.*` columns for a given event type.
- `get_data_group_prefixes(csv_path)` — list of data group column prefixes present in the export.
- `build_filtered_dataframe(event_value, *data_group_prefixes, csv_path)` — same filtering as `export_event_csv` below, but returns the resulting `pandas.DataFrame` instead of writing it anywhere.
- `export_event_csv(event_value, *data_group_prefixes, csv_path, output_path)` — filter the export down to one event type and chosen data groups, writing the result to a new CSV. Only the `event_option.*` columns that are actually populated for the chosen event type are kept, and each data group's `*_value` column is renamed with its unit (e.g. `ctdSBE911.ctd_temperature_C`), with the redundant `*_uom` column dropped. If `output_path` is omitted or is a directory, the file is auto-named `<event_value>_filtered.csv` inside it (next to `csv_path` if omitted entirely).

## Marimo notebook

An interactive [marimo](https://marimo.io) notebook that calls into these utilities lives at
`notebooks/explore_events.py`. It lets you point at a Sealog export CSV, browse the event types found in it,
pick one to filter by, choose which data groups to include, preview the data that will be exported, and then
either save the filtered CSV to disk (with an auto-suggested, editable filename) or download it straight from
the browser — handy if you're running the notebook somewhere without direct filesystem access. Bad or missing
input (no CSV in `data/`, an unreadable file, etc.) shows a friendly message instead of a raw error. Launch it
(editable, reactive UI) with:

```bash
uv run marimo edit notebooks/explore_events.py
```

Or run it as a standalone app:

```bash
uv run marimo run notebooks/explore_events.py
```

## Adding dependencies

```bash
uv add <package>
```
