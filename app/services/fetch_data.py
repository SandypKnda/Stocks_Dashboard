import yfinance as yf
import pandas as pd
import requests
from typing import List, Dict
from functools import lru_cache
# 1. Get S&P 500 stock symbols from Wikipedia
@lru_cache(maxsize=1)
def get_sp500_stocks() -> pd.DataFrame:
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    tables = pd.read_html(url)
    df = tables[0]
    return df[['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry']].rename(
        columns={"Symbol": "symbol", "Security": "name", "GICS Sector": "sector", "GICS Sub-Industry": "industry"}
    )

# 2. Filter all stocks by a given sector
@lru_cache(maxsize=1)
def get_stocks_by_sector(sector: str, limit=50) -> List[Dict]:
    sp500_df = get_sp500_stocks()
    filtered = sp500_df[sp500_df['sector'] == sector]
    if limit:
        filtered = filtered.head(limit)

    data = []
    for _, row in filtered.iterrows():
        ticker = row['symbol']
        try:
            info = yf.Ticker(ticker).info
            data.append({
                "symbol": ticker,
                "name": row['name'],
                "sector": row['sector'],
                "industry": row['industry'],
                "price": info.get("regularMarketPrice", 0)
            })
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            continue

    return data

# 3. Get all index stocks (S&P 500 as example)
def get_all_index_stocks(limit=100) -> List[Dict]:
    sp500_df = get_sp500_stocks().head(limit)
    data = []
    for _, row in sp500_df.iterrows():
        ticker = row['symbol']
        try:
            info = yf.Ticker(ticker).info
            data.append({
                "symbol": ticker,
                "name": row['name'],
                "sector": row['sector'],
                "industry": row['industry'],
                "price": info.get("regularMarketPrice", 0)
            })
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")
            continue
    return data

# 4. Main method: top N stocks per sector
def get_top_stocks_by_all_sectors(limit_per_sector=5) -> List[Dict]:
    sp500_df = get_sp500_stocks()
    sectors = sp500_df['sector'].unique()

    all_data = []
    for sector in sectors:
        print(f"Fetching sector: {sector}")
        all_data += get_stocks_by_sector(sector, limit=limit_per_sector)

    return all_data
