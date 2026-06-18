import os
import sqlite3
import pandas as pd
import kagglehub
from pathlib import Path

def extract_clinic_sales(dataset_name: str = "phazanic/clinic-sales") -> pd.DataFrame:
    """Downloads data using KaggleHub and cleans standard schema characters."""
    path = kagglehub.dataset_download(dataset_name)
    files = os.listdir(path)
    csv_files = [f for f in files if f.endswith('.csv')]

    if not csv_files:
        raise FileNotFoundError("No valid CSV files located in downloaded dataset cache folder.")

    csv_path = Path(path) / csv_files[0]
    df = pd.read_csv(csv_path)
    df.columns = [c.lower().strip() for c in df.columns]

    if "visitdate" in df.columns:
        df["visitdate"] = pd.to_datetime(df["visitdate"], errors="coerce")
    return df

def transform_clinic_sales(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Applies normalization rules to generate Customers, Products, and Transaction tables."""
    df_clean = df.copy()
    df_clean.columns = [c.lower().strip() for c in df_clean.columns]

    if "visitdate" in df_clean.columns:
        df_clean["visitdate"] = pd.to_datetime(df_clean["visitdate"], errors="coerce")
    if "amountspent" in df_clean.columns:
        df_clean["amountspent"] = pd.to_numeric(df_clean["amountspent"], errors="coerce")

    required_cols = ["transactionid", "customerid", "servicecategory", "visitdate", "amountspent"]
    df_clean = df_clean.dropna(subset=[col for col in required_cols if col in df_clean.columns]).reset_index(drop=True)

    df_clean["service_id"] = df_clean["servicecategory"].astype("category").cat.codes + 1

    customers_df = (
        df_clean.groupby("customerid")
        .agg(
            first_visit=("visitdate", "min"),
            last_visit=("visitdate", "max"),
            total_visits=("transactionid", "count"),
            total_spent=("amountspent", "sum")
        ).reset_index()
    )

    products_df = (
        df_clean.groupby(["service_id", "servicecategory"])
        .agg(
            average_price=("amountspent", "mean"),
            total_transactions=("transactionid", "count")
        ).reset_index()
    )

    transactions_df = df_clean[["transactionid", "customerid", "service_id", "visitdate", "amountspent"]].copy()
    transactions_df.columns = ["transaction_id", "customer_id", "service_id", "visit_date", "amount_spent"]

    return customers_df, products_df, transactions_df

def load_clinic_to_sqlite(c_df: pd.DataFrame, p_df: pd.DataFrame, t_df: pd.DataFrame, db_path: Path) -> bool:
    """Feeds normalized clinical entities safely into relational storage blocks."""
    db_path.parent.mkdir(exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        c_df.to_sql("customers", conn, if_exists="replace", index=False)
        p_df.to_sql("products", conn, if_exists="replace", index=False)
        t_df.to_sql("transactions", conn, if_exists="replace", index=False)
        conn.commit()
    return True