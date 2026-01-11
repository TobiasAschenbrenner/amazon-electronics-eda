# Amazon Electronics Product Analysis

**SE_42 – Data Science Basics Hand-In**

## Overview

This project analyzes an Amazon electronics products dataset to explore relationships between pricing, customer feedback, discounts, and sales performance. The analysis applies fundamental data science techniques such as data cleaning, exploratory data analysis (EDA), visualization, and a basic statistical test.

The goal is to identify patterns in purchasing behavior and understand how product ratings and pricing relate to marketplace indicators such as the _Best Seller_ badge.

---

## Research Questions

- How are product ratings distributed across Amazon electronics products?
- Do products with higher ratings or more reviews sell more units per month?
- How does discounting affect sales within different price ranges?
- Is there a relationship between product rating groups and _Best Seller_ status?
- Which price ranges contribute most to estimated monthly revenue?

---

## Dataset

The dataset is sourced from **[Kaggle](https://www.kaggle.com/datasets/ikramshah512/amazon-products-sales-dataset-42k-items-2025?select=amazon_products_sales_data_cleaned.csv)** and contains information on over **42,000 Amazon electronics products**.  
It represents a snapshot collected in **August 2025**.

Key attributes include:

- Product title
- Product rating
- Number of reviews
- Units bought in the last month
- Current (final) product price
- Original listed price
- Discount information
- Best Seller badge indicator
- Data collection timestamp

---

## Files in the Repository

### Data

- `data/raw/amazon_products_sales_data_uncleaned.csv` – raw dataset
- `data/cleaned/amazon_cleaned.csv` – cleaned dataset used for analysis

### Source Code

- `01_load_and_inspect.py` – initial data loading and inspection
- `02_clean_prepare.py` – data cleaning and preprocessing
- `03_eda.py` – exploratory data analysis and visualization
- `04_statistics.py` – statistical analysis (chi-square test)

### Outputs

- `outputs/figures/` – generated plots in PNG format

---

## Key Findings

- **Ratings and Sales:**  
  Higher-rated products tend to sell more units on average, but the relationship is not strictly linear.
- **Reviews and Sales:**  
  Products with more reviews generally show higher average monthly sales, with diminishing returns at very high review counts.
- **Discount Effects:**  
  Discounted products sell more than non-discounted products primarily in the **100–300** and **300–1000** price ranges. In lower price ranges, non-discounted products often perform equally well or better.
- **Best Seller Association:**  
  Higher rating groups are more likely to receive the _Best Seller_ badge.
- **Revenue Contribution:**  
  Mid-priced products contribute the largest share of estimated monthly revenue.

---

## Statistical Analysis

A **chi-square test of independence** was conducted to examine the relationship between **product rating groups** and **Best Seller status**.

- Result: χ² = 35.24, p < 0.001
- Interpretation: Product rating group and Best Seller status are statistically associated; higher-rated products are more likely to be labeled as Best Sellers.

---

## Plots and Visualizations

The analysis includes:

- Histogram of product rating distribution
- Bar charts of average monthly units sold by:
  - Rating group
  - Review count range
  - Discount status within price ranges
- Pie chart showing estimated monthly revenue share by price range

All plots are saved in the `outputs/figures` directory.

---

## How to Run the Project

1. **Clone the repository**

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```
3. **Run the scripts in order**

   ```
   python src/01_load_and_inspect.py
   python src/02_clean_prepare.py
   python src/03_eda.py
   python src/04_statistics.py
   ```
