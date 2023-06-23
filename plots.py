from typing import List
import plotly.graph_objects as go


def map_fig(data) -> go.Figure:
    # create a choropleth map
    choropleth_fig = go.Figure(
        go.Choropleth(
            locations=data.index,
            locationmode="country names",
            z=data["sum renewable:"],
            colorscale="RdYlGn",
            colorbar=dict(
                title="Percent,<br> %", len=0.25, x=-0.07, y=0.9, ticksuffix=""
            ),
            uirevision=True,
        )
    )

    choropleth_fig.update_geos(
        lataxis_showgrid=True,
        lonaxis_showgrid=True,
        showcountries=True,
        countrycolor="gray",
    )
    choropleth_fig.update_layout(
        title="Sum of renewable energy sources by country",
        geo=dict(
            showframe=False, showcoastlines=False, projection_type="equirectangular"
        ),
    )
    return choropleth_fig


def renewable_sources_by_region_fig(data) -> go.Figure:
    # % of the sum of renewable energy sources
    threshold = 50
    above_threshold = (
        data[data["sum renewable:"] > threshold]
        .groupby("region")
        .count()["sum renewable:"]
    )

    # count the total number of countries in each region
    total_countries = data.groupby("region").count()["sum renewable:"]

    # calculate the percentage of countries where the renewable energy
    # value is above the threshold for each region
    percent_above_threshold = above_threshold / total_countries * 100

    # sort the percent_above_threshold series in descending order
    sorted_percent_above_threshold = percent_above_threshold.sort_values(
        ascending=False
    )

    sorted_percent_above_threshold.index.values[
        6
    ] = "Central America <br> and the Caribbean"

    sorted_percent_above_threshold.index.values[8] = "East and <br> Southeast Asia"

    max_indices = sorted_percent_above_threshold.index[:2]

    colors = color_palette()

    barh_fig = go.Figure(
        go.Bar(
            x=sorted_percent_above_threshold,
            y=sorted_percent_above_threshold.index,
            orientation="h",
            marker=dict(
                color=colors,
                line=dict(color="rgba(58, 71, 80, 1.0)", width=1),
            ),
        )
    )

    return barh_fig


def renewable_sources_vs_GDP_fig(data) -> go.Figure:
    scatter_fig_GDP = go.Figure()
    scatter_fig_GDP.add_trace(
        go.Scatter(
            x=data["sum renewable:"],
            y=data["GDP per capita ($):"],
            mode="markers",
            marker=dict(size=8),
        )
    )

    return scatter_fig_GDP


def renewable_sources_vs_latitude_fig(data) -> go.Figure:
    scatter_fig_latitude = go.Figure()
    scatter_fig_latitude.add_trace(
        go.Scatter(
            x=data["sum renewable:"],
            y=data["latitude"],
            mode="markers",
            marker=dict(size=8, color="blue"),
        )
    )

    return scatter_fig_latitude


def renewable_sources_vs_area_fig(data) -> go.Figure:
    scatter_fig_area = go.Figure()
    scatter_fig_area.add_trace(
        go.Scatter(
            x=data["sum renewable:"],
            y=data["area (sq km):"],
            mode="markers",
            marker=dict(size=8, color="red"),
        )
    )

    return scatter_fig_area


def color_palette() -> List[str]:
    colors = [
        "#DA6085",
        "#DC7D8B",
        "#DE9A91",
        "#E0B798",
        "#E2D49E",
        "#D8D29F",
        "#CED0A0",
        "#C4CEA1",
        "#BACCA2",
        "#D7EDE1",
    ]

    colors.reverse()

    return colors
