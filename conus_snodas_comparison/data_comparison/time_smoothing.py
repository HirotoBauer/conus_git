import xarray as xr
from pathlib import Path
import pandas as pd
import datetime


def drop_coords(ds):
    return ds.drop_vars(["lat", "lon"])


def take_average(data_paths, var):
    print(f"started smoothing {var} data")

    # open first file to extract the coords
    data_paths = list(data_paths)
    example_coords = xr.open_dataset(data_paths[0])
    lat = example_coords["lat"]
    lon = example_coords["lon"]
    example_coords.close()

    ds = xr.open_mfdataset(
        data_paths,
        combine="by_coords",
        preprocess=drop_coords,
        chunks={"time": 10, "lat": 1000, "lon": 1000},
    )

    ds = ds.assign_coords(lat=lat, lon=lon)
    ds = ds.fillna(0)

    time_avg = ds[var].mean("time")

    time_avg.to_netcdf(f"{var}_time_avg.nc")

    ds.close()


file_list_dir = Path(
    "C:/Users/noodl/Desktop/usa_snow/file_path_lists/snodas_file_list.csv"
)

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

if data2smooth.empty:
    raise ValueError("no data for given paramters")

take_average(data2smooth["file_path"], var2smooth)

print(f"data smoothing completed for {var2smooth}")
