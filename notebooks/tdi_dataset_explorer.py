# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "altair==6.2.2",
#     "anywidget==0.11.0",
#     "marimo>=0.24.0",
#     "matplotlib==3.11.2",
#     "numpy==2.3.5",
#     "pandas==3.0.5",
#     "rdkit==2026.3.6",
#     "scikit-learn==1.9.1",
#     "shap==0.52.0",
#     "traitlets==5.16.1",
#     "useful-rdkit-utils==0.96",
#     "xgboost==3.4.1",
# ]
# ///

import marimo

__generated_with = "0.24.0"
app = marimo.App(
    app_title="Understanding & exploring drug-drug interactions with OpenADMET",
)


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    # Shared look & size for the builtin mo.mermaid diagrams (bundled, no CDN).
    # fontSize drives the diagram size; colors mirror mermaid's classic "default".
    MMD_THEME = {
        "primaryColor": "#ECECFF",
        "primaryBorderColor": "#9370DB",
        "primaryTextColor": "#333333",
        "lineColor": "#333333",
        "fontSize": "21px",
    }
    return (MMD_THEME,)


@app.cell
def _():
    import os

    import altair as alt
    import numpy as np
    import pandas as pd
    import shap
    import xgboost as xgb

    return alt, np, os, pd, shap, xgb


@app.cell
def _(mo, os, pd):
    # Local checkout first (dev); anywhere else, fetch the one file we use
    # straight from Hugging Face (resolve follows redirects).
    _fname = "cyp-challenge-TRAIN_TDI.csv"
    _local = os.path.join(
        os.path.dirname(__file__), "..", "data", "raw", "openadmet_cyp_challenge", _fname
    )
    if os.path.exists(_local):
        _src = _local
        _where = "local checkout"
    else:
        _src = (
            "https://huggingface.co/datasets/openadmet/cyp-challenge-train-test"
            "/resolve/main/" + _fname
        )
        _where = "Hugging Face"
    with mo.status.spinner(title=f"Loading TDI training data from {_where}"):
        D = {"tdi": pd.read_csv(_src)}
    return (D,)


@app.cell
def _(D):
    df_tdi = D["tdi"]
    ISO = ["CYP1A2", "CYP2C9", "CYP2D6", "CYP3A4"]
    return ISO, df_tdi


@app.cell
def _():
    ISO_ABBREV = {
        "CYP1A2": "1A2",
        "CYP2C9": "2C9",
        "CYP2D6": "2D6",
        "CYP3A4": "3A4",
    }

    def classify_batch(df, iso):
        dcol = f"{iso}_pIC50_direct_inhibition"
        tcol = f"{iso}_pIC50_TDI_condition"
        out = df[dcol].notna() & df[tcol].notna()
        direct = df.loc[out, dcol]
        tdi = df.loc[out, tcol]
        shift = tdi - direct
        rule = (direct > 4) & (shift > 0.301) | (direct <= 4) & (tdi > 4.3)
        return out, rule, direct, tdi, shift

    return (classify_batch,)


@app.cell
def _(alt):
    _base_axis = dict(
        labelFont="Inter, sans-serif",
        labelFontSize=13,
        titleFont="Inter, sans-serif",
        titleFontSize=13,
        gridColor="#e5e7eb",
        gridWidth=0.6,
    )

    @alt.theme.register("Default", enable=True)
    def _default():
        return {}

    @alt.theme.register("Clean", enable=True)
    def _clean():
        return {
            "background": "#ffffff",
            "font": "Inter, sans-serif",
            "view": {"stroke": "transparent"},
            "axis": {**_base_axis, "grid": True},
            "axisX": {"domain": True, "domainColor": "#cbd5e1", "domainWidth": 1.2},
            "axisY": {"domain": False},
            "legend": {"titleFontSize": 13, "labelFontSize": 12, "labelLimit": 260},
        }

    @alt.theme.register("Paper", enable=True)
    def _paper():
        return {
            "background": "#faf9f6",
            "font": "Georgia, serif",
            "title": {"font": "Georgia, serif", "fontSize": 17, "color": "#1f2937"},
            "view": {"stroke": "#d1d5db", "strokeWidth": 1},
            "axis": {
                **_base_axis,
                "labelFont": "Georgia, serif",
                "titleFont": "Georgia, serif",
                "grid": True,
                "gridColor": "#e7e5e4",
            },
            "axisX": {"domain": True, "tickColor": "#d1d5db"},
            "legend": {"labelFont": "Georgia, serif", "titleFont": "Georgia, serif"},
        }

    @alt.theme.register("Ink (dark)", enable=True)
    def _ink():
        return {
            "background": "#0f1115",
            "font": "Inter, sans-serif",
            "title": {"color": "#f9fafb"},
            "view": {"stroke": "transparent"},
            "axis": {
                **_base_axis,
                "labelColor": "#d1d5db",
                "titleColor": "#e5e7eb",
                "grid": True,
                "gridColor": "#1f2937",
                "gridDash": [2, 2],
            },
            "axisX": {"domain": True, "domainColor": "#374151", "tickColor": "#374151"},
            "legend": {
                "labelColor": "#d1d5db",
                "titleColor": "#e5e7eb",
                "labelFontSize": 12,
            },
        }

    return


@app.cell
def _(mo):
    mo.md(r"""
    # Understanding & exploring drug–drug interactions with OpenADMET
    #### A case study in CYP time‑dependent inhibition (TDI)

    **Data:** [`openadmet/cyp-challenge-train-test`](https://huggingface.co/datasets/openadmet/cyp-challenge-train-test)
    · OpenADMET CYP Inhibition Blind Challenge · **License:** Apache‑2.0

    Most drug–drug interactions begin with a stalled enzyme. **Cytochromes
    P450 (CYPs)** clear most small‑molecule drugs — and a compound that
    *quietly disables a CYP over time* (**time‑dependent inhibition, TDI**)
    slows the clearance of every co‑administered **victim drug**, letting its
    exposure climb. Instant screens can pass such compounds as clean, because
    the damage only appears once the enzyme has spent time working on the
    inhibitor.

    This notebook walks the full arc with the OpenADMET challenge data —
    use the outline below to jump around.
    """)
    return


@app.cell
def _(mo):
    mo.outline(label="Jump to a section")
    return


@app.cell
def _(mo):
    theme_sel = mo.ui.radio(
        options=["Default", "Clean", "Paper", "Ink (dark)"],
        value="Clean",
        label="Chart style — switch to re-render every chart",
        inline=True,
    )
    return (theme_sel,)


@app.cell
def _(mo):
    mo.md(r"""
    ## 0 · The assay, told by its widgets

    Start with the panel below: flip the toggle and watch a perpetrator drug
    stall a CYP while its victim piles up. The sections that follow unpack
    what the machine behind that story actually measures.
    """)
    return


