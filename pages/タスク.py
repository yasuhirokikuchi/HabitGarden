import streamlit as st
import streamlit_calendar as st_calendar
import datetime
import pandas as pd

# キー 'task_list' が存在しない場合にのみ空のリストで初期化
if 'task_list' not in st.session_state:
    st.session_state['task_list'] = []

# 日数入力範囲
min_date = datetime.date(2025, 1, 1)
max_date = datetime.date(2100, 12, 31)


# ページ設定
st.set_page_config(page_title="タスク", page_icon="📖")

# タイトル
st.write("# 📖あなたのタスク管理")


with st.form("my_form", clear_on_submit=False):

    name = st.text_input("目標の内容", placeholder="例: 英単語を20個覚える")                                       # タスクの名前
    min_period = st.date_input('いつから', datetime.date(2025, 1, 1), min_value=min_date, max_value=max_date)    # タスクの期限（いつから）
    max_period = st.date_input('いつまで', datetime.date(2025, 1, 1), min_value=min_date, max_value=max_date)    # タスクの期限（いつまで）
    point = st.selectbox("タスクのポイント",options=["5","10","15"])                                              # タスクのポイント

    submitted = st.form_submit_button("追加する")

# フォーム送信時にリストへ追加（表示処理は追加処理と分離）
if submitted:
    st.success(f"タスク：「{name}」を追加しました！")
    st.session_state['task_list'].append({
        "name": name,
        "done": False,
        "min": min_period,
        "max": max_period,
        "point":point+"ポイント",
    })

st.write("### タスク管理")
st.divider()

# タスク表示
if len(st.session_state['task_list']) > 0:

    # 比率 [タスク名(3), いつから(2), いつまで(2), ポイント(2), 削除ボタン(1)]
    h1, h2, h3, h4, h5 = st.columns([3, 2, 2, 2, 1])
    h1.markdown("**タスク名**")
    h2.markdown("**いつから**")
    h3.markdown("**いつまで**")
    h4.markdown("**報酬**")

    # リストをループして1行ずつ表示
    for i, task in enumerate(st.session_state['task_list']):
        c1, c2, c3, c4, c5 = st.columns([3, 2, 2, 2, 1])

        # 各カラムにデータを表示
        c1.write(task['name'])
        c2.write(task['min'])
        c3.write(task['max'])
        c4.write(task['point'])

        # 削除ボタンの実装
        if c5.button("削除", key=f"del_{i}"):
            st.session_state['task_list'].pop(i)  # リストから削除
            st.rerun()  # 画面を更新して削除を反映
else:
    st.info("現在登録されているタスクはありません！今すぐタスクを追加して植物を育てましょう！")