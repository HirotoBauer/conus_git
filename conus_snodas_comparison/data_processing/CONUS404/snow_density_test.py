import xarray as xr
from pathlib import Path
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np

# Load the data
base_dir = Path("C:/Users/noodl/Desktop/usa_snow/CONUS404")
file_dir = base_dir / "swe_mixing_test/wrf2d_d01_2021-02-01_00%3A00%3A00.nc"
vars_to_load = ["SNOW", "SNOWH"]
data = xr.open_dataset(file_dir)
vars_all = list(data.keys())
vars_remove = [var for var in vars_all if var not in vars_to_load]
data.close()
data = xr.open_dataset(file_dir, drop_variables=vars_remove)

# Calculate density
data["density"] = data["SNOW"] / data["SNOWH"]
data["density"] = data["density"].squeeze()

# Extract latitude and longitude from the dataset
lat = data["XLAT"].squeeze()  # Ensure the dimensions are correct
lon = data["XLONG"].squeeze()  # Ensure the dimensions are correct

# Create a plot with a US projection
fig = plt.figure(figsize=(10, 6))
ax = plt.axes(
    projection=ccrs.PlateCarree()
)  # Use PlateCarree projection for latitude/longitude

# Add map features
ax.add_feature(cfeature.STATES, edgecolor="black")  # Add US states
ax.add_feature(cfeature.COASTLINE)  # Add coastline
ax.add_feature(cfeature.BORDERS)  # Add country borders

# Plot the density variable
density_plot = ax.pcolormesh(
    lon, lat, data["density"], cmap="cividis", transform=ccrs.PlateCarree()
)

# Add a colorbar
cbar = plt.colorbar(density_plot, orientation="horizontal", pad=0.05)
cbar.set_label("Snow Density (kg/m³)")

# Set the extent to focus on the US
ax.set_extent(
    [-125, -66, 24, 50], crs=ccrs.PlateCarree()
)  # Adjust these values as needed

# Add a title
plt.title("Snow Density over the US on 2021-02-01")

# Show the plot
plt.show()
