# calculate snow desnity from swe and snow depth
import xarray as xr
from pathlib import Path
import pandas as pd


def rho(swe_ds, snowh_ds):
    # takes xarray datasets as inputs
    snowh = snowh_ds["SNOWH"]
    swe = swe_ds["SNOW"]

    snowh_safe = snowh.where(snowh > 0)  # mask zero or negative depths
    return swe / snowh_safe


filelist_path = Path("/kaiganJ/hiroto/CONUS/urgent//monthly_file_list.csv")
df = pd.read_csv(filelist_path)

varlist = ["SNOW", "SNOWH"]


# extract paths for snowh and swe for each month in the year
# pairing files for calculation
def make_pairs(df):
    print(df.head)
    df2 = df.reset_index().rename(columns={"index": "orig_idx"})
    pairs = (
        df2.merge(df2, on=["water_year", "month"], suffixes=("_swe", "_snowh"))
        .query("variable_swe=='SNOW' and variable_snowh=='SNOWH'")
        .loc[:, ["orig_idx_swe", "orig_idx_snowh", "water_year", "month"]]
    )
    return pairs


pairs = make_pairs(df)

# calculate snow density per month only including points where there is more than 100 mm of snow
# try without the filter first:
# TODO fix the variable naming and ensure that rho has correct dimmensions
# variable should be names rho with dimmensions of XLAT, XLONG, and south_north, east_west
outdir = Path("/kaiganJ/hiroto/conus_monthly/")
for _, row in pairs.iterrows():
    swe_path = df.at[row.orig_idx_swe, "file_path"]
    snowh_path = df.at[row.orig_idx_snowh, "file_path"]
    year, month = int(row.water_year), int(row.month)

    # open datasets
    ds_swe = xr.open_dataset(swe_path)
    ds_snowh = xr.open_dataset(snowh_path)

    # compute density
    density = rho(ds_swe, ds_snowh)

    # remove shallow snow
    density = density.where(ds_swe["SNOW"] > 100)

    # name the variable
    density.name = "rho"
    density = density.to_dataset(name="rho")
    density["XLAT"] = ds_swe["XLAT"]
    density["XLONG"] = ds_swe["XLONG"]

    # save
    fname = outdir / f"conus_density_{year:04d}_{month:02d}.nc"
    density.to_netcdf(fname)
    print(f"Saved {fname}")
