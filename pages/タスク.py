import streamlit as st
import streamlit_calendar as st_calendar
import datetime
import pandas as pd

#
st.set_page_config(page_title="タスク", page_icon="📖")
with st.container(horizontal=True, horizontal_alignment="center"):
    st.subheader("📖現在のタスクリスト")

st.divider()

# 画面レイアウト
col1, col2 = st.columns(2)

# キー 'task_list' が存在しない場合にのみ空のリストで初期化
if 'task_list' not in st.session_state:
    st.session_state['task_list'] = []

# 日数入力範囲
min_date = datetime.date(2025, 1, 1)
max_date = datetime.date(2100, 12, 31)

# フォーム内ではローカル変数で扱う（クラス属性を直接使わない）
with col1:
    with st.form("my_form", clear_on_submit=False):
        name = st.text_input("目標の内容", placeholder="例: 英単語を20個覚える")
        min_period = st.date_input('', datetime.date(2025, 1, 1), min_value=min_date, max_value=max_date)
        max_period = st.date_input('期限', datetime.date(2025, 1, 1), min_value=min_date, max_value=max_date)
        submitted = st.form_submit_button("追加する")

# フォーム送信時にリストへ追加（表示処理は追加処理と分離）
    if submitted:
        st.session_state['task_list'].append({
            "name": name,
            "done": False,
            "min": min_period,
            "max": max_period,
        })


# タスク表示（空なら情報表示）
with col2:
    if len(st.session_state['task_list']) > 0:
        for i, t in enumerate(st.session_state['task_list']):
            st.write(f"・**{t['name']}**")
    else:
        st.info("現在登録されているタスクはありません。")