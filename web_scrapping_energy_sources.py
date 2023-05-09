import sys
from bs4 import BeautifulSoup
import requests
import pandas as pd

# web scrapping from original source
static_url = (
    "https://www.cia.gov/the-world-factbook/field/electricity-generation-sources/"
)
html_code = requests.get(static_url).text
soup = BeautifulSoup(html_code, "html.parser")

# finding an ul object with data
ul_objects = soup.find_all("ul")
data_ul = ul_objects[1]
li_objects = data_ul.find_all("li")

column_names = []
tag_strong = li_objects[0].find_all("strong")
for tag_str in tag_strong:
    column_names.append(tag_str.string)

row_names = []
for index, tag_li in enumerate(li_objects):
    tag_h2 = tag_li.h2.string
    row_names.append(tag_h2)

# create a dataframe object
data = pd.DataFrame(columns=column_names, index=row_names)

# parse data to a dataframe
for row_num, tag_li in enumerate(li_objects):
    tag_strong = tag_li.find_all("strong")
    for col_num, tag_str in enumerate(tag_strong):
        strong_sibl = tag_str.next_sibling.string
        numbers = []
        for i, strong_split in enumerate(strong_sibl.split()):
            if i == 0:
                strong_split = strong_split[:-1]
            elif i == 5:
                strong_split = strong_split[1:]
            try:
                numbers.append(float(strong_split))
            except ValueError:
                pass
        data.iloc[row_num, col_num] = numbers[0]

data.to_csv("Electricity_generation_sources.csv", index=False)
