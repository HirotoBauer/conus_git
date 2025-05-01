# calculates the yearly average
import xarray as xr
from pathlib import Path
import pandas as pd


def take_yearly_avg(data_paths, water_year, var):
    print(f"started smoothing data for {water_year}...")

    with xr.open_mfdataset(
        data_paths,
        combine="by_coords",
        chunks="auto",
    ) as ds:
        ds = ds.chunk({"Time": 168, "south_north": 100, "west_east": 100})
        try:
            yearly_avg = ds.mean(dim="Time")
            print("Calculated Average")

            yearly_avg = yearly_avg.assign_coords({"year": water_year})
            # Expand dimensions to include the year
            yearly_avg = yearly_avg.expand_dims({"year": [water_year]})
            print("Added time dimension")

        except Exception as e:
            print(f"Error occured while calculating the yearly average:\n{e}")
            raise

        # make sure the name of the dataset is corrrect
        file_name = f"conus_{var}_{water_year}_yearly_avg.nc"
        save_dir = Path("/kaiganJ/hiroto/conus_yearly/")
        save_dir.mkdir(parents=True, exist_ok=True)
        encoding = {var: {"zlib": True, "complevel": 4, "chunksizes": (1, 500, 500)}}
        try:
            yearly_avg.to_netcdf(save_dir / file_name, encoding=encoding)
            print("Saved!")
        except Exception as e:
            print(f"An error has occured while saving:\n{e}")
            raise


print("Started make_yearly.py")
data_list = pd.read_csv(Path("/kaiganJ/hiroto/file_list/conus_list_comparison.csv"))
# var_list = pd.read_csv(Path("/kaiganJ/hiroto/file_list/conus_list_comparison.csv"))

var = "SNOWH"

# var_list = data_list.loc[
#     (data_list["variable"] == var)
#     & (data_list["water_year"] >= 2004)
#     & (data_list["water_year"] <= 2022)
# ]

data_list["date"] = pd.to_datetime(data_list["date"])
var_list = data_list.loc[(data_list["date"].dt.hour == 6)]

# del data_list
# gc.collect()

# var_list = var_list.loc[~var_list["corrupted"]]

for year in var_list["water_year"].unique():
    print("test1")
    year_files = var_list.loc[var_list["water_year"] == year]
    print("test2")
    take_yearly_avg(year_files["file_path"].tolist(), year, var)

    print(f"data smoothing completed for {var} {year}")
