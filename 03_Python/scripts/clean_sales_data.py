
import pandas as pd
from pathlib import Path

project_dir = Path.home() / "Desktop" / "Customer_Sales_Intelligence_Project"

input_file = project_dir / "01_Data" / "cleaned" / "sales.csv"
output_file = project_dir / "01_Data" / "cleaned" / "sales_powerbi_ready.csv"

# Read postal codes as text so they are not treated as numbers.
df = pd.read_csv(input_file, dtype={"Postal Code": "string"})

# Remove a trailing ".0" from numeric-looking postal codes.
# Missing postal codes remain missing.
df["Postal Code"] = df["Postal Code"].str.replace(
    r"\.0$",
    "",
    regex=True
)

# Save a separate file; do not overwrite the existing cleaned CSV.
df.to_csv(output_file, index=False)

print("Cleaning complete.")
print("Output file:", output_file)
print("Dataset shape:", df.shape)
print("Missing postal codes:", df["Postal Code"].isna().sum())
print("Values ending in .0:", df["Postal Code"].str.endswith(".0", na=False).sum())
print("Sample postal codes:", df["Postal Code"].dropna().head(10).to_list())


# Validate key business totals after cleaning.
print("Total sales:", round(df["Sales"].sum(), 2))
print("Total profit:", round(df["Profit"].sum(), 2))
print("Duplicate rows:", df.duplicated().sum())

print("Total sales:", round(df["Sales"].sum(), 2))
print("Total profit:", round(df["Profit"].sum(), 2))
print("Duplicate rows:", df.duplicated().sum())
