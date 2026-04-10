import yfinance as yf
import pandas as pd



# Get data from internet ?
Updated_data = True
if Updated_data:
    data = yf.download("AAPL", start="2025-01-01")
else:
    data = pd.read_csv("../Data/Assets/AAPL.csv")


print(data)