@app.cell
def _():
    # Self-contained anywidgets, inlined 1:1 from src/openadmet_tdi/widgets/
    # so the notebook deploys as a single file (e.g. to molab).
    import anywidget
    import traitlets

    ICON_URIS = {
                "liver": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZlcnNpb249IjEuMCIgdmlld0JveD0iMCAwIDMyOS4yMzUgMjc1LjIyNSI+PGRlZnM+PGNsaXBQYXRoIGNsaXBQYXRoVW5pdHM9InVzZXJTcGFjZU9uVXNlIiBpZD0iYSI+PHBhdGggZD0iTTMuOTE4IDEzLjgzMmgzMjguODR2Mjc1LjQzM0gzLjkxOHoiLz48L2NsaXBQYXRoPjwvZGVmcz48cGF0aCBjbGlwLXBhdGg9InVybCgjYSkiIGQ9Ik0yMzQuNjk4IDM0LjU0YzEyLjA3Mi0zLjk5OSAzNS4zNzgtMy4xMTkgNTIuMDQ4LTEuNzYgMTYuMjMgMS4zMiAxOS41NDggMCAzMi4wMiAxLjMyIDE0Ljk5MiAxLjMxOSAxNS4zOTEgNDQuNDUyIDcuOTE2IDU3LjMyNS03LjA3NiAxMi44NzItMTUuODMgMTYuODctMjYuMjI0IDM0LjY1OS0xMC4zOTQgMTcuMzEtMjQuOTg1IDM0LjIxOS00MC43NzUgMzkuMDk2LTE1LjgzIDQuNDM3LTI4Ljc0My02LjY3Ni0zNS4zNzkgNC44NzctNi42NzYgMTEuOTkzLTE5Ljk4OCAyNi4yMjQtNDMuMjk0IDM0LjY1OS0yMy4zMDYgOC40MzUtNjYuMiAzMi40Ni04NS4zNDggNTEuNTI5LTE5LjU0OCAxOS4xMDgtNDEuMTc1IDM4LjY1Ni02Ny44MzkgMjkuMzQyLTI3LjA2My05LjMxNC0xNS43OS02MC40NDMtMTcuMDctNzguNjMyLTEuMjM5LTE4LjY3LTkuOTkzLTQ5Ljc3LTMuMzE4LTEwMC44NkMxMi44MzIgNjcgMjMuNjY1IDM0Ljk4IDU1LjI4NiAyMi4xMDggMTA4LjE3NC43NiAxOTcuMjQgMzMuMjIgMjE5LjMwNyAzNi43NzdjNS4zOTcuODggMTAuMzk0LTEuMzU4IDE1LjM5LTIuMjM4eiIgZmlsbD0iIzg3NTI2MCIgZmlsbC1ydWxlPSJldmVub2RkIi8+PHBhdGggY2xpcC1wYXRoPSJ1cmwoI2EpIiBkPSJNMTUyLjgyNyAyOS4zNDJjLTIwLjM4Ny03LjExNS03NS43NTQtMTUuNTUtMTAyLjQxOCAxLjc2LTI2LjY2MyAxNi44NjktMzUuMzc4IDUyLjM2Ny0zNy40OTcgOTAuOTQ0QzE2LjY3IDEwMi4wOTggMjMuNzQ2IDQ2LjY1MiA1NS40MDYgMzIuOWMzMi4wNjEtMTMuNzUyIDY1LjM2LTkuMzE0IDk3LjQyMS0zLjU1OHoiIGZpbGw9IiNmZmYiIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjxwYXRoIGQ9Ik02Ni4yIDQyLjE3NGMtMzMuNzQgMTUuNTUxLTQwLjQxNiA1NS4wODctNDIuNDk0IDc4LjE5My0yLjUxOSAyMy4xMDYtMS42OCA4MC44MzEtNi4yMzcgOTguNTggMS42NC0xMy43NTEtNy4xMTUtNTguNjA0LTQuOTk3LTk3LjI2QzE0LjU1MiA4My4wMyAyNS43ODQgNDkuMjkgNTIuNDQ4IDMyLjQyYzI2LjY2NC0xNy4zNSA5MC4zODUtOC44NzQgMTExLjE3My0xLjc5OS0xMi40NzMtMi42MzgtNjUuOC0zLjA3OC05Ny40MjEgMTEuNTUzeiIgZmlsbD0iI2EzNzU3ZiIgZmlsbC1ydWxlPSJldmVub2RkIi8+PHBhdGggZD0iTTMwMy40MTYgMTEyLjc3MmMzLjMxOC0yLjIzOSAyLjkxOC44OCAwIDQuNDM3LTEyLjA3MyAxNC4yMzEtMTguMzA5IDM0LjY1OS0zOS4xMzYgNDMuOTczLTE1Ljc5IDcuNTU2LTI5LjE0My0yLjYzOC0zNC45MzkuODgtNS40MzcgMy41NTgtMTIuNTEyIDE1LjExLTIzLjc0NiAyNS43ODQtMTEuMjMzIDEwLjY3NC0zMC4zODEgMTUuOTktNTkuNTI0IDI5Ljc4Mi0yOC43NDIgMTMuNzUyLTQyLjQ1NCAyNi42NjQtNTguNzI0IDQxLjI5NSAxMy4zNTItMTYuNDMgNDEuNjU1LTQzLjA5NCA1OC4yODUtNTEuOTY4IDE2LjY3LTguODc1IDU2LjIwNi0yOS43ODIgNjcuODc5LTQ5LjMzIDExLjYzMy0xOS41NDkgNC45OTctMzcuMjk4IDUuODM2LTU4LjY0NSAxLjI0LTIxLjMwNyA5LjE1NS00Mi42NTQgNi4yMzYtNTYuODg2IDMuMzE4IDguNDc1IDQuNTU4IDE5LjEwOSAzLjc1OCAzMi4wMjEtLjQ0IDEzLjMxMi0uODQgMjMuOTg2IDEuNjM5IDM2Ljg1OCAyLjkxOCAxMi45MTIgMy4zMTggMjcuOTgzIDMuMzE4IDMzLjc4IDAgNS43NTYgMTkuNTg4IDcuNTU1IDM0Ljk3OS0yLjI0IDEyLjA3Mi03Ljk5NSAyMy4zMDYtMjIuMTg2IDM0LjE0LTI5Ljc0MXoiIGZpbGw9IiM3YjQyNTIiIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjxwYXRoIGQ9Ik0zMjMuODg0IDQyLjA5NGM2LjY3NiAxMi40NzMgNS44NzYgMzMuNzggMCA0Ni4yMTItMi41MTkgNS43OTctOC4zNTUgMTMuNzkyLTEyLjU1MyAxOC42Ny0xLjIzOSAxLjc1OC04LjM1NSAxMS4xMTItMTAuNDczIDEyLjQzMi0yLjUxOSAxLjc1OSAwLTMuNTU4LTIuMDgtMS4zMiA4Ljc5Ni0xMi45MTIgMjMuMDI3LTI2LjY2MyAyNS45NDUtNDMuMDkzIDEuMjQtNy45OTYgMy4zNTgtMjMuNTQ2LS44NC0zMS4xMDJ6IiBmaWxsPSIjN2I0MjUyIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiLz48cGF0aCBkPSJNMjMzLjUzOCA1OS45MjRjMS4yNCAxMS4xMTMtMS42NzkgMjEuMzA3LjggMzYuODE3IDIuNTE4IDE1LjU1IDUuODM2IDMzLjc0IDQuNTk3IDQzLjkzNC44NC04Ljg3NS44NC0zMC42MjIgMC00My4wMTQtLjg0LTEyLjQzMy0xLjI0LTM0LjE4LjQtNDAuNDE2IDEuNjc5LTYuMTk2IDYuMjc2LTE3Ljc0OSAyOC43NDMtMTYuMzkgMjIuNTA2IDEuMzIgMzEuNjYtMS4zNTkgMzQuOTc4LTEuNzk5LTQuNTU3IDAtMjkuMTQyLjQ0LTM4LjI5Ni0uODgtOS4xNTUtMS4zMTgtMzMuMzQtMi4yMzgtMzEuMjIyIDIxLjc0OHoiIGZpbGw9IiNhMzc1N2YiIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjxwYXRoIGQ9Ik0yMzEuMSAxMTkuODg3YzIuMDc5IDEwLjY3NCA0Ljk1NyA0OS42OS0zMy4zNCA3Mi43NTYgMTAuODM0LTYuNjM2IDMyLjUtMjcuOTQzIDMzLjM0LTcyLjc1NnptNTYuNDQ2IDIwLjc4OGMtOS45NTQgMTIuOTEyLTE3LjQzIDE4LjI2OS0yNi45ODQgMjEuNzg3LTkuNTU0IDMuNTU3LTE5LjkwOC0uNDQtMjQuNTA1LTEuMzIgNC45OTcgMCAxMy4zMTIgMy4xMTggMjYuMTg0LTIuMTk4IDEyLjg3Mi01Ljc5NyAyMy4yNjYtMTYuMDMgMjUuMzA1LTE4LjI3eiIgZmlsbD0iIzY4MmU0MCIgZmlsbC1ydWxlPSJldmVub2RkIi8+PHBhdGggY2xpcC1wYXRoPSJ1cmwoI2EpIiBkPSJNMjM0LjY5OCAzNC41NGMxMi4wNzItMy45OTkgMzUuMzc4LTMuMTE5IDUyLjA0OC0xLjc2IDE2LjIzIDEuMzIgMTkuNTQ4IDAgMzIuMDIgMS4zMiAxNC45OTIgMS4zMTkgMTUuMzkxIDQ0LjQ1MiA3LjkxNiA1Ny4zMjUtNy4wNzYgMTIuODcyLTE1LjgzIDE2Ljg3LTI2LjIyNCAzNC42NTktMTAuMzk0IDE3LjMxLTI0Ljk4NSAzNC4yMTktNDAuNzc1IDM5LjA5Ni0xNS44MyA0LjQzNy0yOC43NDMtNi42NzYtMzUuMzc5IDQuODc3LTYuNjc2IDExLjk5My0xOS45ODggMjYuMjI0LTQzLjI5NCAzNC42NTktMjMuMzA2IDguNDM1LTY2LjIgMzIuNDYtODUuMzQ4IDUxLjUyOS0xOS41NDggMTkuMTA4LTQxLjE3NSAzOC42NTYtNjcuODM5IDI5LjM0Mi0yNy4wNjMtOS4zMTQtMTUuNzktNjAuNDQzLTE3LjA3LTc4LjYzMi0xLjIzOS0xOC42Ny05Ljk5My00OS43Ny0zLjMxOC0xMDAuODZDMTIuODMyIDY3IDIzLjY2NSAzNC45OCA1NS4yODYgMjIuMTA4IDEwOC4xNzQuNzYgMTk3LjI0IDMzLjIyIDIxOS4zMDcgMzYuNzc3YzUuMzk3Ljg4IDEwLjM5NC0xLjM1OCAxNS4zOS0yLjIzOCIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMzMzIiBzdHJva2Utd2lkdGg9Ii44IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz48cGF0aCBkPSJNMjE5Ljc0NyAzNy4yMTdjMTAuODczIDEuOCAxMC4wMzQgMjcuMTQ0IDguNzk0IDQ3LjU3Mi0xLjIzOSAyMC40MjcgMTMuMzUyIDUzLjc2Ny0xLjY3OCA4Mi4xOSIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMzMzIiBzdHJva2Utd2lkdGg9Ii44IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiLz48L3N2Zz4=",
        "enzyme_yellow": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZlcnNpb249IjEuMCIgdmlld0JveD0iMCAwIDY5LjkyMSA4Mi4wNTQiPjxkZWZzPjxjbGlwUGF0aCBjbGlwUGF0aFVuaXRzPSJ1c2VyU3BhY2VPblVzZSIgaWQ9ImEiPjxwYXRoIGQ9Ik0tLjI0LS4yNGg2OS43OTh2ODIuMTFILS4yNHoiLz48L2NsaXBQYXRoPjwvZGVmcz48cGF0aCBkPSJNMzQuOTc5IDgwLjcxMUMxNS43OSA4MC43MTEuNzU5IDU4Ljk2NC43NTkgNDAuNzM1Ljc2IDIyLjU0NiAxOS4xMS43NiAzNC45OC43NmMxNS44MyAwIDMzLjc0IDExLjU1MyAzMy43NCAxMS41NTNINTcuMDQ0bDIuNTE5IDExLjExMy0xMS42NzMuNDQgNC4xNTcgOS4zNTQtMTIuMDcyIDUuMzE3IDEwLjgzMyA2LjE5Ni00Ljk5NyAxMC42NzMgMTIuMDczLjQ0LTIuMDc5IDExLjExMyAxMS42NzMuODhTNTQuNTY3IDgwLjcxIDM0Ljk4IDgwLjcxeiIgZmlsbD0iI2ZmYzIwMCIgZmlsbC1ydWxlPSJldmVub2RkIiBmaWxsLW9wYWNpdHk9IjEiIHN0cm9rZT0ibm9uZSIvPjxwYXRoIGQ9Ik0zMy43IDMuMzk4QzE5LjE0OCA1LjE5NyAzLjcxOCAyNC43NDUgMy43MTggNDAuNjk1YzAgMTUuOTkgMTEuNjczIDM0LjY2IDI4LjM0MyAzNy4yOThDMTguMzA5IDcyLjIzNiA4LjcxNSA1NS4zNjYgOC43MTUgNDAuNjk1YzAtMTQuNjMgMTIuMTEyLTMxLjUgMjQuOTg1LTM3LjI5N3oiIGZpbGw9IiNmZWUwNzUiIGZpbGwtcnVsZT0iZXZlbm9kZCIgZmlsbC1vcGFjaXR5PSIxIiBzdHJva2U9Im5vbmUiLz48cGF0aCBkPSJNNS4zOTcgNDAuNjk1YzAtMTQuMjMxIDExLjY3My0zMC43MDEgMjQuMTQ1LTM2LjQ5OEMxNi4yMyA4LjY3NSAzLjcxOCAyNi4wMjQgMy43MTggNDAuNjk1YzAgMTQuNzExIDkuNTk0IDMxLjE4MSAyMy4zNDYgMzYuNDk4QzE0LjE1IDcwLjk5NyA1LjM5NyA1NC45NjcgNS4zOTcgNDAuNjk1eiIgZmlsbD0iI2ZmZiIgZmlsbC1ydWxlPSJldmVub2RkIiBmaWxsLW9wYWNpdHk9IjEiIHN0cm9rZT0ibm9uZSIvPjxwYXRoIGNsaXAtcGF0aD0idXJsKCNhKSIgZD0iTTM0Ljk3OSA4MC43MTFDMTUuNzkgODAuNzExLjc1OSA1OC45NjQuNzU5IDQwLjczNS43NiAyMi41NDYgMTkuMTEuNzYgMzQuOTguNzZjMTUuODMgMCAzMy43NCAxMS41NTMgMzMuNzQgMTEuNTUzSDU3LjA0NGwyLjUxOSAxMS4xMTMtMTEuNjczLjQ0IDQuMTU3IDkuMzU0LTEyLjA3MiA1LjMxNyAxMC44MzMgNi4xOTYtNC45OTcgMTAuNjczIDEyLjA3My40NC0yLjA3OSAxMS4xMTMgMTEuNjczLjg4UzU0LjU2NyA4MC43MSAzNC45OCA4MC43MSIgZmlsbD0ibm9uZSIgc3Ryb2tlPSIjMzMzIiBzdHJva2Utd2lkdGg9Ii43OTk1MTU0M3B4IiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiIHN0cm9rZS1taXRlcmxpbWl0PSI0IiBzdHJva2UtZGFzaGFycmF5PSJub25lIiBzdHJva2Utb3BhY2l0eT0iMSIvPjwvc3ZnPg==",
        "drug_tablet": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZlcnNpb249IjEuMCIgdmlld0JveD0iMCAwIDIyMy45NzUgMjExLjg4Ij48ZGVmcz48Y2xpcFBhdGggY2xpcFBhdGhVbml0cz0idXNlclNwYWNlT25Vc2UiIGlkPSJhIj48cGF0aCBkPSJNMS45OTkgMi4yMzloMjIzLjcwNFYyMTQuMjdIMnoiLz48L2NsaXBQYXRoPjwvZGVmcz48cGF0aCBkPSJNMjIzLjk4NCAxMDguMDc1YzAgNTMuNjI3LTQ5Ljc5IDEwNC45NTYtMTEwLjY5MyAxMDQuOTU2LTYxLjEyMyAwLTExMC42OTMtNTAuMzMtMTEwLjY5My0xMDMuNjk3IDAtNTMuNjA4IDQ5LjU3LTg5Ljg2NiAxMTAuNjkzLTg5Ljg2NiA2MC45MDMgMCAxMTAuNjkzIDM1LjIzOSAxMTAuNjkzIDg4LjYwNnoiIGZpbGw9IiNlNGUyYjMiIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjxwYXRoIGQ9Ik0yLjgzOCA5OS45NGMwLTUzLjQ0OCA0OS40Ny05Ni43ODIgMTEwLjQ5My05Ni43ODIgNjEuMDIzIDAgMTEwLjQ5MyA0My4zMzQgMTEwLjQ5MyA5Ni43ODEgMCA1My40NjgtNDkuNDcgOTYuNzgyLTExMC40OTMgOTYuNzgyLTYxLjAyMyAwLTExMC40OTMtNDMuMzE0LTExMC40OTMtOTYuNzgyeiIgZmlsbD0iI2VmZWJjYSIgZmlsbC1ydWxlPSJldmVub2RkIi8+PHBhdGggZD0iTTcuNzk1IDEwMC4wNmMwLTUxLjE3IDQ3LjI5Mi05Mi42NjQgMTA1LjYxNi05Mi42NjQgNTguMzQ1IDAgMTA1LjYxNiA0MS40OTQgMTA1LjYxNiA5Mi42NjMgMCA1MS4xOS00Ny4yNzEgOTIuNjY0LTEwNS42MTYgOTIuNjY0LTU4LjMyNCAwLTEwNS42MTYtNDEuNDc1LTEwNS42MTYtOTIuNjY0eiIgZmlsbD0iI2U0ZTJiMyIgZmlsbC1ydWxlPSJldmVub2RkIi8+PHBhdGggZD0iTTExMy4yNTEgNy4zOTZDNTQuOTg3IDcuMzk2IDcuNzk1IDQ4Ljk1IDcuNzk1IDEwMC4wNTljMCAzNC43NiAyMS45NDcgNjUuMjIgNTQuMjY3IDgxLjA3MSAwIDAtMzMuOTU5LTk2LjE4MSA1MS4xOS0xNzMuNzM0eiIgZmlsbD0iI2QyY2I5NiIgZmlsbC1ydWxlPSJldmVub2RkIi8+PHBhdGggZD0iTTIxMC4xMzMgNzQuOTE1Yy0zLjA3OCAxNS42MS0yOC4zNDMgMjcuOTQzLTUyLjIwOSAyMi4xNjYtMjQuMDg1LTUuNTM2LTM3Ljc5Ny0yNi45NDQtMzQuNzE5LTQyLjU1NCAzLjMxOC0xNS42MSAyNC4zMjYtMjYuMTg0IDQ4LjE5MS0yMC42MjggMjQuMDg2IDUuNzc3IDQyLjAzNSAyNS40MjUgMzguNzM3IDQxLjAxNnoiIGZpbGw9IiNlZGU4YzIiIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjxwYXRoIGQ9Ik0xMjYuNjAzIDE4OS4yMDVzNjUuMzgtMS43NTkgODcuNTQ3LTY3LjIzOWMwIDAtMjUuNDg0IDQ4LjYxLTg3LjU0NyA2Ny4yNHoiIGZpbGw9IiNmZmYiIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjxwYXRoIGQ9Ik0xNzguNDkyIDE1OS40NjNjMC0xLjY1OSAyLjI3OC0zLjAzOCA1LjA3Ny0zLjAzOCAyLjgxOCAwIDUuMDc3IDEuMzggNS4wNzcgMy4wMzggMCAxLjY4LTIuMjU5IDMuMDM5LTUuMDc3IDMuMDM5LTIuNzk5IDAtNS4wNzctMS4zNi01LjA3Ny0zLjAzOXptLTguMDc1IDQuMzE3YzAtMS4wOTkgMS4xMTktMS45OTggMi40NzgtMS45OTggMS4zOCAwIDIuNDc5LjkgMi40NzkgMS45OTkgMCAxLjEyLTEuMSAxLjk5OS0yLjQ3OSAxLjk5OS0xLjM1OSAwLTIuNDc4LS44OC0yLjQ3OC0yeiIgZmlsbD0iI2ZmZiIgZmlsbC1ydWxlPSJldmVub2RkIi8+PHBhdGggZD0iTTMuNTU4IDExMi44NTJzNy4wOTYgNzMuMzE1IDk2LjM0MSA4My42NDlsLS45MzkgMTQuODVzLTg2LjQyOC05LjgxMy05NS40MDItOTguNXoiIGZpbGw9IiNkOGQxYTciIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjxwYXRoIGNsaXAtcGF0aD0idXJsKCNhKSIgZD0iTTMuMTU4IDEwMC4yMmMwLTUzLjQ2OCA0OS40NS05Ni44MjIgMTEwLjQxMy05Ni44MjIgNjAuOTgzIDAgMTEwLjQxMyA0My4zNTQgMTEwLjQxMyA5Ni44MjEgMCA1My40ODgtNDkuNDMgOTYuODIyLTExMC40MTMgOTYuODIyLTYwLjk2MyAwLTExMC40MTMtNDMuMzM0LTExMC40MTMtOTYuODIyIiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmYiIHN0cm9rZS13aWR0aD0iLjgiIHN0cm9rZS1taXRlcmxpbWl0PSI4Ii8+PHBhdGggZD0iTTk3LjI2MSAyMDMuMzU3YzAtMy4xMTggMS4zLTUuNjc3IDIuODc4LTUuNjc3IDEuNiAwIDIuODc5IDIuNTU5IDIuODc5IDUuNjc3IDAgMy4xMzgtMS4yOCA1LjY3Ni0yLjg3OSA1LjY3Ni0xLjU3OSAwLTIuODc4LTIuNTM4LTIuODc4LTUuNjc2em0uMjM5IDcuMDc1YzAtLjc2LjYtMS4zOTkgMS4zMi0xLjM5OS43NCAwIDEuMzIuNjQgMS4zMiAxLjQgMCAuNzc5LS41OCAxLjM5OS0xLjMyIDEuMzk5LS43MiAwLTEuMzItLjYyLTEuMzItMS40eiIgZmlsbD0iI2U0ZTJiMyIgZmlsbC1ydWxlPSJldmVub2RkIi8+PHBhdGggZD0iTTIuODM4IDExMi4yMTJzMS4yIDYzLjcwMSA2OC4yNzkgOTEuMzg1YzAgMC01OS4wNjQtMjguNjgzLTY4LjI3OS05MS4zODV6IiBmaWxsPSIjYzRiYTdkIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiLz48cGF0aCBjbGlwLXBhdGg9InVybCgjYSkiIGQ9Ik0yMjQuMzI0IDEwMS4wNTl2LTFjMC01My42MDctNDkuMzMtOTYuOS0xMTAuNDczLTk2LjktNjAuODgzIDAtMTEwLjQ1MyA0My4yOTMtMTEwLjQ1MyA5Ni45djEuMjZjLS4yNCAyLjQ5OC0uMjQgNS4yNzYtLjI0IDguMDM1IDAgNTMuMzQ3IDQ5LjU3IDEwMy42NzcgMTEwLjY5MyAxMDMuNjc3IDYwLjkwMyAwIDExMC42OTMtNTEuMzI5IDExMC42OTMtMTA0LjkzNyAwLTIuMjU4IDAtNC43NzctLjIyLTcuMDM1IiBmaWxsPSJub25lIiBzdHJva2U9IiMzNDM0MzQiIHN0cm9rZS13aWR0aD0iLjgiIHN0cm9rZS1taXRlcmxpbWl0PSI4Ii8+PHBhdGggZD0iTTY1LjIgMTg2LjU2N2MtNC40OTctMS45NzktOC43NTQtNC4yMTgtMTMuMDMyLTYuNzE2bTMzLjU4IDEzLjU5MmMtMy45NzgtMS4wMi03Ljc1NS0yLjAzOS0xMS43NTMtMy41OThtMTYuMzkgNC41NTdjLS42OC0uMi0xLjM3OS0uMi0yLjMxOC0uNG00MC44NTUgMS43MTljLTQuOTU3Ljc2LTkuNjc0IDEtMTQuNjMxIDEtNy4zMTYgMC0xNC40MTItLjc0LTIxLjI2Ny0xLjc2IiBmaWxsPSJub25lIiBzdHJva2U9IiMzNDM0MzQiIHN0cm9rZS13aWR0aD0iLjMyIiBzdHJva2UtbWl0ZXJsaW1pdD0iOCIvPjxwYXRoIGNsaXAtcGF0aD0idXJsKCNhKSIgZD0iTTI1LjUyNSAxNTcuMzg1QzExLjgzMyAxNDEuMjk1IDMuNzk4IDEyMS40MDYgMy43OTggOTkuNzhjMC01My4zNDggNDkuNTktOTYuNjIyIDExMC40OTMtOTYuNjIyIDYxLjE2MyAwIDExMC40OTMgNDMuMjc0IDExMC40OTMgOTYuNjIyIDAgMjAuODg3LTcuNTU2IDQwLjI1NS0yMC4yODggNTYuMTA2IiBmaWxsPSJub25lIiBzdHJva2U9IiMzNDM0MzQiIHN0cm9rZS13aWR0aD0iLjMyIiBzdHJva2UtbWl0ZXJsaW1pdD0iOCIvPjxwYXRoIGQ9Ik0zMS42MiAxNjYuNWMwLTEuMS44Ni0yIDEuOTItMiAxLjA1OSAwIDEuOTE5LjkgMS45MTkgMiAwIDEuMTE4LS44NiAxLjk5OC0xLjkyIDEuOTk4LTEuMDU5IDAtMS45MTgtLjg4LTEuOTE4LTEuOTk5em0zLjk5OCA0LjQ3NmMwLS43NC41OC0xLjM1OSAxLjI4LTEuMzU5LjcyIDAgMS4yNzkuNjIgMS4yNzkgMS4zNiAwIC43NTktLjU2IDEuMzU5LTEuMjggMS4zNTktLjY5OSAwLTEuMjc5LS42LTEuMjc5LTEuMzZ6bTExOC43MjggMTkuMTA5YzAtLjY2LjYtMS4yIDEuMzItMS4yLjc0IDAgMS4zMTkuNTQgMS4zMTkgMS4yIDAgLjY4LS41OCAxLjItMS4zMiAxLjItLjcxOSAwLTEuMzE5LS41Mi0xLjMxOS0xLjJ6bTQuMzE4LTEuNDM5YzAtLjMuMzYtLjU2LjgtLjU2LjQ2IDAgLjc5OS4yNi43OTkuNTYgMCAuMzItLjM0LjU2LS44LjU2LS40NCAwLS44LS4yNC0uOC0uNTZ6IiBmaWxsPSIjZmZmIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiLz48cGF0aCBkPSJNMjYuMDI0IDQ4LjI1YzE4Ljg4OS0yNC40MjQgNTAuOTctNDAuNTM1IDg3LjMwNy00MC41MzUgNTguMjg1IDAgMTA1LjY5NiA0MS41MzUgMTA1LjY5NiA5Mi42MjQgMCAxLjk5OSAwIDQuMjc4LS4yMiA2LjI3Nk0xOC41ODkgNTkuMDQ0YTc0Ljc1NSA3NC43NTUgMCAwIDEgNS4xMTctNy41MTVtLTkuOTk0IDE4LjA2OWMtNC4wMTggOS41NzQtNS45MTcgMTkuOTA4LTUuOTE3IDMwLjc0MSAwIDkuMDU1IDEuNDQgMTguMTMgNC4yNzggMjYuNDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNmZmYiIHN0cm9rZS13aWR0aD0iLjQ4IiBzdHJva2UtbWl0ZXJsaW1pdD0iOCIvPjxwYXRoIGQ9Ik02LjgzNiA3Ni4xNTRzMTYzLjA4MSAyMi45MDYgMjE1LjQ3IDQzLjAxNGMwIDAtMTc4Ljg3Mi0yMy4zODYtMjE1LjQ3LTQzLjAxNHoiIGZpbGw9IiNiZmI4OGIiIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjxwYXRoIGQ9Ik0xMzUuNzE4IDQuOTE3Uzk2Ljg0IDk5LjM0IDgxLjUxIDE5Mi40ODNjMCAwIDM4Ljg5Ni0xMDguNzU0IDU0LjIwNy0xODcuNTY2eiIgZmlsbD0iI2JmYjg4YiIgZmlsbC1ydWxlPSJldmVub2RkIi8+PHBhdGggZD0iTTE0LjI3MSA3OC4zOTIgMjE0Ljc5IDExNy42NVMyMS4zNjcgODMuMTg5IDE0LjI3IDc4LjM5MnoiIGZpbGw9IiM4OTgyNTkiIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjxwYXRoIGQ9Ik0xMzMuMTYgMTMuNDcyIDgzLjQzIDE4NC4wODhzNDMuMzczLTE2MC41NDIgNDkuNzMtMTcwLjYxNnoiIGZpbGw9IiM4OTgyNTkiIGZpbGwtcnVsZT0iZXZlbm9kZCIvPjxwYXRoIGQ9Ik01NS4wNDcgODEuNjlzNDUuNjEyIDcuNTU2IDUwLjExIDguMjk1YzAgMCAyMC4wODctNTkuODQzIDI0LjMyNS02OS4xNThsLTI0LjMyNiA2MC4zNjRzLTIuODM4IDMuNTE4LTcuMDk1IDQuMjc3Yy00LjI1OC43Ni00My4wMTQtMy43NzgtNDMuMDE0LTMuNzc4em01LjM1NiAxMC4xMzQgNDIuMDU1IDguNTU1cy0xNC4xNzIgNTQuMDA3LTE0LjE3MiA1Ny4wMDZsMTAuNjM0LTUyLjc0OHMtLjI0LTIuOTk5LTIuMzU5LTIuOTk5Yy0yLjExOCAwLTM2LjE1OC05LjgxNC0zNi4xNTgtOS44MTR6IiBmaWxsPSIjZWRlOGMyIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiLz48cGF0aCBkPSJtMTU4LjkwNCAxMDkuMjE0LTQ3LjQ5Mi03Ljc5NS0xNi43OSA1Mi4yODggMTYuNTUtNDcuNzUxczEuNjYtMS43NiA0LjAxOC0xLjc2YzIuMzU5LjI0IDQzLjcxNCA1LjAxOCA0My43MTQgNS4wMTh6TTExNC4xMyA5MS41NDVsNy4zMTYtMjQuNjY2LTQuNDc3IDIxLjE0OHMwIDIuNTE4IDEuMTggMi43NThjMS40MTkgMCAzMy4yNCA4LjU1NSAzMy4yNCA4LjU1NXMtMzUuNi03LjUzNi0zNy4yNTgtNy43OTV6IiBmaWxsPSIjZmZmIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiLz48cGF0aCBkPSJNODEuNTEgMTkyLjQ4M3YxNS4wMzFzLjY0LTEyLjI3MiAwLTE1LjAzeiIgZmlsbD0iI2JmYjg4YiIgZmlsbC1ydWxlPSJldmVub2RkIi8+PC9zdmc+",
        "pill_blue": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB2aWV3Qm94PSIwIDAgMzEuNDYgMTIuNjMiPjxkZWZzPjxzdHlsZT4uY2xzLTEsLmNscy0ye3N0cm9rZTojMjMxZjIwO3N0cm9rZS13aWR0aDowLjI5cHg7fS5jbHMtMXtzdHJva2UtbWl0ZXJsaW1pdDoxMDtmaWxsOnVybCgjbGluZWFyLWdyYWRpZW50KTt9LmNscy0ye3N0cm9rZS1saW5lY2FwOnJvdW5kO3N0cm9rZS1saW5lam9pbjpyb3VuZDtmaWxsOnVybCgjbGluZWFyLWdyYWRpZW50LTIpO308L3N0eWxlPjxsaW5lYXJHcmFkaWVudCBpZD0ibGluZWFyLWdyYWRpZW50IiB4MT0iLTEyMi43NCIgeTE9Ii01Ni44NSIgeDI9Ii0xMjIuNzQiIHkyPSItNjcuMjkiIGdyYWRpZW50VHJhbnNmb3JtPSJ0cmFuc2xhdGUoMTM4LjQ3IDY4LjQxKSIgZ3JhZGllbnRVbml0cz0idXNlclNwYWNlT25Vc2UiPjxzdG9wIG9mZnNldD0iMCIgc3RvcC1jb2xvcj0iIzQzYWVlMyIvPjxzdG9wIG9mZnNldD0iMC4wMyIgc3RvcC1jb2xvcj0iIzQyYWFlMSIvPjxzdG9wIG9mZnNldD0iMC40OSIgc3RvcC1jb2xvcj0iIzM2NmJiNyIvPjxzdG9wIG9mZnNldD0iMC44MyIgc3RvcC1jb2xvcj0iIzJlNDM5ZCIvPjxzdG9wIG9mZnNldD0iMSIgc3RvcC1jb2xvcj0iIzJiMzQ5MyIvPjwvbGluZWFyR3JhZGllbnQ+PGxpbmVhckdyYWRpZW50IGlkPSJsaW5lYXItZ3JhZGllbnQtMiIgeDE9Ii0xMTUuNTYiIHkxPSItNTYuODUiIHgyPSItMTE1LjU2IiB5Mj0iLTY3LjI5IiBncmFkaWVudFRyYW5zZm9ybT0ibWF0cml4KC0xLCAtMC4wOSwgMC4wOSwgLTEsIC0xMDEuMDQsIC02Ni4zNCkiIGdyYWRpZW50VW5pdHM9InVzZXJTcGFjZU9uVXNlIj48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiNmZmYiLz48c3RvcCBvZmZzZXQ9IjAiIHN0b3AtY29sb3I9IiNmZmYiLz48c3RvcCBvZmZzZXQ9IjAuMzgiIHN0b3AtY29sb3I9IiNlNmU4ZWIiLz48c3RvcCBvZmZzZXQ9IjAuNzIiIHN0b3AtY29sb3I9IiNkNmRiZGUiLz48c3RvcCBvZmZzZXQ9IjEiIHN0b3AtY29sb3I9IiNkMWQ2ZGEiLz48L2xpbmVhckdyYWRpZW50PjwvZGVmcz48ZyBpZD0iTGF5ZXJfMiIgZGF0YS1uYW1lPSJMYXllciAyIj48ZyBpZD0iQWJiaWxkdW5nXzEiIGRhdGEtbmFtZT0iQWJiaWxkdW5nIDEiPjxnIGlkPSJEcnVnX3NjcmVlbmluZyIgZGF0YS1uYW1lPSJEcnVnIHNjcmVlbmluZyI+PHJlY3QgY2xhc3M9ImNscy0xIiB4PSIwLjEiIHk9IjEuMTIiIHdpZHRoPSIzMS4yNSIgaGVpZ2h0PSIxMC40NCIgcng9IjUuMjIiIHRyYW5zZm9ybT0idHJhbnNsYXRlKDMwLjg0IDE0LjA1KSByb3RhdGUoLTE3NC45MykiLz48cGF0aCBjbGFzcz0iY2xzLTIiIGQ9Ik0xNC42OCwxMS40OWE4LjUyLDguNTIsMCwwLDAsLjkyLTEwLjRMNS4xNC4xNkMuNzEtLjI0LTIuOTUsNy45LDQuMjgsMTAuNTNaIi8+PC9nPjwvZz48L2c+PC9zdmc+",
    }

    DDI_ESM = r"""\
    export function render({ model, el }) {
      const ic = model.get("icon_uris") || {};

      const img = (name, cls, label) =>
        `<img class="ic ${cls || ""}" src="${ic[name] || ""}" alt="${label || name}" title="${label || name}" draggable="false"/>`;

      // cracked-tablet glyph: the victim drug broken into fragments (cleared)
      const frags = (cls) => `
        <svg class="ic-svg ${cls}" viewBox="0 0 26 22" role="img" aria-label="drug broken into fragments">
          <path d="M11,2 A9,9 0 0 0 11,20 Z" fill="#efebca" stroke="#898259" stroke-width="1" stroke-linejoin="round"/>
          <path d="M15,3 A9.5,9.5 0 0 1 15,21 Z" fill="#e4e2b3" stroke="#898259" stroke-width="1" stroke-linejoin="round" transform="rotate(9 19 12)"/>
          <circle cx="22.5" cy="4.5" r="1.1" fill="#d2cb96"/>
          <circle cx="24" cy="17" r="0.9" fill="#d2cb96"/>
        </svg>`;

      el.innerHTML = `
        <div class="ddi-card">
          <div class="ddi-head">
            <div class="ddi-title">A drug–drug interaction (DDI), in one picture</div>
            <label class="ddi-toggle">
              <input type="checkbox" id="ddi-inhibitor"/>
              <span class="ddi-knob"></span>
              <span class="ddi-toggle-label">Add a CYP inhibitor</span>
            </label>
          </div>

          <div class="ddi-pipeline">
            <div class="ddi-station">
              <div class="ddi-dose-pile" id="ddi-pile"></div>
              <div class="ddi-station-label">victim drug<span class="ddi-sub">repeated doses</span></div>
            </div>

            <div class="ddi-flux"><span class="ddi-pipe-arrow"></span><span class="ddi-flux-stop">&#10005;</span></div>

            <div class="ddi-station">
              <div class="ddi-gate">
                ${img("liver", "ic-liver", "liver")}
                ${img("enzyme_yellow", "ic-enzyme", "CYP enzyme")}
                <div class="ddi-plug">${img("pill_blue", "ic-plug", "inhibitor")}<span class="ddi-x">&#10005;</span></div>
              </div>
              <div class="ddi-station-label">CYP enzyme<span class="ddi-sub">clears the dose (liver)</span></div>
            </div>

            <div class="ddi-flux"><span class="ddi-pipe-arrow"></span></div>

            <div class="ddi-station">
              <div class="ddi-out ddi-out-ok">
                ${frags("ddi-frags-lg")}
                <span class="ddi-out-badge ok">cleared &#10003;</span>
              </div>
              <div class="ddi-out ddi-out-bad">
                <span class="ddi-out-badge bad">nothing cleared &#10005;</span>
              </div>
              <div class="ddi-station-label">removed from the body</div>
            </div>
          </div>

          <div class="ddi-exposure">
            <div class="ddi-exposure-head">
              <span>Plasma level of the victim drug</span>
              <span class="ddi-chips">
                <span class="chip chip-base">no inhibitor</span>
                <span class="chip chip-inh">+ inhibitor</span>
              </span>
            </div>
            <svg class="ddi-chart" viewBox="0 0 560 132" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Plasma concentration of the victim drug over time, with and without a CYP inhibitor">
              <rect x="10" y="10" width="540" height="32" class="ddi-zone-toxic"></rect>
              <rect x="10" y="42" width="540" height="63" class="ddi-zone-safe"></rect>
              <line x1="10" y1="42" x2="550" y2="42" class="ddi-threshold"></line>
              <text x="16" y="37" class="ddi-svg-text warn">toxic threshold</text>
              <path class="ddi-path ddi-path-base" d="M10,100 C120,86 260,74 550,71" pathLength="1"></path>
              <path class="ddi-path ddi-path-inh" d="M10,100 C120,92 220,78 300,48 C340,32 420,24 550,20" pathLength="1"></path>
              <text x="546" y="16" class="ddi-svg-text lab-inh" text-anchor="end">+ inhibitor</text>
              <text x="546" y="64" class="ddi-svg-text lab-base" text-anchor="end">no inhibitor</text>
              <text x="550" y="128" class="ddi-svg-text" text-anchor="end">time &#8594;</text>
            </svg>
            <div class="ddi-cap ddi-cap-off">Each dose is cleared before the next arrives &mdash; plasma level stays in the therapeutic range.</div>
            <div class="ddi-cap ddi-cap-on">The inhibitor slowly shuts the CYP down &mdash; doses pile up and plasma level climbs past the toxic threshold.</div>
          </div>

          <div class="ddi-legend">
            <span>${img("drug_tablet", "ic-legend", "victim drug")} victim drug</span>
            <span>${img("pill_blue", "ic-legend", "inhibitor")} inhibitor</span>
            <span>${img("enzyme_yellow", "ic-legend", "CYP enzyme")} CYP enzyme</span>
            <span>${frags("ic-legend-frag")} cleared (broken down)</span>
          </div>
        </div>`;

      const toggle = el.querySelector("#ddi-inhibitor");
      const card = el.querySelector(".ddi-card");
      const pile = el.querySelector("#ddi-pile");
      let timer = null;

      const setPile = (n, drop) => {
        pile.innerHTML = "";
        if (timer) {
          clearInterval(timer);
          timer = null;
        }
        if (!drop) {
          for (let i = 0; i < n; i += 1) {
            const p = document.createElement("img");
            p.src = ic["drug_tablet"];
            p.className = "ic ic-mini";
            p.alt = "victim drug dose";
            pile.appendChild(p);
          }
          return;
        }
        let k = 0;
        timer = setInterval(() => {
          if (!el.isConnected || k >= n) {
            if (timer) clearInterval(timer);
            timer = null;
            return;
          }
          k += 1;
          const p = document.createElement("img");
          p.src = ic["drug_tablet"];
          p.className = "ic ic-mini ddi-drop";
          p.alt = "accumulating victim drug dose";
          pile.appendChild(p);
        }, 170);
      };

      toggle.addEventListener("change", () => {
        if (toggle.checked) {
          card.classList.add("has-inhibitor");
          setPile(8, true);
        } else {
          card.classList.remove("has-inhibitor");
          setPile(2, false);
        }
      });

      setPile(2, false);
    }
    """
    DDI_CSS = r"""\
    .ddi-card {
      font-family: "Inter", ui-sans-serif, system-ui, -apple-system, sans-serif;
      background: linear-gradient(180deg, #ffffff, #f8fafc);
      border: 1px solid #e5e7eb;
      border-radius: 14px;
      padding: 14px 16px 11px;
      color: #0f172a;
      box-shadow: 0 8px 24px rgba(15, 23, 42, 0.07);
      box-sizing: border-box;
      max-width: 880px;
      margin: 0 auto;
      width: 100%;
    }

    .ddi-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 12px;
    }

    .ddi-title {
      font-weight: 700;
      font-size: 1.02em;
      letter-spacing: -0.01em;
      color: #0f172a;
    }

    .ddi-toggle {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      font-size: 0.82em;
      font-weight: 600;
      color: #475569;
      user-select: none;
    }

    .ddi-toggle input {
      position: absolute;
      opacity: 0;
      pointer-events: none;
    }

    .ddi-knob {
      width: 36px;
      height: 20px;
      border-radius: 999px;
      background: #cbd5e1;
      position: relative;
      transition: background 0.15s ease;
      flex: none;
    }

    .ddi-knob::after {
      content: "";
      position: absolute;
      top: 2px;
      left: 2px;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #fff;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
      transition: transform 0.15s ease;
    }

    .ddi-toggle input:checked + .ddi-knob {
      background: #dc2626;
    }

    .ddi-toggle input:checked + .ddi-knob::after {
      transform: translateX(16px);
    }

    /* ---------- pipeline ---------- */

    .ddi-pipeline {
      display: flex;
      align-items: stretch;
      justify-content: space-between;
      gap: 4px;
      margin: 2px 0 12px;
    }

    .ddi-station {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      min-width: 118px;
    }

    .ddi-station-label {
      font-size: 0.72em;
      font-weight: 700;
      color: #334155;
      text-align: center;
      line-height: 1.3;
    }

    .ddi-station-label .ddi-sub {
      display: block;
      font-weight: 500;
      font-size: 0.92em;
      color: #94a3b8;
    }

    .ddi-flux {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      min-width: 44px;
      padding-bottom: 26px;
    }

    .ddi-pipe-arrow {
      display: block;
      width: 100%;
      max-width: 64px;
      height: 2px;
      position: relative;
    }

    .ddi-pipe-arrow::before {
      content: "";
      position: absolute;
      inset: 0 8px 0 0;
      border-radius: 2px;
      background: repeating-linear-gradient(
        90deg,
        #94a3b8 0 6px,
        transparent 6px 10px
      );
      animation: ddi-flow 1.1s linear infinite;
    }

    .ddi-pipe-arrow::after {
      content: "";
      position: absolute;
      right: 0;
      top: -4px;
      border: 5px solid transparent;
      border-left: 6px solid #94a3b8;
    }

    @keyframes ddi-flow {
      to {
        background-position: 10px 0;
      }
    }

    .ddi-flux-stop {
      position: absolute;
      top: calc(50% - 22px);
      color: #dc2626;
      font-weight: 800;
      font-size: 0.95em;
      opacity: 0;
      transition: opacity 0.3s ease;
    }

    .ddi-card.has-inhibitor .ddi-pipe-arrow {
      opacity: 0.25;
    }

    .ddi-card.has-inhibitor .ddi-pipe-arrow::before {
      animation-play-state: paused;
    }

    .ddi-card.has-inhibitor .ddi-pipe-arrow::after {
      border-left-color: #fca5a5;
    }

    .ddi-card.has-inhibitor .ddi-flux-stop {
      opacity: 1;
    }

    /* ---------- stations ---------- */

    .ddi-dose-pile {
      width: 120px;
      height: 92px;
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
      align-items: center;
      align-content: center;
      justify-content: center;
      border: 1.5px solid #e2e8f0;
      border-radius: 14px;
      background: #fff;
      padding: 6px;
      box-sizing: border-box;
    }

    .ddi-dose-pile .ddi-drop {
      animation: ddi-drop 0.3s ease-out;
    }

    @keyframes ddi-drop {
      from {
        transform: translateY(-14px);
        opacity: 0;
      }
      to {
        transform: translateY(0);
        opacity: 1;
      }
    }

    .ddi-gate {
      position: relative;
      width: 120px;
      height: 92px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1.5px solid #e2e8f0;
      border-radius: 14px;
      background: #fff;
      box-sizing: border-box;
      transition: border-color 0.3s ease, box-shadow 0.3s ease;
    }

    .ddi-gate::before {
      content: "";
      position: absolute;
      inset: 0;
      border-radius: 13px;
      background: rgba(220, 38, 38, 0.07);
      opacity: 0;
      transition: opacity 0.3s ease;
    }

    .ddi-card.has-inhibitor .ddi-gate {
      border-color: #fca5a5;
      box-shadow: 0 0 0 3px rgba(220, 38, 38, 0.08);
    }

    .ddi-card.has-inhibitor .ddi-gate::before {
      opacity: 1;
    }

    .ddi-plug {
      position: absolute;
      top: -9px;
      right: -7px;
      display: none;
      align-items: center;
      gap: 3px;
      background: #fff;
      border: 1px solid #fecaca;
      border-radius: 999px;
      padding: 2px 6px;
      z-index: 2;
    }

    .ddi-card.has-inhibitor .ddi-plug {
      display: flex;
    }

    .ddi-plug .ddi-x {
      color: #dc2626;
      font-weight: 800;
      font-size: 0.85em;
      line-height: 1;
    }

    .ddi-out {
      width: 120px;
      height: 92px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 6px;
      border: 1.5px solid #e2e8f0;
      border-radius: 14px;
      background: #fff;
      box-sizing: border-box;
    }

    .ddi-out-bad {
      display: none;
    }

    .ddi-card.has-inhibitor .ddi-out-ok {
      display: none;
    }

    .ddi-card.has-inhibitor .ddi-out-bad {
      display: flex;
    }

    .ddi-meta-row {
      display: flex;
      gap: 3px;
    }

    .ddi-out-badge {
      font-size: 0.68em;
      font-weight: 700;
      padding: 2px 9px;
      border-radius: 999px;
      white-space: nowrap;
    }

    .ddi-out-badge.ok {
      background: #dcfce7;
      color: #166534;
    }

    .ddi-out-badge.bad {
      background: #fee2e2;
      color: #991b1b;
    }

    /* ---------- exposure chart ---------- */

    .ddi-exposure {
      border: 1px solid #eef2f7;
      border-radius: 10px;
      padding: 8px 10px 6px;
      background: #fff;
    }

    .ddi-exposure-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      flex-wrap: wrap;
      font-size: 0.72em;
      font-weight: 700;
      color: #334155;
      margin-bottom: 2px;
    }

    .ddi-chips {
      display: inline-flex;
      gap: 14px;
      font-weight: 600;
    }

    .chip {
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }

    .chip::before {
      content: "";
      width: 14px;
      height: 3px;
      border-radius: 2px;
      background: currentColor;
    }

    .chip-base {
      color: #0f766e;
    }

    .chip-inh {
      color: #dc2626;
    }

    .ddi-chart {
      width: 100%;
      height: auto;
      display: block;
    }

    .ddi-zone-toxic {
      fill: rgba(220, 38, 38, 0.05);
    }

    .ddi-zone-safe {
      fill: rgba(22, 163, 74, 0.04);
    }

    .ddi-threshold {
      stroke: #dc2626;
      stroke-width: 1.2;
      stroke-dasharray: 5 4;
      opacity: 0.7;
    }

    .ddi-svg-text {
      font-size: 10px;
      fill: #64748b;
      font-family: inherit;
    }

    .ddi-svg-text.warn {
      fill: #b91c1c;
      font-weight: 600;
    }

    .ddi-svg-text.lab-inh {
      fill: #dc2626;
      font-weight: 600;
    }

    .ddi-svg-text.lab-base {
      fill: #0f766e;
      font-weight: 600;
    }

    .ddi-path {
      fill: none;
      stroke-width: 3;
      stroke-linecap: round;
      transition: opacity 0.4s ease;
    }

    .ddi-path-base {
      stroke: #0f766e;
    }

    .ddi-path-inh {
      stroke: #dc2626;
      stroke-dasharray: 1;
      stroke-dashoffset: 0;
    }

    .ddi-card:not(.has-inhibitor) .ddi-path-inh {
      opacity: 0.16;
    }

    .ddi-card.has-inhibitor .ddi-path-base {
      opacity: 0.2;
    }

    .ddi-card.has-inhibitor .ddi-path-inh {
      animation: ddi-draw 1.5s ease-out;
    }

    @keyframes ddi-draw {
      from {
        stroke-dashoffset: 1;
        opacity: 1;
      }
      to {
        stroke-dashoffset: 0;
        opacity: 1;
      }
    }

    .ddi-cap {
      font-size: 0.74em;
      font-weight: 500;
      line-height: 1.4;
      color: #475569;
      padding: 2px 2px 3px;
    }

    .ddi-cap-on {
      display: none;
      color: #991b1b;
      font-weight: 600;
    }

    .ddi-card.has-inhibitor .ddi-cap-off {
      display: none;
    }

    .ddi-card.has-inhibitor .ddi-cap-on {
      display: block;
    }

    /* ---------- legend & icons ---------- */

    .ddi-legend {
      display: flex;
      flex-wrap: wrap;
      gap: 8px 18px;
      margin-top: 10px;
      padding-top: 9px;
      border-top: 1px dashed #e2e8f0;
      font-size: 0.72em;
      color: #64748b;
      align-items: center;
    }

    .ddi-legend span {
      display: inline-flex;
      align-items: center;
      gap: 5px;
    }

    .ic {
      object-fit: contain;
    }

    .ic-svg {
      display: block;
    }

    .ddi-frags-lg {
      height: 30px;
    }

    .ic-legend-frag {
      height: 16px;
    }

    .ic-liver {
      height: 62px;
      opacity: 0.9;
    }

    .ic-enzyme {
      position: absolute;
      height: 38px;
      left: 50%;
      top: 50%;
      transform: translate(-50%, -50%);
    }

    .ic-mini {
      height: 16px;
    }

    .ic-plug {
      height: 20px;
    }

    .ic-meta {
      height: 15px;
    }

    .ic-legend {
      height: 16px;
    }

    @media (max-width: 640px) {
      .ddi-pipeline {
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
      }

      .ddi-flux {
        display: none;
      }
    }
    """
    PROBE_ESM = r"""\
    export function render({ model, el }) {
      const ic = model.get("icon_uris") || {};

      const caged = `
        <svg class="pg-caged" viewBox="0 0 20 20" role="img" aria-label="caged probe (non-fluorescent)">
          <circle cx="10" cy="10" r="5.2" fill="#cbd5e1" stroke="#94a3b8" stroke-width="1"/>
          <circle cx="10" cy="10" r="8.4" fill="none" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2 2.6"/>
        </svg>`;

      const dot = () => `
        <svg class="pg-dot" viewBox="0 0 20 20" role="img" aria-label="fluorescent product">
          <circle cx="10" cy="10" r="5" fill="#4ade80" fill-opacity="0.9"/>
          <circle cx="10" cy="10" r="8.2" fill="none" stroke="#22c55e" stroke-opacity="0.3" stroke-width="1"/>
        </svg>`;

      el.innerHTML = `
        <div class="pg-card">
          <div class="pg-head">
            <div class="pg-title">The readout: caged probe in, glow out</div>
            <label class="pg-slider-wrap">
              <span class="pg-slider-label">Add compound</span>
              <input type="range" id="pg-conc" min="0" max="100" value="0"/>
            </label>
          </div>

          <div class="pg-pipeline">
            <div class="pg-station">
              <div class="pg-probes">${caged}${caged}${caged}${caged}${caged}</div>
              <div class="pg-station-label">caged probe<span class="pg-sub">dark &mdash; cannot glow yet</span></div>
            </div>

            <div class="pg-flux"><span class="pg-pipe-arrow"></span></div>

            <div class="pg-station">
              <div class="pg-gate">
                <img class="ic pg-enzyme" src="${ic["enzyme_yellow"] || ""}" alt="CYP enzyme" draggable="false"/>
              </div>
              <div class="pg-station-label">CYP cleaves it<span class="pg-sub">if it is working</span></div>
            </div>

            <div class="pg-flux"><span class="pg-pipe-arrow"></span></div>

            <div class="pg-station">
              <div class="pg-well" id="pg-well"></div>
              <div class="pg-station-label">product<span class="pg-sub">fluoresces &mdash; the detector sees it</span></div>
            </div>
          </div>

          <div class="pg-meter-row">
            <span class="pg-meter-label">signal vs no-compound control</span>
            <div class="pg-meter"><div class="pg-meter-fill" id="pg-fill"></div></div>
            <span class="pg-pct"><b id="pg-pct">100%</b></span>
            <span class="pg-chip">[compound] = <b id="pg-conc-lbl">none</b></span>
          </div>

          <div class="pg-cap">More glow = more product = more working CYP. An inhibitor dims the glow &mdash; and tracing the signal across concentrations traces out the dose&ndash;response curve that <b>IC50</b> (and <b>pIC50 = &minus;log10(IC50)</b>) come from.</div>
          <div class="pg-cap pg-cap-note">CYP2D6 uses the same logic with a mass spectrometer as the detector: dextromethorphan &rarr; dextrorphan is counted, not seen.</div>
        </div>`;

      const slider = el.querySelector("#pg-conc");
      const well = el.querySelector("#pg-well");
      const fill = el.querySelector("#pg-fill");
      const pct = el.querySelector("#pg-pct");
      const concLbl = el.querySelector("#pg-conc-lbl");
      const arrows = el.querySelectorAll(".pg-pipe-arrow");

      let activity = 100;
      let acc = 0;

      const compute = (v) => {
        if (v <= 0) return { act: 100, lbl: "none" };
        const x = -1 + ((v - 1) / 99) * 3;
        const act = 100 / (1 + Math.pow(10, 0.9 * (x - 1)));
        const uM = Math.pow(10, x);
        const lbl = uM >= 1 ? `${Math.round(uM)} \u00b5M` : `${uM.toFixed(2)} \u00b5M`;
        return { act, lbl };
      };

      const update = () => {
        fill.style.width = `${activity}%`;
        pct.textContent = `${Math.round(activity)}%`;
        const flow = 0.25 + (activity / 100) * 0.75;
        arrows.forEach((a) => {
          a.style.opacity = String(flow);
          a.style.setProperty("--pg-flow-speed", `${(1.6 - (activity / 100) * 0.7).toFixed(2)}s`);
        });
      };

      const spawn = () => {
        acc += (activity / 100) * 0.85;
        while (acc >= 1) {
          acc -= 1;
          if (well.childElementCount > 20 && well.firstChild) {
            well.removeChild(well.firstChild);
          }
          const t = document.createElement("span");
          t.innerHTML = dot();
          const node = t.firstElementChild;
          node.style.left = `${(14 + Math.random() * 72).toFixed(1)}%`;
          node.style.top = `${(14 + Math.random() * 72).toFixed(1)}%`;
          node.style.animationDuration = `${(2.4 + Math.random() * 1).toFixed(2)}s`;
          node.addEventListener("animationend", () => node.remove());
          well.appendChild(node);
        }
      };

      slider.addEventListener("input", () => {
        const { act, lbl } = compute(Number(slider.value));
        activity = act;
        concLbl.textContent = lbl;
        update();
      });

      update();
      setInterval(() => {
        if (el.isConnected) spawn();
      }, 150);
    }
    """
    PROBE_CSS = r"""\
    .pg-card {
      font-family: "Inter", ui-sans-serif, system-ui, -apple-system, sans-serif;
      background: linear-gradient(180deg, #ffffff, #f8fafc);
      border: 1px solid #e5e7eb;
      border-radius: 14px;
      padding: 14px 16px 11px;
      color: #0f172a;
      box-shadow: 0 8px 24px rgba(15, 23, 42, 0.07);
      box-sizing: border-box;
      max-width: 880px;
      margin: 0 auto;
      width: 100%;
    }

    .pg-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 10px;
    }

    .pg-title {
      font-weight: 700;
      font-size: 1.02em;
      letter-spacing: -0.01em;
      color: #0f172a;
    }

    .pg-slider-wrap {
      display: inline-flex;
      align-items: center;
      gap: 10px;
      font-size: 0.8em;
      font-weight: 600;
      color: #475569;
      user-select: none;
    }

    .pg-slider-label {
      white-space: nowrap;
    }

    .pg-slider-wrap input[type="range"] {
      width: 170px;
      accent-color: #dc2626;
      cursor: pointer;
    }

    .pg-pipeline {
      display: flex;
      align-items: stretch;
      justify-content: space-between;
      gap: 4px;
      margin: 2px 0 12px;
    }

    .pg-station {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      min-width: 112px;
    }

    .pg-station-label {
      font-size: 0.72em;
      font-weight: 700;
      color: #334155;
      text-align: center;
      line-height: 1.3;
    }

    .pg-station-label .pg-sub {
      display: block;
      font-weight: 500;
      font-size: 0.92em;
      color: #94a3b8;
    }

    .pg-flux {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      min-width: 40px;
      padding-bottom: 26px;
    }

    .pg-pipe-arrow {
      --pg-flow-speed: 1.6s;
      display: block;
      width: 100%;
      max-width: 56px;
      height: 2px;
      position: relative;
    }

    .pg-pipe-arrow::before {
      content: "";
      position: absolute;
      inset: 0 8px 0 0;
      border-radius: 2px;
      background: repeating-linear-gradient(
        90deg,
        #94a3b8 0 6px,
        transparent 6px 10px
      );
      animation: pg-flow var(--pg-flow-speed) linear infinite;
    }

    .pg-pipe-arrow::after {
      content: "";
      position: absolute;
      right: 0;
      top: -4px;
      border: 5px solid transparent;
      border-left: 6px solid #94a3b8;
    }

    @keyframes pg-flow {
      to {
        background-position: 10px 0;
      }
    }

    .pg-probes {
      width: 118px;
      height: 92px;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      align-items: center;
      align-content: center;
      justify-content: center;
      border: 1.5px solid #e2e8f0;
      border-radius: 14px;
      background: #fff;
      padding: 6px;
      box-sizing: border-box;
    }

    .pg-caged {
      height: 24px;
      display: block;
      opacity: 0.85;
    }

    .pg-gate {
      position: relative;
      width: 118px;
      height: 92px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1.5px solid #e2e8f0;
      border-radius: 14px;
      background: #fff;
      box-sizing: border-box;
    }

    .pg-enzyme {
      height: 46px;
    }

    .pg-well {
      position: relative;
      width: 118px;
      height: 92px;
      border: 1.5px solid #e2e8f0;
      border-radius: 14px;
      background: #0f172a;
      box-sizing: border-box;
      overflow: hidden;
    }

    .pg-dot {
      position: absolute;
      height: 16px;
      transform: translate(-50%, -50%);
      filter: drop-shadow(0 0 3px rgba(74, 222, 128, 0.55));
      animation: pg-life 2.8s ease-in-out forwards;
    }

    @keyframes pg-life {
      0% {
        opacity: 0;
        transform: translate(-50%, -50%) scale(0.7);
      }
      30% {
        opacity: 0.85;
        transform: translate(-50%, -50%) scale(1);
      }
      70% {
        opacity: 0.85;
        transform: translate(-50%, -50%) scale(0.95);
      }
      100% {
        opacity: 0;
        transform: translate(-50%, -50%) scale(0.8);
      }
    }

    .pg-meter-row {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 6px;
    }

    .pg-meter-label {
      font-size: 0.72em;
      font-weight: 700;
      color: #334155;
      white-space: nowrap;
    }

    .pg-meter {
      flex: 1;
      min-width: 140px;
      max-width: 320px;
      height: 14px;
      border-radius: 7px;
      background: #e2e8f0;
      overflow: hidden;
    }

    .pg-meter-fill {
      height: 100%;
      width: 100%;
      border-radius: 7px;
      background: linear-gradient(90deg, #16a34a, #4ade80);
      transition: width 0.35s ease;
    }

    .pg-pct {
      font-size: 0.78em;
      font-weight: 700;
      color: #166534;
      font-variant-numeric: tabular-nums;
      min-width: 42px;
    }

    .pg-chip {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 0.72em;
      font-weight: 600;
      color: #475569;
      background: #f1f5f9;
      border-radius: 999px;
      padding: 2px 9px;
    }

    .pg-chip b {
      color: #0f172a;
      font-variant-numeric: tabular-nums;
    }

    .pg-cap {
      font-size: 0.74em;
      font-weight: 500;
      line-height: 1.4;
      color: #475569;
      padding: 2px 2px 3px;
    }

    .pg-cap-note {
      color: #94a3b8;
      font-size: 0.7em;
    }

    @media (max-width: 640px) {
      .pg-pipeline {
        flex-wrap: wrap;
        justify-content: center;
        gap: 10px;
      }

      .pg-flux {
        display: none;
      }
    }
    """
    SHIFT_ESM = r"""\
    export function render({ model, el }) {
      const X0 = -2, X1 = 2, NHILL = 0.9;
      const PL_X = 48, PL_W = 496, PL_Y = 120, PL_H = 102;
      const P_MIN = 4.4, P_MAX = 6.2;

      const xToSvg = (x) => PL_X + ((x - X0) / (X1 - X0)) * PL_W;
      const act = (x, p) => 100 / (1 + Math.pow(10, NHILL * (x - (6 - p))));
      const pathD = (p) => {
        let d = "";
        for (let i = 0; i <= 100; i += 1) {
          const x = X0 + ((X1 - X0) * i) / 100;
          const y = PL_Y - (act(x, p) / 100) * PL_H;
          d += (i ? " L" : "M") + xToSvg(x).toFixed(1) + "," + y.toFixed(1);
        }
        return d;
      };
      const ic50uM = (p) => Math.pow(10, 6 - p);
      const D_MIN = pathD(P_MIN);

      const tickX = [-2, -1, 0, 1, 2];
      const tickLbl = ["0.01", "0.1", "1", "10", "100"];
      const grid = tickX
        .map(
          (t, i) =>
            `<line x1="${xToSvg(t)}" y1="18" x2="${xToSvg(t)}" y2="120" class="sc-grid"></line>` +
            `<text x="${xToSvg(t)}" y="134" text-anchor="middle" class="sc-svg-text">${tickLbl[i]}</text>`
        )
        .join("");

      el.innerHTML = `
        <div class="sc-card">
          <div class="sc-head">
            <div class="sc-title">One compound, two arms: &minus;NADPH vs +NADPH</div>
            <label class="sc-toggle">
              <input type="checkbox" id="sc-pre"/>
              <span class="sc-knob"></span>
              <span class="sc-toggle-label">TDI arm &mdash; 30 min pre-incubation, +NADPH</span>
            </label>
          </div>

          <svg class="sc-chart" viewBox="0 0 560 158" preserveAspectRatio="xMidYMid meet" role="img"
               aria-label="Dose-response curve of residual enzyme activity, sliding left in the +NADPH arm">
            <text x="8" y="11" class="sc-svg-text">% enzyme activity left</text>
            ${grid}
            <line x1="48" y1="120" x2="544" y2="120" class="sc-axis"></line>
            <line x1="48" y1="18" x2="48" y2="120" class="sc-axis"></line>
            <text x="100" y="69" class="sc-svg-text faint">50%</text>
            <line x1="48" y1="69" x2="544" y2="69" class="sc-grid"></line>
            <text x="544" y="150" text-anchor="end" class="sc-svg-text">compound concentration (&micro;M, log scale) &#8594;</text>
            <line x1="${xToSvg(1)}" y1="18" x2="${xToSvg(1)}" y2="120" class="sc-threshold"></line>
            <text x="${xToSvg(1) + 5}" y="29" class="sc-svg-text warn">hit: IC50 = 10 &micro;M</text>
            <path id="sc-ghost" class="sc-ghost" d="${D_MIN}"></path>
            <path id="sc-main" class="sc-path" d="${D_MIN}"></path>
            <circle id="sc-dot" r="4" cx="${xToSvg(6 - P_MIN)}" cy="69"></circle>
          </svg>

          <div class="sc-readout">
            <span class="sc-chip">pIC50 <b id="sc-pic50">4.40</b></span>
            <span class="sc-chip">IC50 &asymp; <b id="sc-ic50">40</b> &micro;M</span>
            <span class="sc-verdict sc-v-off">direct arm (&minus;NADPH): plain reversible inhibition</span>
            <span class="sc-verdict sc-v-on">+NADPH arm: TDI detected &#10003;</span>
          </div>

          <div class="sc-cap sc-cap-off">Pre-incubated 30 min without NADPH, the enzyme can&#8217;t turn the compound over &mdash; you measure only plain, reversible binding of the parent compound, and the TDI is invisible.</div>
          <div class="sc-cap sc-cap-on">With NADPH in the pre-incubation, the enzyme metabolises the compound and progressively disables itself &mdash; the dose&ndash;response, measured afterwards from both arms (probe + NADPH added to each), has slid left across the hit threshold.</div>
        </div>`;

      const toggle = el.querySelector("#sc-pre");
      const card = el.querySelector(".sc-card");
      const main = el.querySelector("#sc-main");
      const dot = el.querySelector("#sc-dot");
      const pic50El = el.querySelector("#sc-pic50");
      const ic50El = el.querySelector("#sc-ic50");

      let raf = null;
      let cur = P_MIN;

      const draw = () => {
        main.setAttribute("d", pathD(cur));
        dot.setAttribute("cx", xToSvg(6 - cur).toFixed(1));
        pic50El.textContent = cur.toFixed(2);
        const v = ic50uM(cur);
        ic50El.textContent = v >= 10 ? String(Math.round(v)) : v >= 1 ? v.toFixed(1) : v.toFixed(2);
      };

      const animateTo = (target) => {
        if (raf) cancelAnimationFrame(raf);
        const from = cur;
        const t0 = performance.now();
        const dur = 1400;
        const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
        const step = (now) => {
          const t = Math.min(1, (now - t0) / dur);
          cur = from + (target - from) * ease(t);
          draw();
          if (t < 1 && el.isConnected) raf = requestAnimationFrame(step);
        };
        raf = requestAnimationFrame(step);
      };

      toggle.addEventListener("change", () => {
        card.classList.toggle("has-pre", toggle.checked);
        animateTo(toggle.checked ? P_MAX : P_MIN);
      });

      draw();
    }
    """
    SHIFT_CSS = r"""\
    .sc-card {
      font-family: "Inter", ui-sans-serif, system-ui, -apple-system, sans-serif;
      background: linear-gradient(180deg, #ffffff, #f8fafc);
      border: 1px solid #e5e7eb;
      border-radius: 14px;
      padding: 14px 16px 11px;
      color: #0f172a;
      box-shadow: 0 8px 24px rgba(15, 23, 42, 0.07);
      box-sizing: border-box;
      max-width: 880px;
      margin: 0 auto;
      width: 100%;
    }

    .sc-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 8px;
    }

    .sc-title {
      font-weight: 700;
      font-size: 1.02em;
      letter-spacing: -0.01em;
      color: #0f172a;
    }

    .sc-toggle {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
      font-size: 0.82em;
      font-weight: 600;
      color: #475569;
      user-select: none;
    }

    .sc-toggle input {
      position: absolute;
      opacity: 0;
      pointer-events: none;
    }

    .sc-knob {
      width: 36px;
      height: 20px;
      border-radius: 999px;
      background: #cbd5e1;
      position: relative;
      transition: background 0.15s ease;
      flex: none;
    }

    .sc-knob::after {
      content: "";
      position: absolute;
      top: 2px;
      left: 2px;
      width: 16px;
      height: 16px;
      border-radius: 50%;
      background: #fff;
      box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
      transition: transform 0.15s ease;
    }

    .sc-toggle input:checked + .sc-knob {
      background: #0f766e;
    }

    .sc-toggle input:checked + .sc-knob::after {
      transform: translateX(16px);
    }

    .sc-chart {
      width: 100%;
      height: auto;
      display: block;
    }

    .sc-svg-text {
      font-size: 10px;
      fill: #64748b;
      font-family: inherit;
    }

    .sc-svg-text.warn {
      fill: #b91c1c;
      font-weight: 600;
    }

    .sc-svg-text.faint {
      fill: #94a3b8;
    }

    .sc-grid {
      stroke: #eef2f7;
      stroke-width: 1;
    }

    .sc-axis {
      stroke: #cbd5e1;
      stroke-width: 1.2;
    }

    .sc-threshold {
      stroke: #dc2626;
      stroke-width: 1.2;
      stroke-dasharray: 5 4;
      opacity: 0.6;
    }

    .sc-path {
      fill: none;
      stroke: #0f766e;
      stroke-width: 3;
      stroke-linecap: round;
      transition: stroke 0.5s ease;
    }

    .sc-card.has-pre .sc-path {
      stroke: #dc2626;
    }

    .sc-ghost {
      fill: none;
      stroke: #0f766e;
      stroke-width: 2;
      stroke-dasharray: 4 5;
      opacity: 0;
      transition: opacity 0.5s ease;
    }

    .sc-card.has-pre .sc-ghost {
      opacity: 0.45;
    }

    #sc-dot {
      fill: #0f766e;
      stroke: #fff;
      stroke-width: 1.5;
      transition: fill 0.5s ease;
    }

    .sc-card.has-pre #sc-dot {
      fill: #dc2626;
    }

    .sc-readout {
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
      margin: 2px 0 6px;
    }

    .sc-chip {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 0.72em;
      font-weight: 600;
      color: #475569;
      background: #f1f5f9;
      border-radius: 999px;
      padding: 2px 9px;
    }

    .sc-chip b {
      color: #0f172a;
      font-variant-numeric: tabular-nums;
    }

    .sc-verdict {
      font-size: 0.72em;
      font-weight: 700;
      padding: 2px 9px;
      border-radius: 999px;
      margin-left: auto;
    }

    .sc-v-off {
      background: #e2e8f0;
      color: #475569;
    }

    .sc-v-on {
      display: none;
      background: #fee2e2;
      color: #991b1b;
    }

    .sc-card.has-pre .sc-v-off {
      display: none;
    }

    .sc-card.has-pre .sc-v-on {
      display: inline-flex;
    }

    .sc-cap {
      font-size: 0.74em;
      font-weight: 500;
      line-height: 1.4;
      color: #475569;
      padding: 2px 2px 3px;
    }

    .sc-cap-on {
      display: none;
      color: #991b1b;
      font-weight: 600;
    }

    .sc-card.has-pre .sc-cap-off {
      display: none;
    }

    .sc-card.has-pre .sc-cap-on {
      display: block;
    }
    """

    class DDIScene(anywidget.AnyWidget):
        _esm = DDI_ESM
        _css = DDI_CSS
        icon_uris = traitlets.Dict(default_value=ICON_URIS).tag(sync=True)

    class ProbeGlowScene(anywidget.AnyWidget):
        _esm = PROBE_ESM
        _css = PROBE_CSS
        icon_uris = traitlets.Dict(
            default_value={"enzyme_yellow": ICON_URIS["enzyme_yellow"]}
        ).tag(sync=True)

    class ShiftScene(anywidget.AnyWidget):
        _esm = SHIFT_ESM
        _css = SHIFT_CSS

    return DDIScene, ProbeGlowScene, ShiftScene


