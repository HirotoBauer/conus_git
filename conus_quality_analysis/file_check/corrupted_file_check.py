import xarray as xr
from pathlib import Path
import pandas as pd

# checks for corrupted files in the file list
print("started file check")
file_list_dir = Path("/kaiganJ/hiroto/file_list//conus_filelist.csv")
filelist = pd.read_csv(file_list_dir)

output_dir = Path("/kaiganJ/hiroto/file_list/conus_file_list_corrupted_check.csv")

corrupted_list = []

for path in filelist["file_path"]:
    try:
        with xr.open_dataset(path):
            corrupted_list.append(False)

    except (OSError, RuntimeError) as e:
        print(f"Unable to open file: {path}, {e}")
        corrupted_list.append(True)  # true if file is corrupted

print(f"number of corrupted files: {len(corrupted_list)}")

if len(filelist) == len(corrupted_list):
    filelist["corrupted"] = corrupted_list

    print("Exporting new file list with column for corrupted file check....")
    filelist.to_csv(output_dir, index=False)
    print(f"Export to {str(output_dir)} completed!")

else:
    print(
        f"Corrupted list: {len(corrupted_list)} != length of origional filelist: {len(filelist)}"
    )
