import xarray as xr
from pathlib import Path
from matplotlib import pyplot as plt
import regionmask
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
import matplotlib.colors as mcolors

var = "Pearson"

path2data = Path("D:/yearly_pearson/pearson_r_SNOWH_snodas_vs_conus.nc")

ds = xr.open_dataset(path2data)

# trimming to cont usa
contus = regionmask.defined_regions.natural_earth_v5_0_0.us_states_50
excluded_states = ["Alaska", "Hawaii", "Puerto Rico"]
contiguous_ids = [
    contus.map_keys(name) for name in contus.names if name not in excluded_states
]
mask = contus.mask(ds)
cont_mask = mask.isin(contiguous_ids)
trimmed = ds.where(cont_mask)

# print mean
print(np.mean(trimmed))

# set font size
small = 18
medium = 20
large = 23

plt.rc("font", size=small)  # controls default text sizes
plt.rc("axes", titlesize=medium)  # fontsize of the axes title
plt.rc("legend", fontsize=small)  # legend fontsize
plt.rc("figure", titlesize=large)  # fontsize of the figure title

cmin = 0
cmax = 1
levels = np.linspace(cmin, cmax, 11)
n_levels = len(levels) - 1

# Create a discrete colormap and normalization
cmap = plt.get_cmap("Reds", n_levels)  # discrete colormap
colors = cmap(np.arange(cmap.N))

# setting white to middle of color map
colors[0] = mcolors.to_rgba("darkblue")

custom_cmap = mcolors.ListedColormap(colors)
norm = mcolors.BoundaryNorm(boundaries=levels, ncolors=custom_cmap.N)


# plotting
plt.figure(figsize=(12, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

# set grey background
ax.set_facecolor("lightgrey")

mesh = ax.pcolormesh(
    trimmed.lon,
    trimmed.lat,
    trimmed[var],
    cmap=custom_cmap,
    norm=norm,
    transform=ccrs.PlateCarree(),
)

cbar = plt.colorbar(mesh, orientation="vertical", pad=0.02, aspect=30, ticks=levels)
cbar.set_label("Pearson r value")

ax.add_feature(cfeature.BORDERS, edgecolor="black")
ax.add_feature(cfeature.STATES, linewidth=0.5)
ax.add_feature(cfeature.COASTLINE)
ax.set_extent([-125, -66, 24, 50], crs=ccrs.PlateCarree())
plt.title(
    "Pearson Correlation Between CONUS and SNODAS",
)

plt.show()
