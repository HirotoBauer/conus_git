# reduces the large conus list to only a certain time period and variable
from pathlib import Path
import pandas as pd
import gc

output_dir = Path("/kaiganJ/hiroto/file_list/")
data_list = pd.read_csv(
    Path("/kaiganJ/hiroto/file_list/conus_file_list_corrupted_check.csv")
)

var = "SNOWH"

var_list = data_list.loc[
    (data_list["variable"] == var)
    & (data_list["water_year"] >= 2004)
    & (data_list["water_year"] <= 2022)
]
var_list = var_list.loc[~var_list["corrupted"]]

del data_list
gc.collect()

output_path = output_dir / "conus_list_comparison.csv"
var_list.to_csv(output_path, index=False)
