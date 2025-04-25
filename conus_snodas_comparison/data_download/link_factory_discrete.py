from datetime import datetime
import csv

base_url = "https://data.rda.ucar.edu/d559000/wy"


def url_factory(base_url, date):
    year = date.year
    month = f"{date.month:02d}"
    day = f"{date.day:02d}"
    hour = f"{date.hour:02d}"

    yyyymm = f"{year}{month}"
    wrf2d = f"wrf2d_d01_{year}-{month}-{day}_{hour}:00:00.nc"

    # adjust for water year
    if int(month) >= 10:
        url = f"{base_url}{year + 1}/{yyyymm}/{wrf2d}"
    else:
        url = f"{base_url}{year}/{yyyymm}/{wrf2d}"

    return url


# read missing dates from csv
with open(
    "C:/Users/noodl/Desktop/usa_snow/python_scripts/random_tests/missing_dates.csv"
) as f:
    reader = csv.reader(f)
    missing_dates = [row[0] for row in reader]

missing_times = missing_dates[1:]

# for missing_time in missing_times:
#     datetime.strptime(missing_time, "%Y-%m-%d-%H:%M:%S")

urls = []
for missing_time in missing_times:
    url = url_factory(base_url, datetime.strptime(missing_time, "%Y-%m-%d-%H:%M:%S"))
    urls.append(url)

urls.sort()
# save urls to csv
with open("urls.csv", "w", newline="") as f:
    writer = csv.writer(f)
    for url in urls:
        writer.writerow([url])
