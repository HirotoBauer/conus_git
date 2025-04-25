import tarfile
from pathlib import Path
import csv


def extract_tar(file_path, extract_to):
    try:
        with tarfile.open(file_path, "r") as tar:
            tar.extractall(extract_to)
        return True
    except tarfile.ReadError:
        print(f"corrupted tar file: {file_path}")
        corrupted_files.append(file_path)
        return False
    except Exception as e:
        print(f"Error extracting {file_path}: {e}")
        return False


base_dir = Path("/kaigan_testA8TB/hiroto/CONUS404/albedo_snowh_snow/")
path_list = base_dir.glob("*.tar")

output_dir = Path("/kaiganJ/hiroto/CONUS/extracted/")

corrupted_files = []

for path in path_list:
    success = extract_tar(path, output_dir)
    if success:
        print(f"extracted {path} to {output_dir}")

with open("corrupted_tar_files.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Corrupted Files"])  # Optional header
    for file in corrupted_files:
        writer.writerow([file])  # Each file gets its own row

print(f"Processed {len(path_list)} files, {len(corrupted_files)} were corrupted")
