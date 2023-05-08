import pandas as pd
import numpy as np

data = pd.read_csv("data\Electricity_generation_sources_GDP.csv", index_col=0)

# add countries area

data_area = pd.read_csv("data\Countries_area.csv")
merged_data = pd.merge(
    data,
    data_area[["name", "value"]],
    left_index=True,
    right_on="name",
    how="left",
)

merged_data.set_index(data.index, inplace=True)
merged_data.drop("name", axis=1, inplace=True)
merged_data.rename(columns={"value": "area (sq km):"}, inplace=True)

# check the type of the area column

print(merged_data["area (sq km):"].dtype)
print(merged_data["GDP per capita ($):"].dtype)

# remove comma from area column

merged_data["area (sq km):"] = pd.to_numeric(
    merged_data["area (sq km):"].str.replace(",", "")
)

# remove empty space from the end of the columns' names

rename_col = {col: col.replace(": ", " (%):") for col in merged_data.columns}
merged_data = merged_data.rename(columns=rename_col)

# reorder columns

merged_data = merged_data.reindex(
    columns=[
        "region",
        "area (sq km):",
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
)

# find missing values

count_missing_val = merged_data.isna().sum().sum()
print("Amount of missing values:", count_missing_val)

# replace empty spaces with NaN
# merged_data = merged_data.replace(r"^\s*$", np.nan, regex=True)

print(merged_data.iloc[-6:, :4])

merged_data.to_csv("data\Electricity_generation_sources_GDP_area.csv")
