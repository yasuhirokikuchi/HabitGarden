import streamlit as st
import os

# データの読み書き
from process.data import load_data,save_data
# レベル、経験値の管理
from process.level import get_level_info
# 時間管理
from process.timedata import calculate_streak,get_today_str



# ダッシュボード画面
def render_dashboard(data, today_str,XP_PER_TASK,DATA_FILE,LEVEL_DATA):

    st.subheader("📊 ダッシュボード")

    total_habits = len(data["habits"])
    if today_str not in data["history"]:
        data["history"][today_str] = []

    completed_today_ids = data["history"][today_str]
    completed_count = len(completed_today_ids)
    progress_val = completed_count / total_habits if total_habits > 0 else 0.0
    total_completed_all_time = sum(len(ids) for ids in data["history"].values())

    # 上のページ構成
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

    # 下のページ構成
    col_list, col_garden = st.columns([2, 1], gap="large")

    # 左：今日の習慣リスト
    with col_list:
        st.subheader("今日のやること")
        if not data["habits"]:
            st.info("まだタスクがありません。サイドバーから追加してください。")

        for habit in data["habits"]:
            h_id = habit["id"]
            done = h_id in completed_today_ids

            with st.container(border=True):
                c_icon, c_text, c_btn, c_del = st.columns([0.5, 3, 1, 0.5])  # ページ比率

                with c_icon:  # 0.5
                    st.write("✅" if done else "⬜")

                with c_text:  # 3
                    if done:
                        st.markdown(f"~~**{habit['name']}**~~")
                    else:
                        st.markdown(f"**{habit['name']}**")
                    st.caption(f"{habit['category']}")

                with c_btn:   # 1
                    if not done:
                        if st.button("完了", key=f"done_{h_id}"):
                            data["history"][today_str].append(h_id)
                            data["xp"] += XP_PER_TASK
                            save_data(data,DATA_FILE)
                            st.rerun()
                    else:
                        st.button("済", disabled=True, key=f"done_btn_{h_id}")

                with c_del:  # 0.5
                    if st.button("🗑️", key=f"del_{h_id}"):
                        data["habits"] = [h for h in data["habits"] if h["id"] != h_id]
                        for d, ids in data["history"].items():
                            data["history"][d] = [hid for hid in ids if hid != h_id]
                        save_data(data,DATA_FILE)
                        st.rerun()

    # 右：ガーデン
    with col_garden:
        st.subheader("あなたの庭")
        current_xp = data["xp"]
        img_path, label, progress, next_goal = get_level_info(current_xp,LEVEL_DATA)

        with st.container(border=True):
            # 画像を表示 (存在チェックを行う)
            if os.path.exists(img_path):
                st.image(img_path, caption=label, use_container_width=True)
            else: # 画像がない場合
                st.error(f"画像が見つかりません: {img_path}")
                st.write(f"Level: {label}")

            st.write(f"**XP:** {current_xp} / {next_goal}")
            st.progress(progress)
            
            remaining = max(0, next_goal - current_xp)
            if remaining > 0:
                st.caption(f"次のレベルまであと {remaining} XP")
            else:
                st.caption("最高レベル到達！")

            # 水やり機能
            dailytask = (data.get("daily") == get_today_str()) # 今日水をあげたか 

            if dailytask:
                st.button("水やりは終わっています",disabled=True)
            else:
                if st.button("今日の水やり"):
                    data["daily"] = get_today_str()
                    data["xp"] += XP_PER_TASK
                    save_data(data,DATA_FILE)
                    st.rerun


                # リセット画面
        with st.expander("設定・リセット"):
            if st.button("全てのデータをリセット"):
                data.clear()
                data.update({"habits": [], "history": {},"daily":[], "xp": 0}) # 初期値
                save_data(data,DATA_FILE)
                st.rerun()