@app.cell
def _(DDIScene, mo):
    _desc = mo.md(
        "**Cytochromes P450 (CYPs)** are the liver enzymes that clear most "
        "drugs. Test any new compound and the question is: *does it stop a CYP "
        "from doing its job?* If yes, every co‑administered drug that relies "
        "on that CYP (the **victim**) clears more slowly — exposure climbs, "
        "toxicity risk follows. That is a **drug–drug interaction (DDI)**, and "
        "the panel below shows the anatomy of one."
        "\n\n"
        "The dataset covers the four isoforms that do most of the work — "
        "**CYP3A4, CYP2D6, CYP2C9, CYP1A2** — each assayed separately, so "
        "every number is unambiguously about one enzyme."
    )
    _credits = mo.Html(
        '<p style="font-size:0.78em;color:#64748b;line-height:1.45;'
        "margin:8px 0 0;\"><b>Panel icons:</b> liver, enzymes &amp; "
        "drug‑tablet by <b>Servier Medical Art</b> (CC‑BY 3.0); pills, drugs, "
        "metabolites &amp; toxic by Marcel Tisch, Fang‑fang‑yang &amp; David "
        "Eccles (CC0) — via <a href='https://bioicons.com' target='_blank'>"
        "bioicons.com</a>.</p>"
    )
    _widget = mo.ui.anywidget(DDIScene())
    mo.vstack([_desc, _widget, _credits])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### What the assay measures

    Each CYP gets a **caged probe** — non‑fluorescent until the enzyme
    releases it (CYP2D6 instead tracks a mass shift: dextromethorphan →
    dextrorphan). The raw signal is simply *how much product did the enzyme
    make?* An inhibitor makes less product → weaker signal. Sweep the
    compound concentration and you trace a **dose‑response curve**, summarised
    by the **IC50** (concentration at half‑maximal product) and reported as
    **pIC50 = −log10(IC50)** — bigger pIC50, stronger inhibitor.
    """)
    return


@app.cell
def _(ProbeGlowScene, mo):
    mo.vstack([mo.ui.anywidget(ProbeGlowScene())])
    return


@app.cell
def _(MMD_THEME, mo):
    _writeup = mo.md(r"""
    ### The two‑arm design — NADPH separates reversible from time‑dependent inhibition

    CYPs need **NADPH**, their electron donor, as an on‑switch — and the
    assay exploits that. Every compound is pre‑incubated for 30 minutes in
    **two parallel arms** that differ *only* in whether NADPH is present:

    - **Direct arm (−NADPH):** no NADPH → the enzyme can’t turn the compound
      over → no metabolism‑driven inactivation can occur. Any inhibition is
      the parent compound **binding directly** — plain, reversible inhibition.
    - **TDI arm (+NADPH):** enzyme on and metabolising — if metabolism turns
      the compound into something that **progressively disables the CYP**,
      potency grows over the pre‑incubation.

    After the pre‑incubation, probe **and NADPH are added to both arms** for
    the 12‑point dose–response — both enzymes are fully powered at readout,
    so the difference between the curves reflects *what happened during the
    pre‑incubation*, nothing else. A time‑dependent inhibitor shows up as a
    **leftward slide** in the +NADPH arm. The dataset turns that slide into
    its label: `shift = pIC50(+NADPH) − pIC50(−NADPH)`, with
    **`is_TDI = True` at shift ≥ 0.301 (a 2‑fold potency gain)**.
    """)
    _diagram = mo.center(
        mo.mermaid(
            """flowchart TD
    C["Compound"] --> A["Incubate compound + CYP<br/>two arms, same plate, 30 min"]
    A --> D1["<b>DIRECT arm</b> ( –NADPH )<br/>CYP <b>switched off</b><br/>no metabolism<br/>&rarr; reversible<br/>binding only"]
    A --> T1["<b>TDI arm</b> ( +NADPH )<br/>CYP <b>switched on</b><br/>metabolises compound<br/>&rarr; reactive<br/>species may disable CYP"]
    D1 --> D2["12-pt dose-response<br/>&rarr; pIC50 direct"]
    T1 --> T2["12-point dose-response<br/>&rarr; pIC50 TDI"]
    D2 --> S{"shift = pIC50 TDI<br/>&minus; pIC50 direct"}
    T2 --> S
    S -->|"&ge; 2-fold (shift &ge; 0.301)"| P["is_TDI = True"]
    S -->|"no shift"| N["is_TDI = False"]
    """,
            theme="base",
            theme_variables=MMD_THEME,
        ),
    )
    mo.vstack([_writeup, _diagram])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Instant screens miss TDI \u2014 the +NADPH pre\u2011incubation is the point

    Read the compound straight away \u2014 or pre\u2011incubate it without NADPH \u2014 and
    a time\u2011dependent inhibitor looks **clean**: the enzyme has had no chance
    to turn it over, so only plain reversible binding shows up. The damage
    **builds during the +NADPH pre\u2011incubation** as metabolism converts the
    compound into an inactivator, so the dose\u2013response measured afterwards
    has already slid left. Flip the toggle below to watch one compound go
    from "sails through" to "flagged" as you switch arms.
    """)
    return


