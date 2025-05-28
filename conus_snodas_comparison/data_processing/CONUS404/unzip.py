import tarfile
from pathlib import Path
import csv


def extract_tar(file_path, extract_to):
    try:
        with tarfile.open(file_path, "r") as tar:
            for member in tar.getmembers():
                if member.isdir():
                    continue
                # Get the base file name without directories
                original_name = Path(member.name).name
                prefix = Path(file_path).stem
                original_name = f"{prefix}_{Path(member.name).name}"

                # add .nc extension if missing
                if not original_name.endswith(".nc"):
                    original_name += ".nc"

                # Define target path
                target_path = extract_to / original_name

                # Extract and write the file manually
                with tar.extractfile(member) as source, open(target_path, "wb") as dest:
                    dest.write(source.read())

        return True

    except tarfile.ReadError:
        print(f"corrupted tar file: {file_path}")
        corrupted_files.append(file_path)
        return False

    except Exception as e:
        print(f"Error extracting {file_path}: {e}")
        return False


base_dir = Path("/kaiganJ/hiroto/conus_daily/raw/")
path_list = list(base_dir.glob("*.tar"))

output_dir = Path("/kaiganJ/hiroto/conus_daily/extracted/")

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
