import xarray as xr
from pathlib import Path
import pandas as pd
import datetime
import netCDF4 as nc
import gc
import zarr
from numcodecs import Zlib

# to see if the dataset can acurately capture extreme events
# take the 99th percentile for wettest years and 5th percentile for driest years
# the server version takes only the data from 06:00 UTC


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
        chunks={"Time": 24 * 30, "lat": 500, "lon": 500},
    )

    # ds_chunked = ds.chunk({"Time": -1})
    # ds_chunked = ds

    ds_6 = ds.sel(Time=ds["Time"].dt.hour == 6)

    ds_6 = ds_6.assign_coords(lat=lat, lon=lon)
    ds_6 = ds_6.fillna(0).astype("float32")

    ds_6 = ds_6.chunk({"Time": -1})

    quant = ds_6[var].quantile(quantile, dim="Time")
    ds.close()
    del ds, ds_6
    gc.collect()

    print("calculated quantile")

    # with nc.Dataset(
    #     f"{dataset}_{var}_{int(quantile * 100)}th_percentile.nc", "w"
    # ) as ds_out:
    #     ds_out.createDimension("south_north", quant.south_north.size)
    #     ds_out.createDimension("west_east", quant.west_east.size)

    #     # coords
    #     ds_out.createVariable("XLAT", "f4", ("south_north", "west_east"))[:] = (
    #         lat.values
    #     )
    #     ds_out.createVariable("XLONG", "f4", ("south_north", "west_east"))[:] = (
    #         lon.values
    #     )

    #     q_var = ds_out.createVariable(
    #         "SNOWH", "f4", ("south_north", "west_east"), zlib=True, complevel=1
    #     )

    #     block_ns = 500
    #     block_we = 500

    #     for i0 in range(0, quant.south_north.size, block_ns):
    #         i1 = min(i0 + block_ns, quant.south_north.size)
    #         for j0 in range(0, quant.west_east.size, block_we):
    #             j1 = min(j0 + block_we, quant.west_east.size)

    #             mini = quant.isel(
    #                 south_north=slice(i0, i1), west_east=slice(j0, j1)
    #             ).compute()

    #             q_var[i0:i1, j0:j1] = mini.values
    #             del mini

    # ds_out.close()

    compressor = Zlib(level=1)

    # define chunk sizes
    spatial_chunks = (100, 100)  # (south_north, west_east)

    # chunk the DataArray along its *dims*:
    da_q = quant.chunk(
        {"south_north": spatial_chunks[0], "west_east": spatial_chunks[1]}
    )

    # build a tiny Dataset around it
    ds_out = xr.Dataset({var: da_q})

    # write to Zarr with matching encoding:
    ds_out.to_zarr(
        "conus_SNOWH_99th.zarr",
        mode="w",
        encoding={
            var: {
                "compressor": compressor,
                "chunks": spatial_chunks,
                "dtype": "float32",
            }
        },
    )
    print("finished saving!")

    # print("computed the quantile")
    # quant.attrs["description"] = f"{quantile * 100}th percentile across time"
    # print("here comes the tricky part...\n")
    # quant.to_netcdf(
    #     f"{dataset}_{var}_{quantile * 100}th_percentile.nc",
    #     encoding={quant.name: {"dtype": "float32", "zlib": True}},
    # )
    # print("made it through!!!!")


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
