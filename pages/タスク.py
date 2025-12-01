import streamlit as st
import streamlit_calendar as st_calendar
import datetime

# 構造体task
class task:
    def __init__(self):
        self.name = ""
        self.min_period = 0
        self.max_period = 0

# 日数入力範囲
min_date = datetime.date(2025, 1, 1)
max_date = datetime.date(2100, 12, 31)


st.title("タスク管理")

with st.form("my_form", clear_on_submit=False):
    # タスクの名前入力
    task.name = st.text_input("目標の内容", placeholder="例: 英単語を20個覚える")

    # 期間の数値入力
    task.min_period = st.date_input('タスクの期間を設定してください。', datetime.date(2025, 1, 1), min_value=min_date, max_value=max_date)
    task.max_period = st.date_input('' ,datetime.date(2025, 1, 1), min_value=min_date, max_value=max_date)

    submitted = st.form_submit_button("追加する")

#------------------------------------------区切り線------------------------------------------
st.divider()
st.subheader("現在のタスクリスト")

# 入力内容表示
if submitted:
    st.write(f"タスク: {task.name}")
    st.write(f"いつから: {task.min_period}")
    st.write(f"いつまで: {task.max_period}")