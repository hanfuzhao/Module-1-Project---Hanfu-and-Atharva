import os
import glob
import zipfile
import pandas as pd 
from pathlib import Path

RAW_ZIP = Path("data/raw/names.zip")
RAW_DIR = Path("data/raw/ssa_names")
OUT_CSV = Path("data/processed/ssa_baby_names_1880_2024.csv.gz")

def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    # extracting the zip file
    with zipfile.ZipFile(RAW_ZIP, "r") as zf:
        zf.extractall(RAW_DIR)

    # combining all years into a single dataframe
    frames = []
    for p in sorted(RAW_DIR.glob("yob*.txt")):
        year = int(p.name[3:7])
        df = pd.read_csv(p, names=["Name", "Sex", "Count"])
        df["Year"] = year
        frames.append(df)

    combined = pd.concat(frames, ignore_index=True)

    # compressing the csv here
    combined.to_csv(OUT_CSV, index=False, compression="gzip")

if __name__ == "__main__":
    main()