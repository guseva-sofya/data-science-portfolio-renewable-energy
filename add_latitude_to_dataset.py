import pandas as pd
import numpy as np

data = pd.read_csv("data\Electricity_generation_sources_GDP_area.csv", index_col=0)

# add countries geographic coordinates: latitude

data_lat_long = pd.read_csv("data\Countries_geographic_coordinates.csv", index_col=0)
merged_data = pd.merge(
    data,
    data_lat_long,
    left_index=True,
    right_index=True,
    how="inner",
)

column_order = [
    "region",
    "area (sq km):",
    "latitude",
    "longitude",
    "GDP per capita ($):",
    "fossil fuels (%):",
    "nuclear (%):",
    "solar (%):",
    "wind (%):",
    "hydroelectricity (%):",
    "tide and wave (%):",
    "geothermal (%):",
    "biomass and waste (%):",
]
merged_data = merged_data.reindex(columns=column_order)

# print(merged_data.head())
print(merged_data.iloc[:10, :5])

merged_data.to_csv("data\Electricity_generation_sources_GDP_area_lat_long.csv")