@app.cell
def _(ShiftScene, mo):
    mo.vstack([mo.ui.anywidget(ShiftScene())])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1 · Explore the dataset: the decision boundary

    Every point is a compound measured in **both arms** — here `is_TDI` is
    pure geometry: the dashed green **2‑fold shift boundary** (`y = x + 0.301`)
    with detection floors at pIC50 4 (direct arm) and 4.3 (TDI arm). Pick an
    isoform, choose a cursor mode, then **hover any point for its structure**;
    selected compounds land in the table below. The interesting chemistry sits
    within a few tenths of a log unit either side of the boundary — go hover
    there.
    """)
    return


@app.cell
def _():
    IMG_CACHE = {}
    return (IMG_CACHE,)


@app.cell
def _(IMG_CACHE, mo):
    import useful_rdkit_utils as uru

    def structure_uri(smiles, width=300, height=150):
        """PNG data-URI for chart tooltips (cached per SMILES).

        Drawn at 2x so the tooltip shows a crisp image on HiDPI screens.
        """
        key = ("uri", width, height, smiles)
        if key not in IMG_CACHE:
            IMG_CACHE[key] = uru.smi_to_base64_image(
                smiles, target="altair", width=width * 2, height=height * 2
            )
        return IMG_CACHE[key]

    def structure_html(smiles, width=240, height=120):
        """HTML <img> for table cells (cached per SMILES).

        Drawn at 2x and displayed at width x height so it stays crisp on
        HiDPI screens; explicit dimensions + max-*:none keep the table's CSS
        from shrinking it.
        """
        key = ("html", width, height, smiles)
        if key not in IMG_CACHE:
            IMG_CACHE[key] = uru.smi_to_base64_image(
                smiles, target="html", width=width * 2, height=height * 2
            )
        img = IMG_CACHE[key].replace(
            "<img ",
            "<img style='width:%dpx;height:%dpx;max-width:none;"
            "max-height:none;display:block' " % (width, height),
            1,
        )
        return mo.Html(img)

    return structure_html, structure_uri


@app.cell
def _(ISO, mo):
    iso_sel = mo.ui.dropdown(options=ISO, value="CYP3A4", label="Isoform")
    only_pos = mo.ui.checkbox(value=True, label="Only TDI-positive")
    cursor_sel = mo.ui.radio(
        options=["brush", "click", "pan"],
        value="brush",
        label="Cursor",
        inline=True,
    )
    return cursor_sel, iso_sel, only_pos


@app.cell
def _(
    alt,
    classify_batch,
    cursor_sel,
    df_tdi,
    iso_sel,
    mo,
    only_pos,
    pd,
    structure_uri,
    theme_sel,
):
    alt.theme.enable(theme_sel.value)
    _iso = iso_sel.value
    _out, _rule, _direct, _tdi, _shift = classify_batch(df_tdi, _iso)
    _lab = f"{_iso}_is_TDI"
    _has_labels = _lab in df_tdi.columns
    _f = df_tdi.loc[_out, ["Molecule_Name", "SMILES"]].copy()
    _f["direct"] = _direct
    _f["tdi_condition"] = _tdi
    _f["shift"] = _shift
    _f["is_TDI"] = (
        df_tdi.loc[_out, _lab].astype(bool) if _has_labels else _rule
    )
    if only_pos.value:
        _f = _f[_f["is_TDI"]]
    _f["image"] = [structure_uri(s) for s in _f["SMILES"]]
    _pts = (
        alt.Chart(_f)
        .mark_point(opacity=0.6, filled=True, size=30)
        .encode(
            x=alt.X(
                "direct:Q",
                title="pIC50 direct (–NADPH)",
                scale=alt.Scale(domain=[1, 8]),
            ),
            y=alt.Y(
                "tdi_condition:Q",
                title="pIC50 TDI (+NADPH)",
                scale=alt.Scale(domain=[1, 8]),
            ),
            color=alt.Color(
                "is_TDI:N",
                scale=alt.Scale(
                    domain=[False, True], range=["#7f7f7f", "#d62728"]
                ),
                title="is_TDI",
            ),
            tooltip=[
                "image",
                "Molecule_Name",
                "direct",
                "tdi_condition",
                "shift",
            ],
        )
        .properties(width=560, height=460)
    )
    _diag = (
        alt.Chart(pd.DataFrame({"x": [1, 7.7], "y": [1.301, 8.0]}))
        .mark_line(color="#2ca02c", strokeDash=[4, 3])
        .encode(x="x:Q", y="y:Q")
    )
    _vline = (
        alt.Chart(pd.DataFrame({"x": [4]}))
        .mark_rule(color="#9467bd", strokeDash=[4, 3])
        .encode(x="x:Q")
    )
    _hline = (
        alt.Chart(pd.DataFrame({"y": [4.3]}))
        .mark_rule(color="#1f77b4", strokeDash=[4, 3])
        .encode(y="y:Q")
    )
    _title = (
        f"{_iso} — "
        + "shipped is_TDI labels"
        if _has_labels
        else f"{_iso} — coloured by the classification rule (no shipped labels)"
    )
    _layered = _pts + _diag + _vline + _hline
    if cursor_sel.value == "brush":
        _layered = _layered.add_params(
            alt.selection_interval(encodings=["x", "y"])
        )
        scat = mo.ui.altair_chart(
            _layered.properties(title=_title),
            chart_selection=False,
            legend_selection=False,
        )
    elif cursor_sel.value == "click":
        _layered = _layered.add_params(alt.selection_point(on="click"))
        scat = mo.ui.altair_chart(
            _layered.properties(title=_title),
            chart_selection=False,
            legend_selection=False,
        )
    else:
        scat = mo.ui.altair_chart(
            _layered.properties(title=_title).interactive(),
            chart_selection=False,
            legend_selection=False,
        )
    scatter_points = _f
    mo.vstack([mo.hstack([iso_sel, only_pos, cursor_sel]), scat])
    return scat, scatter_points


@app.cell
def _(mo, scat, scatter_points, structure_html):
    _selection = scat.selections
    _selected = (
        scat.apply_selection(scatter_points) if _selection else scatter_points
    )
    _hint = (
        ""
        if _selection
        else " — brush‑select points to isolate yours"
    )
    _shown = _selected.sort_values("shift", ascending=False)
    _table = _shown[
        ["Molecule_Name", "SMILES", "direct", "tdi_condition", "shift", "is_TDI"]
    ].copy().reset_index(drop=True)
    _table.insert(0, "structure", [structure_html(s) for s in _shown["SMILES"]])
    mo.vstack(
        [
            mo.md(f"**{len(_selected):,} compounds** selected{_hint}"),
            mo.ui.table(_table, selection=None, page_size=5),
        ]
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 2 · Which pharmacophores drive TDI? (SHAP)

    Could the flags in §1 have been predicted from structure alone? We
    featurize every molecule with a **2D pharmacophore fingerprint** — unlike
    Morgan/ECFP bits (circular atom environments, unreadable to chemists),
    each bit here **is** a readable pattern: 2–3 feature points (Donor,
    Acceptor, Aromatic, Hydrophobe, …) at topological‑distance bins in bond
    counts, e.g. "Acceptor–Donor @ 5–8 bonds". A gradient‑boosted classifier
    predicts the §1 `is_TDI` label from these bits (molecule‑grouped split,
    no leakage), and **TreeSHAP** attributes each prediction back to its
    pharmacophores.

    *Caveats:* labels are the §1 rule, isoforms are pooled, and model
    discrimination is modest — read this as a **ranked shortlist of candidate
    pharmacophores**, not causal effects.
    """)
    return


