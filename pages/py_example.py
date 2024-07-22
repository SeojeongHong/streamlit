import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

if 'page' not in st.session_state:
    st.session_state['page'] = None

# 사이드바 옵션
with st.sidebar:
    selected = option_menu(
        "데이터 분석 역량 강화", 
        ["파이썬 기초", "pandas 기초", "Matplotlib 기초"], 
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


placeholder = st.empty()


# 파이썬 기초 페이지
if st.session_state['page'] == "파이썬 기초":
    with placeholder.container():
        st.title("파이썬 기초")
        st.info('파이썬 기초 문법을 제공합니다')
        
        # 대단원
        topics = ["대단원01", "대단원02", "대단원03", "대단원04", "대단원05", "대단원06"]
        table = [st.columns(3)] * ((len(topics) + 2) // 3)
        
        for i, title in enumerate(topics):
            with table[i // 3][i % 3]:
                tile = st.container(height=200, border=True)
                tile.subheader(title)
                if tile.button("학습하기", key=f"btn_{i}"):
                    st.session_state['page'] = f"btn_{i}"

# 대단원 페이지
if st.session_state['page'] and st.session_state['page'].startswith('btn_'):
    with placeholder.container():
        st.header("대단원01")
        # 소단원
        topic = st.selectbox("Choose a topic:", [
            '소단원1',
            '소단원2',
            '소단원3',
            '소단원4',
            '소단원5'
        ], label_visibility="hidden")
        
        st.subheader("예시코드01")
        with st.echo():
            import pandas as pd
            df = pd.DataFrame()
        st.divider()
        
        # if st.button("돌아가기"):
        #     st.session_state['page'] = "파이썬 기초"

# pandas 기초 페이지
if st.session_state['page'] == "pandas 기초":
    st.title("pandas 기초")

# Matplotlib 기초 페이지
if st.session_state['page'] == "Matplotlib 기초":
    st.title("Matplotlib 기초")
