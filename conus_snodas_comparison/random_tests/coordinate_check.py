import xarray as xr
import numpy as np

# extract coordinate from SNODAS data
snodas_path = "C:/Users/noodl/Desktop/usa_snow/SNODAS/interpolated_us_ssmv11036tS__T0001TTNATS2003093005HP001.nc"
snodas_data = xr.open_dataset(snodas_path)
snodas_lat = snodas_data.coords["lat"].values
snodas_lon = snodas_data.coords["lon"].values
snodas_data.close()

conus_path = "C:/Users/noodl/Desktop/usa_snow/rmse_test_data/conus/781316.SNOWH.wrf2d_d01_2006-03-01_06_00_00.nc"
conus_data = xr.open_dataset(conus_path)
conus_lat = conus_data.coords["XLAT"].values
conus_lon = conus_data.coords["XLONG"].values
conus_data.close()

# check if coordinates are the same
if np.all(snodas_lat == conus_lat) and np.all(snodas_lon == conus_lon):
    print("coordinate grids are the same")

else:
    print("coordinate grids are different")
