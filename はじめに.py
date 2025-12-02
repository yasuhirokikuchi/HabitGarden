import streamlit as st

st.set_page_config(page_title="Habit Garden", page_icon=":seedling:")

with st.container(horizontal=True, horizontal_alignment="center"):

    st.title("🌱ようこそHabit Gardenへ")
    st.image("image/title/unnamed.png")

    st.subheader("Habit Gardenでは目標を植物の成長度合いで可視化し、目標の進捗が一目でわかるようになるアプリです。")

    