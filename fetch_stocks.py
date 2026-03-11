import yfinance as yf
import json
import time
import os

def fetch_stock_data():
    try:
        # KOSPI Ticker in Yahoo Finance is ^KS11
        kospi = yf.Ticker("^KS11")
        kospi_hist = kospi.history(period="2d")
        
        # Powernet Ticker in Yahoo Finance is 037030.KQ
        powernet = yf.Ticker("037030.KQ")
        powernet_hist = powernet.history(period="2d")
        
        # Calculate current price and percentage change
        kospi_curr = kospi_hist['Close'].iloc[-1]
        kospi_prev = kospi_hist['Close'].iloc[-2]
        kospi_diff = ((kospi_curr - kospi_prev) / kospi_prev) * 100
        
        powernet_curr = powernet_hist['Close'].iloc[-1]
        powernet_prev = powernet_hist['Close'].iloc[-2]
        powernet_diff = ((powernet_curr - powernet_prev) / powernet_prev) * 100
        
        data = {
            "kospi": {
                "price": kospi_curr,
                "diff": kospi_diff
            },
            "powernet": {
                "price": powernet_curr,
                "diff": powernet_diff
            },
            "last_updated": time.strftime("%H:%M")
        }
        
        # Save to local JSON file for the HTML dashboard to read
        with open('c:\\Users\\김예슬\\Projects\\260304\\stock_data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
            
        print("Stock data updated successfully.")
        
    except Exception as e:
        print(f"Error fetching stock data: {e}")

if __name__ == "__main__":
    fetch_stock_data()
