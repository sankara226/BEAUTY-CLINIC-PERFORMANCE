import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def prepare_forecast_df(df: pd.DataFrame) -> pd.DataFrame:
    """Standardizes target queries to fit scikit-learn training inputs."""
    df_out = df.copy()
    df_out["month"] = pd.to_datetime(df_out["month"])
    df_out = df_out.sort_values("month")
    df_out = df_out.rename(columns={"month": "ds", "monthly_revenue": "y"})
    return df_out

def forecast_next_12_months(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Fits cyclic trend predictors to project next year's operational revenues."""
    df_proc = prepare_forecast_df(df)
    df_proc["t"] = np.arange(len(df_proc))
    df_proc["month_num"] = df_proc["ds"].dt.month

    X = df_proc[["t", "month_num"]]
    y = df_proc["y"]

    model = LinearRegression()
    model.fit(X, y)

    future_dates = pd.date_range(df_proc["ds"].max() + pd.offsets.MonthBegin(1), periods=12, freq="MS")
    future_df = pd.DataFrame({
        "ds": future_dates,
        "t": np.arange(len(df_proc), len(df_proc) + 12),
        "month_num": future_dates.month
    })
    future_df["y_pred"] = model.predict(future_df[["t", "month_num"]])
    return df_proc, future_df