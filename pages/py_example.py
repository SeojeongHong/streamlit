import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

if 'topic' not in st.session_state:
    st.session_state['topic'] = None

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
    st.session_state['topic'] = selected


placeholder = st.empty()

if st.session_state['topic']:
    with placeholder.container():
        st.title(st.session_state['topic'])
        st.info('파이썬 기초 문법을 제공합니다')
        
        # 대단원
        chapter = topics[st.session_state['topic']]
        table = [st.columns(3)] * ((len(chapter) + 2) // 3)
        
        for i, title in enumerate(chapter):
            with table[i // 3][i % 3]:
                tile = st.container(height=200, border=True)
                subtile = tile.container(height=110, border=False)
                subtile.subheader(title)

                if tile.button("학습하기", key=f"btn_{i}", use_container_width=True):
                    st.session_state['topic'] = f"btn_{i}"

# 대단원 페이지
if st.session_state['topic'] and st.session_state['topic'].startswith('btn_'):
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
        
        if st.button("돌아가기"):
            st.session_state['topic'] = selected