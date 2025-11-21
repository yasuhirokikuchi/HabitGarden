import streamlit as st

def main():
    # １ページ目表示
    st.sidebar.title("test_streamlit")
    st.markdown("## ボタンでページを変えましょう")
    st.sidebar.button("ページ切り替えボタン", on_click=change_page)

def change_page():
    # ページ切り替えボタンコールバック
    st.session_state["page_control"]=1

def next_page():
    # ２ページ目表示
    st.sidebar.title("ページが切り替わりました")
    st.markdown("## 次のページです")

# 状態保持する変数を作成して確認
if ("page_control" in st.session_state and
   st.session_state["page_control"] == 1):
    next_page()
else:
    st.session_state["page_control"] = 0
    main()