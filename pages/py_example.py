import streamlit as st
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

# 전역 상태
if 'template' not in st.session_state:
    st.session_state['template'] = 'topic'

if 'topic' not in st.session_state:
    st.session_state['topic'] = None

if 'chapter' not in st.session_state:
    st.session_state['chapter'] = None

if 'section' not in st.session_state:
    st.session_state['section'] = None

#topic - chapter - section
contents = {
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
topics = list(contents.keys())

with st.sidebar:
    selected = option_menu(
        "데이터 분석 역량 강화", 
        topics, 
        default_index=0,
        styles={
            "menu-title": {"font-size": "13px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link": {"font-size": "13px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#RGB(255,99,99)"}
        }
    )
if selected :
    st.session_state['topic'] = selected

def show_topic():
    topic = st.session_state['topic']
    chapters = contents[topic]

    st.title(topic)
    table = [st.columns(3)] * ((len(chapters) + 2) // 3)
        
    for i, title in enumerate(chapters):
        with table[i // 3][i % 3]:
            card = st.container(height=200, border=True)
            subcard = card.container(height=110, border=False)
            subcard.subheader(title)

            if card.button("학습하기", key=f"btn_{i}", use_container_width=True):
                st.session_state['chapter'] = title
                st.session_state['template'] = 'chapter'
                st.rerun()

def show_chapter():
    topic = st.session_state['topic']
    chapter = st.session_state['chapter']

    st.title(chapter)
    section = st.selectbox("Choose a section:", 
                               contents[topic][chapter], label_visibility="hidden")
    
    show_section(topic, chapter, section)
    if st.button("돌아가기"):
        st.session_state['template'] = 'topic'
        st.rerun()

def show_section(topic, chapter, section):
    st.write("path : "+topic +" / "+ chapter +" / "+ section)
    with st.echo():
        import pandas as pd
        df = pd.DataFrame()
    st.divider()

if st.session_state['template'] == 'topic':
    show_topic()
elif st.session_state['template'] == 'chapter':
    show_chapter()