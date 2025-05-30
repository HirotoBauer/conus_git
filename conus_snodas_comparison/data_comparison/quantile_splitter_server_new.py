import xarray as xr
from pathlib import Path
import pandas as pd
import datetime

# to see if the dataset can acurately capture extreme events
# take the 99th percentile for wettest years and 5th percentile for driest years
# the server version takes only the data from 06:00 UTC


def drop_coords(ds):
    return ds.drop_vars(["XLAT", "XLONG"])


# takes the yearly quantile then combined them later so that I dont run out of memory
def annual_quantiles(data_paths, var, quantile):
    years = data_paths["water_year"].unique()
    temp_files = []

    example_coords = xr.open_dataset(data_paths["file_path"].iloc[0])
    lat = example_coords["XLAT"]
    lon = example_coords["XLONG"]
    example_coords.close()

    for yr in years:
        # select file paths for that year
        yearly = data_paths.loc[data_paths["water_year"] == yr, "file_path"]
        file_list = yearly.tolist()

        ds = xr.open_mfdataset(
            file_list,
            combine="by_coords",
            preprocess=drop_coords,
            chunks={"Time": 500, "lat": 200, "lon": 200},
        )

        ds6 = ds.sel(Time=ds.Time.dt.hour == 6).fillna(0).astype("float32")

        ds6 = ds6.assign_coords(lat=lat, lon=lon)

        ds6 = ds6.chunk({"Time": -1})
        qyr = ds6[var].quantile(quantile, dim="Time")

        fn = f"quant_{var}_{yr}.nc"

        qyr.load()
        qyr.to_netcdf(fn)  # small 2D file
        temp_files.append(fn)

        ds.close()
        del ds, ds6, qyr

    # Now load the ~20 files and stack on “year”
    yrs = xr.open_mfdataset(temp_files, combine="nested", concat_dim="year")

    yrs = yrs.chunk({"year": -1})
    final = yrs[var].quantile(quantile, dim="year")

    final.to_netcdf(f"{var}_{int(quantile * 100)}th_full.nc")


# calculates the quantile using all the files given to the function wihtout intermediates
# cannot do the entire conus dataset as it will run out of memory
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

    quantile_data = ds_chunked[var].quantile(quantile, dim="Time")

    quantile_data.attrs["description"] = f"{quantile * 100}th percentile across time"

    encoding = {var: {"dtype": "float32", "zlib": True, "complevel": 1}}
    quantile_data.to_netcdf(
        f"{dataset}_{var}_{quantile * 100}th_percentile_6UTC.nc", encoding=encoding
    )


file_list_dir = Path("/kaiganJ/hiroto/file_list//conus_file_list.csv")

filelist = pd.read_csv(file_list_dir)

time_first = datetime.datetime(2003, 10, 1, 0)  # from start of SNODAS data
time_last = datetime.datetime(2022, 9, 30, 0)  # From end of CONUS404 data

filelist["date"] = pd.to_datetime(filelist["date"])

var2smooth = "SNOWH"

data2smooth = filelist[
    (filelist["date"] >= time_first)
    & (filelist["date"] <= time_last)
    & (filelist["variable"] == var2smooth)
]


if data2smooth.empty:
    raise ValueError("no data for given paramters in data2smooth")

# This function computes the annual quantiles then combines them to compute the final quantile
# annual_quantiles(data2smooth, var2smooth, 0.99)

# This function uses only the data at 06:00 UTC to compute the quantile
# same as the quantile computed for SNODAS
smooth_6UTC = filelist[
    (filelist["date"] >= time_first)
    & (filelist["date"] <= time_last)
    & (filelist["variable"] == var2smooth)
    & (filelist["date"].hour == 6)
]

if smooth_6UTC.empty:
    raise ValueError("no data fro given parameters in smooth_6UTC")
find_cutoff(smooth_6UTC, var2smooth, 0.99)

print(f"data smoothing completed for {var2smooth}")
