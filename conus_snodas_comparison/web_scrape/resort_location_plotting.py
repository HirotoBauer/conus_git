import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Load data
data = pd.read_csv(
    "resort_data_coords_altitude_terrain_contUS.csv", usecols=["lat", "lon", "altitude"]
)

cmap = "copper"
alt_min = 0
alt_max = max(data["altitude"].values)

transform = ccrs.PlateCarree()
plot_size = (10, 6)
plot_bounds = [-137.873, -58.463, 17.631, 56.704]  # bound of the CONUS404 dataset

fig = plt.figure(figsize=plot_size)
ax = plt.axes(projection=transform)

ax.add_feature(cfeature.STATES, edgecolor="grey", linewidth=0.5)
ax.add_feature(cfeature.COASTLINE, edgecolor="grey")
ax.add_feature(cfeature.BORDERS, edgecolor="grey")

location_plot = ax.scatter(
    data["lon"],
    data["lat"],
    c=data["altitude"],
    cmap=cmap,
    transform=transform,
    s=9,
    vmin=alt_min,
    vmax=alt_max,
    edgecolor="none",
)

cbar = plt.colorbar(location_plot, orientation="vertical", pad=0.01)
cbar.set_label("Ski Resort Elevation (m)")

ax.set_extent(plot_bounds, crs=transform)

plt.title("Ski Resort Location With Elevation")

plt.show()
