import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Load data
data = pd.read_csv(
    "C:/Users/noodl/Desktop/conus_git/conus_quality_analysis/resort_analysis/resort_density_monthly.csv",
    usecols=["lat", "lon", "north_south", "east_west"],
)

data["region"] = data["north_south"] + "_" + data["east_west"]
region_count = data["region"].value_counts().to_dict()
region_colors = {
    "north_west": "purple",
    "north_rockies": "darkgoldenrod",
    "north_midwest": "cornflowerblue",
    "north_east": "pink",
    "south_west": "mediumblue",
    "south_rockies": "green",
    "south_midwest": "darkorange",
    "south_east": "firebrick",
}
colors = data["region"].map(region_colors)
transform = ccrs.PlateCarree()
plot_size = (12, 10)
plot_bounds = [-127, -65, 27, 50]  # fit to the continental us

fig = plt.figure(figsize=plot_size)
ax = plt.axes(projection=transform)

ax.add_feature(cfeature.STATES, edgecolor="grey", linewidth=0.5)
ax.add_feature(cfeature.COASTLINE, edgecolor="grey")
ax.add_feature(cfeature.BORDERS, edgecolor="grey")

location_plot = ax.scatter(
    data["lon"], data["lat"], transform=transform, s=20, edgecolor="none", c=colors
)

ax.set_extent(plot_bounds, crs=transform)

plt.title("Ski Resort Locations by Region")

legend_elements = [
    plt.Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        label=f"{region} ({region_count.get(region, 0)})",  # Add count to label
        markerfacecolor=color,
        markersize=8,
    )
    for region, color in region_colors.items()
]
ax.legend(
    handles=legend_elements,
    title="Regions (Count)",
    loc="lower right",
    borderaxespad=0.0,
)

plt.show()
