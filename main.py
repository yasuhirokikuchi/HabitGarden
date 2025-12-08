import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date

# --- 設定 ---
DATA_FILE = "habits.json"
XP_PER_TASK = 10

# 画像ファイルのパスとラベルの設定
LEVEL_DATA = {
    0:   {"label": "Seed",   "image": "images/pot/pot_2.png"},
    100: {"label": "Sprout", "image": "images/pot/pot_3.png"},
    300: {"label": "Tree",   "image": "images/pot/pot_4.png"},
    600: {"label": "Forest", "image": "images/pot/pot_5.png"},
}

# =========================
# 説明
# =========================
def render_explanation():
    


# =========================
# データの読み書き
# =========================
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"habits": [], "history": {}, "xp": 0}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# =========================
# レベル・XP ロジック
# =========================
def get_level_info(xp: int):
    """
    XPに基づいて現在のレベル情報（画像パス、ラベル）と、
    次のレベルまでの進捗率を返す。
    """
    # デフォルト値（レベル0）
    current_img = LEVEL_DATA[0]["image"]
    current_label = LEVEL_DATA[0]["label"]
    next_xp = 100 

    # 現在のレベルを判定
    for threshold, info in sorted(LEVEL_DATA.items()):
        if xp >= threshold:
            current_img = info["image"]
            current_label = info["label"]
        else:
            next_xp = threshold
            break
    
    # 最高レベルを超えている場合の処理（次の目標がない場合）
    max_threshold = max(LEVEL_DATA.keys())
    if xp >= max_threshold:
        next_xp = max_threshold # あるいはもっと大きな値

    # 進捗バーの計算
    prev_threshold = max([k for k in LEVEL_DATA.keys() if k <= xp], default=0)
    level_range = next_xp - prev_threshold
    progress_in_level = xp - prev_threshold

    if level_range > 0 and xp < max_threshold:
        progress_percent = min(1.0, max(0.0, progress_in_level / level_range))
    else:
        progress_percent = 1.0

    return current_img, current_label, progress_percent, next_xp

# =========================
# ユーティリティ
# =========================
def get_today_str() -> str:
    return str(date.today())

def get_habit_name_map(data):
    return {h["id"]: h["name"] for h in data["habits"]}

def calculate_streak(history: dict) -> int:
    if not history:
        return 0
    streak = 0
    check_date = date.today()
    today_str = str(date.today())

    while True:
        d_str = str(check_date)
        if d_str in history and len(history[d_str]) > 0:
            streak += 1
            check_date = check_date - pd.Timedelta(days=1)
        else:
            if d_str == today_str and (d_str in history and len(history[d_str]) == 0):
                check_date = check_date - pd.Timedelta(days=1)
                continue
            break
    return streak

# =========================
# ページ描画用関数
# =========================
def render_dashboard(data, today_str):
    st.subheader("📊 ダッシュボード")

    total_habits = len(data["habits"])
    if today_str not in data["history"]:
        data["history"][today_str] = []

    completed_today_ids = data["history"][today_str]
    completed_count = len(completed_today_ids)
    progress_val = completed_count / total_habits if total_habits > 0 else 0.0
    total_completed_all_time = sum(len(ids) for ids in data["history"].values())

    # ---- 上部スタッツ ----
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("今日の進捗", f"{int(progress_val * 100)}%")
        st.progress(progress_val)
    with c2:
        streak = calculate_streak(data["history"])
        st.metric("現在の連続記録", f"{streak} 日")
    with c3:
        st.metric("これまでの完了数", f"{total_completed_all_time} 回")

    st.divider()

    # ---- メイングリッド ----
    col_list, col_garden = st.columns([2, 1], gap="large")

    # 左：今日の習慣リスト
    with col_list:
        st.subheader("今日の習慣")
        if not data["habits"]:
            st.info("まだ習慣がありません。サイドバーから追加してください。")

        for habit in data["habits"]:
            h_id = habit["id"]
            is_done = h_id in completed_today_ids

            with st.container(border=True):
                c_icon, c_text, c_btn, c_del = st.columns([0.5, 3, 1, 0.5])
                with c_icon:
                    st.write("✅" if is_done else "⬜")
                with c_text:
                    if is_done:
                        st.markdown(f"~~**{habit['name']}**~~")
                    else:
                        st.markdown(f"**{habit['name']}**")
                    st.caption(f"{habit['category']}")
                with c_btn:
                    if not is_done:
                        if st.button("完了", key=f"done_{h_id}"):
                            data["history"][today_str].append(h_id)
                            data["xp"] += XP_PER_TASK
                            save_data(data)
                            st.rerun()
                    else:
                        st.button("済", disabled=True, key=f"done_btn_{h_id}")
                with c_del:
                    if st.button("🗑️", key=f"del_{h_id}"):
                        data["habits"] = [h for h in data["habits"] if h["id"] != h_id]
                        for d, ids in data["history"].items():
                            data["history"][d] = [hid for hid in ids if hid != h_id]
                        save_data(data)
                        st.rerun()

    # 右：ガーデン（画像表示に変更）
    with col_garden:
        st.subheader("あなたの庭")
        current_xp = data["xp"]
        img_path, label, progress, next_goal = get_level_info(current_xp)

        with st.container(border=True):
            # 画像を表示 (存在チェックを行う)
            if os.path.exists(img_path):
                st.image(img_path, caption=label, use_container_width=True)
            else:
                st.error(f"画像が見つかりません: {img_path}")
                st.write(f"Level: {label}")

            st.write(f"**XP:** {current_xp} / {next_goal}")
            st.progress(progress)
            
            remaining = max(0, next_goal - current_xp)
            if remaining > 0:
                st.caption(f"次のレベルまであと {remaining} XP")
            else:
                st.caption("最高レベル到達！")

        with st.expander("設定・リセット"):
            if st.button("全てのデータをリセット"):
                data.clear()
                data.update({"habits": [], "history": {}, "xp": 0})
                save_data(data)
                st.rerun()

