import xarray as xr
import numpy as np
from pathlib import Path
import regionmask

file2check = Path(
    "C:/Users/noodl/Desktop/usa_snow/python_scripts/data_comparison/SNOWH_time_avg.nc"
)

ds = xr.open_dataset(file2check)
print(ds.head)
print(ds.dims)

var = "SNOWH"
# plot data
# ds[var].plot()

mean = np.mean(ds[var].values)
print(f"mean: {mean}")
std = np.std(ds[var].values)
print(f"std: {std}")
max = np.max(ds[var].values)
print(f"max {max}")

array = ds[var].values
non_nan = array[~np.isnan(array)]
max_non_nan = np.max(non_nan)
print(f"max non nan: {max_non_nan}")

non_nan = non_nan.reshape(-1)
sorted = np.sort(non_nan)
print(sorted[-10:])

contus = regionmask.defined_regions.natural_earth_v5_0_0.us_states_50
excluded_states = ["Alaska", "Hawaii", "Puerto Rico"]
contiguous_ids = [
    contus.map_keys(name) for name in contus.names if name not in excluded_states
]
# ds = ds.assign_coords(lon=(((ds.lon + 180) % 360) - 180))
mask = contus.mask(ds)
contiguous_mask = mask.isin(contiguous_ids)
trimmed_ds = ds.where(contiguous_mask)

trimmed_ds[var].plot()

# trimmed_non_nan = trimmed_ds[var].values[~np.isnan(trimmed_ds[var].values)]
