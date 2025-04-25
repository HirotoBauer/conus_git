import pandas as pd
from pathlib import Path

data2delete = pd.read_csv("data2delete.csv")

for file_path in data2delete["file_path"]:
    file_path = Path(file_path)

    try:
        file_path.unlink()
        print(f"deleted {file_path}")
    except Exception as e:
        print(f"error delteting {file_path}: {e}")

print("finished deleting files")
