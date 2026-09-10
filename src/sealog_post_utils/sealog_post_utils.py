import functools
import glob
import os

import pandas as pd


def list_data_csvs():
    return sorted(glob.glob(os.path.join("data", "*.csv")))


@functools.lru_cache(maxsize=8)
def _read_csv_cached(csv_path, mtime):
    return pd.read_csv(csv_path)


def _read_csv(csv_path):
    return _read_csv_cached(csv_path, os.path.getmtime(csv_path))


def _default_csv_path():
    data_csvs = list_data_csvs()
    if not data_csvs:
        raise ValueError(
            "No csv_path given and no CSV found in 'data/'. Pass csv_path explicitly, "
            "or put a Sealog export CSV in 'data/'."
        )
    return data_csvs[0]


def get_event_value_types(csv_path=None):
    df = _read_csv(csv_path or _default_csv_path())
    return sorted(df["event_value"].dropna().unique().tolist())


def get_populated_event_option_columns(event_value, csv_path=None):
    csv_path = csv_path or _default_csv_path()
    df = _read_csv(csv_path)
    if event_value not in df["event_value"].dropna().unique():
        raise ValueError(f"event_value '{event_value}' not found in {csv_path}")

    event_option_columns = [col for col in df.columns if col.startswith("event_option.")]
    subset = df.loc[df["event_value"] == event_value, event_option_columns]
    counts = subset.notna().sum()
    return {col: int(count) for col, count in counts.items() if count > 0}


def get_data_group_prefixes(csv_path=None):
    df = _read_csv(csv_path or _default_csv_path())
    columns = [col for col in df.columns if col != "ts" and not col.startswith("event") and "." in col]
    return sorted({col.split(".", 1)[0] for col in columns})


def default_output_path(event_value, output_dir="output"):
    safe_event_name = event_value.replace(" ", "_").replace("/", "_")
    return os.path.join(output_dir, f"{safe_event_name}_filtered.csv")


def _fold_uom_into_value_columns(df, unit_lookup_df):
    rename_map = {}
    uom_columns_to_drop = []
    for col in df.columns:
        if not col.endswith("_value"):
            continue
        uom_col = col[: -len("_value")] + "_uom"
        if uom_col not in df.columns:
            continue
        uom_columns_to_drop.append(uom_col)
        units = unit_lookup_df[uom_col].dropna().unique()
        if len(units) > 0:
            base = col[: -len("_value")]
            rename_map[col] = f"{base}_{units[0]}"
    return df.drop(columns=uom_columns_to_drop).rename(columns=rename_map)


def build_filtered_dataframe(event_value, *data_group_prefixes, csv_path=None):
    csv_path = csv_path or _default_csv_path()
    df = _read_csv(csv_path)
    if event_value not in df["event_value"].dropna().unique():
        raise ValueError(f"event_value '{event_value}' not found in {csv_path}")

    valid_prefixes = get_data_group_prefixes(csv_path)
    invalid_prefixes = [p for p in data_group_prefixes if p not in valid_prefixes]
    if invalid_prefixes:
        raise ValueError(f"Unknown data group prefix(es) {invalid_prefixes}. Valid options: {valid_prefixes}")

    populated_option_columns = get_populated_event_option_columns(event_value, csv_path)
    columns = [
        col
        for col in df.columns
        if col == "id"
        or col == "ts"
        or (col.startswith("event") and not col.startswith("event_option."))
        or col in populated_option_columns
        or col.split(".", 1)[0] in data_group_prefixes
    ]
    filtered = df.loc[df["event_value"] == event_value, columns]
    return _fold_uom_into_value_columns(filtered, unit_lookup_df=df)


def export_event_csv(event_value, *data_group_prefixes, csv_path=None, output_path=None):
    csv_path = csv_path or _default_csv_path()
    filtered = build_filtered_dataframe(event_value, *data_group_prefixes, csv_path=csv_path)

    if output_path is None:
        output_path = default_output_path(event_value, output_dir=os.path.dirname(csv_path))
    elif os.path.isdir(output_path) or output_path.endswith(os.sep):
        output_path = default_output_path(event_value, output_dir=output_path)

    filtered.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    event_types = get_event_value_types()
    print(f"Found {len(event_types)} event_value types:")
    for event_type in event_types:
        print(f"  {event_type}")

    example_event = event_types[0]
    populated_columns = get_populated_event_option_columns(example_event)
    print(f"\nevent_option columns with data for '{example_event}':")
    for col, count in populated_columns.items():
        print(f"  {col}: {count} row(s)")
