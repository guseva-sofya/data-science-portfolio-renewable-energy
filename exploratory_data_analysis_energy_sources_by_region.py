import sys
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import textwrap
import get_color_palette

data = pd.read_csv(
    "data\Electricity_generation_sources_GDP_area_lat_long.csv", index_col=0
)

# sum of the renewable sources
data["sum renewable:"] = data.iloc[:, 7:].sum(axis=1)
print(data.head())

# % of the sum of renewable energy sources
threshold = 50
above_threshold = (
    data[data["sum renewable:"] > threshold].groupby("region").count()["sum renewable:"]
)

# count the total number of countries in each region
total_countries = data.groupby("region").count()["sum renewable:"]

# calculate the percentage of countries where the renewable energy
# value is above the threshold for each region
percent_above_threshold = above_threshold / total_countries * 100
resulted_data = pd.DataFrame(
    {
        "above_threshold": above_threshold,
        "total_countries": total_countries,
        "percent_above_threshold": percent_above_threshold,
    }
)

print(resulted_data)

selected_countries = data[
    (data["sum renewable:"] > 50) & (data["GDP per capita ($):"] < 20000)
]

# scatter plot
fig, ax = plt.subplots(figsize=(9, 6))
plt.scatter(x=data["sum renewable:"], y=data["GDP per capita ($):"])

selected_index = data.loc["Spain", "GDP per capita ($):"]
print(selected_index)
plt.scatter(
    x=data.loc["United States", "sum renewable:"],
    y=data.loc["United States", "GDP per capita ($):"],
    c="red",
)

plt.scatter(
    x=selected_countries["sum renewable:"],
    y=selected_countries["GDP per capita ($):"],
    c="red",
)

plt.xlabel("Sum of the renewable energy sources (%)")
plt.ylabel("GDP per capita ($)")
plt.title("Sum of the renewable energy sources (%) vs. GDP per capita ($)")
# plt.show()

plt.savefig("figures\sum_renewable_energy_sources_vs_GDP.png", dpi=300)
plt.show()

selected_countries = data[
    (data["sum renewable:"] > 50) & (data["GDP per capita ($):"] < 20000)
]
# print(selected_countries.head())
# selected_countries_regions = selected_countries.groupby("region").count()[
#     "sum renewable:"
# ]
# print(selected_countries_regions)

# selected_countries.to_csv("selected_countries_low_GDP.csv")


selected_countries = data[
    (data["sum renewable:"] < 20) & (data["GDP per capita ($):"] > 40000)
]
# print(selected_countries.head())
# selected_countries_regions = selected_countries.groupby("region").count()[
#     "sum renewable:"
# ]
# print(selected_countries_regions)

# selected_countries.to_csv("selected_countries_high_GDP.csv")

fig, ax = plt.subplots(figsize=(9, 6))
plt.scatter(x=data["sum renewable:"], y=abs(data["latitude"]))

plt.xlabel("Sum of the renewable energy sources (%)")
plt.ylabel("Latitude")
plt.title("Sum of the renewable energy sources (%) vs. Latitude")
# plt.show()

plt.savefig("figures\sum_renewable_energy_sources_vs_latitude.png", dpi=300)
plt.show()

fig, ax = plt.subplots(figsize=(9, 6))
plt.scatter(x=data["sum renewable:"], y=abs(data["area (sq km):"]))

plt.xlabel("Sum of the renewable energy sources (%)")
plt.ylabel("Country area [sq km]")
plt.title("Sum of the renewable energy sources (%) vs. Country area")
# plt.show()

plt.savefig("figures\sum_renewable_energy_sources_vs_area.png", dpi=300)
plt.show()
