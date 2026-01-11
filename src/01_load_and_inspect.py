import pandas as pd

DATA_PATH = "data/raw/amazon_products_sales_data_uncleaned.csv"

df = pd.read_csv(DATA_PATH)

print("Shape (rows, cols):", df.shape)
print("\nColumns:\n", df.columns.tolist())

print("\nInfo:")
df.info()

print("\nHead:")
print(df.head())

print("\nMissing values (top 15):")
print(df.isnull().sum().sort_values(ascending=False).head(15))

print("\nDuplicate rows:", df.duplicated().sum())
