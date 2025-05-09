import xarray as xr
import pandas as pd
from pathlib import Path
import gc

# 1. Read in your CSV of file‐paths.
file_list_dir = Path("C:/Users/noodl/Desktop/usa_snow/file_path_lists/")
filelist = pd.read_csv(file_list_dir / "yearly_file_list.csv")

# Filter to get lists of paths for each dataset
var = "SNOWH"
df_var = filelist[filelist["variable"] == var]

snodas_paths = df_var.query("dataset == 'snodas'")["file_path"].tolist()
conus_paths = df_var.query("dataset == 'conus'")["file_path"].tolist()

# 2. Open all years at once, combining by coordinates
#    Select only the variable you care about to save memory.
da_snodas = xr.open_mfdataset(
    snodas_paths,
    combine="nested",
    concat_dim="year",
    parallel=True,
)[var]

da_snodas = da_snodas.rename({"y": "lat", "x": "lon"})

da_conus = xr.open_mfdataset(
    conus_paths, combine="nested", concat_dim="year", parallel=True
)[var]

da_conus = da_conus.rename({"south_north": "lat", "west_east": "lon"})

print(da_conus.dims, da_snodas.dims)

del filelist, snodas_paths, conus_paths
gc.collect()

# 4. Compute Pearson r along the time axis
da_r = xr.corr(da_snodas, da_conus, dim="year")

del da_snodas, da_conus
gc.collect()

da_r = da_r.rename("Pearson")

# 5. Save out the 2D correlation field
output_dir = Path("D:/yearly_pearson")
output_dir.mkdir(parents=True, exist_ok=True)
out_file = output_dir / f"pearson_r_{var}_snodas_vs_conus.nc"
da_r.to_netcdf(out_file)

print(f"Saved Pearson‐r map to {out_file}")
