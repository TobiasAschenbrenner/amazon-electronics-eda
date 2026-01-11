import re
import numpy as np
import pandas as pd

RAW_PATH = "data/raw/amazon_products_sales_data_uncleaned.csv"
OUT_PATH = "data/cleaned/amazon_cleaned.csv"

df = pd.read_csv(RAW_PATH)

# Drop columns that won't be analyzed
drop_cols = ["image_url", "product_url"]
df = df.drop(columns=drop_cols, errors="ignore")

# sustainability_badges is mostly missing, so drop it
if "sustainability_badges" in df.columns:
    missing_ratio = df["sustainability_badges"].isna().mean()
    if missing_ratio > 0.8:
        df = df.drop(columns=["sustainability_badges"], errors="ignore")


# Helper functions to parse messy strings
def parse_rating(x):
    # "4.6 out of 5 stars" -> 4.6
    if pd.isna(x):
        return np.nan
    m = re.search(r"(\d+(\.\d+)?)", str(x))
    return float(m.group(1)) if m else np.nan


def parse_int(x):
    # "1,234" -> 1234
    if pd.isna(x):
        return np.nan
    s = str(x).strip().replace(",", "")
    m = re.search(r"\d+", s)
    return int(m.group(0)) if m else np.nan


def parse_price(x):
    # Removes currency symbols and commas
    if pd.isna(x):
        return np.nan
    s = str(x).replace(",", "")
    m = re.search(r"(\d+(\.\d+)?)", s)
    return float(m.group(1)) if m else np.nan


def parse_bool(x):
    # Handle "True/False", "Yes/No", "1/0"
    if pd.isna(x):
        return False
    s = str(x).strip().lower()
    return s in {"true", "yes", "1", "y", "t"}


# Convert columns
df["rating"] = df["rating"].apply(parse_rating)
df["number_of_reviews"] = df["number_of_reviews"].apply(parse_int)
df["bought_in_last_month"] = df["bought_in_last_month"].apply(parse_int)

df["current/discounted_price"] = df["current/discounted_price"].apply(parse_price)
df["listed_price"] = df["listed_price"].apply(parse_price)
df["price_on_variant"] = df["price_on_variant"].apply(parse_price)

# Only mark True when the badge is explicitly "Best Seller".
if "is_best_seller" in df.columns:
    df["is_best_seller"] = df["is_best_seller"].astype(str).str.strip().eq("Best Seller")
else:
    df["is_best_seller"] = False

# These columns are true/false-like in the raw dataset
df["is_sponsored"] = df["is_sponsored"].apply(parse_bool)
df["is_couponed"] = df["is_couponed"].apply(parse_bool)

# Treat any non-null value as True.
if "buy_box_availability" in df.columns:
    df["buy_box_availability"] = df["buy_box_availability"].notna()
else:
    df["buy_box_availability"] = False

df["collected_at"] = pd.to_datetime(df["collected_at"], errors="coerce")

# Remove rows missing title
df = df.dropna(subset=["title"])

# Save cleaned dataset
df.to_csv(OUT_PATH, index=False)

print("Saved cleaned dataset to:", OUT_PATH)
print("Cleaned shape:", df.shape)
print("\nDtypes:\n", df.dtypes)

print("\nSanity check: is_best_seller value counts:")
print(df["is_best_seller"].value_counts(dropna=False))

print("\nMissing values (top 10):")
print(df.isna().sum().sort_values(ascending=False).head(10))
