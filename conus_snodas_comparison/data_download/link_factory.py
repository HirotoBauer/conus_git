from datetime import datetime, timedelta
import csv

base_url = "https://data.rda.ucar.edu/d559000/wy"


def url_factory(base_url, startdate, enddate):
    urls = []
    current = datetime.strptime(startdate, "%Y-%m-%d-%H:%M:%S")
    end = datetime.strptime(enddate, "%Y-%m-%d-%H:%M:%S")

    while current <= end:
        year = current.year
        month = f"{current.month:02d}"
        day = f"{current.day:02d}"
        hour = f"{current.hour:02d}"

        yyyymm = f"{year}{month}"
        wrf2d = f"wrf2d_d01_{year}-{month}-{day}_{hour}:00:00.nc"

        # adjust for water year
        if int(month) >= 10:
            url = f"{base_url}{year + 1}/{yyyymm}/{wrf2d}"
        else:
            url = f"{base_url}{year}/{yyyymm}/{wrf2d}"
        urls.append(url)

        current += timedelta(hours=1)

    return urls


startdate = "2019-06-09-01:00:00"
enddate = "2022-09-30-23:00:00"

urls = url_factory(base_url, startdate, enddate)

# save urls to csv
with open("urls.csv", "w", newline="") as f:
    writer = csv.writer(f)
    for url in urls:
        writer.writerow([url])

# with open("urls.csv", "r") as f:
#     reader = csv.reader(f)
#     test = list(reader)
