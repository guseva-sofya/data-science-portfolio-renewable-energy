import pandas as pd

data = pd.read_csv("data\Electricity_generation_sources_GDP.csv", index_col=0)

# add real GDP per capita to a table from downloaded .csv
data_GDP = pd.read_csv("Real_GDP_per_capita.csv")

# Perform left join on country name column
merged_df = pd.merge(
    data,
    data_GDP[["name", "value", "region"]],
    left_index=True,
    right_on="name",
    how="left",
)

# Set the index to country names
merged_df.set_index(data.index, inplace=True)
merged_df.drop("name", axis=1, inplace=True)

# remove $ sign from GDP column
merged_df["value"] = pd.to_numeric(
    merged_df["value"].str.replace(",", "").str.replace("$", "")
)

merged_df.rename(columns={"value": "GDP per capita ($):"}, inplace=True)
print(merged_df)

merged_df.to_csv("Electricity_generation_sources_GDP.csv")
