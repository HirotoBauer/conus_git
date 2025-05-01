# calculates the yearly average
import xarray as xr
from pathlib import Path
import pandas as pd


def take_yearly_avg(data_paths, water_year, var):
    print(f"started smoothing data for {water_year}...", end="")

    with xr.open_mfdataset(
        data_paths,
        combine="by_coords",
        chunks="auto",
    ) as ds:
        ds = ds.chunk({"time": 168, "x": "auto", "y": "auto"})
        try:
            yearly_avg = ds.mean(dim="time")
            print("Calculated Average", end=" ")

            yearly_avg = yearly_avg.assign_coords({"year": water_year})
            # Expand dimensions to include the year
            yearly_avg = yearly_avg.expand_dims({"year": [water_year]})
            print("Added time dimension", end=" ")

        except Exception as e:
            print(f"Error occured while calculating the yearly average:\n{e}")
            raise

        # make sure the name of the dataset is corrrect
        file_name = f"snodas_{var}_{water_year}_yearly_avg.nc"
        save_dir = Path("C:/Users/noodl/Desktop/usa_snow/yearly_avgs")
        save_dir.mkdir(parents=True, exist_ok=True)
        encoding = {var: {"zlib": True, "complevel": 4, "chunksizes": (1, 500, 500)}}
        try:
            yearly_avg.to_netcdf(save_dir / file_name, encoding=encoding)
            print("Saved!")
        except Exception as e:
            print(f"An error has occured while saving:\n{e}")
            raise


print("Started make_yearly.py")
data_list = pd.read_csv(
    Path("C:/Users/noodl/Desktop/usa_snow/file_path_lists/snodas_file_list.csv")
)
# var_list = pd.read_csv(Path("C:/Users/noodl/Desktop/usa_snow/file_path_lists/snodas_yearly_file_list.csv"))

var = "SNOWH"

var_list = data_list.loc[
    (data_list["variable"] == var)
    & (data_list["water_year"] >= 2004)
    & (data_list["water_year"] <= 2022)
]

# var_list = var_list.loc[~var_list["corrupted"]]

for year in var_list["water_year"].unique():
    print("test1")
    year_files = var_list.loc[var_list["water_year"] == year]
    print("test2")
    take_yearly_avg(year_files["file_path"].tolist(), year, var)

    print(f"data smoothing completed for {var} {year}")
