# evaluates trend at location of ski resorts
import xarray as xr
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

# TODO make a check that ensures that ski resorts with no close points are not included


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

    valid = np.isfinite(vals.ravel())
    pts_valid = pts[valid]
    tree = cKDTree(pts_valid)

    # print(np.count_nonzero(np.isnan(pts_valid)))

    def interp(lat0, lon0, k):
        """
        Interpolate at a single point (lat0,lon0) using the k nearest neighbors.
        Returns a single scalar.
        """
        # Query the k nearest neighbors
        dists, idxs = tree.query([lat0, lon0], k=k)
        # ensures that the outputs are arrays of 1D even if k=1
        dists = np.atleast_1d(dists)
        idxs = np.atleast_1d(idxs)

        # ensures that there are points close by
        if np.max(dists) > 0.1:  # about 11 km
            return np.nan
        # print(dists, idxs)

        # Get the neighbor values
        vals_valid = vals.ravel()[valid]
        neigh_vals = vals_valid[idxs]

        # If any distance is zero, return that neighbor’s value directly
        if np.any(dists == 0):
            return neigh_vals[dists == 0][0]

        # Compute IDW weights
        weights = 1.0 / (dists**power)
        weights /= weights.sum()

        return np.sum(weights * neigh_vals)

    # print(interp)
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
densitylist_dir = Path(
    "C:/Users/noodl/Desktop/usa_snow/file_path_lists/monthly_file_list.csv"
)
density_filelist = pd.read_csv(densitylist_dir)
density_filelist["month"] = density_filelist["month"].astype(str).str.zfill(2)
density_filelist["water_year"] = density_filelist["water_year"].astype(str)
density_filelist["year-month"] = (
    density_filelist["water_year"] + "-" + density_filelist["month"]
)
density_filelist = density_filelist.loc[density_filelist["variable"] == "density"]

# apply inverse distance interpolation for the closes 3 datapoints to each resort
# this is to avoid outliers and account for ski resort area

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
    print(f"{colname}: {vals_at_resorts.head()}")

print(resorts.iloc[:, -5:])  # last 5 months
resorts.to_csv("resort_density_monthly.csv", index=False)
