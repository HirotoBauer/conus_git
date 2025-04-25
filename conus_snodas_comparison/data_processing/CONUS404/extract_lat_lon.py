# extracts the lat and lon values from the 2d arrays used in CONUS
import xarray as xr
from pathlib import Path
import numpy as np

# define grid for upscaling
conus_path = Path(
    "C:/Users/noodl/Desktop/usa_snow/SNODAS/conus_data_for_grid/781316.SNOW.wrf2d_d01_1980-04-24_00_00_00.nc"
)
conus = xr.open_dataset(conus_path)

lat = conus["XLAT"].values.flatten()
lon = conus["XLONG"].values.flatten()

np.savetxt("lat_list.csv", lat, delimiter=",")
np.savetxt("lon_list.csv", lon, delimiter=",")
