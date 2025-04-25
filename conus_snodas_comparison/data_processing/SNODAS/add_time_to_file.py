import xarray as xr
import pandas as pd
from dask.diagnostics import ProgressBar
from datetime import datetime


dataset_list = pd.read_csv(
    "C:/Users/noodl/Desktop/usa_snow/file_path_lists/snodas_SNOW.csv"
)

dataset_list["date"] = pd.to_datetime(dataset_list["date"])

with ProgressBar():
    for index, row in dataset_list.iterrows():
        ds = xr.open_dataset(row["file_path"])
        ds = ds.expand_dims(time=[row["date"]])

        ds_name = row["file_path"].split(sep="/")[-1]
        ds.to_netcdf(f"D:/SNODAS/interpolated_w_time/timestamp_{ds_name}")


# ds = xr.open_dataset("C:/Users/noodl/Desktop/usa_snow/SNODAS/interpolated_us_ssmv11036tS__T0001TTNATS2006030105HP001.nc")
# time = datetime.strptime("2006/03/01 05:00:00", '%Y/%m/%d %H:%M:%S')
# ds = ds.expand_dims(time=[time])

# ds_name = "interpolated_us_ssmv11036tS__T0001TTNATS2006030105HP001.nc"
# ds.to_netcdf(f"D:/SNODAS/interpolated_w_time/timestamp_{ds_name}")
