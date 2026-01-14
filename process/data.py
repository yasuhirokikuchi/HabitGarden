import json
import gspread
import streamlit as st
import os

def get_connection():
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # 1. まずローカルにある鍵ファイルを探す
    json_key_file = "service_account.json"
    
    if os.path.exists(json_key_file):
        # ローカル環境（ファイルがある場合）
        gc = gspread.service_account(filename=json_key_file, scopes=scopes)
    else:
        # 2. Cloud環境（ファイルがない場合）は st.secrets を使う
        # secretsに設定された情報を辞書として取得
        try:
            creds_dict = dict(st.secrets["gcp_service_account"])
            
            # Cloud上でも改行コードの問題が起きないよう念のため補正
            if "private_key" in creds_dict:
                creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
            
            gc = gspread.service_account_from_dict(creds_dict, scopes=scopes)
        except Exception as e:
            st.error("認証情報が見つかりません。Secretsの設定を確認してください。")
            st.stop()
            
 
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