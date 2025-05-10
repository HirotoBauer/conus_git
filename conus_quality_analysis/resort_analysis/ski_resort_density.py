# evaluates trend at location of ski resorts
import xarray as xr
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree


def build_idw_interpolator(da, power, var="rho"):
    """
    Given a 2D DataArray da(lat,lon), return a function f(lat0,lon0,k)
    that does k-nearest IDW (power) interpolation.
    """
    # Extract the coordinate arrays from CONUS
    lats = da["XLAT"].values
    lons = da["XLONG"].values
    vals = da[var].values  # shape (1015, 1367)

    # creates an array with format (lat,lon)
    pts = np.column_stack([lats.ravel(), lons.ravel()])

    # Build KDTree
    tree = cKDTree(pts)

    def interp(lat0, lon0, k):
        """
        Interpolate at a single point (lat0,lon0) using the k nearest neighbors.
        Returns a single scalar.
        """
        # Query the k nearest neighbors
        dists, idxs = tree.query([lon0, lat0], k=k)
        # ensures that the outputs are arrays of 1D even if k=1
        dists = np.atleast_1d(dists)
        idxs = np.atleast_1d(idxs)

        # Get the neighbor values
        neigh_vals = vals.ravel()[idxs]

        # If any distance is zero, return that neighbor’s value directly
        if np.any(dists == 0):
            return neigh_vals[dists == 0][0]

        # Compute IDW weights
        weights = 1.0 / (dists**power)
        weights /= weights.sum()

        return np.sum(weights * neigh_vals)

    return interp


# seperate ski resorts into four quadrants:
# northern rockies, southern rockies, midwest, east coast
resort_list_path = Path(
    "C:/Users/noodl/Desktop/conus_git/conus_snodas_comparison/web_scrape/resort_data_coords_altitude_terrain_contUS.csv"
)
resorts = pd.read_csv(resort_list_path, usecols=["resort", "lat", "lon", "altitude"])

# add region column
resorts["north_south"] = np.where(resorts["lat"] > 42, "north", "south")

lon_bins = [-180, -117, -104, -81, 0]
bin_names = ["west", "rockies", "midwest", "east"]
resorts["east_west"] = pd.cut(resorts["lon"], bins=lon_bins, labels=bin_names)

# extract values for snow density at ski resort locations
# by averaging 3 closest values for each time monthly average
density_filelist = pd.read_csv("density_monthly_file_list.csv")  # TODO check this
density_filelist["month"] = density_filelist["month"].astype(str).str.zfill(2)
density_filelist["year"] = density_filelist["year"].astype(str)
density_filelist["year-month"] = (
    density_filelist["year"] + "-" + density_filelist["month"]
)

# apply inverse distance interpolation for the closes 3 datapoints to each resort
# this is to avoid outliers and account for ski resort area

# TODO check this
k = 3  # take 3 nearest
power = 2
for idx, frow in density_filelist.iterrows():
    ds = xr.open_dataset(frow["file_path"])

    idw_fun = build_idw_interpolator(ds, power)  # builds the tree

    # Apply to each resort
    vals_at_resorts = resorts.apply(lambda row: idw_fun(row.lat, row.lon, k), axis=1)

    # create new column for every year-month calculated
    colname = frow["year-month"]
    resorts[colname] = vals_at_resorts.values

resorts.to_csv("resort_density_monthly.csv", index=False)
