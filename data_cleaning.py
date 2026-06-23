import pandas as pd
from pathlib import Path

# Project root folder
ROOT = Path(__file__).resolve().parent.parent

# File paths
input_file = ROOT / "data" / "Product-Sales-Region.xlsx"
output_file = ROOT / "data" / "clean_sales_data.csv"

print("Reading:", input_file)

# Load Excel
df = pd.read_excel(input_file)

# Remove duplicates
df.drop_duplicates(inplace=True)

# Fill missing values
if "Promotion" in df.columns:
    df["Promotion"] = df["Promotion"].fillna("No Promotion")

# Convert dates
df["OrderDate"] = pd.to_datetime(df["OrderDate"])
df["DeliveryDate"] = pd.to_datetime(df["DeliveryDate"])

# Create new metrics
df["NetSales"] = df["TotalPrice"] * (1 - df["Discount"])

df["DeliveryDays"] = (
    df["DeliveryDate"] - df["OrderDate"]
).dt.days

# Save cleaned data
df.to_csv(output_file, index=False)

print("\n✅ Cleaning completed successfully")
print("Saved:", output_file)
print("Rows:", len(df))