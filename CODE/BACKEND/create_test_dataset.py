import pandas as pd
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

DATASET_PATH = (
    PROJECT_DIR
    / "DATA_SET"
    / "Crop recommendation dataset.csv"
)

OUTPUT_PATH = BASE_DIR / "test_dataset_all_crops.csv"


# ============================================================
# LOAD DATASET
# ============================================================

print("=" * 70)
print("CREATING TEST DATASET")
print("=" * 70)

print("Dataset:")
print(DATASET_PATH)

df = pd.read_csv(DATASET_PATH)


print("\nDataset shape:")
print(df.shape)


print("\nColumns:")

for column in df.columns:
    print(" -", column)


# ============================================================
# CROP COLUMN
# ============================================================

CROP_COLUMN = "CROPS"


if CROP_COLUMN not in df.columns:

    raise ValueError(
        f"Column '{CROP_COLUMN}' was not found."
    )


print("\nCrop column:", CROP_COLUMN)


# ============================================================
# CHECK UNIQUE CROPS
# ============================================================

unique_crops = df[CROP_COLUMN].dropna().unique()

print("\n" + "=" * 70)
print("CROP INFORMATION")
print("=" * 70)

print("Number of unique crops:", len(unique_crops))

print("\nCrops:")

for i, crop in enumerate(unique_crops, start=1):

    print(f"{i:02d}. {crop}")


# ============================================================
# CREATE ONE REAL SAMPLE FOR EACH CROP
# ============================================================

test_df = (
    df
    .groupby(CROP_COLUMN, group_keys=False)
    .head(1)
    .reset_index(drop=True)
)


# ============================================================
# SAVE TEST DATASET
# ============================================================

test_df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ============================================================
# FINAL INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("TEST DATASET CREATED SUCCESSFULLY")
print("=" * 70)

print("Total test samples:", len(test_df))

print("Total crops:", test_df[CROP_COLUMN].nunique())

print("\nSaved to:")

print(OUTPUT_PATH)

print("\nTest dataset preview:")

print(
    test_df[
        [
            "CROPS",
            "SOIL",
            "SEASON",
            "WATER_SOURCE",
            "SOIL_PH",
            "TEMP",
            "RELATIVE_HUMIDITY",
            "N",
            "P",
            "K"
        ]
    ].to_string(index=False)
)

print("=" * 70)