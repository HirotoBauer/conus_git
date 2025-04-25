import gzip
import shutil
import os

# Define the input and output directories
input_folder = "D:/SNODAS/extracted"  # Folder containing .dat.gz files
output_folder = "D:/SNODAS/extracted/extracted"  # Folder to store extracted .dat files

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through all .dat.gz files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".dat.gz"):
        # Full path to the compressed file
        gz_file_path = os.path.join(input_folder, filename)

        # Full path to the output .dat file
        dat_file_path = os.path.join(
            output_folder, filename[:-3]
        )  # Remove .gz extension

        # Extract the .dat.gz file
        with gzip.open(gz_file_path, "rb") as gz_file:
            with open(dat_file_path, "wb") as dat_file:
                shutil.copyfileobj(gz_file, dat_file)

        print(f"Extracted: {filename} -> {dat_file_path}")

print("Extraction complete!")
