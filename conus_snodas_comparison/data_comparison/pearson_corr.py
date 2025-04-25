import xarray as xr
from pathlib import Path
import pandas as pd


def pearson_corr(ds1, ds2):
    return xr.corr(ds1, ds2, dimeension="time")


file_list_dir = Path(
    "C:/Users/noodl/Desktop/usa_snow/file_path_lists/snodas_yearly_files"
)

output_dir = Path("D:/yearly_pearson")

filelist = pd.read_csv(file_list_dir)

var = "SNOWH"

var_data = filelist.loc[filelist["variable"] == var]

# FIXME load all datasets at once and compute over the time dimension
for water_year in var_data["water_year"].unique():
    wy_files = var_data.loc[var_data["water_year"] == water_year]

    snodas_file = wy_files.loc[wy_files["dataset"] == "snodas"]
    conus_file = wy_files.loc[wy_files["dataset"] == "conus"]

    snodas = xr.open_dataset(snodas_file["file_path"])
    conus = xr.open_dataset(conus_file["file_path"])

    pearson = pearson_corr(snodas, conus)

    pearson.to_netcdf(output_dir / f"pearson_corr_{var}_{water_year}.nc")
