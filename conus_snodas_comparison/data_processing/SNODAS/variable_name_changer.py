import xarray as xr
import pandas as pd
from tqdm import tqdm

dataset_list = pd.read_csv(
    "C:/Users/noodl/Desktop/usa_snow/file_path_lists/snodas_SNOW.csv"
)

for index, row in tqdm(dataset_list.iterrows()):
    if row["variable"] == "SNOWH":
        ds = xr.open_dataset(row["file_path"])
        ds = ds.rename_vars({"interpolated_data_snowh": "SNOWH"})

        ds_name = row["file_path"].split(sep="/")[-1]
        ds.to_netcdf(f"D:/SNODAS/interpolated_w_time_w_vars_renamed/renamed_{ds_name}")
    else:
        continue


# ds = xr.open_dataset("D:/SNODAS/interpolated_w_time/timestamp_interpolated_us_ssmv11036tS__T0001TTNATS2006030105HP001.nc")
# ds = ds.rename_vars({"interpolated_data_swe": "SNOWH"})

# ds_name = "timestamp_interpolated_us_ssmv11036tS__T0001TTNATS2006030105HP001.nc"
# ds.to_netcdf(f"D:/SNODAS/interpolated_w_time_w_vars_renamed/renamed_{ds_name}")
