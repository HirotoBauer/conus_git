import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np


path = "C:/Users/noodl/Desktop/usa_snow/SNODAS/interpolated_us_ssmv11036tS__T0001TTNATS2003093005HP001.nc"

data = xr.open_dataset(path)

data["interpolated_data_snowh"].plot()
plt.show()

snowh_values = data["interpolated_data_snowh"].values

print(np.max(snowh_values))


path2 = "D:/CONUS404/density_test/SNOWH/781316.SNOWH.wrf2d_d01_1979-10-06_18_00_00.nc"

data2 = xr.open_dataset(path2)

data2["SNOWH"].plot()
plt.show()

snowh_values2 = data2["SNOWH"].values

print(np.max(snowh_values2))
