import streamlit as st

# 説明

def render_explanation():

    with st.container(horizontal=True, horizontal_alignment="center"):

        st.image("images/title/title.jpeg", width=500)

        st.markdown('<h1 style="text-align:center;">🌿ようこそ <span style="color:green;">Habit Garden</span> へ</h1>',unsafe_allow_html=True)

        st.subheader("Habit Gardenでは決めた目標を植物の成長度合いで表し、目標の達成が一目でわかるようになるアプリ")
