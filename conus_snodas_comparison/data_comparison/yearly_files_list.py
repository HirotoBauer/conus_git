import pandas as pd
from pathlib import Path

base_dir = Path("C:/Users/noodl/Desktop/usa_snow/yearly_avgs/snodas")

path_list = base_dir.glob("*.nc")

export_list = pd.DataFrame(columns=["file_path", "variable", "water_year"])

for path in path_list:
    filename = path.name
    dataset = filename.split(sep="_")[0]
    var = filename.split(sep="_")[1]
    water_year = filename.split(sep="_")[2]

    row = pd.DataFrame(
        [[path, var, water_year]],
        columns=["file_path", "variable", "water_year"],
    )

    export_list = pd.concat([export_list, row], ignore_index=True)
    concat = pd.DataFrame()

output_dir = Path("C:/Users/noodl/Desktop/usa_snow/file_path_lists")

file_name = "snodas_yearly_file_list.csv"
export_list.to_csv(output_dir / file_name, index=False)
