# creates header files for converting .dat files into .nc files

import os

header_content = """ENVI
samples = 6935
lines = 3351
bands = 1
header offset = 0
file type = ENVI Standard
data type = 2
interleave = bsq
byte order = 1"""

data_directory = "D:/SNODAS/extracted/extracted"

for filename in os.listdir(data_directory):
    if filename.endswith(".dat"):
        hdr_filename = filename.replace(".dat", ".hdr")
        hdr_filepath = os.path.join(data_directory, hdr_filename)

        with open(hdr_filepath, "w") as hdr_file:
            hdr_file.write(header_content)

        print(f"Created header file: {hdr_filepath}")
