import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plots


def update_xylabels_fig(text, num_row, num_col):
    fig.update_xaxes(
        title_text="Sum of renewable energy sources (%)", row=num_row, col=num_col
    )
    fig.update_yaxes(title_text=text, row=num_row, col=num_col)


data = pd.read_csv(
    "data\Electricity_generation_sources_GDP_area_lat_long.csv", index_col=0
)
data["sum renewable:"] = data.iloc[:, 7:].sum(axis=1)

# create a choropleth map
choropleth_fig = plots.map_fig(data)

# create horizontal bar chart
barh_fig = plots.renewable_sources_by_region_fig(data)

# create scatter plot
scatter_fig_GDP = plots.renewable_sources_vs_GDP_fig(data)
scatter_fig_latitude = plots.renewable_sources_vs_latitude_fig(data)
scatter_fig_area = plots.renewable_sources_vs_area_fig(data)

# create subplot layout
fig = make_subplots(
    rows=3,
    cols=4,
    specs=[
        [{"type": "choropleth", "colspan": 2}, None, None, {}],
        [{"type": "xy", "colspan": 2}, None, None, {}],
        [{"type": "xy", "colspan": 2}, None, None, {}],
    ],
    subplot_titles=[
        "Sum of renewable energy sources by country (%)",
        "Percentage of countries in each region with sum <br> of renewable energy sources above 50%",
        "Sum of renewable energy sources vs GDP per capita",
        "Sum of renewable energy sources vs country's latitude",
        "Sum of renewable energy sources vs country's area",
    ],
    row_heights=[0.5, 0.5, 0.5],
    column_widths=[0.45, 0.1, 0.05, 0.4],
)
fig.add_trace(choropleth_fig.data[0], row=1, col=[1, 2])
fig.add_trace(barh_fig.data[0], row=1, col=4)
fig.add_trace(scatter_fig_GDP.data[0], row=2, col=[1, 2])
fig.add_trace(scatter_fig_latitude.data[0], row=2, col=4)
fig.add_trace(scatter_fig_area.data[0], row=3, col=[1, 2])
fig.update_layout(
    height=1500,
    width=1200,
    # margin={"r": 10, "t": 10, "l": 10, "b": 10},
    showlegend=False,
    yaxis=dict(autorange="reversed"),
    xaxis=dict(range=[0, 100]),
    xaxis_title="Percentage of countries in a region (%)",
)

update_xylabels_fig("GDP per capita ($)", num_row=2, num_col=1)
update_xylabels_fig("Latitude", num_row=2, num_col=4)
update_xylabels_fig("Area (sq km)", num_row=3, num_col=1)


app = dash.Dash()
app.layout = html.Div(
    style={
        "height": "100vh",
        "display": "flex",
        "flex-direction": "column",
        "align-items": "center",
    },
    children=[
        html.Div(
            style={"margin-top": "1vh"},  # Adjust the top margin for the title
            children=[
                html.H1(
                    "Renewable Energy Sources Dashboard",
                    style={"text-align": "center", "color": "#503D36", "font-size": 40},
                )
            ],
        ),
        # html.Br(),
        html.Div(dcc.Graph(figure=fig)),
    ],
)

if __name__ == "__main__":
    app.run_server(debug=True)  # use_reloader=False
