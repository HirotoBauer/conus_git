# compares CONUS and SNODAS datasets using SNODAS as observed values
import xskillscore as xs
import xarray as xr
from pathlib import Path
import regionmask
from matplotlib import pyplot as plt

var = "SNOWH"
snodas_path = Path(
    f"C:/Users/noodl/Desktop/usa_snow/SNODAS/time_smoothed_03-22/snodas_{var}_99.0th_percentile.nc"
)

conus_path = Path(f"C:/Users/noodl/Desktop/usa_snow/processed_data/{var}_99th_full.nc")

snodas_data = xr.open_dataset(snodas_path)
# snodas_data = snodas_data.rename({"interpolated_data_snowh": "SNOWH"})
snodas_data = snodas_data.rename({"lon": "XLONG"})
snodas_data = snodas_data.rename({"lat": "XLAT"})
snodas_data = snodas_data.rename({"y": "south_north", "x": "west_east"})


conus_data = xr.open_dataset(conus_path)

snodas = snodas_data[var]
conus = conus_data[var] * 1000  # convert to mm
# conus = conus.drop_vars("XTIME")
# conus = conus.drop_vars("Time")
# conus = conus.squeeze("Time", drop=True)

# snodas = snodas.fillna(0)  # dont do this, it messes up the rmse calculation
# conus = conus.fillna(0)

# trim datasets to conttinuouse USA
contus = regionmask.defined_regions.natural_earth_v5_0_0.us_states_50
excluded_states = ["Alaska", "Hawaii", "Puerto Rico"]
contiguous_ids = [
    contus.map_keys(name) for name in contus.names if name not in excluded_states
]

snodas_mask = contus.mask(snodas.XLONG, snodas.XLAT)
snodas_contiguous_mask = snodas_mask.isin(contiguous_ids)
snodas_trimmed = snodas.where(snodas_contiguous_mask)

conus_mask = contus.mask(conus.XLONG, conus.XLAT)
conus_contiguous_mask = conus_mask.isin(contiguous_ids)
conus_trimmed = conus.where(conus_contiguous_mask)


# calculate rmse
rmse = xs.rmse(
    snodas_trimmed, conus_trimmed, dim=["south_north", "west_east"], skipna=True
).values
print(f"rmse = {rmse}")

conus_mean = conus.mean(dim=["south_north", "west_east"]).values
snodas_mean = snodas.mean(dim=["south_north", "west_east"]).values

conus_max = conus.max(dim=["south_north", "west_east"]).values
snodas_max = snodas.max(dim=["south_north", "west_east"]).values

print(
    f"conus mean: {conus_mean}\nsnodas mean: {snodas_mean}\nconus max: {conus_max}\nsnodas max: {snodas_max}"
)

# # normalize with standard deviation
# conus_std = conus.std(dim=['south_north', 'west_east'])
# nrmse = rmse / conus_std
# print(nrmse)

# snodas.to_netcdf("snodas_zerod.nc")


# dot plot of the difference
x = snodas_trimmed.values.flatten()
y = conus_trimmed.values.flatten()

plt.figure(figsize=(10, 8))
plt.scatter(x, y, alpha=0.5, s=5, c="royalblue")

# set font size
small = 20
medium = 20
large = 25

plt.rc("font", size=small)  # controls default text sizes
plt.rc("axes", titlesize=large)  # fontsize of the axes title
plt.rc("axes", labelsize=medium)  # fontsize of the x and y labels
plt.rc("xtick", labelsize=small)  # fontsize of the tick labels
plt.rc("ytick", labelsize=small)  # fontsize of the tick labels
plt.rc("legend", fontsize=small)  # legend fontsize
plt.rc("figure", titlesize=large)  # fontsize of the figure title

plt.title(f"SNODAS vs CONUS404 {var} Data")
plt.xlabel("SNODAS")
plt.ylabel("CONUS404")

ax_max = 6000
ax = plt.gca()
ax.set_xlim(0, ax_max)
ax.set_ylim(0, ax_max)

# add 1:1 line
plt.plot(
    [0, ax_max],
    [0, ax_max],
    color="red",
    linestyle="--",
    linewidth=1.3,
    label="1:1 line",
)

plt.show()
