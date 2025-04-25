import os, subprocess, re

input_dir = "D:/SNODAS/extracted/extracted/"
output_dir = "D:/SNODAS/data/"

os.makedirs(output_dir, exist_ok=True)

gdal_command = "gdal_translate"

for filename in os.listdir(input_dir):
    if filename.endswith(".dat"):
        input_file = os.path.join(input_dir, filename)
        output_file = os.path.join(output_dir, filename.replace(".dat", ".nc"))
        # with open(output_file, "w") as fp:
        #     pass

        file_time = filename.split("TTNATS")[1]
        time = re.split("HP|DP", file_time)[0]
        print(f"Processing {filename} at {time}\n")

        if int(time) < 20131001:
            options = [
                "-of",
                "NetCDF",
                "-a_srs",
                "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs",
                "-a_nodata",
                "-9999",
                "-a_ullr",
                "-124.73375000000000",
                "52.87458333333333",
                "-66.94208333333333",
                "24.94958333333333",
            ]

        if int(time) >= 20131001:
            options = [
                "-of",
                "NetCDF",
                "-a_srs",
                "+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs",
                "-a_nodata",
                "-9999",
                "-a_ullr",
                "-124.73333333333333",
                "52.87500000000000",
                "-66.94166666666667",
                "24.95000000000000",
            ]

        command = [gdal_command] + options + [input_file, output_file]

        print(f"Processing: {input_file} -> {output_file}")
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode != 0:
            print(f"Error processing {input_file}:")
            print(result.stderr.decode())
        else:
            print(f"Successfully created {output_file}")

print("Batch conversion complete!")
