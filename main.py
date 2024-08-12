import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False
import numpy as np


class IndexAllocator:
    def __init__(self):
        self.parentIdx = 0
        self.childIdx = 0

    #format : 1. / 2. / 3. ...
    def getHeadIdx(self) :
        #섹션 변경
        self.parentIdx += 1
        self.childIdx = 0
        return f"{self.parentIdx}. "

    #format : 1.1 / 1.2 ...
    def getSubIdx(self):
        self.childIdx += 1
        return f"{self.parentIdx}.{self.childIdx} "

idx = IndexAllocator()

@st.cache_data
def load_contents() :
    #topic - chapter
    contents = {
        "파이썬 기초": ["자료형", "제어문", "고급"],
        "Pandas 기초": ["DataFrame", "Excel/CSV", "Data 전처리", "Data 연결과 병합", "Static"],
        "Matplotlib 기초":["Matplotlib 기본", "그래프 그리기?", "그래프에 text", "그래프", "스타일 세부 설정", 
                         "Grid, Annotate", "Plot", "막대 그래프", "이외?"],
        "실습 프로젝트":["대기오염 데이터 분석"],
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
            "Matplotlib 기초" : '''matplotlib.pyplot 모듈은 명령어 스타일로 동작하는 함수의 모음입니다.\n
matplotlib.pyplot 모듈의 각각의 함수를 사용해서 그래프 영역을 만들고, 몇 개의 선을 표현하고, 레이블로 꾸미는 등 간편하게 그래프를 만들고 변화를 줄 수 있습니다.''',
            "실습 프로젝트" : "데이터 분석 및 시각화 실습 코드를 제공합니다.",
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

### pandas에서 사용할 타이타닉 데이터셋
def pandas_dataset():
        st.subheader(f"{idx.getSubIdx()}실습에 사용할 데이터셋")
        with st.echo():
            import seaborn as sns
            df = sns.load_dataset('titanic')
            df

        st.subheader(f"{idx.getSubIdx()}컬럼(columns) 설명")
        st.markdown('- survived: 생존여부 (1: 생존, 0: 사망)\n'
                    '- pclass: 좌석 등급 (1등급, 2등급, 3등급)\n'
                    '- sex: 성별\n'
                    '- age: 나이\n'
                    '- sibsp: 형제 + 배우자 수\n'
                    '- parch: 부모 + 자녀 수\n'
                    '- fare: 좌석 요금\n'
                    '- embarked: 탑승 항구 (S, C, Q)\n'
                    '- class: pclass와 동일\n'
                    '- who: 남자(man), 여자(woman), 아이(child)\n'
                    '- adult_male: 성인 남자 여부\n'
                    '- deck: 데크 번호 (알파벳 + 숫자 혼용)\n'
                    '- embark_town: 탑승 항구 이름\n'
                    '- alive: 생존여부 (yes, no)\n'
                    '- alone: 혼자 탑승 여부\n')
        st.divider()

def show_chapter(topic, chapter):
    st.title(chapter)
    path = (topic, chapter)

    ### Python 컨텐츠 작성
    if path == ("파이썬 기초", "자료형") :
        st.header(f"{idx.getHeadIdx()}숫자형")
        st.write("숫자형에는 정수형(Integer)과 실수형(Float)이 있습니다. 정수는 양의 정수와 음의 정수, 0이 될 수 있는 숫자입니다. 실수는 소수점이 포함된 숫자를 의미합니다.")
        st.code('''
                #정수형(Integer)
                a = 123
                b = - 50

                #실수형(Floating)
                a = 3.14
                b = 100.0
                ''')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}숫자형의 연산 - 산술 연산자")
        st.write('''
                |연산자	|의미	|
                |----------|-----------|
                |+          |덧셈
                |-	        |뺄셈
                |*	        |곱셈
                |**	        |거듭제곱
                |/	        |나눗셈
                |//	        |몫
                |%	        |나머지
                 ''')

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