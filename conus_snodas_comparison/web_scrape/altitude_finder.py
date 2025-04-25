import pandas as pd
import requests
import numpy as np
import time


# Function to get altitude_m from latitude and longitude
def get_altitude_m(lat, lon):
    url = f"https://api.opentopodata.org/v1/test-dataset?locations={lat},{lon}"
    response = requests.get(url)
    if response.status_code == 200:
        altitude_out = response.json()["results"][0]["elevation"]
        return altitude_out
    else:
        return np.nan


data = pd.read_csv("resort_data_coords_altitude.csv")

for index, row in data.iterrows():
    if pd.isnull(row["altitude"]):
        time.sleep(2)

        if row["lat"] is np.nan or row["lon"] is np.nan:
            altitude = np.nan

        else:
            altitude = get_altitude_m(row["lat"], row["lon"])

        data.at[index, "altitude"] = altitude
        print(altitude)

    data.to_csv("resort_data_coords_altitude.csv", index=False)
