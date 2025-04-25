# dataset is too large

from pykrige.uk import UniversalKriging
import numpy as np
import xarray as xr
from pathlib import Path
import matplotlib.pyplot as plt

# vars dict
d = {"swe": "1034", "snowh": "1036"}

var = "swe"
# load data
data_path = Path("D:/SNODAS/data")
data = xr.open_dataset(data_path / "us_ssmv01025SlL00T0024TTNATS2003093005DP001.nc")

print("1")
var = "snowh"

lon = np.array(data["lon"]).astype("float32")
lat = np.array(data["lat"]).astype("float32")
z = np.array(data["Band1"]).astype("float32")

lon_mesh, lat_mesh = np.meshgrid(lon, lat)
x_flat = lon_mesh.ravel()
y_flat = lat_mesh.ravel()
z_flat = z.ravel()

uk = UniversalKriging(
    x_flat, y_flat, z_flat, variogram_model="linear", drift_terms=["regional_linear"]
)

variogram_params = uk.variogram_model_parameters
print("Fitted Variogram Parameters:", variogram_params)
uk.display_variogram_model()
plt.show
