import pandas as pd
from pathlib import Path
import datetime
import csv

list_dir = Path("C:/Users/noodl/Desktop/Delete/conus_file_list.csv")

filelist = pd.read_csv(list_dir)

time_first = datetime.datetime(2002, 12, 1, 0)
time_last = datetime.datetime(2021, 3, 31, 23)

filelist["date"] = pd.to_datetime(filelist["date"])

first_date = filelist.loc[filelist["variable"] == "SNOWH"]["date"].min()
last_date = filelist.loc[filelist["variable"] == "SNOWH"]["date"].max()
# check for duplicates
duplicate_mask = filelist.duplicated(subset=["date", "variable"], keep="last")

data2delete = filelist[duplicate_mask].copy()

data2delete.to_csv("data2delete.csv", index=False)


# check for missing dates
expected_times = pd.date_range(start=time_first, end=time_last, freq="H")
# variables = filelist["variable"].unique()
variables = ["SNOWH"]
missing_dates = []

for var in variables:
    var_times = filelist[filelist["variable"] == var]["date"]
    missing = expected_times.difference(var_times)
    if not missing.empty:
        missing_dates.append((var, missing))
    else:
        print(f"No missing dates for {var}")

missing_dates_list = []
for var, missing_times in missing_dates:
    missing_dates_list.extend(missing_times)

missing_dates_list.sort()

missing_dates_list = list(set(missing_dates_list))

formatted_dates = [
    dt.strftime("%Y-%m-%d %H:%M:%S").replace(" ", "-") for dt in missing_dates_list
]

with open("missing_dates.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["missing_timestamps"])
    writer.writerows([[dt] for dt in formatted_dates])

print(len(missing_dates_list))

snow_only = filelist.loc[filelist["variable"] == "SNOW"]
snow_only = snow_only.sort_values("date")
