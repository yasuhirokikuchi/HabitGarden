import streamlit as st
import time

# 変更したdata.pyからインポート
from process.data import load_data, save_data, authenticate_user, register_user
from process.level import get_level_info
from process.timedata import get_today_str

from draw.explanation import render_explanation
from draw.dashbord import render_dashboard
from draw.garden import render_garden_page
from draw.history import render_history_page

XP_PER_TASK = 10
LEVEL_DATA = {
    0:   {"label": "芽",   "image": "images/pot/pot_2.png"},
    100: {"label": "栄養成長", "image": "images/pot/pot_3.png"},
    300: {"label": "生殖成長",   "image": "images/pot/pot_4.png"},
    600: {"label": "成熟", "image": "images/pot/pot_5.png"},
}

def login_page():
    st.title("🌿 Habit Garden - ログイン")
    
    tab1, tab2 = st.tabs(["ログイン", "新規登録"])
    
    with tab1:
        username = st.text_input("ユーザー名", key="login_user")
        password = st.text_input("パスワード", type="password", key="login_pass")
        if st.button("ログイン"):
            if authenticate_user(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.success("ログイン成功！")
                time.sleep(1)
                st.rerun()
            else:
                st.error("ユーザー名またはパスワードが間違っています")

    with tab2:
        new_user = st.text_input("ユーザー名", key="reg_user")
        new_pass = st.text_input("パスワード", type="password", key="reg_pass")
        if st.button("登録"):
            if new_user and new_pass:
                success, msg = register_user(new_user, new_pass)
                if success:
                    st.success(msg + " ログインしてください。")
                else:
                    st.error(msg)
            else:
                st.warning("全ての項目を入力してください")

def main_app():
    # ユーザー名を取得
    username = st.session_state["username"]

    # dataに値がない場合、初期化する
    if "data" not in st.session_state:
        st.session_state.data = load_data(DATA_FILE)

    data = st.session_state.data
    today_str = get_today_str()    # 現在の日付

 
    
    with st.sidebar:
        st.header(f"🌱 {username}の庭") # ユーザー名を表示
        if st.button("ログアウト"):
            st.session_state.clear()
            st.rerun()
            
        page = st.radio("ページを選んでください", ["説明","ダッシュボード", "ガーデン", "履歴"])
        st.markdown("---")
        st.subheader("➕ 新しい習慣")
        new_habit_name = st.text_input("習慣の名前", placeholder="例: 読書をする")
        new_habit_cat = st.selectbox("カテゴリ", ["健康", "勉強", "運動", "提出", "作品"])

        if st.button("習慣を追加"):
            if new_habit_name:
                existing_ids = [h["id"] for h in data["habits"]]
                new_id = max(existing_ids) + 1 if existing_ids else 1
                new_item = {
                    "id": new_id,
                    "name": new_habit_name,
                    "category": new_habit_cat,
                    "created_at": today_str,
                }
                data["habits"].append(new_item)
                save_data(data,DATA_FILE)
                st.success(f"「{new_habit_name}」を追加しました！")
                st.rerun()
            else:
                st.warning("習慣の名前を入力してください。")

    st.title("🍃 Habit Garden")

    if page == "説明":   
        render_explanation()  # 説明画面
    elif page == "ダッシュボード":
        render_dashboard(data, today_str,XP_PER_TASK,DATA_FILE,LEVEL_DATA)  # ダッシュボード画面
    elif page == "ガーデン":
        render_garden_page(data, today_str,XP_PER_TASK,DATA_FILE,LEVEL_DATA)  # ガーデンの画面
    else:
        render_history_page(data)        # 履歴の画面

if __name__ == "__main__":
    main()