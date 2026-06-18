from pathlib import Path
from src.pipeline_etl import extract_clinic_sales, transform_clinic_sales, load_clinic_to_sqlite
from src.analytics import run_all_business_queries
from src.forecasting import forecast_next_12_months
from src.plots import generate_all_visualizations, plot_revenue_forecast

def main():
    BASE_DIR = Path(__file__).resolve().parent
    DB_PATH = BASE_DIR / "data" / "clinic.db"
    OUT_DIR = BASE_DIR / "outputs"

    print("[ETL Engine] Initiating clinical logs download pipeline...")
    raw_df = extract_clinic_sales()

    print("[ETL Engine] Standardizing categorical treatments and computing attributes...")
    c_df, p_df, t_df = transform_clinic_sales(raw_df)

    print(f"[ETL Engine] Normalizing schemas and exporting tables directly into DB -> {DB_PATH}")
    load_clinic_to_sqlite(c_df, p_df, t_df, DB_PATH)

    print("[Business Intelligence] Pulling financial analytical reports via SQL queries...")
    query_results = run_all_business_queries(DB_PATH)

    print("[Machine Learning] Training time-series forecasting algorithms...")
    historical_df, forecast_df = forecast_next_12_months(query_results["monthly_revenue"])

    print(f"[Graphics Layer] Compiling dashboard profiles to output folders -> {OUT_DIR}")
    generate_all_visualizations(query_results, OUT_DIR)
    plot_revenue_forecast(historical_df, forecast_df, OUT_DIR)

    print(f"\n Clinical Pipeline Execution Complete. Analytics assets stored at: {OUT_DIR}")

if __name__ == "__main__":
    main()