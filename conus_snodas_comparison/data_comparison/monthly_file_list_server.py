import pandas as pd
from pathlib import Path

base_dir = Path("D:/CONUS404/conus_monthly")

path_list = base_dir.glob("*.nc")

export_list = pd.DataFrame(columns=["file_path", "variable", "water_year", "month"])

for path in path_list:
    filename = path.name
    filename = filename.split(sep=".")[0]
    var = filename.split(sep="_")[1]
    water_year = filename.split(sep="_")[2]
    month = filename.split(sep="_")[3]

    row = pd.DataFrame(
        [[path, var, water_year, month]],
        columns=["file_path", "variable", "water_year", "month"],
    )

    export_list = pd.concat([export_list, row], ignore_index=True)
    concat = pd.DataFrame()

output_dir = Path("C:/Users/noodl/Desktop/usa_snow/file_path_lists")

file_name = "monthly_file_list.csv"
output_path = output_dir / file_name
export_list.to_csv(output_dir / file_name, index=False)
