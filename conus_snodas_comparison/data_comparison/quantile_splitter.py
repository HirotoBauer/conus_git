import xarray as xr
from pathlib import Path
import pandas as pd
import datetime

# to see if the dataset can acurately capture extreme events
# take the 99th percentile for wettest years and 5th percentile for driest years


def drop_coords(ds):
    return ds.drop_vars(["XLAT", "XLONG"])


def find_cutoff(data_paths, var, quantile):
    dataset = "conus"

    # open first file to extract the coords
    data_paths = list(data_paths)
    example_coords = xr.open_dataset(data_paths[0])
    lat = example_coords["XLAT"]
    lon = example_coords["XLONG"]
    example_coords.close()

    print(f"finding cutoff value for {quantile}th percentile of {var} data")

    ds = xr.open_mfdataset(
        data_paths,
        combine="by_coords",
        preprocess=drop_coords,
        chunks={"time": 5, "lat": 100, "lon": 100},
    )

    ds = ds.assign_coords(lat=lat, lon=lon)
    ds = ds.fillna(0).astype("float32")

    ds_chunked = ds.chunk({"Time": -1})
    # ds_chunked = ds

    quantile_data = ds_chunked[var].quantile(quantile, dim="Time")

    quantile_data.attrs["description"] = f"{quantile * 100}th percentile across time"

    encoding = {var: {"dtype": "float32", "zlib": True, "complevel": 1}}
    quantile_data.to_netcdf(
        f"{dataset}_{var}_{quantile * 100}th_percentile.nc", encoding=encoding
    )


file_list_dir = Path("/kaiganJ/hiroto/file_list//conus_file_list.csv")

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

find_cutoff(data2smooth["file_path"], var2smooth, 0.99)

print(f"data smoothing completed for {var2smooth}")
