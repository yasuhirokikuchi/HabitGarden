import json
import gspread
import streamlit as st
import os

# スプレッドシートへの接続設定（JSONファイル直接読み込み版）
def get_connection():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # 【ここを修正】
    # ダウンロードしたJSONファイルの名前を正確に入力してください
    json_key_file = "habitgarden-484200-d4ffd5c84b37.json" 
    
    # ファイルが存在するかチェック（エラー防止）
    if not os.path.exists(json_key_file):
        st.error(f"鍵ファイル '{json_key_file}' が見つかりません。フォルダに置かれているか、名前が合っているか確認してください。")
        st.stop()

    gc = gspread.service_account(filename=json_key_file, scopes=scopes)
    
    sheet_url = "https://docs.google.com/spreadsheets/d/1_jNdU5rWPi7x7BnuMUszsC3RXAcPlVjKlJPoUMSywkI/edit"
    
    return gc.open_by_url(sheet_url).sheet1

# ユーザー認証（ログイン）
def authenticate_user(username, password):
    sheet = get_connection()
    try:
        cell = sheet.find(username)
        if cell:
            # ユーザーが見つかった場合、パスワードを確認（B列）
            stored_password = sheet.cell(cell.row, 2).value
            if stored_password == password:
                return True
    except gspread.exceptions.CellNotFound:
        return False
    return False

# ユーザー登録
def register_user(username, password):
    sheet = get_connection()
    try:
        if sheet.find(username):
            return False, "そのユーザー名は既に使用されています。"
    except gspread.exceptions.CellNotFound:
        pass 
    
    # 初期データ
    initial_data = {"habits": [], "history": {}, "daily": None, "xp": 0}
    json_str = json.dumps(initial_data, ensure_ascii=False)
    
    # 行を追加 [username, password, data]
    sheet.append_row([username, password, json_str])
    return True, "登録しました。"

# データ読み込み
def load_data(username):
    sheet = get_connection()
    try:
        cell = sheet.find(username)
        # C列（3列目）にデータが入っている想定
        data_str = sheet.cell(cell.row, 3).value
        if data_str:
            return json.loads(data_str)
        else:
            # データが空の場合の初期値
            return {"habits": [], "history": {}, "daily": None, "xp": 0}
    except Exception as e:
        st.error(f"データ読み込みエラー: {e}")
        return {"habits": [], "history": {}, "daily": None, "xp": 0}

# データ保存
def save_data(data, username):
    sheet = get_connection()
    try:
        cell = sheet.find(username)
        json_str = json.dumps(data, ensure_ascii=False)
        # 3列目を更新
        sheet.update_cell(cell.row, 3, json_str)
    except Exception as e:
        st.error(f"データ保存エラー: {e}")