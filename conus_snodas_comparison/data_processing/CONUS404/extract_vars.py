# extracts desired variables from the downloaded conus files
import xarray as xr
from pathlib import Path
from datetime import datetime
import csv

base_dir = "/kaiganJ/hiroto/CONUS/"
file_list = list(Path(base_dir).glob("*.nc"))

output_dir = f"{base_dir}/extracted"

corrupted_files = []

desired_vars = ["SNOWH", "SNOW", "QVAPOR", "ALBEDO", "TK"]
for path in file_list:
    # catch corrupted files and add to list so I canfix them later
    try:
        data = xr.open_dataset(path)

        date_str = str(data["XTIME"].values)
        cleaned_date = date_str.strip("[']")
        date = datetime.strptime(cleaned_date.split(".")[0], "%Y-%m-%dT%H:%M:%S")

        year = date.year
        month = f"{date.month:02d}"
        day = f"{date.day:02d}"
        hour = f"{date.hour:02d}"

        for var in desired_vars:
            var_data = data[var]
            var_data.to_netcdf(
                f"{output_dir}/781316.{var}.wrf2d_d01_{year}-{month}-{day}_{hour}:00:00.nc"
            )

    except Exception as e:
        print(f"Error opening {path.name}: {e}")
        corrupted_files.append(path)
        continue

with open("corrupted_files.csv", "w", newline="") as f:
    writer = csv.writer(f)
    for url in corrupted_files:
        writer.writerow([url])
