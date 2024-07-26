import streamlit as st
from streamlit_option_menu import option_menu

@st.cache_data
def load_contents() :
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
    return contents
CONTENTS = load_contents()
TOPICS = list(CONTENTS.keys())

def init_session_state() :
    if 'template' not in st.session_state:
        st.session_state['template'] = 'topic'
        
    if 'topic' not in st.session_state:
        st.session_state['topic'] = TOPICS[0]

    if 'chapter' not in st.session_state:
        st.session_state['chapter'] = None

    if 'section' not in st.session_state:
        st.session_state['section'] = None

def change_topic(key) :
    st.session_state['template'] = 'topic'
    st.session_state['topic'] = st.session_state[key]
    st.session_state['chapter'] = None
    st.session_state['section'] = None


def show_topic():
    topic = st.session_state['topic']
    chapters = CONTENTS[topic]

    st.title(topic)
    info_txt = {
            "파이썬 기초" : "파이썬 기초 문법을 제공합니다.",
            "Pandas 기초" : "Pandas 기초 문법을 제공합니다.",
            "Matplotlib 기초" : "Matplotlib 기초 문법을 제공합니다.",
            }
    st.info(info_txt[topic])
    
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
    sections = CONTENTS[topic][chapter]

    st.title(chapter)
    
    st.session_state['section'] = st.selectbox("Choose a section:", 
                               sections, label_visibility="hidden")
    section = st.session_state['section']

    show_section(topic, chapter, section)
    if st.button("돌아가기"):
        st.session_state['template'] = 'topic'
        st.session_state['chapter'] = None
        st.session_state['section'] = None
        st.rerun()

def show_section(topic, chapter, section):
    st.write(f"path : {topic}  / {chapter} / {section}")
    st.write("예시코드 1")
    with st.echo():
        import pandas as pd
        df = pd.DataFrame()
    st.divider()

    st.write("예시코드 2")
    with st.echo():
        import pandas as pd
        df = pd.DataFrame()
    st.divider()

def main() :
    init_session_state()
        
    with st.sidebar:
        option_menu(
            "데이터 분석 역량 강화", 
            TOPICS,
            manual_select = TOPICS.index(st.session_state['topic']),
            key = "topicChange",
            on_change=change_topic,
            styles={
                "menu-title": {"font-size": "13px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link": {"font-size": "13px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#RGB(255,99,99)"}
            }
        )

    if st.session_state['template'] == 'topic':
        show_topic()
    elif st.session_state['template'] == 'chapter':
        show_chapter()

if __name__ == "__main__":
    main()