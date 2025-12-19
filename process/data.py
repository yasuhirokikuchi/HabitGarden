import json
import os
from datetime import datetime, date


# データの読み書き

def load_data(DATA_FILE):
    if not os.path.exists(DATA_FILE): # dataにデータがない場合初期化
        return {"habits": [], "history": {},"daily":None, "xp": 0}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data,DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)