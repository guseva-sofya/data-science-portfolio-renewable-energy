import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from plots import map_fig, renewable_sources_by_region


data = pd.read_csv(
    "data\Electricity_generation_sources_GDP_area_lat_long.csv", index_col=0
)
data["sum renewable:"] = data.iloc[:, 7:].sum(axis=1)

# create a choropleth map
choropleth_fig = map_fig(data)

# create horizontal bar chart
barh_fig = renewable_sources_by_region(data)

# create random scatter plot
# scatter_fig = go.Figure()
# scatter_fig.add_trace(
#     go.Scatter(
#         x=[1, 2, 3, 4, 5, 6],
#         y=[30, 20, 50, 10, 40, 60],
#         mode="markers",
#         marker=dict(size=10),
#         name="Random Scatter Plot",
#     )
# )
# scatter_fig.update_layout(title="Random Scatter Plot")


# create subplot layout
fig = make_subplots(
    rows=1,
    cols=4,
    specs=[[{"type": "choropleth", "colspan": 2}, None, None, {}]],
    subplot_titles=[
        "Sum of renewable energy sources by country (%)",
        "Percentage of countries in each region with sum <br> of renewable energy sources above 50%",
    ],
    row_heights=[0.3],
    column_widths=[0.45, 0.1, 0.05, 0.4],
)
fig.add_trace(choropleth_fig.data[0], row=1, col=[1, 2])
fig.add_trace(barh_fig.data[0], row=1, col=4)
fig.update_layout(
    height=600,
    width=1200,
    # margin={"r": 10, "t": 10, "l": 10, "b": 10},
    showlegend=False,
    yaxis=dict(autorange="reversed"),
    xaxis=dict(range=[0, 100]),
)

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
