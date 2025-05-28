# extracts the date from the file name
# works for conus or snodas data but should be in seperate directories
# automatically finds dataset, var, and date of file
# this is ther server version of the script

from pathlib import Path
from datetime import datetime
import pandas as pd


def get_date(filename):
    # extract the date from the filename
    # only for conus data filenames

    parts = filename.split(".")[-2].split("_")

    try:
        date_str = "_".join(parts[-4:])
        # print("p1 ", date_str)
        return datetime.strptime(date_str, "%Y-%m-%d_%H_%M_%S")
    except (ValueError, IndexError):
        pass

    try:
        date_str = "_".join(parts[-2:])
        # print("p2 ", date_str)
        return datetime.strptime(date_str, "%Y-%m-%d_%H:%M:%S")
    except (ValueError, IndexError):
        pass

    raise ValueError(
        "Date done not match the expected patterns. File name: " + filename
    )


base_dirs = [
    Path("/kaiganJ/hiroto/CONUS/extracted/"),
    Path("/kaiganJ/hiroto/CONUS/extracted2/"),
    Path("/kaiganJ/hiroto/CONUS/extracted3/"),
]

# extracts all of the file lists from the base directories above
path_list_all = []
for base_dir in base_dirs:
    path_list_all.extend(base_dir.glob("*.nc"))

export_list = pd.DataFrame(columns=["file_path", "variable", "date", "water_year"])
for path in path_list_all:
    path = path.as_posix()
    file_name = str(path).split(sep="/")[-1]

    # check for CONUS data file
    if "781316" == file_name.split(sep=".")[0]:
        var = file_name.split(sep=".")[1]

        date = get_date(file_name)

        water_year = date.year
        if date.month >= 10:
            water_year += 1

        row = pd.DataFrame(
            [[path, var, date, water_year]],
            columns=["file_path", "variable", "date", "water_year"],
        )

        export_list = pd.concat([export_list, row], ignore_index=True)
        concat = pd.DataFrame()

    else:
        print("File name does not appear to match CONUS naming convensions")

output_dir = Path("/kaiganJ/hiroto/file_list/")
output_dir.mkdir(parents=True, exist_ok=True)


# save
filename = "conus_file_list.csv"
export_list.to_csv(output_dir / filename, index=False)