@app.cell
def _(ISO, classify_batch, df_tdi, mo, np, os, pd):
    import rdkit
    from rdkit import Chem, RDLogger
    from rdkit.Chem import ChemicalFeatures
    from rdkit.Chem.Pharm2D import Generate
    from rdkit.Chem.Pharm2D.SigFactory import SigFactory

    RDLogger.DisableLog("rdApp.*")

    # 2D pharmacophore signature: 2- and 3-point patterns over 8 feature
    # families, 5 topological-distance bins (bond counts, not Å).
    _fdef = os.path.join(os.path.dirname(rdkit.__file__), "Data", "BaseFeatures.fdef")
    PHARM_SIG = SigFactory(
        ChemicalFeatures.BuildFeatureFactory(_fdef),
        minPointCount=2,
        maxPointCount=3,
        trianglePruneBins=False,
    )
    PHARM_SIG.SetBins([(0, 2), (2, 3), (3, 4), (4, 5), (5, 8)])
    PHARM_SIG.Init()

    with mo.status.spinner(
        title=f"Computing {PHARM_SIG.GetSigSize():,}-bit pharmacophore fingerprints "
        "(first run only, cached per molecule)"
    ):
        BITS = {
            _smi: np.asarray(
                Generate.Gen2DFingerprint(Chem.MolFromSmiles(_smi), PHARM_SIG), np.uint8
            )
            for _smi in df_tdi["SMILES"].dropna().unique()
        }

    # pooled (compound, isoform) samples labelled by the §1 rule
    _rows = []
    for _iso in ISO:
        _out, _rule, *_ = classify_batch(df_tdi, _iso)
        _sub = df_tdi.loc[_out, ["Molecule_Name", "SMILES"]].copy()
        _sub["isoform"] = _iso
        _sub["label"] = _rule.to_numpy()
        _rows.append(_sub)
    PHARM_DATA = pd.concat(_rows, ignore_index=True)

    mo.md(
        f"**{len(BITS):,}** molecules fingerprinted → "
        f"**{PHARM_SIG.GetSigSize():,}** pharmacophore bits each · "
        f"**{len(PHARM_DATA):,}** (compound, isoform) samples · "
        f"TDI rate **{PHARM_DATA.label.mean():.0%}**"
    )
    return BITS, Chem, Generate, PHARM_DATA, PHARM_SIG


