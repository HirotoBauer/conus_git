# plots yearly averages of SNODAS and CONUS data
import xarray as xr
from pathlib import Path
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

var = "SNOWH"
start_year = 2004
end_year = 2022


# function for smoothing out the spatial dimiension of the data. Takes xr array
def smooth_space(ds):
    smoothed = ds.values.flatten()
    return np.mean(smoothed[~np.isnan(smoothed)])


snodas_file_path_list = Path(
    "C:/Users/noodl/Desktop/usa_snow/file_path_lists/snodas_yearly_file_list.csv"
)
snodas_files = pd.read_csv(snodas_file_path_list)
snodas_files2plot = snodas_files.loc[
    (snodas_files["water_year"] >= start_year)
    & (snodas_files["water_year"] <= end_year)
    & (snodas_files["variable"] == var)
]

conus_file_path_list = Path(
    "C:/Users/noodl/Desktop/usa_snow/file_path_lists/conus_yearly_file_list.csv"
)
conus_files = pd.read_csv(conus_file_path_list)
conus_files2plot = conus_files.loc[
    (conus_files["water_year"] >= start_year)
    & (conus_files["water_year"] <= end_year)
    & (conus_files["variable"] == var)
]

snodas_mean = []
conus_mean = []
water_year = []

for year in range(start_year, end_year + 1):
    snodas = xr.open_dataset(
        snodas_files2plot.loc[snodas_files2plot["water_year"] == year][
            "file_path"
        ].values[0]
    )
    snodas_smoothed = smooth_space(snodas[var])

    conus = xr.open_dataset(
        conus_files2plot.loc[snodas_files2plot["water_year"] == year][
            "file_path"
        ].values[0]
    )
    conus_smoothed = smooth_space(conus[var])

    snodas_mean.append(snodas_smoothed)
    conus_mean.append(conus_smoothed)
    water_year.append(year)

water_year = [int(x) for x in water_year]

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(
    water_year, snodas_mean, label="SNODAS", color="orange", markersize=10, marker="o"
)
ax.plot(
    water_year, conus_mean, label="CONUS404", color="blue", markersize=10, marker="s"
)

ax.set_xticks(water_year)
ax.tick_params(axis="x", rotation=45)
ax.set_xlabel("Water Year")
ax.set_ylabel(f"{var} (mm)")
ax.set_title(f"{var} Yearly Mean")
ax.legend()
