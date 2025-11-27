import streamlit as st
import streamlit_calendar as st_calendar

st.set_page_config(page_title="ガーデン", page_icon="🌷")

st.title("あなたのガーデン")

st_calendar.calendar()
