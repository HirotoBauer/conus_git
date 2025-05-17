# uses the same idea that Furano uses
# to calculate new snow density
import xarray as xr
import pandas as pd
from pathlib import Path
import numpy as np


def snow_ratio(T):
    # Convert to Celsius
    Tc = T - 273.15

    # Initialize with zeros
    sr = xr.full_like(T, 0.0)

    mask = (T >= 230.0) & (T <= 280.0)

    # Parameters
    a = 16.1
    b = 0.2182
    c = 0.5373

    # Apply the snow ratio formula only where valid
    sr = sr.where(~mask, a / (1 + np.exp((Tc - b) / c)))

    return sr


filelist_path = Path("/kaiganJ/hiroto/CONUS/urgent/monthly_file_list.csv")

filelist = pd.read_csv(filelist_path)
temp_paths = filelist.loc[filelist["variable"] == "TK", "file_path"]

outdir = Path("/kaiganJ/hiroto/conus_monthly/")
for path in temp_paths:
    Tdata = xr.open_dataset(path)

    wy = int(Tdata["water_year"].item())
    month = int(Tdata["month"].item())

    sr = snow_ratio(Tdata["TK"])
    sr.name = "snow_ratio"
    sr = sr.to_dataset(name="snow_ratio")
    sr["XLAT"] = Tdata["XLAT"]
    sr["XLONG"] = Tdata["XLONG"]

    # save
    fname = outdir / f"conus_sr_{wy:04d}_{month:02d}.nc"
    sr.to_netcdf(fname)
    print(f"Saved {fname}")
