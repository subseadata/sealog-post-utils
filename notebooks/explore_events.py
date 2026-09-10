import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Filter and Export from Sealog csv's
    """)
    return


@app.cell
def _():
    import os

    import marimo as mo

    from sealog_post_utils.sealog_post_utils import (
        build_filtered_dataframe,
        default_output_path,
        export_event_csv,
        get_data_group_prefixes,
        get_event_value_types,
        get_populated_event_option_columns,
        list_data_csvs,
    )

    return (
        build_filtered_dataframe,
        default_output_path,
        export_event_csv,
        get_data_group_prefixes,
        get_event_value_types,
        get_populated_event_option_columns,
        list_data_csvs,
        mo,
        os,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Choose the sealog data file
    """)
    return


@app.cell
def _(list_data_csvs, mo):
    data_csvs = list_data_csvs()
    if data_csvs:
        csv_path_dropdown = mo.ui.dropdown(
            options=data_csvs, value=data_csvs[0], label="Sealog export CSV (from data/)"
        )
    else:
        csv_path_dropdown = mo.ui.text(
            value="",
            placeholder="data/your_export.csv",
            label="No CSVs found in data/ — enter a path",
            full_width=True,
        )
    csv_path_dropdown
    return (csv_path_dropdown,)


@app.cell
def _(csv_path_dropdown, get_event_value_types, mo):
    csv_path = csv_path_dropdown.value or None
    try:
        event_types = get_event_value_types(csv_path)
    except Exception as e:
        mo.stop(True, mo.callout(str(e), kind="warn", title="Couldn't load the CSV"))
    mo.md(f"Found **{len(event_types)}** event types in `{csv_path}`.")
    return csv_path, event_types


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The event values found
    """)
    return


@app.cell
def _(event_types, mo):
    mo.md("\n".join(f"- `{event_type}`" for event_type in event_types))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Choose the event value to filter the csv by
    """)
    return


@app.cell
def _(event_types, mo):
    event_dropdown = mo.ui.dropdown(
        options=event_types, value=event_types[0], label="event_value"
    )
    event_dropdown
    return (event_dropdown,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The "Event options" that have information for the event value choosen
    """)
    return


@app.cell
def _(csv_path, event_dropdown, get_populated_event_option_columns, mo):
    populated_columns = get_populated_event_option_columns(
        event_dropdown.value, csv_path
    )
    mo.md(
        "**Populated `event_option.*` columns for this event type:**\n\n"
        + "\n".join(f"- `{col}`: {count}" for col, count in populated_columns.items())
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Choose the auxillary data to be kept
    """)
    return


@app.cell
def _(csv_path, get_data_group_prefixes, mo):
    data_group_prefixes = get_data_group_prefixes(csv_path)
    prefix_select = mo.ui.multiselect(
        options=data_group_prefixes, label="Data group prefixes to include in export"
    )
    prefix_select
    return (prefix_select,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Preview of the data that will be exported
    """)
    return


@app.cell
def _(build_filtered_dataframe, csv_path, event_dropdown, mo, prefix_select):
    try:
        preview_df = build_filtered_dataframe(
            event_dropdown.value, *prefix_select.value, csv_path=csv_path
        )
    except Exception as e:
        mo.stop(True, mo.callout(str(e), kind="warn", title="Couldn't build a preview"))
    mo.ui.table(preview_df.head())
    return (preview_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Choose how to get your filtered CSV
    """)
    return


@app.cell
def _(mo):
    save_mode = mo.ui.radio(
        options=["Save to disk", "Download"],
        value="Save to disk",
        label="",
    )
    save_mode
    return (save_mode,)


@app.cell
def _(default_output_path, event_dropdown, mo, save_mode):
    if save_mode.value == "Save to disk":
        output_path_input = mo.ui.text(
            value=default_output_path(event_dropdown.value),
            label="Output CSV path (a folder to auto-name into, or a full file path)",
            full_width=True,
        )
    else:
        output_path_input = None
    output_path_input
    return (output_path_input,)


@app.cell
def _(mo, save_mode):
    if save_mode.value == "Save to disk":
        export_button = mo.ui.run_button(label="Export filtered CSV")
    else:
        export_button = None
    export_button
    return (export_button,)


@app.cell
def _(
    csv_path,
    event_dropdown,
    export_button,
    export_event_csv,
    mo,
    output_path_input,
    prefix_select,
    save_mode,
):
    if save_mode.value != "Save to disk":
        export_result = None
    elif export_button.value:
        try:
            output_path = export_event_csv(
                event_dropdown.value,
                *prefix_select.value,
                csv_path=csv_path,
                output_path=output_path_input.value or None,
            )
            export_result = mo.callout(f"Exported to `{output_path}`", kind="success")
        except Exception as e:
            export_result = mo.callout(str(e), kind="danger", title="Export failed")
    else:
        export_result = mo.md("_Click the button above to export the filtered CSV._")
    export_result
    return


@app.cell
def _(default_output_path, event_dropdown, mo, os, preview_df, save_mode):
    if save_mode.value == "Download":
        download_filename = os.path.basename(default_output_path(event_dropdown.value))
        download_button = mo.download(
            data=lambda: preview_df.to_csv(index=False).encode("utf-8"),
            filename=download_filename,
            mimetype="text/csv",
            label="Download filtered CSV",
        )
    else:
        download_button = None
    download_button
    return


if __name__ == "__main__":
    app.run()
