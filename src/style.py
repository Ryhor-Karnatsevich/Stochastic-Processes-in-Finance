import  pandas as pd

def print_styled_table(df, title, length=140):
    print("\n" + "=" * length)
    print(title.center(length))
    print("=" * length)

    df_print = df.copy()

    df_print = df_print.rename(columns={
        "mean": "Mean Annual Return",
        "volatility": "Volatility",
        "autocorr": "Autocorr (lag1)",
        "adf_pvalue": "ADF p-value",
        "adf_price": "ADF price",
        "skewness": "Skewness",
        "kurtosis": "Kurtosis",
        "max_drawdown": "Max Drawdown"
    })

    percent_cols = ["Mean Annual Return", "Max Drawdown"]
    small_float_cols = ["Volatility","ADF price"]
    normal_float_cols = ["Autocorr (lag1)", "ADF p-value", "Skewness", "Kurtosis"]

    for col in percent_cols:
        if col in df_print.columns:
            df_print[col] = df_print[col].apply(
                lambda x: f"{x * 100:.2f}%" if pd.notnull(x) else "-"
            )

    for col in small_float_cols:
        if col in df_print.columns:
            df_print[col] = df_print[col].apply(
                lambda x: f"{x:.6f}" if pd.notnull(x) else "-"
            )

    for col in normal_float_cols:
        if col in df_print.columns:
            df_print[col] = df_print[col].apply(
                lambda x: f"{x:.3f}" if pd.notnull(x) else "-"
            )

    ordered_cols = [
        "Mean Annual Return",
        "Volatility",
        "Autocorr (lag1)",
        "ADF p-value",
        "ADF price",
        "Skewness",
        "Kurtosis",
        "Max Drawdown"
    ]

    df_print = df_print[[col for col in ordered_cols if col in df_print.columns]]

    df_print = df_print.sort_values(by="Kurtosis", ascending=False)

    output = df_print.to_string(justify='center', col_space=14)
    print(output)
    print("=" * length)