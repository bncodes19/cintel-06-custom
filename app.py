### Imports ###
import pandas as pd
from pathlib import Path
from faicons import icon_svg
from functools import partial

from shiny import App, ui, reactive, render
from shiny.ui import page_navbar
from shiny.express import render, ui, input
from shinywidgets import render_plotly
import plotly.express as px
import plotly.graph_objects as go
import shinyswatch

### Theme ###
shinyswatch.theme.spacelab()


### Dataset ###
def vgsales_df():
    infile = Path(__file__).parent.joinpath("vgsales.csv")
    return pd.read_csv(infile)


### Page Overview ###
ui.page_opts(title="Video Game Sales Dashboard", fillable=True)

### Sidebar ###
with ui.sidebar(position="left", bg="#f8f8f8", open="open"):
    ui.h5("Video Games Sales (1980-2020)", class_="text-center")
    ui.p(
        "Explore the video game sales dataset.",
        class_="text-center",
    )
    ui.hr()
    ui.input_selectize(
        "selected_genre_list",
        "Select a genre:",
        {
            "Action": "Action",
            "Adventure": "Adventure",
            "Fighting": "Fighting",
            "Misc": "Misc",
            "Platform": "Platform",
            "Puzzle": "Puzzle",
            "Racing": "Racing",
            "Role-Playing": "Role-Playing",
            "Shooter": "Shooter",
            "Simulation": "Simulation",
            "Sports": "Sports",
        },
        selected=["Action"],
        multiple=True,
    )
    ui.input_action_button("reset", "Reset filters")
    ui.hr()
    ui.h5("Project Links:")
    ui.a(
        "GitHub Project Repo",
        href="https://github.com/bncodes19/cintel-06-custom",
        target="_blank",
    )
    ui.a(
        "README.md",
        href="https://github.com/bncodes19/cintel-06-custom/blob/main/README.md",
        target="_blank",
    )
    ui.a(
        "app.py",
        href="https://github.com/bncodes19/cintel-06-custom/blob/main/app.py",
        target="_blank",
    )
    ui.a(
        "vgsales.csv",
        href="https://github.com/bncodes19/cintel-06-custom/blob/main/vgsales.csv",
        target="_blank",
    )
    ui.a(
        "requirements.txt",
        href="https://github.com/bncodes19/cintel-06-custom/blob/main/requirements.txt",
        target="_blank",
    )

### Top KPIs (Sales) ###
with ui.layout_columns():
    with ui.value_box(showcase=icon_svg("dollar-sign"), theme="bg-gradient-green-blue"):
        "North America Sales"

        @render.ui
        def na_sales():
            return f"${round(filtered_df()['NA_Sales'].sum())} million"

    with ui.value_box(showcase=icon_svg("dollar-sign"), theme="bg-gradient-green-blue"):
        "Europe Sales"

        @render.ui
        def eu_sales():
            return f"${round(filtered_df()['EU_Sales'].sum())} million"

    with ui.value_box(showcase=icon_svg("dollar-sign"), theme="bg-gradient-green-blue"):
        "Japan Sales"

        @render.ui
        def jp_sales():
            return f"${round(filtered_df()['JP_Sales'].sum())} million"


### Line graph ###
with ui.layout_columns():
    with ui.card():

        @render_plotly
        def total_sales():
            summed_data = (
                filtered_df()
                .groupby(["Year", "Genre"])["Global_Sales"]
                .sum()
                .reset_index()
            )
            plotly_total_sales = px.line(
                filtered_df(),
                x=summed_data["Year"],
                y=summed_data["Global_Sales"],
                color=summed_data["Genre"],
                title="Global Sales by Year and Genre",
            )
            plotly_total_sales.update_layout(
                xaxis_title="Year", yaxis_title="Global Sales"
            )
            return plotly_total_sales


### Data Grid ###
with ui.card():
    ui.card_header("Data Grid")

    @render.data_frame
    def data_grid():
        return render.DataGrid(filtered_df())


### Filtered data ###
@reactive.calc
def filtered_df():
    genre_input = input.selected_genre_list()
    return vgsales_df()[(vgsales_df()["Genre"].isin(genre_input))]


### Reset filters to original state ###
@reactive.effect
@reactive.event(input.reset)
def _():
    ui.update_selectize(
        "selected_genre_list",
        selected=["Action"],
    )
