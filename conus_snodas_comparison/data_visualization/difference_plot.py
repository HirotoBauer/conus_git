import xarray as xr
from pathlib import Path
from matplotlib import pyplot as plt
import regionmask
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import matplotlib.colors as mcolors


var = "SNOWH"
snodas_path = Path(
    f"C:/Users/noodl/Desktop/usa_snow/SNODAS/time_smoothed_03-22/snodas_{var}_time_avg.nc"
)

conus_path = Path("D:/CONUS404/comparison/conus_SNOWH_time_avg.nc")


# make the names of the variables the same between the datasets
snodas_data = xr.open_dataset(snodas_path)
try:
    snodas_data = snodas_data.squeeze("time", drop=True)
except KeyError:
    pass
snodas_data = snodas_data.rename({"y": "south_north", "x": "west_east"})

conus_data = xr.open_dataset(conus_path)
try:
    conus_data = conus_data.squeeze("Time", drop=True)
except KeyError:
    pass
# conus_data = conus_data.rename({"XLONG": "lon", "XLAT": "lat"}) # not sure why this line is not needed
conus_data[var] = conus_data[var] * 1000

# set nan values to zeros
snodas_data = snodas_data.fillna(0)
conus_data = conus_data.fillna(0)

# calculate the difference between the datasets while maintaining the spatial dimension
difference = conus_data[var] - snodas_data[var]

# trimm the difference to only usa
contus = regionmask.defined_regions.natural_earth_v5_0_0.us_states_50
excluded_states = ["Alaska", "Hawaii", "Puerto Rico"]
contiguous_ids = [
    contus.map_keys(name) for name in contus.names if name not in excluded_states
]

mask = contus.mask(difference)
contiguous_mask = mask.isin(contiguous_ids)
trimmed_difference = difference.where(contiguous_mask)


# spatial plot of the difference
# Define discrete levels for the colorbar
# cmap_norm = max(abs(np.nanmin(trimmed_difference.values)), abs(np.nanmax(trimmed_difference.values)))
cmap_norm = 500
# levels = np.linspace(-1 * cmap_norm, cmap_norm, 14)
levels = [-500, -200, -100, -50, -5, 5, 50, 100, 200, 500]
n_levels = len(levels) - 1

# Create a discrete colormap and normalization
cmap = plt.get_cmap("seismic", n_levels)  # discrete colormap

colors = cmap(np.arange(cmap.N)).copy()

# setting white to middle of color map
white_range = 3
norm = mcolors.Normalize(vmin=-cmap_norm, vmax=cmap_norm)
lower_idx = int(norm(-white_range) * cmap.N)
upper_idx = int(norm(white_range) * cmap.N)

colors[lower_idx:upper_idx] = [1, 1, 1, 1]  # sets the color

white_seismic = mcolors.ListedColormap(colors)
norm = mcolors.BoundaryNorm(boundaries=levels, ncolors=white_seismic.N)

# norm = mcolors.BoundaryNorm(boundaries=levels, ncolors=cmap.N)

plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

# set font size
SMALL_SIZE = 12
MEDIUM_SIZE = 20
BIGGER_SIZE = 25

plt.rc("font", size=SMALL_SIZE)  # controls default text sizes
plt.rc("axes", titlesize=BIGGER_SIZE)  # fontsize of the axes title
plt.rc("axes", labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc("xtick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc("ytick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc("legend", fontsize=SMALL_SIZE)  # legend fontsize
plt.rc("figure", titlesize=BIGGER_SIZE)  # fontsize of the figure title

# set grey background
ax.set_facecolor("lightgrey")


mesh = ax.pcolormesh(
    trimmed_difference.lon,
    trimmed_difference.lat,
    trimmed_difference,
    cmap=white_seismic,
    norm=norm,
    transform=ccrs.PlateCarree(),
)

cbar = plt.colorbar(
    mesh,
    orientation="vertical",
    pad=0.02,
    aspect=30,
    ticks=levels,
    spacing="proportional",
)
cbar.set_label("Snow Depth Difference (mm)")

ax.add_feature(cfeature.BORDERS, edgecolor="black")
ax.add_feature(cfeature.STATES, linewidth=0.5)
ax.add_feature(cfeature.COASTLINE)
ax.set_extent([-125, -66, 24, 50], crs=ccrs.PlateCarree())
plt.title(
    # f"99th Percentile\nCONUS404: {var} - SNODAS: {var}"
    f"Time Averaged\nCONUS404: {var} - SNODAS: {var}"
)

plt.show()
