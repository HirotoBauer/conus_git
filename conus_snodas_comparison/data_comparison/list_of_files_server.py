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


# vars dict for snodas data
d = {"SNOW": "1034", "SNOWH": "1036"}
inv_d = {v: k for k, v in d.items()}

base_dir = Path(
    "/kaiganJ/hiroto/CONUS/extracted/"
)  # path to files to extract info from
path_list = base_dir.glob("*.nc")

export_list = pd.DataFrame(columns=["file_path", "variable", "date", "water_year"])
for path in path_list:
    path = path.as_posix()
    file_name = str(path).split(sep="/")[-1]

    # check for snodas data
    if file_name.split(sep="_")[3] == "us":
        flag = 0  # used for exporting list with name of dataset

        var_num = file_name.split(sep="_")[4][5:9]
        var = inv_d[var_num]

        date_section = file_name.split(sep="_")[-1]
        index = date_section.find("TTNATS")
        if index != -1:
            start = index + len("TTNATS")
            date_str = date_section[start : start + 10]
            try:
                date = datetime.strptime(date_str, "%Y%m%d%H")  # for YYYYMMDDHH

                water_year = date.year
                if date.month >= 10:
                    water_year += 1

                row = pd.DataFrame(
                    [[path, var, date, water_year]],
                    columns=["file_path", "variable", "date", "water_year"],
                )

                export_list = pd.concat([export_list, row], ignore_index=True)
                concat = pd.DataFrame()

            except ValueError as e:
                print("error parsing date:", e)

        else:
            print("TTNATS not found in SNODAS filename")

    # check for CONUS data file
    elif "781316" == file_name.split(sep=".")[0]:
        flag = 1

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
        print("File name does not appear to match SNODAS or CONUS naming convensions")

output_dir = Path("/kaiganJ/hiroto/file_list/")
output_dir.mkdir(parents=True, exist_ok=True)

if flag == 0:
    filename = "snodas_file_list.csv"
    export_list.to_csv(output_dir / filename, index=False)

if flag == 1:
    filename = "conus_file_list.csv"
    export_list.to_csv(output_dir / filename, index=False)
