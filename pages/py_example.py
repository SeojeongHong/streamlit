import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

#topic - chapter - section
topics = {
    "파이썬 기초": {
        "대단원 01": ["소단원01", "소단원02"],
        "대단원 02": ["소단원01"],
        "대단원 03": ["소단원01", "소단원02", "소단원03"]
    },
    "Pandas 기초": {
        "대단원 01": ["소단원01", "소단원02", "소단원03"],
        "대단원 02": ["소단원01", "소단원02"],
        "대단원 03": ["소단원01"],
        "대단원 04": ["소단원01", "소단원02", "소단원03", "소단원04"],
        "대단원 05": ["소단원01", "소단원02"]
    },
    "Matplotlib 기초": {
        "대단원 01": ["소단원01", "소단원02", "소단원03"],
        "대단원 02": ["소단원01", "소단원02"]
    }
}
if 'page' not in st.session_state:
    st.session_state['page'] = list(topics.keys())[0]

# 사이드바 옵션
with st.sidebar:
    selected = option_menu(
        "데이터 분석 역량 강화", 
        list(topics.keys()), 
        default_index=0,
        styles={
            "menu-title": {"font-size": "13px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link": {"font-size": "13px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#RGB(255,99,99)"}
        }
    )

#사이드바 -> 대단원
if selected :
    st.session_state['page'] = selected

def show_topic():
    st.write(st.session_state['page'])

def show_chapter():
    st.write("챕터")

def show_section():
    st.write("섹션")

if st.session_state['page'] :
    show_topic()