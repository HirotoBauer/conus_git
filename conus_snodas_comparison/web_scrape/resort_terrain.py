import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np

df = pd.read_csv("resort_data_coords_altitude.csv")

beginner_terrain = []
intermediate_terrain = []
expert_terrain = []
for url in df["url"]:
    page = requests.get(f"{url}/slope-offering/")
    soup = BeautifulSoup(page.content, "html.parser")

    # Find all <td> elements with the class "percent hidden-xs"
    percent_elements = soup.find_all("td", class_="percent hidden-xs")

    # Extract the percentages from the elements
    percentages = [
        element.get_text(strip=True).strip("()%") for element in percent_elements
    ]

    # Ensure we have exactly 3 percentages (beginner, intermediate, expert)
    if len(percentages) >= 3:
        beginner, intermediate, expert = percentages[:3]
    else:
        print(f"manually check {url}")
        beginner, intermediate, expert = np.nan, np.nan, np.nan

    # Append the percentages to the DataFrame
    beginner_terrain.append(beginner)
    intermediate_terrain.append(intermediate)
    expert_terrain.append(expert)

df["beg"] = beginner_terrain
df["int"] = intermediate_terrain
df["adv"] = expert_terrain

df.to_csv("resort_data_coords_altitude_terrain.csv", index=False)
