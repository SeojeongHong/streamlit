import streamlit as st
from streamlit_option_menu import option_menu

@st.cache_data
def load_contents() :
    #topic - chapter
    contents = {
        "파이썬 기초": ["대단원1", "대단원2"],
        "Pandas 기초": ["대단원1", "대단원2"],
        "Matplotlib 기초": ["대단원1", "대단원2"],
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

    #(page, topic, chapter)
    return (st.session_state['page'], st.session_state['topic'], 
            st.session_state['chapter'])

def update_session_state(*args) :
    key = args[0]

    #topic 변경(사이드바)
    if key == 'change_topic':
        st.session_state['page'] = 'page_topic'
        st.session_state['topic'] = st.session_state['change_topic']
        st.session_state['chapter'] = None
    
    #chapter 변경(학습하기)
    elif key == 'change_chapter' :
        st.session_state['page'] = 'page_chapter'
        st.session_state['chapter'] = args[1]['chapter']
    
    #돌아가기
    elif key == 'go_back' :
        st.session_state['page'] = 'page_topic'
        st.session_state['chapter'] = None

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
    path = (topic, chapter)
    st.title(chapter)

    ### 컨텐츠 작성
    if path == ("파이썬 기초", "대단원1") :
        st.write("예시코드 1")
    else :
        st.error("Content Not Found !")

    st.button("돌아가기", on_click=update_session_state, args=('go_back',))

def main() :
    page, topic, chapter = init_session_state()
    
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