@app.cell
def _(BITS, PHARM_DATA, mo, np, xgb):
    from sklearn.metrics import average_precision_score, roc_auc_score
    from sklearn.model_selection import GroupShuffleSplit

    SH_X = np.stack([BITS[s] for s in PHARM_DATA["SMILES"]]).astype(np.float32)
    _y = PHARM_DATA["label"].astype(int).to_numpy()
    _tr, SH_TE = next(
        GroupShuffleSplit(n_splits=1, test_size=0.25, random_state=0).split(
            SH_X, _y, PHARM_DATA["SMILES"]
        )
    )
    SH_CLF = xgb.XGBClassifier(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.1,
        subsample=0.9,
        colsample_bytree=0.5,
        tree_method="hist",
        n_jobs=-1,
        eval_metric="auc",
        scale_pos_weight=float((_y[_tr] == 0).sum() / (_y[_tr] == 1).sum()),
        random_state=0,
    )
    SH_CLF.fit(SH_X[_tr], _y[_tr])
    _p = SH_CLF.predict_proba(SH_X[SH_TE])[:, 1]
    mo.md(
        f"Hold-out (molecule-grouped): AUROC **{roc_auc_score(_y[SH_TE], _p):.2f}** · "
        f"average precision **{average_precision_score(_y[SH_TE], _p):.2f}** "
        f"(base rate {PHARM_DATA.label.mean():.0%}) — modest, as expected for "
        "rule-derived labels and 0/1 bits, but enough signal to rank "
        "pharmacophores by SHAP attribution."
    )
    return SH_CLF, SH_TE, SH_X


