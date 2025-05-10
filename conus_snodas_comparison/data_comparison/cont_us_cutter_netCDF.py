import xarray as xr
import regionmask

data = xr.open_dataset("SNOW_time_avg.nc")

# Load U.S. states (including non-continental)
contus = regionmask.defined_regions.natural_earth_v5_0_0.us_states_50

# Define states to exclude (Alaska, Hawaii, Puerto Rico, etc.)
excluded_states = ["Alaska", "Hawaii", "Puerto Rico"]

# Get region IDs for contiguous states
contiguous_ids = [
    contus.map_keys(name) for name in contus.names if name not in excluded_states
]

# Generate mask for the dataset
mask = contus.mask(data)

# Create a combined mask for all contiguous states
contiguous_mask = mask.isin(contiguous_ids)

# Apply the mask to the data
contus_data = data.where(contiguous_mask, drop=True)

contus_data.to_netcdf("SNODAS_SNOW_cut_time_avg.nc")