def render_garden_page(data):
    """詳細ガーデンビュー（画像表示に変更）"""
    st.subheader("🌿 ガーデンビュー")

    current_xp = data["xp"]
    img_path, label, progress, next_goal = get_level_info(current_xp)

    # 上部：ガーデン全体の状態
    with st.container(border=True):
        col_img, col_info = st.columns([1, 2])
        
        with col_img:
            if os.path.exists(img_path):
                # 大きめに表示
                st.image(img_path, use_container_width=True)
            else:
                st.error("No Image")
        
        with col_info:
            st.markdown(f"## {label}")
            st.write(f"**総XP:** {current_xp}")
            st.progress(progress)
            remaining = max(0, next_goal - current_xp)
            if remaining > 0:
                st.caption(f"次のレベルまであと {remaining} XP")
            else:
                st.caption("素晴らしい！最高レベルに到達しています。")

    st.markdown("### あなたの習慣たち（植物）")
    if not data["habits"]:
        st.info("まだ習慣がありません。サイドバーから追加してください。")
        return

    for habit in data["habits"]:
        h_id = habit["id"]
        with st.container(border=True):
            st.markdown(f"**{habit['name']}**")
            st.caption(f"カテゴリ: {habit['category']} / 作成日: {habit.get('created_at', '-')}")
            done_count = sum(1 for ids in data["history"].values() if h_id in ids)
            st.write(f"これまでの完了回数: {done_count} 回")

def render_history_page(data):
    st.subheader("📜 履歴")
    history = data["history"]
    if not history:
        st.info("まだ履歴がありません。")
        return

    name_map = get_habit_name_map(data)

    for d_str in sorted(history.keys(), reverse=True):
        ids = history[d_str]
        with st.container(border=True):
            st.markdown(f"**{d_str}** - {len(ids)} 件 完了")
            if not ids:
                st.caption("この日は完了した習慣はありません。")
                continue
            for h_id in ids:
                name = name_map.get(h_id, f"削除された習慣 (id={h_id})")
                st.markdown(f"- {name}")

# =========================
# メイン処理
# =========================
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

    if "data" not in st.session_state:
        st.session_state.data = load_data()

    data = st.session_state.data
    today_str = get_today_str()

    with st.sidebar:
        st.header("🌱 Habit Garden")
        page = st.radio("ページを選んでください", ["ダッシュボード", "ガーデン", "履歴"])
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
                save_data(data)
                st.success(f"「{new_habit_name}」を追加しました！")
                st.rerun()
            else:
                st.warning("習慣の名前を入力してください。")

    st.title("🍃 Habit Garden")
    st.caption("毎日続けて、あなたの庭を育てましょう。")

    if page == "はじめに":
        render_explanation();
    elif page == "ダッシュボード":
        render_dashboard(data, today_str)
    elif page == "ガーデン":
        render_garden_page(data)
    else:
        render_history_page(data)

if __name__ == "__main__":
    main()