@app.cell
def _(PHARM_SIG, SH_CLF, SH_TE, SH_X, alt, mo, np, pd, shap, theme_sel):
    alt.theme.enable(theme_sel.value)

    _BINS = [(0, 2), (2, 3), (3, 4), (4, 5), (5, 8)]

    def bit_label(i):
        feats, *mat = PHARM_SIG.GetBitDescription(i).split("|")
        names = "-".join(w.replace("Ionizable", "Ion") for w in feats.split())
        dists = "/".join(
            f"{_BINS[int(d)][0]}\u2013{_BINS[int(d)][1]}" for d in mat[0].split()
        )
        return f"{names} @ {dists} bonds"

    _sub = np.random.RandomState(0).choice(
        SH_TE, size=min(1500, len(SH_TE)), replace=False
    )
    SH_EXPL = shap.TreeExplainer(SH_CLF)
    SH_SCORES = SH_CLF.predict_proba(SH_X)[:, 1]
    _sv = SH_EXPL.shap_values(SH_X[_sub].astype(np.float32))
    _mean, _mag = _sv.mean(0), np.abs(_sv).mean(0)
    _idx = np.argsort(-_mag)[:15]
    SH_TOP = pd.DataFrame(
        {
            "bit": _idx,
            "pharmacophore": [bit_label(i) for i in _idx],
            "mean |SHAP|": _mag[_idx],
            "signed mean SHAP": _mean[_idx],
            "direction": np.where(_mean[_idx] > 0, "presence \u2192 TDI", "presence \u2192 non-TDI"),
            "carrier rate": [float((SH_X[:, i] > 0).mean()) for i in _idx],
        }
    )
    mo.md(
        "Top 15 pharmacophore bits by mean |SHAP|. Positive attribution means "
        "**bit presence pushes the prediction toward TDI**; click bars for "
        "magnitude, sign and how often each bit is switched on across the "
        "dataset."
    )
    return SH_EXPL, SH_SCORES, SH_TOP, bit_label


