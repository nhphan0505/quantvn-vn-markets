import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from quantvn import client
from quantvn.vn.data import get_derivatives_hist
from quantvn.vn.metrics import Backtest_Derivates, Metrics

load_dotenv()
api_key = os.getenv('API_KEY')
client(apikey=api_key)

def gen_position(df: pd.DataFrame) -> pd.DataFrame:
    """
    Chiến lược kết hợp giữa EMA crossover và RSI để xác định xu hướng và động lượng:
    - Sử dụng EMA(9) và EMA(21) crossover để bắt xu hướng mượt mà hơn, tránh nhiễu.
    - Bộ lọc Động lượng RSI:
        - Chỉ Long khi RSI > 52 (xu hướng tăng mạnh) và RSI < 70 (chưa quá mua).
        - Chỉ Short khi RSI < 48 (xu hướng giảm mạnh) và RSI > 30 (chưa quá bán).
    - Giảm thiểu số lượng giao dịch ảo (Whipsaw) khi thị trường đi ngang.
    """
    df = df.copy()
    
    # 1. Tính toán các đường trung bình động Exponential (EMA)
    df["EMA_fast"] = df["Close"].ewm(span=9, adjust=False).mean()
    df["EMA_slow"] = df["Close"].ewm(span=26, adjust=False).mean()
    
    # 2. Tính toán RSI đơn giản
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / (loss + 1e-9)
    df["RSI"] = 100 - (100 / (1 + rs))
    
    # 3. Tạo tín hiệu Vị thế
    df["position"] = 0
    
    # Điều kiện Long (Mua): EMA_fast vượt EMA_slow VÀ RSI đang nằm trong vùng tăng trưởng lành mạnh (52 -> 70)
    long_cond = (df["EMA_fast"] > df["EMA_slow"]) & (df["RSI"] > 52) & (df["RSI"] < 70)
    # Điều kiện Short (Bán): EMA_fast dưới EMA_slow VÀ RSI đang nằm trong vùng sụt giảm lành mạnh (30 -> 48)
    short_cond = (df["EMA_fast"] < df["EMA_slow"]) & (df["RSI"] < 48) & (df["RSI"] > 30)
    
    df.loc[long_cond, "position"] = 1
    df.loc[short_cond, "position"] = -1
    
    # Giữ nguyên vị thế trước đó nếu không có tín hiệu mới (tránh đóng/mở vị thế liên tục khi nhiễu)
    # (Nếu không thỏa cả 2 điều kiện trên, ta có thể giữ nguyên vị thế thay vì đưa về 0)
    df["position"] = df["position"].replace(0, np.nan).ffill().fillna(0)
    
    return df

df = get_derivatives_hist("VN30F1M", "1m")
df_pos = gen_position(df)
backtest = Backtest_Derivates(df_pos, pnl_type="raw")
backtest.PNL().plot()

metrics = Metrics(backtest)

# Tính các metrics cơ bản
print("Average Return:", metrics.avg_return())
print("Average Win:", metrics.avg_win())
print("Average Loss:", metrics.avg_loss())
print("Win Rate:", metrics.win_rate())
print("Volatility:", metrics.volatility())

print("\n=== Risk/Reward Metrics ===")
print("Sharpe Ratio:", metrics.sharpe())
print("Sortino Ratio:", metrics.sortino())
print("Calmar Ratio:", metrics.calmar())
print("Max Drawdown:", metrics.max_drawdown())
print("Profit Factor:", metrics.profit_factor())
print("Risk of Ruin:", metrics.risk_of_ruin())
print("Value at Risk:", metrics.value_at_risk())