import os
from matplotlib.patches import Patch

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = "data/cleaned/amazon_cleaned.csv"
OUTPUT_DIR = "outputs/figures"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Constants
PRICE_BINS = [0, 50, 100, 300, 1000]  # last bin edge added dynamically via max()
PRICE_LABELS = ["≤50", "50–100", "100–300", "300–1000", "1000+"]

REVIEW_BINS_BASE = [0, 100, 500, 1000, 2000, 5000]  # last bin edge added dynamically via max()
REVIEW_LABELS = ["0–100", "100–500", "500–1000", "1000–2000", "2000–5000", "5000+"]

AVG_UNITS_LABEL = "Avg. Monthly Units Sold (per product)"

sns.set(style="whitegrid")

# Load data
df = pd.read_csv(DATA_PATH, parse_dates=["collected_at"])
print("Dataset used for EDA:", df.shape)

# Main analysis focuses on products where purchase data exists
df_sales = df.dropna(subset=["bought_in_last_month"]).copy()

# Plot: Rating distribution (Histogram)
plt.figure(figsize=(8, 5))
sns.histplot(df["rating"].dropna(), bins=20, kde=False)
plt.title("Product Rating Distribution")
plt.xlabel("Product Rating")
plt.ylabel("Number of Products")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/rating_distribution.png")
plt.show()

# Plot: Purchases by review count range (Bar)
reviews_df = df_sales.dropna(subset=["number_of_reviews"]).copy()
reviews_df["number_of_reviews"] = pd.to_numeric(reviews_df["number_of_reviews"], errors="coerce")
reviews_df = reviews_df.dropna(subset=["number_of_reviews"])

max_reviews = reviews_df["number_of_reviews"].max()
reviews_df["review_range"] = pd.cut(
    reviews_df["number_of_reviews"],
    bins=REVIEW_BINS_BASE + [max_reviews],
    labels=REVIEW_LABELS,
    include_lowest=True
)

avg_purchases_by_reviews = (
    reviews_df.groupby("review_range", observed=True)["bought_in_last_month"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(8, 5))
sns.barplot(data=avg_purchases_by_reviews, x="review_range", y="bought_in_last_month")
plt.title("Purchases by Review Count Range")
plt.xlabel("Number of Reviews")
plt.ylabel(AVG_UNITS_LABEL)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/purchases_by_review_range.png")
plt.show()

# Plot 3: Purchases by rating group (Bar)
rating_df = df_sales.dropna(subset=["rating"]).copy()

rating_df["rating_group"] = pd.cut(
    rating_df["rating"],
    bins=[0, 3, 4, 4.5, 5],
    labels=["≤3", "3–4", "4–4.5", "4.5–5"],
    include_lowest=True
)

avg_purchases_by_rating = (
    rating_df.groupby("rating_group", observed=True)["bought_in_last_month"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(8, 5))
sns.barplot(data=avg_purchases_by_rating, x="rating_group", y="bought_in_last_month")
plt.title("Purchases by Rating Group")
plt.xlabel("Rating Group")
plt.ylabel(AVG_UNITS_LABEL)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/purchases_by_rating_group.png")
plt.show()

# Plot 4: Discount impact by final price range (Grouped Bar)
discount_df = df_sales.dropna(subset=["current/discounted_price"]).copy()
discount_df["listed_price"] = pd.to_numeric(discount_df["listed_price"], errors="coerce")

discount_df["is_discounted"] = (
    discount_df["listed_price"].notna()
    & (discount_df["listed_price"] > discount_df["current/discounted_price"])
)

max_price = discount_df["current/discounted_price"].max()
discount_df["final_price_group"] = pd.cut(
    discount_df["current/discounted_price"],
    bins=PRICE_BINS + [max_price],
    labels=PRICE_LABELS,
    include_lowest=True
)

discount_df = discount_df.dropna(subset=["final_price_group"])

print("\nCounts per final price group and discount status:")
print(discount_df.groupby(["final_price_group", "is_discounted"], observed=True).size())

avg_purchases_discounted = (
    discount_df.groupby(["final_price_group", "is_discounted"], observed=True)["bought_in_last_month"]
    .mean()
    .reset_index()
)

palette = {False: "steelblue", True: "orange"}

plt.figure(figsize=(9, 5))
ax = sns.barplot(
    data=avg_purchases_discounted,
    x="final_price_group",
    y="bought_in_last_month",
    hue="is_discounted",
    hue_order=[False, True],
    palette=palette
)

plt.title("Discount Impact on Purchases by Final Price Range")
plt.xlabel("Final Price Range")
plt.ylabel(AVG_UNITS_LABEL)

legend_handles = [
    Patch(facecolor=palette[False], label="No"),
    Patch(facecolor=palette[True], label="Yes"),
]
ax.legend(handles=legend_handles, title="Discounted")

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/purchases_discounted_vs_not_by_price.png")
plt.show()

# Plot 5: Revenue share by final price range (Pie)
revenue_df = df_sales.dropna(subset=["current/discounted_price"]).copy()
revenue_df["estimated_monthly_revenue"] = (
    revenue_df["bought_in_last_month"] * revenue_df["current/discounted_price"]
)

max_price = revenue_df["current/discounted_price"].max()
revenue_df["final_price_group"] = pd.cut(
    revenue_df["current/discounted_price"],
    bins=PRICE_BINS + [max_price],
    labels=PRICE_LABELS,
    include_lowest=True
)

revenue_share = (
    revenue_df.groupby("final_price_group", observed=True)["estimated_monthly_revenue"]
    .sum()
)

plt.figure(figsize=(7, 7))
plt.pie(
    revenue_share,
    labels=revenue_share.index,
    autopct="%1.1f%%",
    startangle=140
)
plt.title("Revenue Share by Final Price Range")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/revenue_share_by_price_range.png")
plt.show()
