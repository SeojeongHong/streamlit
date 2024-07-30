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
    topics = list(contents.keys())
    return contents, topics
CONTENTS , TOPICS = load_contents()

def init_session_state() :
    if 'page' not in st.session_state:
        st.session_state['page'] = 'page_topic'

    if 'topic' not in st.session_state:
        st.session_state['topic'] = TOPICS[0]

    if 'chapter' not in st.session_state:
        st.session_state['chapter'] = None

    if 'section' not in st.session_state:
        st.session_state['section'] = None

    #(page, topic, chapter, section)
    return (st.session_state['page'], st.session_state['topic'], 
            st.session_state['chapter'], st.session_state['section'])

def update_session_state(*args) :
    key = args[0]

    #topic 변경(사이드바)
    if key == 'change_topic':
        st.session_state['page'] = 'page_topic'
        st.session_state['topic'] = st.session_state['change_topic']
        st.session_state['chapter'] = None
        st.session_state['section'] = None
    
    #chapter 변경(학습하기)
    elif key == 'change_chapter' :
        st.session_state['page'] = 'page_chapter'
        st.session_state['chapter'] = args[1]['chapter']
    
    #section 변경(셀렉트박스)
    elif key == 'change_section' :
        st.session_state['section'] = st.session_state['change_section']
    
    #돌아가기
    elif key == 'go_back' :
        st.session_state['page'] = 'page_topic'
        st.session_state['chapter'] = None
        st.session_state['section'] = None

def show_topic(topic):
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

            card.button("학습하기", 
                        key=f"btn_{i}",
                        on_click=update_session_state, 
                        args=('change_chapter', {'chapter':title}),
                        use_container_width=True)

def show_chapter(topic, chapter):
    sections = CONTENTS[topic][chapter]

    st.title(chapter)
    
    st.session_state['section'] = st.selectbox("Choose a section:",
                                               sections,
                                               key = 'change_section',
                                               on_change = update_session_state,
                                               args=('change_section',),
                                               label_visibility="hidden")
    section = st.session_state['section']
    show_section(topic, chapter, section)

    st.button("돌아가기", on_click=update_session_state, args=('go_back',))

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
    page, topic, chapter, section = init_session_state()
    
    if page == 'page_topic':
        show_topic(topic)
    elif page == 'page_chapter':
        show_chapter(topic, chapter)
    
    with st.sidebar:
        option_menu(
            "데이터 분석 역량 강화", 
            TOPICS,
            manual_select = TOPICS.index(topic) if topic in TOPICS else 0,
            key = "change_topic",
            on_change = update_session_state,
            styles={
                "menu-title": {"font-size": "13px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link": {"font-size": "13px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#RGB(255,99,99)"}
            }
        )

if __name__ == "__main__":
    main()