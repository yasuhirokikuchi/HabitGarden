import streamlit as st
import os

from process.level import get_level_info
from process.data import save_data

def render_garden_page(data, today_str,XP_PER_TASK,username,LEVEL_DATA):
    st.subheader("🌿 ガーデンビュー")

    current_xp = data["xp"]
    img_path, label, progress, next_goal = get_level_info(current_xp,LEVEL_DATA)

    # 上部：ガーデン全体の状態
    with st.container(border=True):
        col_img, col_info = st.columns([1, 2]) # 画面構成1対2
        
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

            # 水やり機能
            dailytask = (data.get("daily") == today_str) # 今日水をあげたか 

            if dailytask:
                st.button("水やりは終わっています",disabled=True)
            else:
                if st.button("今日の水やり"):
                    data["daily"] = today_str
                    data["xp"] += XP_PER_TASK
                    save_data(data,username)
                    st.rerun()


    st.markdown("### あなたのタスク")
    if not data["habits"]:
        st.info("まだタスクがありません。サイドバーから追加してください。")
        return

    for habit in data["habits"]:
        h_id = habit["id"]
        with st.container(border=True):
            st.markdown(f"**{habit['name']}**")
            st.caption(f"カテゴリ: {habit['category']} / 作成日: {habit.get('created_at', '-')}")
            done_count = sum(1 for ids in data["history"].values() if h_id in ids)
            st.write(f"これまでの完了回数: {done_count} 回")