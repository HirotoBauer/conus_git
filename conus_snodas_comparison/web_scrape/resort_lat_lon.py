import pandas as pd
import numpy as np

data = pd.read_csv("resort_urls_with_maps.csv")

lat = []
lon = []

for url in data["maps_url"]:
    if url is not np.nan:
        lat_temp = url.split("q=")[1].split(",")[0]
        lon_temp = url.split("q=")[1].split(",")[1]

        lat.append(lat_temp)
        lon.append(lon_temp)

    else:
        lat.append(np.nan)
        lon.append(np.nan)

data["lat"] = lat
data["lon"] = lon

data.to_csv("resort_data_coords.csv", index=False)

print(data.head())
