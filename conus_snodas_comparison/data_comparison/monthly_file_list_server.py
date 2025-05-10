import pandas as pd
from pathlib import Path

base_dir = Path("/kaiganJ/hiroto/CONUS/urgent/extracted/")

path_list = base_dir.glob("*.nc")

export_list = pd.DataFrame(columns=["file_path", "variable", "water_year", "month"])

for path in path_list:
    filename = path.name
    var = filename.split(sep="_")[1]
    water_year = filename.split(sep="_")[2]
    month = filename.split(sep="_")[3]

    row = pd.DataFrame(
        [[path, var, water_year, month]],
        columns=["file_path", "variable", "water_year", "month"],
    )

    export_list = pd.concat([export_list, row], ignore_index=True)
    concat = pd.DataFrame()

output_dir = Path("/kaiganJ/hiroto/CONUS/urgent/")

file_name = "monthly_file_list.csv"
export_list.to_csv(output_dir / file_name, index=False)
