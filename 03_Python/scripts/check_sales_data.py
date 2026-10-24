
import pandas as pd
from pathlib import Path

project_dir = Path.home() / "Desktop" / "Customer_Sales_Intelligence_Project"
sales_file = project_dir / "01_Data" / "cleaned" / "sales.csv"

df = pd.read_csv(sales_file, dtype={"Postal Code": "string"})

print("Dataset shape:", df.shape)
print("\nPostal Code data type:", df["Postal Code"].dtype)
print("\nSample postal codes:")
print(df["Postal Code"].dropna().head(15).to_list())

print("\nMissing postal codes:", df["Postal Code"].isna().sum())
print("Values ending in .0:", df["Postal Code"].str.endswith(".0", na=False).sum())
