import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime, date

# --- 設定 ---
DATA_FILE = "habits.json"
XP_PER_TASK = 10
LEVEL_THRESHOLDS = {0: "🌱 Seed", 100: "🌿 Sprout", 300: "🌳 Tree", 600: "🌲 Forest"}

# --- 関数: データの読み書き ---
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"habits": [], "history": {}, "xp": 0}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- 関数: ロジック ---
def get_level_info(xp):
    # XPに基づいて現在のレベル（アイコンと名前）を決定
    current_icon = "🌱"
    current_label = "Seed"
    next_xp = 100
    
    for threshold, label in sorted(LEVEL_THRESHOLDS.items()):
        if xp >= threshold:
            current_icon, current_label = label.split(" ")
        else:
            next_xp = threshold
            break
            
    # 次のレベルまでの進捗率
    prev_threshold = max([k for k in LEVEL_THRESHOLDS.keys() if k <= xp], default=0)
    level_range = next_xp - prev_threshold
    progress_in_level = xp - prev_threshold
    progress_percent = min(1.0, max(0.0, progress_in_level / level_range)) if level_range > 0 else 1.0
    
    return current_icon, current_label, progress_percent, next_xp

# --- メイン処理 ---
def main():
    st.set_page_config(page_title="Habit Garden", page_icon="🍃", layout="wide")
    
    # CSSで見た目を少し調整（カード風デザイン）
    st.markdown("""
    <style>
    .stButton>button {
        border-radius: 20px;
        width: 100%;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # データのロード
    if 'data' not in st.session_state:
        st.session_state.data = load_data()
    
    data = st.session_state.data
    today_str = str(date.today())

    # --- サイドバー: 新しい習慣の追加 ---
    with st.sidebar:
        st.header("➕ 新しい習慣")
        new_habit_name = st.text_input("習慣の名前", placeholder="例: 読書をする")
        new_habit_cat = st.selectbox("カテゴリ", ["Health", "Learning", "Mindfulness", "Creativity", "Other"])
        
        if st.button("習慣を追加"):
            if new_habit_name:
                new_id = len(data["habits"]) + 1 # 簡易的なID生成
                # IDが重複しないように調整
                existing_ids = [h['id'] for h in data["habits"]]
                if new_id in existing_ids:
                    new_id = max(existing_ids) + 1 if existing_ids else 1
                
                new_item = {
                    "id": new_id,
                    "name": new_habit_name,
                    "category": new_habit_cat,
                    "created_at": today_str
                }
                data["habits"].append(new_item)
                save_data(data)
                st.success(f"「{new_habit_name}」を追加しました！")
                st.rerun()

    # --- ヘッダーエリア ---
    col_head_1, col_head_2 = st.columns([3, 1])
    with col_head_1:
        st.title("🍃 Habit Garden")
        st.caption("毎日続けて、あなたの庭を育てましょう。")

    # --- 統計データの計算 ---
    total_habits = len(data["habits"])
    
    # 今日の履歴エントリーを取得、なければ作成
    if today_str not in data["history"]:
        data["history"][today_str] = []
    
    completed_today_ids = data["history"][today_str]
    completed_count = len(completed_today_ids)
    
    progress_val = completed_count / total_habits if total_habits > 0 else 0.0
    
    # 合計完了数（全期間）
    total_completed_all_time = sum(len(ids) for ids in data["history"].values())

    # --- ダッシュボード上部: スタッツ (3枚のカード) ---
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("今日の進捗", f"{int(progress_val * 100)}%", delta_color="normal")
        st.progress(progress_val)
    with c2:
        # 簡易的な連続記録（ストリーク）計算
        streak = 0
        check_date = date.today()
        while True:
            d_str = str(check_date)
            if d_str in data["history"] and len(data["history"][d_str]) > 0:
                streak += 1
                check_date = check_date - pd.Timedelta(days=1)
            else:
                # 今日まだ何もしていない場合はストリークが0にならないように、昨日チェック
                if d_str == today_str and len(data["history"][d_str]) == 0:
                     check_date = check_date - pd.Timedelta(days=1)
                     continue
                break
        
        st.metric("現在の連続記録", f"{streak} 日", "Keep going!")
    with c3:
        st.metric("これまでの完了数", f"{total_completed_all_time} 回")

    st.divider()

    # --- メイングリッド ---
    col_list, col_garden = st.columns([2, 1], gap="large")

    # --- 左カラム: 習慣リスト ---
    with col_list:
        st.subheader("今日の習慣")
        
        if not data["habits"]:
            st.info("まだ習慣がありません。サイドバーから追加してください。")
        
        # 習慣リストの表示
        for habit in data["habits"]:
            h_id = habit["id"]
            is_done = h_id in completed_today_ids
            
            # カード風のコンテナ
            with st.container(border=True):
                c_icon, c_text, c_btn, c_del = st.columns([0.5, 3, 1, 0.5])
                
                with c_icon:
                    st.write("✅" if is_done else "⬜")
                
                with c_text:
                    if is_done:
                        st.markdown(f"~~**{habit['name']}**~~") # 取り消し線
                    else:
                        st.markdown(f"**{habit['name']}**")
                    st.caption(f"{habit['category']}")
                
                with c_btn:
                    # 完了ボタン
                    if not is_done:
                        if st.button("完了", key=f"done_{h_id}"):
                            data["history"][today_str].append(h_id)
                            data["xp"] += XP_PER_TASK
                            save_data(data)
                            st.rerun()
                    else:
                        st.button("済", disabled=True, key=f"done_btn_{h_id}")

                with c_del:
                    # 削除ボタン
                    if st.button("🗑️", key=f"del_{h_id}", help="削除"):
                        data["habits"] = [h for h in data["habits"] if h["id"] != h_id]
                        # 履歴からも削除する場合はここにロジックを追加
                        save_data(data)
                        st.rerun()

    # --- 右カラム: 庭（Garden）とXP ---
    with col_garden:
        st.subheader("あなたの庭")
        
        current_xp = data["xp"]
        icon, label, progress, next_goal = get_level_info(current_xp)
        
        with st.container(border=True):
            st.markdown(f"<h1 style='text-align: center; font-size: 80px; margin: 0;'>{icon}</h1>", unsafe_allow_html=True)
            st.markdown(f"<h3 style='text-align: center;'>{label}</h3>", unsafe_allow_html=True)
            
            st.write(f"**XP:** {current_xp} / {next_goal}")
            st.progress(progress)
            st.caption(f"次のレベルまであと {next_goal - current_xp} XP")
        
        # リセットボタン（デバッグ用・やり直し用）
        with st.expander("設定・リセット"):
            if st.button("全てのデータをリセット"):
                st.session_state.data = {"habits": [], "history": {}, "xp": 0}
                save_data(st.session_state.data)
                st.rerun()

if __name__ == "__main__":
    main()