import sys
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import textwrap
import get_color_palette

# read .csv file
data = pd.read_csv('data\Electricity_generation_sources_GDP.csv', index_col=0)

# sum of the renewable sources
data['sum renewable:'] = data.iloc[:, 2:8].sum(axis=1)
print(data.head())

# % of the sum of renewable energy sources
threshold = 50 
above_threshold = data[data['sum renewable:'] > 
                       threshold].groupby('region').count()['sum renewable:']

# count the total number of countries in each region
total_countries = data.groupby('region').count()['sum renewable:']

# calculate the percentage of countries where the renewable energy 
# value is above the threshold for each region
percent_above_threshold = above_threshold / total_countries * 100

# create a new dataframe with the results
results_df = pd.DataFrame({'above_threshold': above_threshold, 
                           'total_countries': total_countries, 
                           'percent_above_threshold': percent_above_threshold})

print(results_df)

# plot a horizontal bar chart
fig, ax = plt.subplots(figsize=(9,6))

# sort the percent_above_threshold series in descending order
sorted_percent_above_threshold = percent_above_threshold.sort_values(ascending=False)

# take the first two indices with the highest values
max_indices = sorted_percent_above_threshold.index[:2]

# create a list of colors for the bars
# colors = ['red' if region in max_indices else 'blue' 
# for region in sorted_percent_above_threshold.index]
colors = get_color_palette.color_palette()

ax.barh(sorted_percent_above_threshold.index, sorted_percent_above_threshold, color=colors)

# add labels and title
ax.set_xlabel('Percentage of countries with sum of renewable energy sources above 50%')
ax.set_ylabel('Region')
ax.set_title(f"Percentage of countries with sum of renewable energy sources above 50% by region")

# set the x-axis limit to 100%
ax.set_xlim([0, 100])

# split the ticklabels on y-axis into two lines
wrap_width = 13 # set the number of characters per line
ax.set_yticklabels([ '\n'.join(textwrap.wrap(label, wrap_width)) 
                     for label in sorted_percent_above_threshold.index])

# invert the y-axis
ax.invert_yaxis()

plt.savefig('figures\energy_threshold.png', dpi=300) 
plt.show()

# find unique regions
unique_regions = data['region'].unique()
print(unique_regions)