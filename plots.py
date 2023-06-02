import plotly.graph_objects as go
import get_color_palette


def map_fig(data):
    # create a choropleth map
    choropleth_fig = go.Figure(
        go.Choropleth(
            locations=data.index,
            locationmode="country names",
            z=data["sum renewable:"],
            colorscale="RdYlGn",
            colorbar=dict(
                title="Percent,<br> %", len=0.8, x=-0.07, y=0.525, ticksuffix=""
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


def renewable_sources_by_region(data):
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

    colors = get_color_palette.color_palette()

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