@app.cell
def _(SH_TOP, alt, theme_sel):
    alt.theme.enable(theme_sel.value)
    _bar = (
        alt.Chart(SH_TOP)
        .mark_bar()
        .encode(
            x=alt.X("mean |SHAP|:Q", title="mean |SHAP| attribution"),
            y=alt.Y("pharmacophore:N", sort="-x", title=None),
            color=alt.Color(
                "direction:N",
                scale=alt.Scale(
                    domain=["presence \u2192 TDI", "presence \u2192 non-TDI"],
                    range=["#d62728", "#1f77b4"],
                ),
                title=None,
            ),
            tooltip=[
                alt.Tooltip("pharmacophore:N", title="pharmacophore"),
                alt.Tooltip("mean |SHAP|:Q", format=".3f"),
                alt.Tooltip("signed mean SHAP:Q", format=".3f"),
                alt.Tooltip("carrier rate:Q", format=".1%", title="carrier rate"),
            ],
        )
        .properties(height=380, title="Top pharmacophore bits by SHAP attribution")
    )
    _bar
    return


@app.cell
def _(PHARM_DATA, SH_SCORES, mo, pd):
    _sc = pd.DataFrame(
        {"SMILES": PHARM_DATA["SMILES"], "name": PHARM_DATA["Molecule_Name"], "p": SH_SCORES}
    )
    _sc = (
        _sc.groupby("SMILES", as_index=False)
        .agg({"p": "max", "name": "first"})
        .sort_values("p", ascending=False)
    )
    _opts = {}
    for _, _r in pd.concat([_sc.head(20), _sc.tail(15)]).iterrows():
        _opts[f"{_r['name']}  \u00b7  p(TDI) {_r['p']:.2f}"] = _r["SMILES"]
    mol_src = mo.ui.radio(
        options={"Dataset molecule": "dataset", "Custom SMILES": "custom"},
        value="Dataset molecule",
        inline=True,
        label="Molecule source",
    )
    mol_pick = mo.ui.dropdown(
        options=_opts,
        value=next(iter(_opts)),
        label="Curated: 20 highest- and 15 lowest-scoring dataset molecules",
        full_width=True,
    )
    smi_box = mo.ui.text(
        value="OC(Cn1cncn1)(Cn2cncn2)c3ccc(F)cc3F",
        label="Arbitrary SMILES (e.g. paste a candidate)",
        full_width=True,
    )
    mo.vstack([mol_src, mol_pick, smi_box])
    return mol_pick, mol_src, smi_box


@app.cell
def _(
    Chem,
    Generate,
    PHARM_SIG,
    SH_EXPL,
    bit_label,
    mo,
    mol_pick,
    mol_src,
    np,
    smi_box,
):
    if mol_src.value == "dataset":
        _smi = mol_pick.value
    else:
        _smi = smi_box.value
    EXPL_MOL = Chem.MolFromSmiles(_smi)
    if EXPL_MOL is None:
        EXPL_BITINFO, EXPL_SV = {}, np.zeros(0)
        bit_sel = mo.ui.multiselect(
            options={"(no valid molecule)": ""},
            value=[],
            label="Pharmacophore bits to highlight",
            full_width=True,
        )
    else:
        _bi = {}
        _fp = Generate.Gen2DFingerprint(EXPL_MOL, PHARM_SIG, bitInfo=_bi)
        EXPL_BITINFO = _bi
        EXPL_SV = SH_EXPL.shap_values(np.asarray(_fp, np.float32).reshape(1, -1))[0]
        _on = sorted(
            ((int(_b), float(EXPL_SV[_b])) for _b in _bi if abs(EXPL_SV[_b]) >= 0.01),
            key=lambda _t: -abs(_t[1]),
        )
        _opts = {f"{bit_label(_b)}  (SHAP {_s:+.2f})": _b for _b, _s in _on[:30]}
        _fallback = {"(no pharmacophore bits above threshold)": ""}
        bit_sel = mo.ui.multiselect(
            options=_opts if _opts else _fallback,
            value=[],
            label="Pharmacophore bits to highlight (none selected = SHAP map only)",
            full_width=True,
        )
    bit_sel
    return EXPL_BITINFO, EXPL_MOL, EXPL_SV, bit_sel


@app.cell
def _(EXPL_BITINFO, EXPL_MOL, EXPL_SV, SH_EXPL, bit_label, bit_sel, mo, np):
    import matplotlib

    from rdkit.Chem import Draw, rdDepictor
    from rdkit.Chem.Draw import rdMolDraw2D
    from rdkit.Geometry import Point2D

    if EXPL_MOL is None:
        _view = mo.md("**Invalid SMILES** \u2014 try another string.")
    elif EXPL_MOL.GetNumAtoms() < 2:
        _view = mo.md("Molecule too small to contour \u2014 needs at least 2 atoms.")
    else:
        # net SHAP attribution distributed over the atoms of each ON bit
        _w = np.zeros(EXPL_MOL.GetNumAtoms())
        for _b, _occs in EXPL_BITINFO.items():
            for _occ in _occs:
                for _pt in _occ:
                    for _a in _pt:
                        _w[_a] += EXPL_SV[_b] / (len(_occs) * len(_occ))

        # atoms covered by the selected bits -> single shared highlight colour
        _hl = set()
        for _b in bit_sel.value:
            if _b != "":
                for _occ in EXPL_BITINFO[int(_b)]:
                    for _pt in _occ:
                        _hl.update(_pt)
        _hb = [
            _bond.GetIdx()
            for _bond in EXPL_MOL.GetBonds()
            if _bond.GetBeginAtomIdx() in _hl and _bond.GetEndAtomIdx() in _hl
        ]

        # inline the similarity-map drawing so highlights can be passed through
        _mol = rdMolDraw2D.PrepareMolForDrawing(EXPL_MOL, addChiralHs=False)
        if not _mol.GetNumConformers():
            rdDepictor.Compute2DCoords(_mol)
        _conf = _mol.GetConformer()
        if _mol.GetNumBonds() > 0:
            _b0 = _mol.GetBondWithIdx(0)
            _sigma = 0.3 * (
                _conf.GetAtomPosition(_b0.GetBeginAtomIdx())
                - _conf.GetAtomPosition(_b0.GetEndAtomIdx())
            ).Length()
        else:
            _sigma = 0.3 * (
                _conf.GetAtomPosition(0) - _conf.GetAtomPosition(1)
            ).Length()
        _locs = [
            Point2D(_conf.GetAtomPosition(_i).x, _conf.GetAtomPosition(_i).y)
            for _i in range(_mol.GetNumAtoms())
        ]
        _d2d = Draw.MolDraw2DCairo(450, 400)
        _ps = Draw.ContourParams()
        _ps.fillGrid = True
        _ps.gridResolution = 0.1
        _ps.extraGridPadding = 0.5
        _ps.setColourMap(
            [tuple(_c) for _c in matplotlib.colormaps["RdBu_r"]([0, 0.5, 1])]
        )
        _d2d.ClearDrawing()
        Draw.ContourAndDrawGaussians(
            _d2d,
            _locs,
            _w.tolist(),
            [round(_sigma, 2)] * _mol.GetNumAtoms(),
            nContours=5,
            params=_ps,
        )
        _d2d.drawOptions().clearBackground = False
        _d2d.drawOptions().highlightColour = (1.0, 0.7, 0.0)
        _d2d.DrawMolecule(_mol, highlightAtoms=sorted(_hl), highlightBonds=_hb)
        _d2d.FinishDrawing()

        _p = float(1 / (1 + np.exp(-(SH_EXPL.expected_value + EXPL_SV.sum()))))
        _head = mo.callout(
            mo.md(
                f"**Model p(TDI) = {_p:.0%}** \u2014 predicted probability this "
                "molecule behaves as a time-dependent inhibitor."
            ),
            kind="warn" if _p >= 0.5 else "neutral",
        )
        if _hl:
            _cap = mo.md(
                f"p(TDI) = **{_p:.0%}**. Red = pushed **toward** TDI, blue = away. "
                "Amber highlights the atoms of: "
                + "; ".join(bit_label(int(_b)) for _b in bit_sel.value if _b != "")
                + "."
            )
        else:
            _cap = mo.md(
                f"p(TDI) = **{_p:.0%}**. Red atoms are pushed **toward** TDI by the "
                "model, blue **away** \u2014 the per-atom sum of signed SHAP over every "
                "pharmacophore bit this molecule switches on. Select bits above to "
                "highlight (amber) where they sit."
            )
        _view = mo.vstack([_head, mo.image(_d2d.GetDrawingText(), width=520), _cap])
    _view
    return


if __name__ == "__main__":
    app.run()
