# calculates the yearly average
import xarray as xr
from pathlib import Path
import pandas as pd


def take_yearly_avg(data_paths, water_year, var):
    print(f"started smoothing data for {water_year}")

    with xr.open_mfdataset(
        data_paths,
        combine="by_coords",
        chunks="auto",
    ) as ds:
        yearly_avg = ds.mean(dim="Time")

        # make sure the name of the dataset is corrrect
        file_name = f"snodas_{var}_{water_year}_yearly_avg.nc"
        save_dir = Path("/kaiganJ/hiroto/conus_yearly/")
        yearly_avg.to_netcdf(save_dir / file_name)


data_list = pd.read_csv(
    Path("/kaiganJ/hiroto/file_list/conus_file_list_corrupted_check.csv/")
)

var = "SNOWH"

var_list = data_list.loc[data_list["variable"] == var]
var_list = var_list.loc[~var_list["corrupted"]]

for year in var_list["water_year"].unique():
    year_files = var_list.loc[var_list["water_year"] == year]
    take_yearly_avg(year_files["file_path"], year, var)

    print(f"data smoothing completed for {var} {year}")
