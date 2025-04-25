# IDW works well if data is evenly spaced (such as SNODAS)

from scipy.spatial import cKDTree
import xarray as xr
import numpy as np
from pathlib import Path


def idw(lat_snodas, lon_snodas, z_snodas, lat_conus, lon_conus, power=2):
    tree = cKDTree(np.vstack([lat_snodas, lon_snodas]).T)
    distances, indices = tree.query(
        np.vstack([lat_conus, lon_conus]).T,
        k=3,  # 3 nearest
    )

    weights = 1 / (distances**power)
    weights /= weights.sum(axis=1, keepdims=True)

    z_interp = np.sum(weights * z_snodas[indices], axis=1)
    return z_interp


# vars dict
d = {"swe": "1034", "snowh": "1036"}

var = "swe"  # change this line an make sure the desired variable is in a serperate file

grid_shape = (1015, 1367)  # dimmensions of the CONUS dataset

# load data
base_dir = Path(f"D:/SNODAS/data/{var}/")  # ensure this file exists

file_list = list(base_dir.glob(f"us_ssmv1{d[var]}*.nc"))


lon_conus_flat = np.loadtxt("lon_list.csv", dtype="float32", delimiter=",")
lat_conus_flat = np.loadtxt("lat_list.csv", dtype="float32", delimiter=",")

# lon_conus_2d, lat_conus_2d = np.meshgrid(lon_conus_1d, lat_conus_1d)

lat_conus_2d = lat_conus_flat.reshape(grid_shape)
lon_conus_2d = lon_conus_flat.reshape(grid_shape)

output_path = Path("C:/Users/noodl/Desktop/usa_snow/SNODAS/interp_data/")


for snodas_file in file_list:
    data = xr.open_dataset(snodas_file)

    lon_vals = np.array(data["lon"]).astype("float32")
    lat_vals = np.array(data["lat"]).astype("float32")
    z_array = np.array(data["Band1"]).astype("float32")

    # make everything 1D
    lon_mesh, lat_mesh = np.meshgrid(lon_vals, lat_vals)
    lon_snodas = lon_mesh.ravel()
    lat_snodas = lat_mesh.ravel()
    z_snodas = z_array.ravel()

    z_interp = idw(lat_snodas, lon_snodas, z_snodas, lat_conus_flat, lon_conus_flat)

    z_interp_2d = z_interp.reshape(grid_shape)

    # Create an xarray DataArray
    z_interp_da = xr.DataArray(
        z_interp_2d,
        dims=("y", "x"),
        coords={"lat": (("y", "x"), lat_conus_2d), "lon": (("y", "x"), lon_conus_2d)},
        name=f"interpolated_data_{var}",
    )

    # Create an xarray Dataset
    ds = xr.Dataset({f"interpolated_data_{var}": z_interp_da})

    # Save to NetCDF file
    output_file = output_path.with_name(f"interpolated_{snodas_file.name}")
    ds.to_netcdf(output_file)

    print(f"Saved interpolated data to {output_file}")
