import xarray as xr
from pathlib import Path
import pandas as pd
import datetime


def drop_coords(ds):
    return ds.drop_vars(["XLAT", "XLONG"])


def take_average(data_paths, var):
    print(f"started smoothing {var} data")

    # open first file to extract the coords
    data_paths = list(data_paths)
    example_coords = xr.open_dataset(data_paths[0])
    lat = example_coords["XLAT"]
    lon = example_coords["XLONG"]
    example_coords.close()

    ds = xr.open_mfdataset(
        data_paths,
        combine="by_coords",
        preprocess=drop_coords,
        chunks={"time": 15, "XLAT": 1000, "XLONG": 1000},
    )

    ds = ds.assign_coords(lat=lat, lon=lon)
    ds = ds.fillna(0)

    time_avg = ds[var].mean("Time")

    time_avg.to_netcdf(f"{var}_time_avg.nc")  # save to same folder as the script

    ds.close()


file_list_dir = Path("/kaiganJ/hiroto/file_list/conus_file_list.csv")

filelist = pd.read_csv(file_list_dir)

time_first = datetime.datetime(2003, 9, 30, 0)  # from start of SNODAS data
time_last = datetime.datetime(2022, 9, 30, 0)  # From end of CONUS404 data

filelist["date"] = pd.to_datetime(filelist["date"])

var2smooth = "SNOWH"

data2smooth = filelist[
    (filelist["date"] >= time_first)
    & (filelist["date"] <= time_last)
    & (filelist["variable"] == var2smooth)
]

data2smooth = data2smooth.drop_duplicates(subset=["date"], keep="first")

if data2smooth.empty:
    raise ValueError("no data for given parameters")

take_average(data2smooth["file_path"], var2smooth)

print(f"data smoothing completed for {var2smooth}")
