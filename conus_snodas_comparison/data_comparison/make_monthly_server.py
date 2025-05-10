# calculates the monthly average
import xarray as xr
from pathlib import Path
import pandas as pd
import gc


# takes the average of all the files given in data_paths
def take_avg(data_paths, year, month, var):
    print(f"started smoothing data for {year}-{month}...")

    with xr.open_mfdataset(
        data_paths,
        combine="by_coords",
        chunks="auto",
    ) as ds:
        ds = ds.chunk({"Time": 168, "south_north": 100, "west_east": 100})
        try:
            avg = ds.mean(dim="Time")
            print("Calculated Average")

            avg = avg.assign_coords({"water_year": year, "month": month})
            # Expand dimensions to include the year and month
            avg = avg.expand_dims({"water_year": [year], "month": month})
            print("Added time dimension")

        except Exception as e:
            print(f"Error occured while calculating the monthly average:\n{e}")
            raise

        # make sure the name of the dataset is corrrect
        file_name = f"conus_{var}_{year}_{month}_monthly_avg.nc"
        save_dir = Path("/kaiganJ/hiroto/conus_monthly/")
        save_dir.mkdir(parents=True, exist_ok=True)
        encoding = {var: {"zlib": True, "complevel": 4, "chunksizes": (1, 500, 500)}}
        try:
            avg.to_netcdf(save_dir / file_name, encoding=encoding)
            print("Saved!")
        except Exception as e:
            print(f"An error has occured while saving:\n{e}")
            raise


print("Started make_monthly.py")
data_list = pd.read_csv(Path("/kaiganJ/hiroto/CONUS/urgent/conus_file_list.csv"))
# var_list = pd.read_csv(Path("/kaiganJ/hiroto/file_list/conus_list_comparison.csv"))

var = ["SNOWH", "SNOW"]
need = [2005, 1985]
var_list = data_list.loc[(data_list["water_year"].isin(need))]
var_list = var_list.loc[(data_list["variable"].isin(var))]
var_list["date"] = pd.to_datetime(var_list["date"])
var_list["month"] = var_list["date"].dt.month

# data_list["date"] = pd.to_datetime(data_list["date"])
# var_list = data_list.loc[(data_list["date"].dt.hour == 6)]

del data_list
gc.collect()

# var_list = var_list.loc[~var_list["corrupted"]]
for v in var:
    vfiles = var_list.loc[var_list["variable"] == v]
    for year in var_list["water_year"].unique():
        year_files = vfiles.loc[vfiles["water_year"] == year]
        for month in year_files["month"].unique():
            paths = year_files.loc[year_files["month"] == month, "file_path"].tolist()
            take_avg(paths, year, month, v)
            print(f"data smoothing completed for {v} {year}")
