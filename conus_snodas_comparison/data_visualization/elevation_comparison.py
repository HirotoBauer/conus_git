# plots a constant to a spatial dataset for comparison
import xarray as xr
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt


var_dict = {
    "HGT": "elevation",
    "ISLTYPE": "soil_type",
    "IVGTYPE": "vegetation_type",
    "LU_INDEX": "land_use",
    "SHDMAX": "annual_max_veg",
    "SHDMIN": "annual_min_veg",
    "SNOALB": "annual_max_snow_albedo_in_fraction",
}

const = "HGT"
data = "Pearson"
constant_path = Path(
    f"D:/CONUS404/constants/781316_{var_dict[const]}_wrf2d_d01_constant.nc"
)
ds_const = xr.open_dataset(constant_path)
ds_const = ds_const.drop_vars(["XTIME", "Time"])

ds_path = Path("D:/yearly_pearson/pearson_r_SNOWH_snodas_vs_conus.nc")
ds = xr.open_dataset(ds_path)
ds = ds.drop_vars(["lat", "lon"])
ds_renamed = ds.rename_dims({"lat": "south_north", "lon": "west_east"})

# ds_lat = ds['lat'].values
# ds_lon = ds['lon'].values
ds_XLAT = ds["XLAT"].values
ds_XLONG = ds["XLONG"].values
const_XLAT = ds_const["XLAT"].values
const_XLONG = ds_const["XLONG"].values

# check if coords are the same
if np.array_equal(ds_XLAT, const_XLAT) and np.array_equal(ds_XLONG, const_XLONG):
    # add the constant data to the dataset as a new variable
    ds_combined = ds_renamed.assign(**{const: ds_const[const]})
    print("ds and const combined succesfully!")
    ds.close()
    ds_renamed.close()
    ds_const.close()
else:
    print("Coordinates do not match. Cannot combine")
    raise

# plotting with constant on x axis
constant = ds_combined[const].values.flatten()
data = ds_combined[data].values.flatten()
lat = ds_combined["XLAT"].values.flatten()
lon = ds_combined["XLONG"].values.flatten()

# Create the plot
plt.figure(figsize=(10, 6))
plt.scatter(constant, data, alpha=0.5, s=2, label="Data points")
plt.xlabel("Elevation (HGT) [m]", fontsize=12)
plt.ylabel("Pearson Correlation Coefficient", fontsize=12)
plt.title("Pearson Correlation vs. Elevation", fontsize=14)
plt.grid(True, linestyle="--", alpha=0.5)
plt.legend()
plt.show()

# seperate into bins and take average:
# elevation = ds_combined["HGT"].squeeze(dim="Time", drop=True)
# pearson = ds_combined["Pearson"]

bin_edges = np.arange(0, 4000 + 500, 500)
bin_indices = np.digitize(constant, bin_edges)

bin_means = []
bin_centers = []
for i in range(1, len(bin_edges)):
    mask = bin_indices == i
    if np.any(mask):
        bin_mean = np.nanmean(data[mask])
        bin_means.append(bin_mean)
        bin_centers.append((bin_edges[i - 1] + bin_edges[i]) / 2)
