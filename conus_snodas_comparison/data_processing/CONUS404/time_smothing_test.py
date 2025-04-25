import xarray as xr
import os
import datetime
from pathlib import Path


# mode = 1: for averaging smaller chunks and saving to intermediate files
# mode = 2: for combining the intermediate files to create the finall file
def smooth(files_2_smooth, var, base_dir, start_date, end_date, mode, i):
    output_dir = base_dir / f"{var}_smoothed"
    os.makedirs(output_dir, exist_ok=True)

    ct = datetime.datetime.now()

    print(f"{ct}: Smoothing {var}... \n")

    # smoothing the data over the time dimension by averaging
    data = xr.open_mfdataset(files_2_smooth)

    if mode == 1:
        time_smoothed = data.mean(dim="Time")

        # add dummy variable for taking the mean across the intermediate files
        time_smoothed = time_smoothed.expand_dims(dummy=[i])

        # saving the smooth data as netcdf in output directory
        output_path = output_dir / "intermediate" / f"{var}_time_avg_intermediate{i}.nc"
        os.makedirs(output_path.parent, exist_ok=True)
        time_smoothed.to_netcdf(output_path)

        data.close()
        time_smoothed.close()
        ct = datetime.datetime.now()
        print(f"{ct}: Completed smoothing intermediate{i} and saved to {output_path}")

    if mode == 2:
        time_smoothed = data.mean(dim="dummy")

        # saving the smooth data as netcdf in output directory
        output_path = output_dir / f"{var}_time_avg_{start_date}_{end_date}.nc"
        time_smoothed.to_netcdf(output_path)
        print(f"Smooth file saved to {output_dir}")
        data.close()
        time_smoothed.close()


def batch_baker(list, batch_size):
    for j in range(0, len(list), batch_size):
        yield list[j : j + batch_size]


# calling the command
# repeat call for any other varaibles
var = "ALBEDO"
# base_dir = Path("D:/CONUS404")
base_dir = Path("C:/Users/noodl/Desktop/usa_snow/CONUS404/time_smoothing_test")

files_2_smooth_full = [
    str(item).replace("\\", "/") for item in base_dir.glob("781316*.nc")
]

file_date_list = [
    str(ffile).split("/")[-1].split("_")[2].replace("-", "")  # Convert Path to string
    for ffile in files_2_smooth_full
]

# extracting the start and end date for files that have been smoothed
if (
    str(files_2_smooth_full[0]).split(".")[0].endswith("781316")
):  # checks if file is conus or snodas
    try:
        file_date_list = [
            str(ffile)
            .split("/")[-1]
            .split("_")[2]
            .replace("-", "")  # Convert Path to string
            for ffile in files_2_smooth_full
        ]
        file_date_list.sort()
        start_date = file_date_list[0]
        end_date = file_date_list[-1]
    except Exception:
        print("Error extracting dates from file names")
        start_date = "unkown"
        end_date = "unknown"

intermediate_dir = base_dir / f"{var}_smoothed" / "intermediate"

intermediate_files = intermediate_dir.glob(f"{var}_time_avg_intermediate*.nc")

# split file list into managable sizes
batch_size = 4000

i = 1
# smooth to create intermediate files
for batch in batch_baker(files_2_smooth_full, batch_size):
    smooth(batch, var, base_dir, start_date, end_date, 1, i)
    i += 1
ct = datetime.datetime.now()
print(f"{ct}: completed smoothing intermediate batches")

# initiate final smoothing of intermediate files
smooth(intermediate_files, var, base_dir, start_date, end_date, 2, i)


ct = datetime.datetime.now()
print(f"{ct}: Smoothing {var} from {start_date} to {end_date} completed!")
