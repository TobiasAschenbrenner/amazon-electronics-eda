import pandas as pd
from scipy.stats import chi2_contingency

DATA_PATH = "data/cleaned/amazon_cleaned.csv"


def main() -> None:
    # Load cleaned data
    df = pd.read_csv(DATA_PATH, parse_dates=["collected_at"])

    # Focus on products with sales information
    df_sales = df.dropna(subset=["bought_in_last_month"]).copy()

    # Rating + best seller status for this test
    test_df = df_sales.dropna(subset=["rating", "is_best_seller"]).copy()

    # Create the same rating groups used in EDA
    test_df["rating_group"] = pd.cut(
        test_df["rating"],
        bins=[0, 3, 4, 4.5, 5],
        labels=["≤3", "3–4", "4–4.5", "4.5–5"],
        include_lowest=True,
    )

    # Build contingency table: rows = rating groups, columns = best seller (False/True)
    contingency = pd.crosstab(test_df["rating_group"], test_df["is_best_seller"])

    print("Chi-square Test: Rating Group vs Best Seller Status")
    print("\nContingency table (counts):")
    print(contingency)

    # Run chi-square test of independence
    chi2, p_value, dof, expected = chi2_contingency(contingency)

    print("\nResults:")
    print(f"Chi-square statistic: {chi2:.2f}")
    print(f"Degrees of freedom: {dof}")
    print(f"P-value: {p_value:.5f}")


if __name__ == "__main__":
    main()
