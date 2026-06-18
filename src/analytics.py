import sqlite3
import pandas as pd
from pathlib import Path

def run_all_business_queries(db_path: Path) -> dict[str, pd.DataFrame]:
    """Executes high-level financial reporting queries directly on storage instances."""
    results = {}
    with sqlite3.connect(db_path) as conn:
        results["revenue_by_category"] = pd.read_sql_query(
            "SELECT p.servicecategory AS category, SUM(t.amount_spent) AS total_revenue "
            "FROM transactions t JOIN products p ON t.service_id = p.service_id "
            "GROUP BY p.servicecategory ORDER BY total_revenue DESC;", conn
        )
        results["customer_lifetime_value"] = pd.read_sql_query(
            "SELECT customer_id, SUM(amount_spent) AS clv FROM transactions GROUP BY customer_id ORDER BY clv DESC;", conn
        )
        results["monthly_revenue"] = pd.read_sql_query(
            "SELECT strftime('%Y-%m', visit_date) AS month, SUM(amount_spent) AS monthly_revenue "
            "FROM transactions GROUP BY month ORDER BY month;", conn
        )
        results["top_customers"] = pd.read_sql_query(
            "SELECT customer_id, SUM(amount_spent) AS total_spent FROM transactions GROUP BY customer_id ORDER BY total_spent DESC LIMIT 10;", conn
        )
        results["repeat_purchase_rate"] = pd.read_sql_query(
            "WITH vc AS (SELECT customer_id, COUNT(*) AS v FROM transactions GROUP BY customer_id) "
            "SELECT (SELECT COUNT(*) FROM vc WHERE v > 1) * 1.0 / (SELECT COUNT(*) FROM vc) AS repeat_rate;", conn
        )
    return results