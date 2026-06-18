import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from pathlib import Path

def generate_all_visualizations(results: dict[str, pd.DataFrame], output_dir: Path):
    """Compiles clean corporate visual documentation to target directories."""
    output_dir.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid")

    # Revenue by Category
    plt.figure(figsize=(10, 5))
    sns.barplot(
        data=results["revenue_by_category"],
        x="category",
        y="total_revenue",
        hue="category",
        legend=False,
        palette="viridis",
    )
    plt.title("Revenue Mix Across Clinical Treatment Modalities")
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig(output_dir / "revenue_by_category.png")
    plt.close()

    # CLV Profile
    plt.figure(figsize=(8, 4))
    sns.histplot(results["customer_lifetime_value"]["clv"], bins=20, kde=True, color="skyblue")
    plt.title("Patient Customer Lifetime Value (LTV) Distribution Profiles")
    plt.tight_layout()
    plt.savefig(output_dir / "clv_distribution.png")
    plt.close()

    # Monthly Trend
    plt.figure(figsize=(10, 5))
    sns.lineplot(data=results["monthly_revenue"], x="month", y="monthly_revenue", marker="o", color="green")
    plt.title("Historical Month-Over-Month Performance Tracking")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / "monthly_revenue.png")
    plt.close()

def plot_revenue_forecast(df: pd.DataFrame, future_df: pd.DataFrame, output_dir: Path):
    """Maps dynamic predictive patterns out over future operational quarters."""
    plt.figure(figsize=(12, 6))
    plt.plot(df["ds"], df["y"], marker="o", label="Actual Historical Ledger")
    plt.plot(future_df["ds"], future_df["y_pred"], marker="o", linestyle="--", color="orange", label="ML Projected Run-Rate")
    plt.title("12-Month Advanced Clinical Revenue Forecasting Outlook")
    plt.xlabel("Timeline Horizons")
    plt.ylabel("Revenue Volumes ($)")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_dir / "revenue_forecast.png")
    plt.close()