# extracts desired variables from the downloaded conus files
import xarray as xr
from pathlib import Path

base_dir = "D:/CONUS404/constants"
file_list = list(Path(base_dir).glob("*.nc"))

output_dir = base_dir

corrupted_files = []

desired_vars = ["HGT", "ISLTYP", "IVGTYP", "LU_INDEX", "SHDMAX", "SHDMIN", "SNOALB"]
var_dict = {
    "HGT": "elevation",
    "ISLTYPE": "soil_type",
    "IVGTYPE": "vegetation_type",
    "LU_INDEX": "land_use",
    "SHDMAX": "annual_max_veg",
    "SHDMIN": "annual_min_veg",
    "SNOALB": "annual_max_snow_albedo_in_fraction",
}

for path in file_list:
    try:
        data = xr.open_dataset(path)

        for var in desired_vars:
            var_data = data[var]
            var_data.to_netcdf(
                f"{output_dir}/781316_{var_dict[var]}_wrf2d_d01_constant.nc"
            )

    except Exception as e:
        print(f"Error opening {path.name}: {e}")
        corrupted_files.append(path)
        continue

# with open("corrupted_files.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     for url in corrupted_files:
#         writer.writerow([url])
