import pandas as pd
import requests
from bs4 import BeautifulSoup

# Read CSV with URLs
resorts = pd.read_csv("resort_urls.csv")

column_names = ["resort", "url", "maps_url", "adv", "int", "beg"]

maps_urls = []

for url in resorts["url"]:
    # Get maps link
    # Get HTML from URL
    page = requests.get(f"{url}/arrival-car/")
    soup = BeautifulSoup(page.content, "html.parser")

    # Get maps URL
    try:
        maps_url = soup.find("a", class_="more-infos")["href"]
    except (AttributeError, TypeError):
        # If the map URL is not found, append None or an empty string
        maps_url = None

    # Append the map URL (or None if not found) to the list
    maps_urls.append(maps_url)

# Optionally, add the map URLs to the DataFrame
resorts["maps_url"] = maps_urls

# Save the updated DataFrame to a new CSV file if needed
resorts.to_csv("resort_urls_with_maps.csv", index=False)
