import streamlit as st
import json
import os

# データの読み書き
from process.data import load_data,save_data
# レベル、経験値の管理
from process.level import get_level_info
# 時間管理
from process.timedata import get_today_str,get_habit_name_map,calculate_streak


# アプリケーションの説明画面
from draw.explanation import render_explanation
# ダッシュボード画面
from draw.dashbord import render_dashboard
# ガーデンの画面
from draw.garden import render_garden_page
# 履歴画面
from draw.history import render_history_page

# 設定
DATA_FILE = "habits.json"
XP_PER_TASK = 10

# 画像ファイルのパスとラベルの設定
LEVEL_DATA = {
    0:   {"label": "Seed",   "image": "images/pot/pot_2.png"},
    100: {"label": "Sprout", "image": "images/pot/pot_3.png"},
    300: {"label": "Tree",   "image": "images/pot/pot_4.png"},
    600: {"label": "Forest", "image": "images/pot/pot_5.png"},
}

# メイン処理
def main():
    st.set_page_config(page_title="Habit Garden", page_icon="🍃", layout="wide")
    st.markdown(
        """
        <style>
        .stButton>button { border-radius: 20px; width: 100%; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 
    if "data" not in st.session_state:
        st.session_state.data = load_data(DATA_FILE)

    data = st.session_state.data
    today_str = get_today_str()    # 現在の日付

    with st.sidebar:
        st.header("🌱 Habit Garden")
        page = st.radio("ページを選んでください", ["説明","ダッシュボード", "ガーデン", "履歴"])
        st.markdown("---")
        st.subheader("➕ 新しい習慣")
        new_habit_name = st.text_input("習慣の名前", placeholder="例: 読書をする")
        new_habit_cat = st.selectbox(
            "カテゴリ", ["Health", "Learning", "Mindfulness", "Creativity", "Other"]
        )

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
    st.caption("毎日続けて、あなたの庭を育てましょう。")

    # サイドバー選択項目
    if page == "説明":   
        render_explanation()    # 説明画面
    elif page == "ダッシュボード":
        render_dashboard(data, today_str,XP_PER_TASK,DATA_FILE,LEVEL_DATA)  # ダッシュボード画面
    elif page == "ガーデン":
        render_garden_page(data,LEVEL_DATA)         # ガーデンの画面
    else:
        render_history_page(data)        # 履歴の画面

if __name__ == "__main__":
    main()