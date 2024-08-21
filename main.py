import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import os
import io
from matplotlib import font_manager as fm
fpath = os.path.join(os.getcwd(), "customfont/NanumGothic-Regular.ttf")
prop = fm.FontProperties(fname=fpath)
import numpy as np
import seaborn as sns
from streamlit_float import *
from streamlit_server_state import server_state, server_state_lock
import sqlite3
import socket
from streamlit import runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.web.server.websocket_headers import _get_websocket_headers

def get_remote_ip():
    try:
        ctx = get_script_run_ctx()
        if ctx is None:
            return None

        session_info = runtime.get_instance().get_client(ctx.session_id)
        if session_info is None:
            return None
    except Exception as e:
        return None

    return session_info.request.remote_ip

def get_forwarded_ip():
    headers = st.context.headers()
    return headers


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))
    ip = s.getsockname()[0]
    return ip

def db_init() :
    con = sqlite3.connect('./user_info.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS USER(IP text PRIMARY KEY);")
    con.commit()

    try:
        cur.execute('INSERT INTO USER VALUES(?);', ((get_ip()),))
        con.commit()
    except:
        pass
    
    cur.execute('SELECT COUNT(*) FROM USER')
    user_count = cur.fetchone()[0]
    con.close()
    return user_count




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
        "Matplotlib 기초":["Matplotlib 기본", "그래프 그리기", "그래프에 text", "그래프 세부 속성", "스타일 세부 설정", 
                         "Grid, Annotate", "다양한 Plot", "막대 그래프", "Pie chart, 3D plot"],
        "실습 프로젝트":["대기오염 데이터 분석", "지역별 음식점 소비 트렌드 분석", "날씨별 공공자전거 수요 분석"],
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
            "Pandas 기초" : '''pandas는 데이터를 쉽게 다루고 분석할 수 있게 도와주는 라이브러리입니다. \n
데이터를 표 형태로 나타낼 수 있으며, 효과적으로 저장하고 조작할 수 있고, 필터링하고 정렬하는 데 유용합니다''',
            "Matplotlib 기초" : '''matplotlib.pyplot 모듈은 명령어 스타일로 동작하는 함수의 모음입니다.\n
matplotlib.pyplot 모듈의 각각의 함수를 사용해서 그래프 영역을 만들고, 몇 개의 선을 표현하고, 레이블로 꾸미는 등 간편하게 그래프를 만들고 변화를 줄 수 있습니다.''',
            "실습 프로젝트" : "데이터 분석 및 시각화 실습 코드를 제공합니다.",
    }
    with st.container():
        st.info(info_txt[topic])
    
    table = [st.columns(3)] * ((len(chapters) + 2) // 3)
    for i, title in enumerate(chapters):
        with table[i // 3][i % 3]:
            formatted_title = title.replace('\n', ' ')
            card = st.container(height=200, border=True)
            subcard = card.container(height=110, border=False)
            subcard.markdown(f"""<h3 style='
                    text-align: left;
                    word-break: keep-all;
                    overflow-wrap: break-word;
                    display: -webkit-box;
                    -webkit-line-clamp: 3;
                    -webkit-box-orient: vertical;
                    overflow: hidden;
                    '>{formatted_title}</h3>""", unsafe_allow_html=True)

            card.button("학습하기", 
                        key=f"btn_{i}",
                        on_click=update_session_state, 
                        args=('change_chapter', {'chapter':title}),
                        use_container_width=True)

def show_chapter(topic, chapter):
    st.title(chapter)
    path = (topic, chapter)

    ### Python 컨텐츠 작성
    if path == ("파이썬 기초", "자료형") :
        st.header(f"{idx.getHeadIdx()}숫자형")
        st.write("숫자형에는 **정수형**(Integer)과 **실수형**(Float)이 있습니다. 정수는 양의 정수와 음의 정수, 0이 될 수 있는 숫자입니다. 실수는 소수점이 포함된 숫자를 의미합니다.")
        st.code('''
                #정수형(Integer)
                a = 123
                b = - 50

                #실수형(Floating)
                a = 3.14
                b = 100.0
                ''',line_numbers=True)
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
        
        st.code('''
                a = 5
                b = 2

                print( a + b )
                #출력 : 7

                print( a - b )
                #출력 : 3

                print( a * b )
                #출력 : 10

                print( a ** b )
                #출력 : 25

                print( a / b )
                #출력 : 2.5

                print( a // b )
                #출력 : 2

                print( a % b )
                #출력 : 1
                ''',line_numbers=True)
        st.divider()

        st.subheader(f"{idx.getSubIdx()}숫자형의 연산 - 복합 연산자")
        st.write("복합 연산자는 앞서 살펴본 +, - 와 같은 산술 연산자와 대입 연산자(=)를 합쳐 놓은 것입니다. 복합 연산자를 사용하면 코드를 더욱 간결하고 가독성 있게 작성할 수 있습니다.")
        st.write('''
                | 연산자        | 동치              | 의미               |
                |---------------|-------------------|--------------------|
                | a = b         |                   | 대입 연산자        |
                | a += b        | a = a + b         | 덧셈 후 대입       |
                | a -= b        | a = a - b         | 뺄셈 후 대입       |
                | a *= b        | a = a * b         | 곱셈 후 대입       |
                | a **= b       | a = a ** b        | 거듭제곱 후 대입   |
                | a /= b        | a = a / b         | 나눗셈 후 대입     |
                | a //= b       | a = a // b        | 몫 연산 후 대입    |
                | a %= b        | a = a % b         | 나머지 연산 후 대입 |

                 ''')
        st.code('''
                a = 12
                print(a)
                #출력 : 12

                a = 3
                a += 5  #a = a + 5
                print(a)
                #출력 : 8

                a = 6
                a -= 2  #a = a - 2
                print(a)
                #출력 : 4

                a = 7
                a *= 3  #a = a * 3
                print(a)
                #출력 : 21

                a = 5
                a **= 3  #a = a ** 3
                print(a)
                #출력 : 125

                a = 10
                a /= 4  #a = a / 4
                print(a)
                #출력 : 2.5

                a = 7
                a //= 2  #a = a // 2
                print(a)
                #출력 : 3

                a = 13
                a %= 9  #a = a % 9
                print(a)
                #출력 : 4
                ''',line_numbers=True)
        st.divider()
        
        st.header(f"{idx.getHeadIdx()}문자열")
        st.write('''문자열(string)이란 연속된 문자들의 나열을 말합니다. 큰따옴표("") 또는 작은따옴표('')로 묶어서 정의합니다.''')
        st.code('''
                str1 = "Hello World !"
                print(str1)
                #출력 : Hello World !

                str2 = 'Python is Easy'
                print(str2)
                #출력 : Python is Easy
                ''',line_numbers=True)
        st.divider()
        st.subheader(f"{idx.getSubIdx()}문자열 길이 구하기")
        st.write("문자열의 길이는 다음과 같이 **len** 함수를 사용해 구할 수 있습니다.")
        st.code('''
                a = "Life is too short"
                print(len(a))
                #출력 : 17
                ''',line_numbers=True)
        st.divider()
        
        st.subheader(f"{idx.getSubIdx()}문자열 인덱싱")
        st.write("인덱싱이란 문자열에서 문자를 추출하는 것입니다. 문자열의 문자에 접근하기 위해서 '**문자열[인덱스]**' 형식으로 접근할 수 있습니다. 이때 인덱스는 0부터 시작합니다.")
        st.code('''
                str = "Hello World"
                
                print(str[0])   #출력 : H
                print(str[3])   #출력 : l
                print(str[-1])   #출력 : d
                print(str[-5])   #출력 : W
                ''',line_numbers=True)
        st.write("인덱스의 (-) 는 문자열을 뒤에서부터 읽기 위해 사용합니다. 즉, str[-1]은 뒤에서 첫 번째가 되는 문자를 의미하며, str[-5]는 뒤에서 5번째 문자를 의미합니다.")
        st.divider()

        st.subheader(f"{idx.getSubIdx()}문자열 슬라이싱")
        st.write('''슬라이싱은 문자열의 일부분을 추출하는 것입니다. 문자열의 슬라이싱은 아래와 같은 형식으로 수행할 수 있습니다.
                 
                        문자열[start : end : step]
                
**start**는 시작 인덱스, **end**는 끝 인덱스, **step**은 슬라이싱 간격을 의미합니다. step의 기본 값은 1으로 생략 가능합니다.
                 ''')
        st.code('''
                str = "Life is too short, You need Python"
                print(str[0:4])
                # 출력 : Life
                ''',line_numbers=True)
        
        st.write('''
                슬라이싱할 때 start를 생략하면 처음부터 end까지, end를 생략하면 start부터 끝까지 문자열을 추출합니다.
                 ''')
        st.code('''
                str = "Life is too short, You need Python"
                
                # start 생략
                print(str[ : 4])
                # 출력 : Life

                # end 생략
                print(str[ -6: ])
                # 출력 : Python
                ''',line_numbers=True)
        st.divider()
        st.subheader(f"{idx.getSubIdx()}문자열 관련 함수")
        st.write('''
                - **count()** : 문자 개수 세기
                 ''')
        st.code('''
                a = "hobby"
                print(a.count('b'))   #문자열 중 문자 b의 개수 리턴
                #출력 : 2
                ''',line_numbers=True)
        
        st.write('''
                - **find()** : 위치 알려 주기1
                 ''')
        st.code('''
                a = "Python is the best choice"
                print(a.find('b'))   #문자열 중 문자 b가 처음으로 나온 위치 리턴
                #출력 : 14

                print(a.find('k'))   #찾는 문자나 문자열이 존재하지 않는다면 -1을 리턴
                #출력 : -1
                ''',line_numbers=True)
        
        st.write('''
                - **index()** : 위치 알려 주기2
                 ''')
        st.code('''
                a = "Life is too short"
                print(a.index('t'))   #문자열 중 문자 t가 맨 처음으로 나온 위치를 리턴
                #출력 : 8

                print(a.index('k'))   #찾는 문자나 문자열이 존재하지 않는다면 오류 발생
                #Traceback (most recent call last):
                #File "<stdin>", line 1, in <module>
                #ValueError: substring not found
                ''',line_numbers=True)
        
        st.write('''
                - **join()** : 문자열 삽입
                 ''')
        st.code('''
                print(",".join('abcd'))   #abcd 문자열의 각각의 문자 사이에 ‘,’를 삽입
                #출력 : a,b,c,d
                ''',line_numbers=True)
        
        st.write('''
                - **upper()** : 소문자를 대문자로 바꾸기
                 ''')
        st.code('''
                a = "hi"
                print(a.upper())
                #출력 : 'HI'
                ''',line_numbers=True)
        
        st.write('''
                - **lower()** : 대문자를 소문자로 바꾸기
                 ''')
        st.code('''
                a = "HELLO"
                print(a.lower())
                #출력 : 'hello'
                ''',line_numbers=True)
        
        st.write('''
                - **lstrip()** : 왼쪽 공백 지우기
                 ''')
        st.code('''
                a = "  hi  "
                print(a.lstrip())
                #출력 : 'hi  '
                ''',line_numbers=True)
        
        st.write('''
                - **rstrip()** : 오른쪽 공백 지우기
                 ''')
        st.code('''
                a = "  hi  "
                print(a.rstrip())
                #출력 : '  hi'
                ''',line_numbers=True)
        
        st.write('''
                - **strip()** : 양쪽 공백 지우기
                 ''')
        st.code('''
                a = "  hi  "
                print(a.strip())
                #출력 : 'hi'
                ''',line_numbers=True)
        
        st.write('''
                - **replace()** : 문자열 바꾸기
                 ''')
        st.code('''
                a = "Good mornig"
                print(a.replace("mornig", "evening"))  #replace(바뀔_문자열, 바꿀_문자열)
                #출력 : Good evening
                ''',line_numbers=True)
        st.write("replace 함수는 replace(바뀔_문자열, 바꿀_문자열)처럼 사용해서 문자열 안의 특정한 값을 다른 값으로 치환해 줍니다.")
        st.write('''
                - **split()** : 문자열 나누기
                 ''')
        st.code('''
                a = "Life is too short"
                print(a.split())
                #출력 : ['Life', 'is', 'too', 'short']

                b = "a:b:c:d"
                print(b.split(':'))
                #출력 : ['a', 'b', 'c', 'd']
                ''',line_numbers=True)
        st.write("split 함수는 a.split()처럼 괄호 안에 아무 값도 넣어 주지 않으면 공백([Space], [Tab], [Enter])을 기준으로 문자열을 나누어 줍니다. 만약 b.split(':')처럼 괄호 안에 특정 값이 있을 경우에는 괄호 안의 값을 구분자로 해서 문자열을 나누어 줍니다.")    
        st.divider()
        
        st.header(f"{idx.getHeadIdx()}불")
        st.write('''
                불(bool)이란 **참**(True)과 **거짓**(False)을 나타내는 자료형입니다. 불 자료형은 다음 2가지 값만을 가질 수 있습니다.

                - True: 참을 의미한다.
                - False: 거짓을 의미한다.
                
                True나 False는 파이썬의 예약어로, true, false와 같이 작성하면 안 되고 첫 문자를 항상 대문자로 작성해야 합니다.
                 ''')
        st.divider()
        st.subheader(f"{idx.getSubIdx()}불 자료형 사용법")
        st.write("불 자료형은 조건문의 리턴값으로도 사용됩니다.")
        st.code('''
                a = 5 > 3
                print(a)
                #출력 : True

                a = 5 < 3
                print(a)
                #출력 : False
                ''',line_numbers=True)
        st.divider()
        st.subheader(f"{idx.getSubIdx()}자료형의 참과 거짓")
        st.write('''
                문자열, 리스트, 튜플, 딕셔너리 등의 값이 비어 있으면("", [], (), {}) 거짓(False)이 되고 비어 있지 않으면 참(True)이 됩니다. 숫자에서는 그 값이 0일 때 거짓이 됩니다.
                 
                |값         |True or False |
                |-----------|-----------|
                |"python"	|True         |
                |""	        |False       |
                |[1, 2, 3]	|True         |
                |[]	        |False       |
                |(1, 2, 3)	|True         |
                |()	        |False       |
                |{'a': 1}	|True         |
                |{}	        |False       |
                |1	        |True         |
                |0	        |False       |
                 
                 ''')
        st.divider()
        
        st.header(f"{idx.getHeadIdx()}리스트")
        st.write("리스트는 데이터들을 편리하게 관리하기 위해 묶어서 관리하는 자료형 중의 하나입니다. 리스트 안에는 어떠한 자료형도 포함할 수 있습니다.")
        st.code('''
                a = []  #값이 없는 리스트
                print(a)
                #출력 : []
                
                a = [1,2,3] 
                print(a)
                #출력 : [1, 2, 3]

                a = ["To", "do", "List"]  #문자가 입력된 리스트
                print(a)
                #출력 : ['To', 'do', 'List']

                a = ["To", "do", "List", 10, 20]  #문자+숫자 같이 입력된 리스트
                print(a)
                #출력 : ['To', 'do', 'List', 10, 20]

                a = [1,2,['P',3]]  #리스트 안에 입력된 리스트
                print(a)
                #출력 : [1, 2, ['P', 3]]
                ''',line_numbers=True)
        st.divider()
        st.subheader(f"{idx.getSubIdx()}리스트의 인덱싱")
        st.write("리스트 역시 문자열처럼 인덱싱을 적용할 수 있습니다.")
        st.code('''
                a = [1, 2, 3]

                print(a[0])
                #출력 : 1

                print(a[0] + a[2])
                #출력 : 4

                print(a[-1])
                #출력 : 3
                ''',line_numbers=True)
        
        st.write("리스트 안에 리스트가 있는 경우에도 인덱싱이 가능합니다.")
        st.code('''
                a = [1, 2, 3, ['a', 'b', 'c']]

                print(a[0])
                #출력 : 1

                print(a[-1])
                #출력 : ['a', 'b', 'c']

                print(a[-1][1])
                #출력 : 'b'
                ''',line_numbers=True)
        st.divider()

        st.subheader(f"{idx.getSubIdx()}리스트의 슬라이싱")
        st.write("문자열과 마찬가지로 리스트에서도 슬라이싱 기법을 적용할 수 있습니다.")
        st.code('''
                a = [1, 2, 3, 4, 5]
                print(a[0:2])
                #출력 : [1, 2]

                print(a[:2])
                #출력 : [1, 2]

                print(a[2:])
                #출력 : [3, 4, 5]
                ''',line_numbers=True)
        st.divider()
        st.subheader(f"{idx.getSubIdx()}리스트 길이 구하기")
        st.write("리스트 길이를 구하기 위해서는 다음처럼 **len** 함수를 사용해야 합니다.")
        st.code('''
                a = [1, 2, 3]
                print(len(a))
                #출력 : 3
                ''',line_numbers=True)
        st.write("len은 문자열, 리스트 외에 앞으로 배울 튜플과 딕셔너리에도 사용할 수 있는 함수입니다.")
        
        st.divider()
        st.subheader(f"{idx.getSubIdx()}리스트 값 수정하기")
        st.write("리스트의 인덱스를 통해 요소에 접근하고 값을 수정할 수 있습니다.")
        st.code('''
                a = [1, 2, 3]
                a[2] = 4

                print(a)
                #출력 : [1, 2, 4]
                ''',line_numbers=True)
        st.divider()
        st.subheader(f"{idx.getSubIdx()}리스트 요소 삭제하기")
        st.write("**del** 함수를 사용해 리스트의 요소를 삭제할 수 있습니다. 삭제 또한 인덱스를 통해 요소에 접근합니다.")
        st.code('''
                a = [1, 2, 3]
                del a[1]

                print(a)
                #출력 : [1, 3]
                ''',line_numbers=True)
        st.write("다음처럼 슬라이싱 기법을 사용하여 리스트의 요소 여러 개를 한꺼번에 삭제할 수도 있습니다.")
        st.code('''
                a = [1, 2, 3, 4, 5]
                del a[2:]

                print(a)
                #출력 : [1, 2]
                ''',line_numbers=True)
        st.divider()
        st.subheader(f"{idx.getSubIdx()}리스트 관련 함수")
        st.write('''
                - **append()** : 리스트에 요소 추가하기
                 ''')
        st.code('''
                a = [1, 2, 3]
                a.append(4)
                print(a)   #리스트의 맨 마지막에 4를 추가
                #출력 : [1, 2, 3, 4]
                ''',line_numbers=True)
        st.write("리스트 안에는 어떤 자료형도 추가할 수 있습니다.")
        st.code('''
                a.append([5, 6])
                print(a)   #리스트에 리스트를 추가
                #출력 : [1, 2, 3, 4, [5, 6]]
                ''',line_numbers=True)
        
        st.write('''
                - **sort()** : 리스트 정렬
                 ''')
        st.code('''
                a = [1, 4, 3, 2]
                a.sort()
                print(a)
                #출력 : [1, 2, 3, 4]
                ''',line_numbers=True)
        st.write("문자 역시 알파벳 순서로 정렬할 수 있습니다.")
        st.code('''
                a = ['a', 'c', 'b']
                a.sort()
                print(a)
                #출력 : ['a', 'b', 'c']
                ''',line_numbers=True)
        
        st.write('''
                - **reverse()** : 리스트 뒤집기
                 ''')
        st.code('''
                a = ['a', 'c', 'b']
                a.reverse()
                print(a)
                #출력 : ['b', 'c', 'a']
                ''',line_numbers=True)
        
        st.write('''
                - **index()** : 인덱스 반환
                 ''')
        st.code('''
                a = [1, 2, 3]
                print(a.index(3))     #3의 위치(인덱스) 리턴
                #출력 : 2

                print(a.index(1))     #1의 위치(인덱스) 리턴
                #출력 : 0

                print(a.index(0))     #0의 위치(인덱스) 리턴 -> 오류
                #Traceback (most recent call last):
                #    File "<stdin>", line 1, in <module>
                #ValueError: 0 is not in list
                ''',line_numbers=True)
        st.write("값 0은 a 리스트에 존재하지 않기 때문에 오류가 발생합니다.")

        st.write('''
                - **insert()** : 리스트에 요소 삽입
                 ''')
        st.code('''
                a = [1, 2, 3]
                a.insert(0, 4)      #0번째 자리에 4 삽입
                print(a)
                #출력 : [4, 1, 2, 3]

                a.insert(3, 5)      #3번째 자리에 5 삽입
                print(a)
                #출력 : [4, 1, 2, 5, 3]
                ''',line_numbers=True)
        st.write("insert(a, b)는 리스트의 a번째 위치에 b를 삽입합니다.")
        
        st.write('''
                - **remove()** : 리스트 요소 제거
                 ''')
        st.code('''
                a = [1, 2, 3, 1, 2, 3]
                a.remove(3)
                print(a)
                #출력 : [1, 2, 1, 2, 3]
                ''',line_numbers=True)
        st.write("remove(x)는 리스트에서 첫 번째로 나오는 x를 삭제하는 함수입니다. a가 3이라는 값을 2개 가지고 있을 경우, 첫 번째 3만 제거됩니다.")

        st.write('''
                - **pop()** : 리스트 요소 끄집어 내기
                 ''')
        st.code('''
                a = [1, 2, 3]
                print(a.pop())    #맨 마지막 요소를 리턴하고, 해당 요소 삭제
                #출력 : 3

                print(a)
                #출력 : [1, 2]
                ''',line_numbers=True)
        st.write("pop()은 리스트의 맨 마지막 요소를 리턴하고 그 요소는 삭제합니다. a리스트에서 3을 끄집어 내고, [1, 2]만 남게 됩니다.")
        st.code('''
                a = [1, 2, 3]
                print(a.pop(1))    #인덱스 1의 요소를 리턴하고, 해당 요소 삭제
                #출력 : 2

                print(a)
                #출력 : [1, 3]
                ''',line_numbers=True)
        st.write("pop(x)은 리스트의 x번째 요소를 리턴하고 그 요소는 삭제합니다. a리스트에서 a[1]의 값을 끄집어 내고, [1, 3]만 남게 됩니다.")
        
        st.write('''
                - **count()** : 리스트에 포함된 요소 x의 개수 세기
                 ''')
        st.code('''
                a = [1, 2, 3, 1]
                print(a.count(1))    #1이라는 값이 a에 총 2개
                #출력 : 2
                ''',line_numbers=True)
        st.write("count(x)는 리스트 안에 x가 몇 개 있는지 조사하여 그 개수를 리턴하는 함수입니다.")
        
        st.write('''
                - **extend()** : 리스트 확장
                 ''')
        st.code('''
                a = [1, 2, 3]
                a.extend([4, 5])
                print(a)
                #출력 : [1, 2, 3, 4, 5]

                b = [6, 7]
                a.extend(b)
                print(a)
                #출력 : [1, 2, 3, 4, 5, 6, 7]
                ''',line_numbers=True)
        st.write("extend(x)에서 x에는 리스트만 올 수 있으며 원래의 a 리스트에 x 리스트를 더하게 됩니다.") 
        st.divider()
        
        st.header(f"{idx.getHeadIdx()}튜플")
        st.write('''
                튜플(Tuple)은 몇 가지 점을 제외하곤 리스트와 거의 비슷하며 리스트와 다른 점은 다음과 같습니다.
                
                - 리스트는 [], 튜플은 ()으로 둘러싼다.
                - 리스트는 요솟값의 생성, 삭제, 수정이 가능하지만, 튜플은 요솟값을 바꿀 수 없다.
                 
                 ''')
        st.code('''
                #튜플 생성하기
                t1 = ()
                t2 = (1,)
                t3 = (1, 2, 3)
                t4 = 1, 2, 3
                t5 = ('a', 'b', ('ab', 'cd'))
                ''',line_numbers=True)
        st.write('''
                모습은 리스트와 거의 비슷하지만, 튜플에서는 리스트와 다른 2가지 차이점을 찾아볼 수 있습니다. t2 = (1,)처럼 단지 1개의 요소만을 가질 때는 요소 뒤에 쉼표(,)를 반드시 붙여야 한다는 것과 t4 = 1, 2, 3처럼 소괄호()를 생략해도 된다는 점입니다.
                 ''')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}튜플의 인덱싱")
        st.write("문자열, 리스트와 마찬가지로 튜플 또한 인덱싱이 가능합니다.")
        st.code('''
                t1 = (1, 2, 'a', 'b')

                print(t1[0])
                # 출력 : 1

                print(t1[3])
                # 출력 : 'b'
                ''',line_numbers=True)
        st.divider()

        st.subheader(f"{idx.getSubIdx()}튜플의 슬라이싱")
        st.code('''
                t1 = (1, 2, 'a', 'b')

                print(t1[1:])
                # 출력 : (2, 'a', 'b')
                ''',line_numbers=True)
        st.divider()

        st.subheader(f"{idx.getSubIdx()}튜플 길이 구하기")
        st.code('''
                t1 = (1, 2, 'a', 'b')
                print(len(t1))
                #출력 : 4
                ''',line_numbers=True)
        st.divider()
        
        st.header(f"{idx.getHeadIdx()}딕셔너리")
        st.write('''
                딕셔너리(dictionary)란 단어 그대로 '사전'이라는 뜻입니다. 딕셔너리의 기본 구조는 아래와 같이 **Key**와 **Value**를 한 쌍으로 가지며, 리스트나 튜플처럼 순차적으로 해당 요솟값을 구하지 않고 Key를 통해 Value를 얻는 특징을 가집니다.
        
                    {Key1: Value1, Key2: Value2, Key3: Value3, ...}
                
                ''')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}딕셔너리 생성하기")
        st.write('''
                |Key	|Value	|
                |----------|-----------|
                |name	|Alice	|
                |age	|30	|
                |city	|New York|

                표와 같은 데이터를 저장하는 딕셔너리를 아래와 같이 생성할 수 있습니다. 
                 ''')
        st.code('''
                person = {
                    "name" : "Alice",
                    "age" : 30,
                    "city" : "New York"
                }
                ''',line_numbers=True)
        
        st.write("딕셔너리는 Key - Value 로 이루어진 데이터 타입이기 때문에 리스트와 같이 인덱스를 사용해서 요소에 접근할 수 없습니다. 딕셔너리의 특정 요소에 접근하기 위해선 지정된 '키' 값을 이용해야 합니다.")
        st.code('''
                #Key를 사용해 Value 얻기
                print(person["name"])
                #출력 : Alice

                print(person["age"])
                #출력 : 30
                ''',line_numbers=True)
        st.divider()
        st.subheader(f"{idx.getSubIdx()}딕셔너리 쌍 추가, 삭제하기")
        st.code('''
                #쌍 추가하기
                person["job"] = "Chef"
                print(person)
                #출력 : {'name': 'Alice', 'age': 30, 'city': 'New York', 'job': 'Chef'}
                
                #쌍 삭제하기
                del person["city"]
                print(person)
                #출력 : {'name': 'Alice', 'age': 30, 'job': 'Chef'}
                ''',line_numbers=True)
        st.divider()

        st.subheader(f"{idx.getSubIdx()}딕셔너리 관련 함수")
        st.write('''
                - **keys()** : Key 리스트 만들기
                 ''')
        st.code('''
                print(person.keys())
                #출력 : dict_keys(['name', 'age', 'job'])
                ''',line_numbers=True)
        
        st.write('''
                - **values()** : Value 리스트 만들기
                 ''')
        st.code('''
                print(person.values())
                #출력 : dict_values(['Alice', 30, 'Chef'])
                ''',line_numbers=True)
        
        st.write('''
                - **items()** : Key, Value 쌍 얻기
                 ''')
        st.code('''
                print(person.items())
                #출력 : dict_items([('name', 'Alice'), ('age', 30), ('job', 'Chef')])
                ''',line_numbers=True)
        
        st.write('''
                - **get()** : Key로 Value 얻기
                 ''')
        st.code('''
                print(person.get("name"))
                #출력 : Alice
                ''',line_numbers=True)
        
        st.write('''
                - **in()** : 해당 Key가 딕셔너리 안에 있는지 조사하기
                 ''')
        st.code('''
                print("name" in person)
                #출력 : True

                print("birth" in person)
                #출력 : False
                ''',line_numbers=True)
        st.write('''
                - **clear()** : Key: Value 쌍 모두 지우기
                 ''')
        st.code('''
                print(person.clear())
                #출력 : None
                ''',line_numbers=True)
        st.divider()
        
        st.header(f"{idx.getHeadIdx()}집합")
        st.write("집합(set)은 집합에 관련된 것을 쉽게 처리하기 위해 만든 자료형입니다.")
        st.code('''
                #set 키워드 사용해서 집합 만들기
                s1 = set([1, 2, 3])

                s2 = set("Hello")
                print(s2)
                # 출력 : {'e', 'H', 'l', 'o'}
                ''',line_numbers=True)
        st.write('''
                's2 = set("Hello")' 결과에서 확인할 수 있듯, set에는 다음과 같은 2가지 특징이 있습니다.
                 
                 - 중복을 허용하지 않는다.
                 - 순서가 없다(Unordered).

                 set은 중복을 허용하지 않는 특징 때문에 데이터의 중복을 제거하기 위한 필터로 종종 사용됩니다. 또한, 리스트나 튜플은 순서가 있기 때문에 인덱싱을 통해 요솟값을 얻을 수 있지만, set 자료형은 순서가 없기 때문에 인덱싱을 통해 요솟값을 얻을 수 없습니다.
                 ''')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}집합의 연산")
        st.code('''
                # 연산에 사용할 2개의 set 생성
                s1 = set([1, 2, 3, 4, 5, 6])
                s2 = set([4, 5, 6, 7, 8, 9])
                ''',line_numbers=True)
        
        st.write('''
                - **교집합** : & , intersection
                 ''')
        st.code('''
                print(s1 & s2)
                #출력 : {4, 5, 6}

                print(s1.intersection(s2))
                #출력 : {4, 5, 6}
                ''',line_numbers=True)
        
        st.write('''
                - **합집합** : | , union
                 ''')
        st.code('''
                print(s1 | s2)
                #출력 : {1, 2, 3, 4, 5, 6, 7, 8, 9}

                print(s1.union(s2))
                #출력 : {1, 2, 3, 4, 5, 6, 7, 8, 9}
                ''',line_numbers=True)
        
        st.write('''
                - **차집합** : -(빼기), difference
                 ''')
        st.code('''
                print(s1 - s2)
                #출력 : {1, 2, 3}

                print(s2 - s1)
                #출력 : {8, 9, 7}

                print(s1.difference(s2))
                #출력 : {1, 2, 3}

                print(s2.difference(s1))
                #출력 : {8, 9, 7}
                ''',line_numbers=True)
        st.divider()

        st.subheader(f"{idx.getSubIdx()}집합 관련 함수")
        st.write('''
                - **add()** : 값 1개 추가하기
                 ''')
        st.code('''
                s1 = set([1, 2, 3])
                s1.add(4)
                
                print(s1)
                #출력 : {1, 2, 3, 4}
                ''',line_numbers=True)
        
        st.write('''
                - **update()** : 값 여러 개 추가하기
                 ''')
        st.code('''
                s1 = set([1, 2, 3])
                s1.update([4, 5, 6])
                
                print(s1)
                #출력 : {1, 2, 3, 4, 5, 6}
                ''',line_numbers=True)
        
        st.write('''
                - **remove()** : 특정 값 제거하기
                 ''')
        st.code('''
                s1 = set([1, 2, 3])
                s1.remove(2)
                
                print(s1)
                #출력 : {1, 3}
                ''',line_numbers=True)
        st.divider()

    elif path == ("실습 프로젝트", "날씨별 공공자전거 수요 분석"):
        st.header(f"{idx.getHeadIdx()}날씨별 공공자전거 수요 분석")
        st.write('''
                자전거 대여소는 계절과 날씨에 따라 대여 건수의 변동이 심해, 운영 비용에 큰 영향을 미치고 있습니다. 따라서 날씨 예보 정보를 활용해 대여 건수를 사전에 예측하고, 
                 운영 비용을 조정하기 위한 데이터 분석 및 시각화 실습을 진행합니다.
                 ''')
        st.divider()


        st.subheader(f"{idx.getSubIdx()}데이터 준비")
        st.write('- 실습을 위해 **아래의 버튼**을 클릭하여 데이터를 다운로드해 주세요')
        with open('data/실습03.zip', "rb") as template_file:
            template_zip = template_file.read()
        st.download_button(label="download data",
                            type="primary",
                            data=template_zip,
                           file_name = "실습03.zip"
        )
        st.write('해당 파일의 압축을 풀고, **실습03** 폴더를 :blue-background[./data/**실습03**/]경로로 옮겨주세요.')
        st.code('''
                .
                ├─ 현재작업파일.ipynb
                ├─ 📁data
                │   └─📁실습03
                │       ├─ 공공자전거이용정보0.csv
                │       ├─         ...
                ''', language="text")
        st.divider()


        st.subheader(f"{idx.getSubIdx()}패키지 설치 및 호출")
        st.write('''
                CMD 창을 열고 아래의 패키지들을 설치해 줍니다. 
                 ''')
        st.code('''
                $ pip install pandas
                ''', language="text")
        st.code('''
                $ pip install seaborn
                ''', language="text")
        st.code('''
                $ pip install matplotlib
                ''', language="text")
        
        st.write("다시 작업 파일(.ipynb)로 돌아와서, 설치한 패키지들을 호출해 줍니다.")
        st.code('''
                import pandas as pd
                import seaborn as sns
                import matplotlib.pyplot as plt
                ''')
        st.divider()


        st.subheader(f"{idx.getSubIdx()}데이터 불러오기")
        st.write("실습에 필요한 데이터를 불러오겠습니다.")
        st.code('''
                # 기상관측자료 데이터
                weather_info = pd.read_csv('data/실습03/기상관측자료202306.csv', encoding='cp949')

                #자전거 이용정보 데이터
                files = [
                    "data/실습03/공공자전거이용정보0.csv",
                    "data/실습03/공공자전거이용정보1.csv",
                    "data/실습03/공공자전거이용정보2.csv",
                    "data/실습03/공공자전거이용정보3.csv",
                    "data/실습03/공공자전거이용정보4.csv",
                    "data/실습03/공공자전거이용정보5.csv"
                ]

                #파일 병합
                bike_info = pd.concat([pd.read_csv(file, encoding='cp949') for file in files], ignore_index=True)
                ''', line_numbers=True)
        
        import numpy as np
        import pandas as pd
        import seaborn as sns
        import matplotlib.pyplot as plt
        import io
        # 기상관측자료 데이터
        weather_info = pd.read_csv('data/실습03/기상관측자료202306.csv', encoding='cp949')

        #자전거 이용정보 데이터
        files = [
            "data/실습03/공공자전거이용정보0.csv",
            "data/실습03/공공자전거이용정보1.csv",
            "data/실습03/공공자전거이용정보2.csv",
            "data/실습03/공공자전거이용정보3.csv",
            "data/실습03/공공자전거이용정보4.csv",
            "data/실습03/공공자전거이용정보5.csv"
        ]

        #파일 병합
        bike_info = pd.concat([pd.read_csv(file, encoding='cp949') for file in files], ignore_index=True)
        st.write("**weather_info**")
        st.code('''weather_info.sample(5)''', line_numbers=True)
        st.write(weather_info.sample(5))
        
        st.write("**bike_info**")
        st.code('''bike_info.sample(5)''', line_numbers=True)
        st.write(bike_info.sample(5))
        st.divider()
        

        st.header(f"{idx.getHeadIdx()}공공자전거 데이터 전처리")
        st.subheader(f"{idx.getSubIdx()}집계 데이터 생성")
        st.write('''날씨 정보와의 결합에 필요한 데이터(**이용건수**)를 생성하기 위해 **대여일자**, **대여시간**으로 집계해 줍니다.''')
        st.code('''
                #공공자전거 집계 데이터 생성
                bike_df2 = bike_info.groupby(['대여일자', '대여시간'])['이용건수'].sum()
                bike_df2 = bike_df2.reset_index() #인덱스 재 정렬 , 기존 인덱스를 열로

                bike_df2.sample(5)
                ''', line_numbers=True)
        bike_df2 = bike_info.groupby(['대여일자', '대여시간'])['이용건수'].sum()
        bike_df2 = bike_df2.reset_index() #인덱스 재 정렬 , 기존 인덱스를 열로
        st.write(bike_df2.sample(5))
        st.divider()


        st.subheader(f"{idx.getSubIdx()}파생변수 생성")
        st.write('''대여일자에서 **년도, 월, 일, 요일, 공휴일** 변수를 생성합니다.''')
        st.code('''
                #공공자전거 파생변수 생성
                bike_df2['대여일자'] = pd.to_datetime(bike_df2['대여일자'])
                bike_df2['년도'] = bike_df2['대여일자'].dt.year
                bike_df2['월'] = bike_df2['대여일자'].dt.month
                bike_df2['일'] = bike_df2['대여일자'].dt.day
                bike_df2['요일(num)'] = bike_df2['대여일자'].dt.dayofweek
                bike_df2['공휴일'] = 0  #0: 평일 1: 공휴일

                # 토요일, 일요일을 공휴일로 설정
                bike_df2.loc[bike_df2['요일(num)'].isin([5,6]),['공휴일']] = 1
                bike_df2.sample(5)
                ''',line_numbers=True)
        
        bike_df2['대여일자'] = pd.to_datetime(bike_df2['대여일자'])
        bike_df2['년도'] = bike_df2['대여일자'].dt.year
        bike_df2['월'] = bike_df2['대여일자'].dt.month
        bike_df2['일'] = bike_df2['대여일자'].dt.day
        bike_df2['요일(num)'] = bike_df2['대여일자'].dt.dayofweek
        bike_df2['공휴일'] = 0  #0: 평일 1: 공휴일

        # 토요일, 일요일을 공휴일로 설정
        bike_df2.loc[bike_df2['요일(num)'].isin([5,6]),['공휴일']] = 1
        st.write(bike_df2.sample(5))
        st.divider()


        st.header(f"{idx.getHeadIdx()}날씨 데이터 전처리")
        st.subheader(f"{idx.getSubIdx()}날짜, 시간 컬럼 생성")
        st.write('''자전거 이용정보와의 결합을 위해 **일시** 칼럼에서 **날짜**와 **시간** 정보를 추출합니다.''')
        st.code('''
                #날씨 데이터 전처리
                weather_info['날짜'] = weather_info['일시'].str[:10]
                weather_info['시간'] = weather_info['일시'].str[11:13].astype(int)

                weather_info.info()
                ''',line_numbers=True)
        
        weather_info['날짜'] = weather_info['일시'].str[:10]
        weather_info['시간'] = weather_info['일시'].str[11:13].astype(int)

        #weather_info.info() 출력 코드
        buffer = io.StringIO()
        weather_info.info(buf=buffer)
        st.text(buffer.getvalue())
        st.divider()


        st.subheader(f"{idx.getSubIdx()}컬럼 선택")
        st.write("분석에 사용할 컬럼을 순서대로 가져와서 새 데이터 프레임을 생성합니다.")
        st.code('''
                weather_df = weather_info[['날짜', '시간', '기온(°C)', '강수량(mm)', '풍속(m/s)', '풍향(16방위)', '습도(%)','일조(hr)','일사(MJ/m2)', '적설(cm)','전운량(10분위)', '지면온도(°C)']]

                #칼럼명 변경
                weather_df.columns = ['날짜', '시간', '기온', '강수량(mm)', '풍속(m/s)', '풍향(16방위)', '습도(%)','일조','일사', '적설(cm)','전운량',  '지면온도']
                weather_df.columns
                ''',line_numbers=True)
        
        weather_df = weather_info[['날짜', '시간', '기온(°C)', '강수량(mm)', '풍속(m/s)', '풍향(16방위)', '습도(%)','일조(hr)','일사(MJ/m2)', '적설(cm)','전운량(10분위)', '지면온도(°C)']]

        #칼럼명 변경
        weather_df.columns = ['날짜', '시간', '기온', '강수량(mm)', '풍속(m/s)', '풍향(16방위)', '습도(%)','일조','일사', '적설(cm)','전운량',  '지면온도']
        st.write(weather_df.columns)
        st.divider()
        

        st.subheader(f"{idx.getSubIdx()}결측치 확인")
        st.code('''
                #결측치 확인
                weather_df.isnull().sum()
                ''',line_numbers=True)
        st.write(weather_df.isnull().sum())
        st.write('''
                **강수량, 적설, 일조, 일사**와 같이 NaN값이 0인 경우는 0으로 fill 해줍니다. **전운량, 기온, 지면온도, 풍향, 풍속**은 같은 일자의 이전 시간대의 데이터로 대체합니다.
                ''')
        
        st.write('''
                - NaN 값을 0으로 fill (fillna)
                 ''')
        st.code('''
                # NaN 값을 0으로 fill (fillna)
                weather_df.loc[:, '강수량(mm)'] = weather_df['강수량(mm)'].fillna(0)
                weather_df.loc[:, '적설(cm)'] = weather_df['적설(cm)'].fillna(0)
                weather_df.loc[:, '일조'] = weather_df['일조'].fillna(0)
                weather_df.loc[:, '일사'] = weather_df['일사'].fillna(0)
                ''',line_numbers=True)
        weather_df.loc[:, '강수량(mm)'] = weather_df['강수량(mm)'].fillna(0)
        weather_df.loc[:, '적설(cm)'] = weather_df['적설(cm)'].fillna(0)
        weather_df.loc[:, '일조'] = weather_df['일조'].fillna(0)
        weather_df.loc[:, '일사'] = weather_df['일사'].fillna(0)

        st.write('''
                - NaN 값을 직전 데이터의 값으로 fill (ffill)
                 ''')
        st.code('''
                # NaN 값을 직전 데이터의 값으로 fill (ffill)
                # 날짜 시간으로 정렬
                weather_df = weather_df.sort_values(['날짜','시간'])

                # 전 값으로 
                weather_df['기온'] = weather_df['기온'].ffill()
                weather_df['풍속(m/s)']= weather_df['풍속(m/s)'].ffill()
                weather_df['풍향(16방위)'] = weather_df['풍향(16방위)'].ffill()
                weather_df['전운량'] = weather_df['전운량'].ffill()
                weather_df['지면온도'] = weather_df['지면온도'].ffill()
                ''',line_numbers=True)
        weather_df = weather_df.sort_values(['날짜','시간'])
        weather_df['기온'] = weather_df['기온'].ffill()
        weather_df['풍속(m/s)']= weather_df['풍속(m/s)'].ffill()
        weather_df['풍향(16방위)'] = weather_df['풍향(16방위)'].ffill()
        weather_df['전운량'] = weather_df['전운량'].ffill()
        weather_df['지면온도'] = weather_df['지면온도'].ffill()
        
        st.write("결측치를 제거한 결과를 확인해 보겠습니다.")
        st.code('''
                #결측치 제거 확인
                weather_df.isnull().sum()
                ''',line_numbers=True)
        st.write(weather_df.isnull().sum())
        st.divider()


        st.header(f"{idx.getHeadIdx()}데이터 결합")
        st.write("전처리된 공공자전거 데이터와 날씨 데이터를 결합해 날씨별 자전거 대여 데이터를 만들어보겠습니다.")
        st.code('''
                #데이터 결합
                weather_df['날짜'] = pd.to_datetime(weather_df['날짜'])

                #데이터 타입 맞추기 
                bike_mg = pd.merge (bike_df2, 
                                    weather_df, 
                                    left_on =['대여일자', '대여시간'], 
                                    right_on = ['날짜', '시간']) #default = inner 
                bike_mg.head()
                ''',line_numbers=True)
        weather_df['날짜'] = pd.to_datetime(weather_df['날짜'])
        bike_mg = pd.merge (bike_df2, 
                            weather_df, 
                            left_on =['대여일자', '대여시간'], 
                            right_on = ['날짜', '시간']) #default = inner 
        st.write(bike_mg.head())

        st.write("**대여일자, 날짜, 시간** 데이터가 중복되는 것을 확인할 수 있습니다. 중복되는 데이터를 제거해 보겠습니다.")
        st.code('''
                #중복데이터 제거
                bike_mg = bike_mg.drop(['대여일자', '날짜', '시간'], axis = 1)

                bike_mg.head()
                ''',line_numbers=True)
        bike_mg = bike_mg.drop(['대여일자', '날짜', '시간'], axis = 1)
        st.write(bike_mg.head())
        st.divider()


        st.header(f"{idx.getHeadIdx()}데이터 시각화")
        st.write("원본 데이터프레임을 보존하기 위해 복사본을 생성한 후 시각화를 진행하겠습니다.")
        st.code('''
                #복사본 생성
                data = bike_mg.copy()
                ''',line_numbers=True)
        data = bike_mg.copy()

        st.write("그래프를 그리기에 앞서, 한글 출력을 위한 폰트 설정을 해줍니다.")
        st.code('''
                #한글 표시
                plt.rcParams['font.family'] = 'NanumGothic'
                plt.rc('font', family='NanumGothic')
                ''', line_numbers=True)
        st.divider()


        st.subheader(f"{idx.getSubIdx()}데이터 요약 통계")
        st.write("데이터의 요약 통계를 확인해 정상적인 값인지 확인해 보겠습니다.")
        st.code('''
                #데이터 요약 통계
                desc_df = data.describe().T
                desc_df
                ''',line_numbers=True)
        desc_df = data.describe().T
        st.write(desc_df)
        st.divider()


        st.subheader(f"{idx.getSubIdx()}이용건수 분포 시각화")
        st.code('''
                sns.histplot(data['이용건수'])

                plt.show()
                ''',line_numbers=True)

        fig, ax = plt.subplots()
        sns.histplot(data['이용건수'], ax=ax)
        ax.set_title("이용건수 분포", fontproperties=prop)
        ax.set_xlabel("이용건수", fontproperties=prop)
        st.pyplot(fig)
        plt.close(fig)
        st.code('''
                sns.lineplot(x=data['일'], y=data['이용건수'])

                plt.show()
                ''',line_numbers=True)
        fig, ax = plt.subplots()
        sns.lineplot(x=data['일'], y=data['이용건수'], ax=ax)
        ax.set_xlabel("일", fontproperties=prop)
        ax.set_ylabel("이용 건수", fontproperties=prop)
        st.pyplot(fig)
        plt.close(fig)
        st.divider()

        
        st.subheader(f"{idx.getSubIdx()}피처의 분포 시각화")
        st.write("원하는 컬럼을 선택해 피처의 분포를 확인합니다.")
        st.code('''
                #컬럼 선택
                con_cols = ["기온", "강수량(mm)", "풍속(m/s)", "습도(%)", "일조"]
                ''',line_numbers=True)
        con_cols = ["기온", "강수량(mm)", "풍속(m/s)", "습도(%)", "일조"]
        
        
        st.write("선택된 칼럼에 대한 피처의 분포를 시각화합니다.")
        st.code('''
                #피처의 분포 시각화
                fig, axes = plt.subplots(1,5, figsize = (20, 4))
                ax = axes.flatten()
                
                # axes = (n,n)형태 / ax = m형태
                for i, col in enumerate(con_cols):
                    sns.histplot(data = data, x = col, ax = ax[i])

                plt.show()
                ''',line_numbers=True)
        
        fig, axes = plt.subplots(1,5, figsize = (20, 4))
        ax = axes.flatten()
        # axes = (n,n)형태 / ax = m형태
        for i, col in enumerate(con_cols):
            sns.histplot(data = data, x = col, ax = ax[i])
            ax[i].set_xlabel(col, fontproperties=prop)
        
        st.pyplot(fig)
        plt.close(fig)
        st.divider()


        st.subheader(f"{idx.getSubIdx()}이용건수와 피처와의 관계")
        st.write("공공자전거 이용 건수와 피처와의 관계를 시각화합니다.")
        st.code('''
                fig, axes = plt.subplots(2,2, figsize = (20,8))
                
                sns.barplot(data = data, x = '일', y= '이용건수', ax = axes[0,0])
                sns.barplot(data = data, x = '공휴일', y= '이용건수', ax = axes[0,1])
                sns.lineplot(data = data, x = '기온', y= '이용건수', ax = axes[1,0])
                sns.lineplot(data = data, x = '강수량(mm)', y= '이용건수', ax = axes[1,1])

                #제목 설정 
                axes[0,0].set_title('일별 이용건수')
                axes[0,1].set_title('공휴일여부에 따른 이용건수')
                axes[1,0].set_title('기온별 이용건수')
                axes[1,1].set_title('강수량(mm)별 이용건수')

                # 간격조정
                fig.subplots_adjust(hspace = 0.4)

                plt.show()
                ''',line_numbers=True)
        
        fig, axes = plt.subplots(2,2, figsize = (20,8))
                
        sns.barplot(data = data, x = '일', y= '이용건수', ax = axes[0,0])
        sns.barplot(data = data, x = '공휴일', y= '이용건수', ax = axes[0,1])
        sns.lineplot(data = data, x = '기온', y= '이용건수', ax = axes[1,0])
        sns.lineplot(data = data, x = '강수량(mm)', y= '이용건수', ax = axes[1,1])

        #제목 설정 
        axes[0,0].set_title('일별 이용건수', fontproperties=prop)
        axes[0,0].set_xlabel("일", fontproperties=prop)
        axes[0,0].set_ylabel("이용건수", fontproperties=prop)
        
        axes[0,1].set_title('공휴일여부에 따른 이용건수', fontproperties=prop)
        axes[0,1].set_xlabel("공휴일", fontproperties=prop)
        axes[0,1].set_ylabel("이용건수", fontproperties=prop)
        
        axes[1,0].set_title('기온별 이용건수', fontproperties=prop)
        axes[1,0].set_xlabel("기온", fontproperties=prop)
        axes[1,0].set_ylabel("이용건수", fontproperties=prop)
        
        axes[1,1].set_title('강수량(mm)별 이용건수', fontproperties=prop)
        axes[1,1].set_xlabel("강수량(mm)", fontproperties=prop)
        axes[1,1].set_ylabel("이용건수", fontproperties=prop)

        # 간격조정
        fig.subplots_adjust(hspace = 0.4)
        st.pyplot(fig)
        plt.close(fig)
        st.write('''
                - 공휴일 이용건수보다 평일 이용건수가 더 많습니다.
                - 기온이 높을수록 이용건수가 증가하는 경향을 보입니다.
                - 강수량이 적을수록 이용건수가 높습니다.
                ''')
        st.divider()


        st.subheader(f"{idx.getSubIdx()}평일과 공휴일 이용건수 차이")
        st.code('''
                sns.pointplot(x='대여시간', y='이용건수',data = data, hue = '공휴일')
            
                plt.show()
                ''',line_numbers=True)
        fig, ax = plt.subplots()
        sns.pointplot(x='대여시간', y='이용건수',data = data, hue = '공휴일', ax=ax)
        ax.set_xlabel("대여시간", fontproperties=prop)
        ax.set_ylabel("이용건수", fontproperties=prop)
        
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, title='공휴일', title_fontproperties=prop, prop=prop)

        st.pyplot(fig)
        plt.close(fig)
        st.write('''평일과 공휴일에는 완전히 다른 이용 현황을 보이는 것을 확인할 수 있습니다.
                 평일의 경우 오전 8시, 오후 6시에 이용건수 피크를 보이는데, 출퇴근으로 인한 영향으로 추측해 볼 수 있겠습니다.
                 ''')
        st.divider()


        st.subheader(f"{idx.getSubIdx()}요일에 따른 이용건수 차이")
        st.code('''
                sns.pointplot(x='대여시간', y='이용건수',data = data, hue = '요일(num)')

                plt.show()
                ''',line_numbers=True)
        fig, ax = plt.subplots()
        sns.pointplot(x='대여시간', y='이용건수',data = data, hue = '요일(num)', ax=ax)
        ax.set_xlabel("대여시간", fontproperties=prop)
        ax.set_ylabel("이용건수", fontproperties=prop)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, title='요일(num)', title_fontproperties=prop, prop=prop)
       

        st.pyplot(fig)
        plt.close(fig)
        st.write("토요일에 이용건수가 더 많고, 토요일 오후에 전반적으로 이용률이 높은 모습을 보입니다.")
        st.divider()


        st.subheader(f"{idx.getSubIdx()}요일에 따른 이용건수 차이(box)")
        st.code('''
                sns.boxplot(x='요일(num)', y='이용건수',data = data)
                dofw = list('월화수목금토일')
                plt.xticks([0,1,2,3,4,5,6],dofw)
                
                plt.show()
                ''',line_numbers=True)
        fig, ax = plt.subplots()
        sns.boxplot(x='요일(num)', y='이용건수',data = data, ax=ax)
        dofw = list('월화수목금토일')
        plt.xticks([0,1,2,3,4,5,6],dofw, fontproperties=prop)
        ax.set_xlabel("요일(num)", fontproperties=prop)
        ax.set_ylabel("이용건수", fontproperties=prop)
        
        st.pyplot(fig)
        plt.close(fig)
        st.write("공휴일은 상대적으로 변동성이 적고, 평일은 변동성이 큰 편입니다.")
        st.divider()
        
        
        st.header(f"{idx.getHeadIdx()}결론 도출")
        st.subheader(f"{idx.getSubIdx()}시간대 및 공휴일 여부에 따른 특성")
        st.write('''
                - 공공자전거 이용이 가장 많은 시간대는 **평일 오후 6시**입니다.
                - 두 번째로 이용이 많은 시간대는 **평일 오전 8시**입니다.
                - 공휴일에는 **오후 2시에서 5시 사이**에 이용이 가장 많습니다.
                - **평일 이용건수**가 공휴일 이용건수보다 **더 많습니다**.
                - 평일에는 **출퇴근 시간**에 뚜렷한 이용 피크가 나타납니다.
                - 공휴일에는 **오전부터 오후까지 완만한 이용 패턴**을 보입니다.
                ''')
        st.subheader(f"{idx.getSubIdx()}날씨와 이용건수의 상관관계")
        st.write('''
                - 기온이 적정할 때 이용건수가 **증가**하는 경향을 보입니다.
                - 강수량이 증가할수록 이용건수가 **감소**하는 추세를 보입니다.
                - 습도, 풍속, 일조량도 이용건수에 **영향**을 미치는 것으로 보입니다.
                ''')
        st.divider()
        
    else :
        st.error("Content Not Found !")

def goback_btn() :
    float_init()
    button_container = st.container()
    with button_container:
         st.button("돌아가기", on_click=update_session_state, args=('go_back',), type="primary")
    button_container.float(float_css_helper(width="2.2rem", right="5rem",bottom="1rem"))

def main() :
    visitors = db_init()
    page, topic, chapter = init_session_state()
    
    if page == 'page_topic':
        show_topic(topic)
    elif page == 'page_chapter':
        goback_btn()
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
        
        st.markdown(
                    f"""
                    <div style="position: relative; height: 1rem;">
                            <div style="position: absolute; right: 0rem; bottom: 0rem; color: gray;">
                            {visitors} views
                            </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                    )
        st.write(get_ip())
        st.markdown(f"remote {get_remote_ip()}")
        st.markdown(f"forwarded {get_forwarded_ip()}")
if __name__ == "__main__":
    main()
    
