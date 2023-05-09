import sys
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


def parse_coordinates(coordinates):
    lat_long = coordinates.split(", ")
    lat_str, long_str = lat_long[0], lat_long[1]
    lat = float(lat_str.replace(" ", ".", 1)[:5])
    long = float(long_str.replace(" ", ".", 1)[:5])

    if "S" in lat_str:
        lat = -lat
    if "W" in long_str:
        long = -long

    return lat, long


# web scrapping from original source
static_url = "https://www.cia.gov/the-world-factbook/field/geographic-coordinates/"
html_code = requests.get(static_url).text
soup = BeautifulSoup(html_code, "html.parser")

# print(soup.prettify())

# finding an ul object with data
ul_objects = soup.find_all("ul")
data_ul = ul_objects[1]
li_objects = data_ul.find_all("li")

row_names = []
lat = []
long = []
for index, tag_li in enumerate(li_objects):
    tag_h2 = tag_li.h2.string
    row_names.append(tag_h2)

    if index == 14:
        tag_p = tag_li.p.get_text()
        tag_p = tag_p[:17]
    elif index == 83:
        tag_p = tag_li.p.get_text()
        tag_p = tag_p[21:36]
    elif index in [85, 193, 245]:
        tag_p = np.nan
    else:
        tag_p = tag_li.p.string

    if tag_p is not np.nan:
        # print(tag_p)
        lat_, long_ = parse_coordinates(tag_p)
        lat.append(lat_)
        long.append(long_)
    else:
        lat.append(np.nan)
        long.append(np.nan)

dict_lat_long = {"latitude": lat, "longitude": long}

data = pd.DataFrame(data=dict_lat_long, index=row_names)

print(data.tail(50))

data.to_csv("data\Countries_geographic_coordinates.csv")
