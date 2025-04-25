import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# URL of the webpage containing the ski resort names

url = "https://www.skiresort.info/ski-resorts/north-america/"

# Send a GET request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find all <a> tags with the specified class
    resort_links = soup.find_all("a", class_="pull-right btn btn-default btn-sm")

    # Extract and print the ski resort names from the href attribute
    column_names = ["resort", "url"]
    resort_data = []
    for link in resort_links:
        href = link["href"]
        resort_name = href.split("/")[-2]  # Extract the resort name from the URL
        print(resort_name)
        resort_data.append({"resort": resort_name, "url": href})
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


pages = [2, 3, 4, 5]

for page in pages:
    url = f"https://www.skiresort.info/ski-resorts/north-america/page/{page}/"

    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all <a> tags with the specified class
        resort_links = soup.find_all("a", class_="pull-right btn btn-default btn-sm")

        # Extract and print the ski resort names from the href attribute
        for link in resort_links:
            href = link["href"]
            resort_name = href.split("/")[-2]  # Extract the resort name from the URL
            print(resort_name)
            resort_data.append({"resort": resort_name, "url": href})
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")


# save to csv
df = pd.DataFrame(resort_data, columns=column_names)
df.to_csv("resort_urls.csv", index=False)
