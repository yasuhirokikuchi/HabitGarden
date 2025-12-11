import streamlit as st
from process.timedata import get_habit_name_map


# 履歴画面
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

