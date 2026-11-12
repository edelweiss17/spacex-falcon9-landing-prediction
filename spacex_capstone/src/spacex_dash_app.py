import os
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import plotly.express as px

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "spacex_launch_dash.csv")
spacex_df = pd.read_csv(DATA_PATH)
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

app = Dash(__name__)

launch_sites = spacex_df["Launch Site"].unique().tolist()
site_options = [{"label": "All Sites", "value": "ALL"}] + [{"label": s, "value": s} for s in launch_sites]

app.layout = html.Div(children=[
    html.H1("SpaceX Launch Records Dashboard", style={"textAlign": "center", "color": "#503D36", "fontSize": 36}),
    dcc.Dropdown(
        id="site-dropdown",
        options=site_options,
        value="ALL",
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),
    html.Div(dcc.Graph(id="success-pie-chart")),
    html.Br(),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id="payload-slider",
        min=0,
        max=10000,
        step=1000,
        marks={i: f"{i}" for i in range(0, 10001, 2000)},
        value=[min_payload, max_payload]
    ),
    html.Div(dcc.Graph(id="success-payload-scatter-chart")),
])

@app.callback(
    Output(component_id="success-pie-chart", component_property="figure"),
    Input(component_id="site-dropdown", component_property="value")
)
def get_pie_chart(entered_site):
    if entered_site == "ALL":
        fig = px.pie(
            spacex_df,
            values="class",
            names="Launch Site",
            title="Total Success Launches by Site"
        )
        return fig
    filtered_df = spacex_df[spacex_df["Launch Site"] == entered_site]
    counts = filtered_df["class"].value_counts().reset_index()
    counts.columns = ["Outcome", "Count"]
    counts["Outcome"] = counts["Outcome"].map({1: "Success", 0: "Failure"})
    fig = px.pie(
        counts,
        values="Count",
        names="Outcome",
        title=f"Total Success Launches for site {entered_site}",
        color="Outcome",
        color_discrete_map={"Success": "#2ca02c", "Failure": "#d9534f"}
    )
    return fig

@app.callback(
    Output(component_id="success-payload-scatter-chart", component_property="figure"),
    [
        Input(component_id="site-dropdown", component_property="value"),
        Input(component_id="payload-slider", component_property="value")
    ]
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    filtered_df = spacex_df[
        (spacex_df["Payload Mass (kg)"] >= low) &
        (spacex_df["Payload Mass (kg)"] <= high)
    ]
    if entered_site == "ALL":
        fig = px.scatter(
            filtered_df,
            x="Payload Mass (kg)",
            y="class",
            color="Booster Version Category",
            title="Correlation between Payload and Success for All Sites",
            labels={"class": "Launch Outcome (0: Failure, 1: Success)"}
        )
        return fig
    site_filtered_df = filtered_df[filtered_df["Launch Site"] == entered_site]
    fig = px.scatter(
        site_filtered_df,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        title=f"Correlation between Payload and Success for site {entered_site}",
        labels={"class": "Launch Outcome (0: Failure, 1: Success)"}
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True, port=8050)

