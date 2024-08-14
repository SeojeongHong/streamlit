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
                         "Grid, Annotate", "Plot", "막대 그래프", "Pie chart, 3D plot"],
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
                ''')
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
                ''')
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
                ''')
        st.divider()
        st.subheader(f"{idx.getSubIdx()}문자열 길이 구하기")
        st.write("문자열의 길이는 다음과 같이 len 함수를 사용하면 구할 수 있습니다.")
        st.code('''
                a = "Life is too short"
                print(len(a))
                #출력 : 17
                ''')
        st.divider()
        
        st.subheader(f"{idx.getSubIdx()}문자열 인덱싱")
        st.write("인덱싱이란 문자열에서 문자를 추출하는 것입니다. 문자열의 문자에 접급하기 위해서 '문자열[인덱스]' 형식으로 접든할 수 있습니다. 이때 인덱스는 0부터 시작합니다.")
        st.code('''
                str = "Hello World"
                
                print(str[0])   #출력 : H
                print(str[3])   #출력 : l
                print(str[-1])   #출력 : d
                print(str[-5])   #출력 : W
                ''')
        st.write("인덱스의 (-) 는 문자열을 뒤에서부터 읽기 위해 사용합니다. 즉, str[-1]은 뒤에서 첫 번째가 되는 문자를 의미하며, str[-5]는 뒤에서 5번째 문자를 의미합니다.")
        st.divider()

        st.subheader(f"{idx.getSubIdx()}문자열 슬라이싱")
        st.write('''슬라이싱은 문자열의 일부분을 추출하는 것입니다. 문자열의 슬라이싱은 아래와 같은 형식으로 수행할 수 있습니다.
                 
                        문자열[start : end : step]
                
start는 시작 인덱스, end는 끝 인덱스, step은 슬라이싱 간격을 의미합니다. step의 기본 값은 1으로 생략 가능합니다.
                 ''')
        st.code('''
                str = "Life is too short, You need Python"
                print(str[0:4])
                # 출력 : Life
                ''')
        
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
                ''')
        st.divider()
        st.subheader(f"{idx.getSubIdx()}문자열 관련 함수")
        st.write('''
                - **count()** : 문자 개수 세기
                 ''')
        st.code('''
                a = "hobby"
                print( a.count('b') )   #문자열 중 문자 b의 개수 리턴
                #출력 : 2
                ''')
        
        st.write('''
                - **find()** : 위치 알려 주기1
                 ''')
        st.code('''
                a = "Python is the best choice"
                print( a.find('b') )   #문자열 중 문자 b가 처음으로 나온 위치 리턴
                #출력 : 14

                print( a.find('k') )   #찾는 문자나 문자열이 존재하지 않는다면 -1을 리턴
                #출력 : -1
                ''')
        
        st.write('''
                - **index()** : 위치 알려 주기2
                 ''')
        st.code('''
                a = "Life is too short"
                print( a.index('t') )   #문자열 중 문자 t가 맨 처음으로 나온 위치를 리턴
                #출력 : 8

                print( a.index('k') )   #찾는 문자나 문자열이 존재하지 않는다면 오류 발생
                #Traceback (most recent call last):
                #File "<stdin>", line 1, in <module>
                #ValueError: substring not found
                ''')
        
        st.write('''
                - **join()** : 문자열 삽입
                 ''')
        st.code('''
                print( ",".join('abcd') )   #abcd 문자열의 각각의 문자 사이에 ‘,’를 삽입
                #출력 : a,b,c,d
                ''')
        
        st.write('''
                - **upper()** : 소문자를 대문자로 바꾸기
                 ''')
        st.code('''
                a = "hi"
                print( a.upper() )
                #출력 : 'HI'
                ''')
        
        st.write('''
                - **lower()** : 대문자를 소문자로 바꾸기
                 ''')
        st.code('''
                a = "HELLO"
                print( a.lower() )
                #출력 : 'hello'
                ''')
        
        st.write('''
                - **lstrip()** : 왼쪽 공백 지우기
                 ''')
        st.code('''
                a = "  hi  "
                print( a.lstrip() )
                #출력 : 'hi  '
                ''')
        
        st.write('''
                - **rstrip()** : 오른쪽 공백 지우기
                 ''')
        st.code('''
                a = "  hi  "
                print( a.lstrip() )
                #출력 : '  hi'
                ''')
        
        st.write('''
                - **strip()** : 양쪽 공백 지우기
                 ''')
        st.code('''
                a = "  hi  "
                print( a.lstrip() )
                #출력 : 'hi'
                ''')
        
        st.write('''
                - **replace()** : 문자열 바꾸기
                 ''')
        st.code('''
                a = "Good mornig"
                print( a.replace("mornig", "evening") )  #replace(바뀔_문자열, 바꿀_문자열)
                #출력 : Good evening
                ''')
        st.write("replace 함수는 eplace(바뀔_문자열, 바꿀_문자열)처럼 사용해서 문자열 안의 특정한 값을 다른 값으로 치환해 줍니다.")
        st.write('''
                - **split()** : 문자열 나누기
                 ''')
        st.code('''
                a = "Life is too short"
                print( a.split() )
                #출력 : ['Life', 'is', 'too', 'short']

                b = "a:b:c:d"
                print( b.split(':') )
                #출력 : ['a', 'b', 'c', 'd']
                ''')
        st.write("split 함수는 a.split()처럼 괄호 안에 아무 값도 넣어 주지 않으면 공백([Space], [Tab], [Enter])을 기준으로 문자열을 나누어 줍니다. 만약 b.split(':')처럼 괄호 안에 특정 값이 있을 경우에는 괄호 안의 값을 구분자로 해서 문자열을 나누어 줍니다.")    
        st.divider()
        
        st.header(f"{idx.getHeadIdx()}불")
        st.write('''
                불(bool)이란 참(True)과 거짓(False)을 나타내는 자료형입니다. 불 자료형은 다음 2가지 값만을 가질 수 있습니다.

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
                ''')
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
        st.write("리스트는 데이터들을 편리하게 관리하기 위해 묶어서 관리하는 자료형 중의 하나 입니다. 리스트 안에는 어떠한 자료형도 포함할 수 있습니다.")
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
                ''')
        st.divider()
        st.subheader(f"{idx.getSubIdx()}리스트의 인덱싱")
        st.write("리스트 역시 문자열처럼 인덱싱을 적용할 수 있습니다.")
        st.code('''
                a = [1, 2, 3]

                print( a[0] )
                #출력 : 1

                print( a[0] + a[2] )
                #출력 : 4

                print( a[-1] )
                #출력 : 3
                ''')
        
        st.write("리스트 안에 리스트가 있는 경우에도 인덱싱이 가능합니다.")
        st.code('''
                a = [1, 2, 3, ['a', 'b', 'c']]

                print( a[0] )
                #출력 : 1

                print( a[-1] )
                #출력 : ['a', 'b', 'c']

                print( a[-1][1] )
                #출력 : 'b'
                ''')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}리스트의 슬라이싱")
        st.write("문자열과 마찬가지로 리스트에서도 슬라이싱 기법을 적용할 수 있습니다.")
        st.code('''
                a = [1, 2, 3, 4, 5]
                print( a[0:2])
                #출력 : [1, 2]

                print(a[:2])
                #출력 : [1, 2]

                print(a[2:])
                #출력 : [3, 4, 5]
                ''')
        st.divider()
        st.subheader(f"{idx.getSubIdx()}리스트 길이 구하기")
        st.write("리스트 길이를 구하기 위해서는 다음처럼 len 함수를 사용해야 합니다.")
        st.code('''
                a = [1, 2, 3]
                print(len(a))
                #출력 : 3
                ''')
        st.write("len은 문자열, 리스트 외에 앞으로 배울 튜플과 딕셔너리에도 사용할 수 있는 함수입니다.")
        
        st.divider()
        st.subheader(f"{idx.getSubIdx()}리스트 값 수정하기")
        st.write("리스트의 인덱스를 통해 요소에 접근하고 값을 수정할 수 있습니다.")
        st.code('''
                a = [1, 2, 3]
                a[2] = 4

                print(a)
                #출력 : [1, 2, 4]
                ''')
        st.divider()
        st.subheader(f"{idx.getSubIdx()}리스트 요소 삭제하기")
        st.write("del 함수를 사용해 리스트의 요소를 삭제할 수 있습니다. 삭제 또한 인덱스를 통해 요소에 접근합니다.")
        st.code('''
                a = [1, 2, 3]
                del a[1]

                print(a)
                #출력 : [1, 3]
                ''')
        st.write("다음처럼 슬라이싱 기법을 사용하여 리스트의 요소 여러 개를 한꺼번에 삭제할 수도 있습니다.")
        st.code('''
                a = [1, 2, 3, 4, 5]
                del a[2:]

                print(a)
                #출력 : [1, 2]
                ''')
        st.divider()
        st.subheader(f"{idx.getSubIdx()}리스트 관련 함수")
        st.write('''
                - **append()** : 리스트에 요소 추가하기
                 ''')
        st.code('''
                a = [1, 2, 3]
                a.append(4)
                print( a )   #리스트의 맨 마지막에 4를 추가
                #출력 : [1, 2, 3, 4]
                ''')
        st.write("리스트 안에는 어떤 자료형도 추가할 수 있습니다.")
        st.code('''
                a.append([5, 6])
                print( a )   #리스트에 리스트를 추가
                #출력 : [1, 2, 3, 4, [5, 6]]
                ''')
        
        st.write('''
                - **sort()** : 리스트 정렬
                 ''')
        st.code('''
                a = [1, 4, 3, 2]
                a.sort()
                print( a )
                #출력 : [1, 2, 3, 4]
                ''')
        st.write("문자 역시 알파벳 순서로 정렬할 수 있습니다.")
        st.code('''
                a = ['a', 'c', 'b']
                a.sort()
                print( a )
                #출력 : ['a', 'b', 'c']
                ''')
        
        st.write('''
                - **reverse()** : 리스트 뒤집기
                 ''')
        st.code('''
                a = ['a', 'c', 'b']
                a.reverse()
                print( a )
                #출력 : ['b', 'c', 'a']
                ''')
        
        st.write('''
                - **index()** : 인덱스 반환
                 ''')
        st.code('''
                a = [1, 2, 3]
                print( a.index(3) )     #3의 위치(인덱스) 리턴
                #출력 : 2

                print( a.index(1) )     #1의 위치(인덱스) 리턴
                #출력 : 0

                print( a.index(0) )     #0의 위치(인덱스) 리턴 -> 오류
                #Traceback (most recent call last):
                #    File "<stdin>", line 1, in <module>
                #ValueError: 0 is not in list
                ''')
        st.write("값 0은 a 리스트에 존재하지 않기 때문에 오류가 발생합니다.")

        st.write('''
                - **insert()** : 리스트에 요소 삽입
                 ''')
        st.code('''
                a = [1, 2, 3]
                a.insert(0, 4)      #0번째 자리에 4 삽입
                print( a )
                #출력 : [4, 1, 2, 3]

                a.insert(3, 5)      #3번째 자리에 5 삽입
                print( a )
                #출력 : [4, 1, 2, 5, 3]
                ''')
        st.write("insert(a, b)는 리스트의 a번째 위치에 b를 삽입합니다.")
        
        st.write('''
                - **remove()** : 리스트 요소 제거
                 ''')
        st.code('''
                a = [1, 2, 3, 1, 2, 3]
                a.remove(3)
                print( a )
                #출력 : [1, 2, 1, 2, 3]
                ''')
        st.write("remove(x)는 리스트에서 첫 번째로 나오는 x를 삭제하는 함수입니다. a가 3이라는 값을 2개 가지고 있을 경우, 첫 번째 3만 제거됩니다.")

        st.write('''
                - **pop()** : 리스트 요소 끄집어 내기
                 ''')
        st.code('''
                a = [1, 2, 3]
                print( a.pop() )    #맨 마지막 요소를 리턴하고, 해당 요소 삭제
                #출력 : 3

                print( a )
                #출력 : [1, 2]
                ''')
        st.write("pop()은 리스트의 맨 마지막 요소를 리턴하고 그 요소는 삭제합니다. a리스트에서 3을 끄집어 내고, [1, 2]만 남게 됩니다.")
        st.code('''
                a = [1, 2, 3]
                print( a.pop(1) )    #인덱스 1의 요소를 리턴하고, 해당 요소 삭제
                #출력 : 2

                print( a )
                #출력 : [1, 3]
                ''')
        st.write("pop(x)은 리스트의 x번째 요소를 리턴하고 그 요소는 삭제합니다. a리스트에서 a[1]의 값을 끄집어 내고, [1, 3]만 남게 됩니다.")
        
        st.write('''
                - **count()** : 리스트에 포함된 요소 x의 개수 세기
                 ''')
        st.code('''
                a = [1, 2, 3, 1]
                print( a.count(1) )    #1이라는 값이 a에 총 2개
                #출력 : 2
                ''')
        st.write("count(x)는 리스트 안에 x가 몇 개 있는지 조사하여 그 개수를 리턴하는 함수입니다.")
        
        st.write('''
                - **extend()** : 리스트 확장
                 ''')
        st.code('''
                a = [1, 2, 3]
                a.extend([4, 5])
                print( a )
                #출력 : [1, 2, 3, 4, 5]

                b = [6, 7]
                a.extend(b)
                print(a)
                #출력 : [1, 2, 3, 4, 5, 6, 7]
                ''')
        st.write("extend(x)에서 x에는 리스트만 올 수 있으며 원래의 a 리스트에 x 리스트를 더하게 됩니다.") 
        st.divider()
        
        st.header(f"{idx.getHeadIdx()}튜플")
        st.write('''
                튜플(Tuple)은 몇 가지 점을 재외하곤 리스트와 거의 비슷하며 리스트와 다른 점은 다름과 같습니다.
                
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
                ''')
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
                ''')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}튜플의 슬라이싱")
        st.code('''
                t1 = (1, 2, 'a', 'b')

                print(t1[1:])
                # 출력 : (2, 'a', 'b')
                ''')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}튜플 길이 구하기")
        st.code('''
                t1 = (1, 2, 'a', 'b')
                print(len(t1))
                #출력 : 4
                ''')   
        st.divider()
        
        st.header(f"{idx.getHeadIdx()}딕셔너리")
        st.write('''
                딕셔너리(dictionary)란 단어 그대로 '사전'이라는 뜻입니다. 딕셔너리의 기본 구조는 아래와 같이 Key와 Value를 한 쌍으로 가지며, 리스트나 튜플처럼 순차적으로 해당 요솟값을 구하지 않고 Key를 통해 Value를 얻는 특징을 가집니다.
        
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
                ''')
        
        st.write("딕셔너리는 Key - Value 로 이루어진 데이터 타입이기 때문에 리스트와 같이 인덱스를 사용해서 요소에 접근할 수 없습니다. 딕셔너리의 특정 요소에 접근하기 위해선 지정된 '키' 값을 이용해야 합니다.")
        st.code('''
                #Key를 사용해 Value 얻기
                print(person["name"])
                #출력 : Alice

                print(person["age"])
                #출력 : 30
                ''')
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
                ''')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}딕셔너리 관련 함수")
        st.write('''
                - **keys()** : Key 리스트 만들기
                 ''')
        st.code('''
                print(person.keys())
                #출력 : dict_keys(['name', 'age', 'job'])
                ''')
        
        st.write('''
                - **values()** : Value 리스트 만들기
                 ''')
        st.code('''
                print(person.values())
                #출력 : dict_values(['Alice', 30, 'Chef'])
                ''')
        
        st.write('''
                - **items()** : Key, Value 쌍 얻기
                 ''')
        st.code('''
                print(person.items())
                #출력 : dict_items([('name', 'Alice'), ('age', 30), ('job', 'Chef')])
                ''')
        
        st.write('''
                - **get()** : Key로 Value 얻기
                 ''')
        st.code('''
                print(person.get("name"))
                #출력 : Alice
                ''')
        
        st.write('''
                - **in()** : 해당 Key가 딕셔너리 안에 있는지 조사하기
                 ''')
        st.code('''
                print("name" in person)
                #출력 : True

                print("birth" in person)
                #출력 : False
                ''')
        st.write('''
                - **clear()** : Key: Value 쌍 모두 지우기
                 ''')
        st.code('''
                print(person.clear())
                #출력 : None
                ''')
        st.divider()
        
        st.header(f"{idx.getHeadIdx()}집합")
        st.write("집합(set)은 집합에 관련된 것을 쉽게 처리하기 위해 만든 자료형입니다.")
        st.code('''
                #set 키워드 사용해서 집합 만들기
                s1 = set([1, 2, 3])

                s2 = set("Hello")
                print(s2)
                # 출력 : {'e', 'H', 'l', 'o'}
                ''')
        st.write('''
                's2 = set("Hello")' 결과에서 확인할 수 있듯, set에는 다음과 같은 2가지 특징이 있습니다.
                 
                 - 중복을 허용하지 않는다.
                 - 순서가 없다(Unordered).

                 set은 중복을 허용하지 않는 특징 때문에 데이터의 중복을 제거하기 위한 필터로 종종 사용됩니다. 또한, 리스트나 튜플은 순서가 있기(ordered) 때문에 인덱싱을 통해 요솟값을 얻을 수 있지만, set 자료형은 순서가 없기(unordered) 때문에 인덱싱을 통해 요솟값을 얻을 수 없습니다.
                 ''')
        st.subheader(f"{idx.getSubIdx()}집합의 연산")
        st.code('''
                # 연산에 사용할 2개의 set 생성
                s1 = set([1, 2, 3, 4, 5, 6])
                s2 = set([4, 5, 6, 7, 8, 9])
                ''')
        
        st.write('''
                - **교집합** : & , intersection
                 ''')
        st.code('''
                print( s1 & s2 )
                #출력 : {4, 5, 6}

                print( s1.intersection(s2) )
                #출력 : {4, 5, 6}
                ''')
        
        st.write('''
                - **합집합** : | , union
                 ''')
        st.code('''
                print( s1 | s2 )
                #출력 : {1, 2, 3, 4, 5, 6, 7, 8, 9}

                print( s1.union(s2) )
                #출력 : {1, 2, 3, 4, 5, 6, 7, 8, 9}
                ''')
        
        st.write('''
                - **차집합** : -(빼기), difference
                 ''')
        st.code('''
                print( s1 - s2 )
                #출력 : {1, 2, 3}

                print( s2 - s1 )
                #출력 : {8, 9, 7}

                print( s1.difference(s2) )
                #출력 : {1, 2, 3}

                print( s2.difference(s1) )
                #출력 : {8, 9, 7}
                ''')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}집합 관련 함수")
        st.write('''
                - **add()** : 값 1개 추가하기
                 ''')
        st.code('''
                s1 = set([1, 2, 3])
                s1.add(4)
                
                print( s1 )
                #출력 : {1, 2, 3, 4}
                ''')
        
        st.write('''
                - **update()** : 값 여러 개 추가하기
                 ''')
        st.code('''
                s1 = set([1, 2, 3])
                s1.update([4, 5, 6])
                
                print( s1 )
                #출력 : {1, 2, 3, 4, 5, 6}
                ''')
        
        st.write('''
                - **remove()** : 특정 값 제거하기
                 ''')
        st.code('''
                s1 = set([1, 2, 3])
                s1.remove(2)
                
                print( s1 )
                #출력 : {1, 3}
                ''')
    ################################################################################################################################################################################
    elif path == ("파이썬 기초", "제어문") :
        st.header(f"{idx.getHeadIdx()}if문")
        st.subheader(f"{idx.getSubIdx()}if문 기본 구조")
        st.write('''
                - **if** : 조건이 True인 경우에만 실행
                 
                        if 조건:
                            조건이 True면 수행할 문장
                 
                - **if - else** : 조건이 True라면 if 실행문을, False라면 else 실행문을 실행
                 
                        if 조건:
                            조건이 True면 수행할 문장
                            ...
                        else:
                            조건이 False면 수행할 문장
                            ...
                - **if - elif - else** : 여러 개의 조건을 사용하는 경우. 조건문이 True가 되는 if 혹은 elif 문을 실행하고, 모든 조건문이 False라면 else 실행문을 실행.
                 
                        if 조건1:
                            조건1이 True면 수행할 문장
                            ...
                        elif 조건2:
                            조건2이 True면 수행할 문장

                        elif 조건3:
                            조건3이 True면 수행할 문장
                        
                        else:
                            모든 조건이 False면 수행할 문장
                            ...

                 ''')
        st.divider()
        st.subheader(f"{idx.getSubIdx()}조건문 유형 - 비교 연산자")
        st.write('''
                |비교연산자|	설명|
                |------------|-------------|
                |x < y	|x가 y보다 작다.	    |
                |x > y	|x가 y보다 크다.	    |
                |x == y	|x와 y가 같다.	    |
                |x != y	|x와 y가 같지 않다.	    |
                |x >= y	|x가 y보다 크거나 같다.|
                |x <= y	|x가 y보다 작거나 같다.|
                ''')
        st.write("아래 예시를 통해 비교 연산자의 사용법을 알아보겠습니다.")
        
        st.code('''
                #숫자형의 비교 연산
                score = 75

                if score >= 90 :
                    grade = "A"
                elif score >= 80 :
                    grade = "B"
                elif score >= 70 :
                    grade = "C"
                else :
                    grade = "F"

                print(grade)
                #출력 : C


                #문자열의 비교 연산
                str1 = "abc"
                str2 = "def"
                
                if str1 == str2 :
                    print("str1과 str2는 같다")
                else :
                    print("str1과 str2는 같지 않다")
                #출력 : str1과 str2는 같지 않다
                ''')
        st.divider()
        st.subheader(f"{idx.getSubIdx()}조건문 유형 - and, or, not")
        st.write('''
                |연산자|	설명|
                |------------|-------------|
                |x or y	|x와 y 둘 중 하나만 참이어도 참이다.	    |
                |x and y	|x와 y 모두 참이어야 참이다.    |
                |not x	|x가 거짓이면 참이다.	    |
                 ''')
        
        st.write("아래 예시를 통해 and, or, not 연산자의 사용법을 알아보겠습니다.")
        st.code('''
                a = 150
                b = 200

                if (a > 200) or (b > 100) :
                    print("True")
                else :
                    print("False")
                #출력 : True

                if (a > 200) and (b > 100) :
                    print("True")
                else :
                    print("False")
                #출력 : False

                if not (a > 200) :
                    print("True")
                else :
                    print("False")
                #출력 : True

                ''')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}조건문 유형 - in, not in")
        st.write('''
                |연산자|	설명|
                |------------|-------------|
                |x in 리스트(튜플, 문자열)	|x가 리스트 안에 존재한다	    |
                |x not in 리스트(튜플, 문자열)	|x가 리스트 안에 존재하지 않는다   |
                 ''')
        st.write("아래 예시를 통해 in, not in 연산자의 사용법을 알아보겠습니다.")
        st.code('''
                student = ["Alice", "Emily", "Andrew", "John"]

                if "John" in student :
                    print("True")
                else :
                    print("False")
                #출력 : True

                if "Lisa " not in student :
                    print("True")
                else :
                    print("False")
                #출력 : True
                ''')
        st.divider()
        
        st.header(f"{idx.getHeadIdx()}while문")
        st.write("문장을 반복해서 수행해야 할 경우 while 문을 사용합니다. 그래서 while 문을 ‘반복문’이라고도 부릅니다.")
        st.divider()

        st.subheader(f"{idx.getSubIdx()}while문의 기본 구조")
        st.write('''
                while 문은 조건문이 참인 동안 while 문에 속한 문장들을 반복해서 수행하고, 조건문이 거짓이 되는 경우 반복을 중지합니다.
                        
                    while 조건문:
                        수행할_문장1
                        수행할_문장2
                        수행할_문장3
                        ...

                 ''')
        st.write("아래 코드는 1부터 10까지 더해주는 코드를 반복문으로 작성한 예시입니다. ")
        st.code('''
                i = 1
                sum = 0

                while i <= 10 :
                    sum += i       #sum 변수에 i 값을 더해줍니다
                    i += 1         #i 값을 1만큼 증가시킵니다
                
                print(sum)
                # 출력 : 55
                ''')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}while 문 강제로 빠져나가기")
        st.write("while 문은 조건문이 참인 동안 계속 while 문 안의 내용을 반복적으로 수행합니다. 하지만 강제로 while 문을 빠져나가고 싶은 경우엔 break를 사용해 반복문을 빠져나갈 수 있습니다.")
        st.write("아래 코드는 조건문이 True이기 때문에 무한 반복하게 됩니다.")
        st.code('''
                a = 30
                while True : #무한 반복
                    a -= 5
                ''')
        st.write("while문을 강제로 빠져나오기 위해, 특정 조건을 만족할 경우 break를 사용하여 while문을 빠져나올 수 있습니다.")
        st.code('''
                a = 30
                while True : #무한 반복
                    a -= 5

                    # a 가 10보다 작아지는 경우 break
                    if a < 10 :
                        break
                print(a)
                # 출력 : 5
                ''')
        st.divider()
        st.subheader(f"{idx.getSubIdx()}while 문의 맨 처음으로 돌아가기")
        st.write("while 문 안의 문장을 수행할 때 입력 조건을 검사해서 조건에 맞지 않으면 while 문을 빠져나갑니다. 그런데 프로그래밍을 하다 보면 while 문을 빠져나가지 않고 while 문의 맨 처음(조건문)으로 다시 돌아가게 만들고 싶은 경우가 생기게 되는데, 이때 사용하는 것이 바로 continue 문입니다.")
        st.code('''
                a = 0
                while a < 10 :
                    a = a + 1
                
                    if a % 2 == 0 :     #a가 짝수인 경우
                        continue        #처음으로
                    print(a)
                
                #출력 :
                #1
                #3
                #5
                #7
                #9
                ''')
        st.write("위는 1부터 10까지의 숫자 중 홀수만 출력하는 예시입니다. a가 10보다 작은 동안 a는 1만큼씩 계속 증가합니다. a % 2 == 0(a를 2로 나누었을 때 나머지가 0인 경우)이 참이 되는 경우는 a가 짝수인 경우입니다. 즉, a가 짝수이면 continue 문을 수행하게 됩니다. 이 continue 문은 while 문의 맨 처음인 조건문(a < 10)으로 돌아가게 하는 명령어입니다. 따라서 위 예에서 a가 짝수이면 print(a) 문장은 수행되지 않을 것입니다.")
        st.divider()
        
        st.header(f"{idx.getHeadIdx()}for문")
        st.write('''
                 for문은 정해진 횟수나 범위 안에서 차례대로 대입하며 반복을 수행하는 반복문입니다. 아래와 같은 기본 구조를 가집니다.
                 
                        for 변수 in 리스트(또는 튜플, 문자열):
                            수행할_문장1
                            수행할_문장2
                            ...

                리스트나 튜플, 문자열의 첫 번째 요소부터 마지막 요소까지 차례로 변수에 대입되어 for문 내 문장들이 수행됩니다.

                 ''')
        st.divider()
        st.subheader(f"{idx.getSubIdx()}for문 사용법")
        st.code('''
                numList = ['one', 'two', 'three']

                for i in numList :
                    print(i)
                
                #출력 : 
                #one
                #two
                #three
                ''')
        st.write("['one', 'two', 'three'] 리스트의 첫 번째 요소인 'one'이 먼저 i 변수에 대입된 후 print(i) 문장을 수행합니다. 다음에 두 번째 요소 'two'가 i 변수에 대입된 후 print(i) 문장을 수행하고 리스트의 마지막 요소까지 이것을 반복합니다.")
        st.divider()

        st.subheader(f"{idx.getSubIdx()}for문과 continue문")
        st.write('''
                while 문에서 살펴본 continue 문을 for 문에서도 사용할 수 있습니다. 즉, for 문 안의 문장을 수행하는 도중 continue 문을 만나면 for 문의 처음으로 돌아가게 됩니다.
                 ''')
        st.code('''
                for i in [10, 23, 17, 22, 12] :
                    if i % 2 == 0 :     #짝수인 경우
                        continue        #처음으로 되돌아감 
                    print(i)        #출력
                
                #출력 :
                # 23
                # 17
                ''')
        
        st.write("i의 값이 짝수인 경우 continue문이 수행되어 출력이 수행되지 않습니다.")
        st.divider()

        st.subheader(f"{idx.getSubIdx()}for문과 함께 자주 사용하는 range 함수")
        st.write("for 문은 숫자 리스트를 자동으로 만들어 주는 range 함수와 함께 사용하는 경우가 많습니다. 다음은 range 함수의 간단한 사용법입니다.")
        st.code('''
                a = range(10)

                print(a)
                # 출력 : range(0, 10)
                ''')
        st.write("range(10)은 0부터 10 미만의 숫자를 포함하는 range 객체를 만들어 줍니다. 시작 숫자와 끝 숫자를 지정하려면 range(시작_숫자, 끝_숫자) 형태를 사용하는데, 이때 끝 숫자는 포함되지 않습니다.")
        st.code('''
                add = 0

                for i in range(1, 11) :
                    add += i
                
                print(add)
                # 출력 : 55
                ''')
        st.write("range(1, 11)은 숫자 1부터 10까지(1 이상 11 미만)의 숫자를 데이터로 가지는 객체입니다. 따라서 위 예에서 i 변수에 숫자가 1부터 10까지 하나씩 차례로 대입되면서 add += i 문장을 반복적으로 수행하고 add 최종적으로 55가 됩니다.")
    
    elif path == ("파이썬 기초", "고급") :
        st.header(f"{idx.getHeadIdx()}함수")
        st.write("코드의 반복을 줄이거나 어떠한 용도를 위해 특정 코드들을 모아둔 것입니다. 한 번 작성해두면 해당 코드가 필요할 때 함수를 호출해서 쉽게 재사용 할 수 있고, 용도에 따라 분리가 가능해 가독성이 좋습니다.")
        st.divider()

        st.subheader(f"{idx.getSubIdx()}함수의 구조")
        st.write('''def는 함수를 만들 때 사용하는 예약어이며, 함수 이름은 함수를 만드는 사람이 임의로 만들 수 있습니다. 함수 이름 뒤 괄호 안의 매개변수는 이 함수에 입력으로 전달되는 값을 받는 변수입니다. 이렇게 함수를 정의한 후 if, while, for 문 등과 마찬가지로 함수에서 수행할 문장을 입력합니다.''')
        st.code('''
                def 함수명(매개변수):
                    수행할_문장1
                    수행할_문장2
                    ...
                    return 결과값
                 ''')
        
        st.write("다음의 함수명은 add이고 입력으로 a, b 2개의 값을 받으며 리턴값(출력값)은 2개의 입력값을 더한 값입니다.")
        st.code('''
                def add(a, b): 
                    return a + b
                
                x = 10
                y = 7
                z = add(10, 7)

                print(z)
                #출력 : 17
                ''')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}매개변수와 인수")
        st.write("매개변수는 함수에 입력으로 전달된 값을 받는 변수, 인수는 함수를 호출할 때 전달하는 입력값을 의미합니다.")

        st.code('''
                def add(a, b):  # a, b는 매개변수
                    return a+b

                print(add(3, 4))  # 3, 4는 인수
                ''')
        st.divider()
        st.subheader(f"{idx.getSubIdx()}return(반환값)")
        st.write("함수는 들어온 입력값을 받은 후 처리를 하여 적절한 값을 리턴해 줍니다. 함수의 형태는 입력값과 리턴값의 존재 유무에 딸 4가지 유형으로 나뉩니다.")
        st.write('''
                - 입력값과 리턴값이 모두 있는 일반적인 함수
                 ''')
        st.code('''
                def add(a, b): 
                    result = a + b 
                    return result

                print(add(3, 4))
                # 출력 : 7
                ''')
        st.write('''
                - 입력값이 없는 함수
                 ''')
        st.code('''
                def say(): 
                    return 'Hi'

                print(say())
                # 출력 : Hi
                ''')
        
        st.write('''
                - 리턴값이 없는 함수
                 ''')
        st.code('''
                def add(a, b): 
                    print("%d, %d의 합은 %d입니다." % (a, b, a+b))

                add(3, 4)
                # 출력 : 3, 4의 합은 7입니다.
                ''')
        st.write('''
                - 입력값도, 리턴값도 없는 함수
                 ''')
        st.code('''
                def say(): 
                    print("Hi")

                say()
                # 출력 : Hi
                ''')
        st.divider()
        st.subheader(f"{idx.getSubIdx()}lambda")
        st.write('''
                 lambda는 함수를 생성할 때 사용하는 예약어로, def와 동일한 역할을 합니다. 보통 함수를 한 줄로 간결하게 만들 때 사용합니다. def를 사용해야 할 정도로 복잡하지 않거나 def를 사용할 수 없는 곳에 주로 사용됩니다.
                 
                        함수_이름 = lambda 매개변수1, 매개변수2, ... : 매개변수를_이용한_표현식
                 
                 ''')
        st.code('''
                add = lambda a, b : a+b
                result = add(3, 4)

                print(result)
                #출력 : 7
                ''')
        st.write("add는 2개의 인수를 받아 서로 더한 값을 리턴하는 lambda 함수입니다. lambda로 만든 함수는 return 명령어가 없어도 표현식의 결과값을 리턴합니다.")
        st.divider()

        st.header(f"{idx.getHeadIdx()}패키지")
        st.write('''
                패키지는 모듈의 집합을 뜻합니다. 모듈은 하나의 .py 파이썬 파일, 패키지는 여러개의 .py 파일을 모아놓은 폴더 개념으로 생각할 수 있습니다.
                파이썬 패키지 중 예로는 넘파이 (NumPy)와 Pandas (판다스)가 있습니다.
                ''')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}pip를 이용하여 패키지 설치하기")
        st.write('''
                 일부 패키지는 파이썬을 설치할 때 함께 설치됩니다. 그러나 그 외에 추가로 패키지를 더 사용해야 할 때는 사용자가 수동으로 설치해야 합니다.
                 파이썬은 간단한 명령어만으로 패키지를 쉽게 내려받아 설치할 수 있습니다.

                        pip install 패키지이름
                 
                예를 들어 pandas 패키지를 설치하려면 :blue-background[pip install pandas] 명령을 통해 설치할 수 있습니다.
                ''')
        st.divider()
        
        st.subheader(f"{idx.getSubIdx()}pip를 이용하여 설치된 패키지 확인하기")
        st.write('''
                 :blue-background[pip list] 명령을 통해 설치된 패키지 목록을 볼 수 있습니다.

                        pip list

                ''')
    
    ### Pandas 컨텐츠 작성
    elif path == ("Pandas 기초", "DataFrame") :
        st.header(f"{idx.getHeadIdx()}데이터프레임 생성") ## 소단원01

        st.markdown('- 2차원 데이터 구조 (Excel 데이터 시트와 비슷합니다.) \n'
            '- 행(row), 열(column)으로 구성되어 있습니다. \n' 		# 공백 2칸
            '- 각 열(column)은 각각의 데이터 타입 (dtype)을 가집니다. \n' 		# 공백 2칸
            )
        
        st.subheader(f"{idx.getSubIdx()}list 통한 생성")
        st.markdown("**list 를 통해 생성**할 수 있습니다. DataFrame을 만들 때는 **2차원 list를 대입**합니다.")
        with st.echo():
            import pandas as pd
            df = pd.DataFrame([[1,2,3],
                        [4,5,6],
                        [7,8,9]])
            df

        st.divider()
        st.markdown("**columns를 지정**하면, DataFrame의 각 열에 대한 컬럼명이 붙습니다.")
        with st.echo():
            import pandas as pd
            df = pd.DataFrame([[1, 2, 3], 
                            [4, 5, 6], 
                            [7, 8, 9]], columns=['가', '나', '다'])
            df

        st.divider()
        st.subheader(f"{idx.getSubIdx()}dictionary 통한 생성")
        st.markdown('**dictionary를 통한 생성**도 가능합니다.\n'
                    'dictionary의 **key 값이 자동으로 column 명으로 지정**되어 편리합니다.')
        with st.echo():
            import pandas as pd
            data = {
                'name': ['Kim', 'Lee', 'Park'], 
                'age': [24, 27, 34], 
                'children': [2, 1, 3]
            }
            df = pd.DataFrame(data)
            df


        st.divider()

        st.header(f"{idx.getHeadIdx()}데이터프레임 속성") # 소단원02

        st.markdown('DataFrame은 다음과 같은 **속성**을 가집니다.\n'
                    '- **index**: index (기본 값으로 RangeIndex)\n'
                    '- **columns**: column 명\n'
                    '- **values**: numpy array 형식의 데이터 값\n'
                    '- **dtypes**: column 별 데이터 타입\n')

        with st.echo():
            import pandas as pd
            data = {
                'name': ['Kim', 'Lee', 'Park'], 
                'age': [24, 27, 34], 
                'children': [2, 1, 3]
            }
            df = pd.DataFrame(data)

        st.divider()

        st.subheader(f"{idx.getSubIdx()}df.index")
        st.write('''데이터프레임의''', '**인덱스(행)**','''을 출력합니다.''')
        with st.echo():
            df.index
        st.divider()

        st.subheader(f"{idx.getSubIdx()}df.columns")
        st.write("데이터프레임의", "**컬럼(열)**", "을 출력합니다.")
        with st.echo():
            df.columns
        st.divider()

        st.subheader(f"{idx.getSubIdx()}df.values")
        st.write("데이터프레임의 **데이터 값** 을 출력합니다.")
        with st.echo():
            df.values
        st.divider()

        st.subheader(f"{idx.getSubIdx()}df.dtypes")
        st.write("데이터프레임의 **데이터 타입** 을 출력합니다.")
        with st.echo():
            df.dtypes
        st.divider()

        st.header(f"{idx.getHeadIdx()}데이터프레임 조회") ## 소단원03

        st.write('데이터프레임(DataFrame)에서 가장 많이 사용하는 **조회, 정렬 그리고 조건필터**에 대해 알아보겠습니다.')
        st.write('조회, 정렬, 조건필터 기능은 엑셀에서도 가장 많이 활용하는 기능입니다.')
        st.write('Pandas는 조회, 정렬, 조건필터의 기능을 매우 편리하게 사용할 수 있도록 지원합니다.')
        st.divider()

        pandas_dataset()

        st.subheader(f"{idx.getSubIdx()}head() 앞 부분 / tail() 뒷 부분 조회")
        st.write('- default 옵션 값으로 **5개의 행이 조회**됩니다.')
        st.write('- 괄호 안에 숫자를 넣어 명시적으로 조회하고 싶은 행의 갯수를 지정할 수 있습니다.')
        
        import seaborn as sns
        df = sns.load_dataset('titanic')
        import io
        st.code('''df.head()''')
        st.write(df.head())
        
        st.code('''df.tail()''')
        
        st.write(df.tail())
        st.divider()

        with st.echo():
            df.head(3)

        st.write(df.head(3))
        st.divider()

        st.code('''df.tail(7)''')
        st.write(df.tail(7))
        st.divider()

        st.subheader(f"{idx.getSubIdx()}info()")
        st.write('- 컬럼별 정보(information)를 보여줍니다.')
        st.write('- 데이터의 갯수, 그리고 데이터 타입(dtype)을 확인할 때 사용합니다.')
        st.code('''df.info()''')
        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

        st.write('- **object** 타입은 쉽게 문자열이라고 생각하면 됩니다.')
        st.write('''- **category** 타입도 있습니다. category 타입은 문자열이지만, '남자' / '여자'처럼 카테고리화 할 수 있는 컬럼을 의미 합니다''')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}value_counts()")
        st.write('- column 별 **값의 분포를 확인**할 때 사용합니다.')
        st.write('- **남자, 여자, 아이의 데이터 분포를 확인**하고 싶다면 다음과 같이 실행합니다.')

        with st.echo():
            df['who'].value_counts()
        st.write(df['who'].value_counts())
        st.divider()

        st.subheader(f"{idx.getSubIdx()}Attributes : 속성")
        st.write('속성 값은 **함수형으로 조회하지 않습니다.**')
        st.write('자주 활용하는 DataFrame은 **속성 값**들은 다음과 같습니다.')
        st.markdown('- ndim\n' '- shape\n' '- index\n' '- columns\n' '- values\n')
        st.divider()

        st.write('**차원**을 나타냅니다. DataFrame은 2가 출력됩니다.')
        with st.echo():
            df.ndim
        st.divider()

        st.write('**(행, 열)** 순서로 출력됩니다.')
        with st.echo():
            df.shape
        st.divider()

        st.write('index는 기본 설정된 **RangeIndex**가 출력됩니다.')
        with st.echo():
            df.index
        st.divider()

        st.write('columns **열**을 출력합니다.')
        with st.echo():
            df.columns
        st.divider()

        st.write('values는 모든 값을 출력하며, **numpy array 형식**으로 출력됩니다.')
        with st.echo():
            df.values

        st.header(f"{idx.getHeadIdx()}데이터프레임 정렬") ## 소단원04

        st.write('데이터프레임(DataFrame)에서 가장 많이 사용하는 **조회, 정렬 그리고 조건필터**에 대해 알아보겠습니다.')
        st.write('조회, 정렬, 조건필터 기능은 엑셀에서도 가장 많이 활용하는 기능입니다.')
        st.write('Pandas는 조회, 정렬, 조건필터의 기능을 매우 편리하게 사용할 수 있도록 지원합니다.')
        st.divider()

        pandas_dataset()

        st.subheader(f"{idx.getSubIdx()}sort_index: index 정렬")
        st.write('- index 기준으로 정렬합니다. (기본 오름차순이 적용되어 있습니다.)')
        st.write('내림차순 정렬을 적용하려면, :blue-background[ascending=False]를 옵션 값으로 설정합니다.')

        import seaborn as sns
        df = sns.load_dataset('titanic')

        st.code('''df.sort_index().head(5)''')
        st.write(df.sort_index().head(5))
        st.divider()

        st.code('''df.sort_index(ascending=False).head(5)''')
        st.write(df.sort_index(ascending=False).head(5))
        st.divider()

        st.subheader(f"{idx.getSubIdx()}sort_values: 값에 대한 정렬")
        st.write('- 값을 기준으로 행을 정렬합니다.')
        st.write('- by에 기준이 되는 행을 설정합니다.')
        st.write('- by에 2개 이상의 컬럼을 지정하여 정렬할 수 있습니다.')
        st.write('- 오름차순/내림차순을 컬럼 별로 지정할 수 있습니다.')
        st.code('''df.sort_values(by='age').head()''')
        st.write(df.sort_values(by='age').head())
        st.divider()

        st.write('내림차순 정렬: :blue-background[ascending=False]')
        st.code('''df.sort_values(by='age', ascending=False).head()''')
        st.write(df.sort_values(by='age', ascending=False).head())
        st.divider()

        st.write('**문자열 컬럼도 오름차순/내림차순 정렬이 가능**하며 알파벳 순서로 정렬됩니다.')
        st.code('''df.sort_values(by='class', ascending=False).head()''')
        st.write(df.sort_values(by='class', ascending=False).head())    
        st.divider()

        st.write('**2개 이상의 컬럼**을 기준으로 값 정렬 할 수 있습니다.')
        st.code('''df.sort_values(by=['fare', 'age']).head()''')
        st.write(df.sort_values(by=['fare', 'age']).head())
        st.divider()

        st.write('오름차순/내림차순 정렬도 컬럼 **각각에 지정**해 줄 수 있습니다.')
        st.code('''df.sort_values(by=['fare', 'age'], ascending=[False, True]).head()''')
        st.write(df.sort_values(by=['fare', 'age'], ascending=[False, True]).head())
        st.divider()

        st.header(f"{idx.getHeadIdx()}Indexing, Slicing, 조건 필터링") ## 소단원05

        st.write('데이터프레임(DataFrame)에서 가장 많이 사용하는 **조회, 정렬 그리고 조건필터**에 대해 알아보겠습니다.')
        st.write('조회, 정렬, 조건필터 기능은 엑셀에서도 가장 많이 활용하는 기능입니다.')
        st.write('Pandas는 조회, 정렬, 조건필터의 기능을 매우 편리하게 사용할 수 있도록 지원합니다.')
        st.divider()

        pandas_dataset()

        import seaborn as sns
        df = sns.load_dataset('titanic')

        st.subheader(f"{idx.getSubIdx()}loc - indexing / slicing")
        st.write('- indexing과 slicing을 할 수 있습니다.')
        st.write('- slicing은 [**시작(포함): 끝(포함)**] 규칙에 유의합니다. 둘 다 포함 합니다.')

        st.write('**01. indexing 예시**')
        st.code('''df.loc[5, 'class']''')
        st.write(df.loc[5, 'class'])
        st.divider()

        st.write('**02. fancy indexing 예시**')
        st.code('''df.loc[2:5, ['age', 'fare', 'who']]''')
        st.write(df.loc[2:5, ['age', 'fare', 'who']])
        st.divider()

        st.write('**03. slicing 예시**')
        st.code('''df.loc[2:5, 'class':'deck'].head()''')
        st.write(df.loc[2:5, 'class':'deck'].head())

        st.code('''df.loc[:6, 'class':'deck']''')
        st.write(df.loc[:6, 'class':'deck'])
        st.divider()

        st.write('**04. loc - 조건 필터**')
        st.write('boolean index을 만들어 조건에 맞는 데이터만 추출해 낼 수 있습니다.')
        st.code('''cond = (df['age'] >= 70)\ncond''')
        cond = (df['age'] >= 70)
        st.write(cond)
        st.divider()
        st.code('''df.loc[cond]''')
        st.write(df.loc[cond])
        st.divider()

        st.write('**05. loc - 다중조건**')
        st.write('다중 조건은 먼저 condition(조건)을 정의하고 **&** 와 **|** 연산자로 **복합 조건을 생성**합니다.')
        st.code(
            '''# 조건1 정의\ncond1 = (df['fare'] > 30)\n# 조건2 정의\ncond2 = (df['who'] == 'woman')''')
        cond1 = (df['fare'] > 30)
        cond2 = (df['who'] == 'woman')
        st.code('''df.loc[cond1 & cond2]''')
        st.write(df.loc[cond1 & cond2])
        st.divider()

        st.code('''df.loc[cond1 | cond2]''')
        st.write(df.loc[cond1 | cond2])
        st.divider()

        st.write('**06. 조건 필터 후 데이터 대입**')
        st.code('''cond = (df['age'] >= 70)\ncond''')
        cond = (df['age'] >= 70)
        st.write(cond)
        st.divider()
        st.code('''#조건 필터\ndf.loc[cond]''')
        st.write(df.loc[cond])
        st.divider()

        st.write('**07. 나이 컬럼**만 가져옵니다.')
        with st.echo():
            df.loc[cond, 'age']
        st.divider()

        st.write('**조건 필터** 후 원하는 값을 대입할 수 있습니다. (단일 컬럼 선택에 유의)')
        with st.echo():
            df.loc[cond, 'age'] = -1
        with st.echo():
            df.loc[cond]
        st.divider()

        st.subheader(f"{idx.getSubIdx()}iloc")
        st.write('- :blue-background[loc]와 유사하지만, index만 허용합니다.')
        st.write('loc와 마찬가지고, indexing / slicing 모두 가능합니다.')
        st.code('''df.head()''')
        st.write(df.head())
        st.divider()

        st.write('**01. indexing**')
        st.code('''df.iloc[1, 3]''')
        st.write(df.iloc[1, 3])
        st.divider()

        st.write('**02. Fancy Indexing**')
        st.code('''df.iloc[[0, 3, 4], [0, 1, 5, 6]]''')
        st.write(df.iloc[[0, 3, 4], [0, 1, 5, 6]])
        st.divider()

        st.write('**03. Slicing**')
        st.code('''df.iloc[:3, :5]''')
        st.write(df.iloc[:3, :5])
        st.divider()

        st.write('**04. isin**')
        st.write('특정 값의 포함 여부는 isin 함수를 통해 비교가 가능합니다. (파이썬의 in 키워드는 사용 불가 합니다.)')
        with st.echo():
            import pandas as pd
            sample = pd.DataFrame({'name': ['kim', 'lee', 'park', 'choi'], 
                                'age': [24, 27, 34, 19]
                            })
            sample
        st.divider()
        st.code('''sample['name'].isin(['kim', 'lee'])''')
        st.write(sample['name'].isin(['kim', 'lee']))

        st.divider()
        st.code('''sample.isin(['kim', 'lee'])''')
        st.write(sample.isin(['kim', 'lee']))
        st.divider()

        st.write(':blue-background[loc] 를 활용한 **조건 필터링**으로도 찰떡궁합입니다.')
        with st.echo():
            condition = sample['name'].isin(['kim', 'lee'])
        with st.echo():
            sample.loc[condition]
            
    ## Excel/CSV        

    elif path == ("Pandas 기초", "Excel/CSV") :
        
        st.header(f"{idx.getHeadIdx()}Excel") ## 소단원01
        st.subheader(f"{idx.getSubIdx()}Excel-불러오기") ## 소단원01 - 세부01
        

        st.write('- Excel 데이터를 바로 읽어들일 수 있습니다. sheet_name 지정시 해당 sheet를 가져옵니다.\n'
                    '''- [참고] :blue-background[pd.read_excel()]로 데이터 로드시 에러 발생한다면 engine='openpyxl'을 추가합니다.''' 
                    )
        st.write('- 실습을 위해 **아래의 버튼**을 클릭하여 데이터를 다운로드 해주세요')
        
        with open('data/서울시대중교통/seoul_transportation.xlsx', "rb") as template_file:
            template_byte = template_file.read()

        st.download_button(label="download data",
                            type="primary",
                            data=template_byte,
                           file_name = "seoul_transportation.xlsx"
        )
        st.write('다운 받은 데이터를 현재 작업 중인 jupyter 디렉터리로 이동해주세요')

        st.divider()
        
        st.write('**철도 Sheet의 데이터 불러오기**')

        st.code('''
            import pandas as pd
            excel = pd.read_excel('seoul_transportation.xlsx', 
                                sheet_name='철도', engine='openpyxl')
            excel.head()
            ''')
        
        import pandas as pd
        excel = pd.read_excel('data/서울시대중교통/seoul_transportation.xlsx', 
                                sheet_name='철도', engine='openpyxl')
        st.write(excel.head())

        # st.divider()

        st.write('**버스 Sheet의 데이터 불러오기**')

        st.code('''
            import pandas as pd
            excel = pd.read_excel('seoul_transportation.xlsx', 
                                sheet_name='버스', engine='openpyxl')
            excel.head()
            ''')
        excel = pd.read_excel('data/서울시대중교통/seoul_transportation.xlsx', 
                                sheet_name='버스', engine='openpyxl')
        st.write(excel.head())
        st.divider()
        st.markdown(''':blue-background[sheet_name]을 None으로 지정하면 모든 sheet를 가지고 옵니다.''')
                    
        st.write('가지고 올 때는 OrderedDict로 가져오며, :blue-background[keys()]로 시트명을 조회할 수 있습니다.')
        st.code('''
            import pandas as pd
            excel = pd.read_excel('seoul_transportation.xlsx', 
                                sheet_name=None, engine='openpyxl')
            excel
            ''')
        excel = pd.read_excel('data/서울시대중교통/seoul_transportation.xlsx', 
                                sheet_name=None, engine='openpyxl')
        st.write(excel)

        st.divider()
        st.markdown(':blue-background[keys()]를 통해 엑셀이 포함하고 있는 시트를 조회할 수 있습니다.')
        with st.echo():
            excel.keys()
        st.write(excel.keys())
        st.divider()

        st.subheader(f"{idx.getSubIdx()}Excel-저장하기") ## 소단원01 - 세부02

        st.write('DataFrame을 Excel로 저장할 수 있으며, Excel로 저장시 **파일명**을 지정합니다.\n'
                    '- index=False 옵션은 가급적 꼭 지정하는 옵션입니다. 지정을 안하면 **index가 별도의 컬럼으로 저장**되게 됩니다.\n'
                    '- sheet_name을 지정하여, 저장할 시트의 이름을 변경할 수 있습니다.\n'
                    )
        st.divider()

        st.code('''
            import pandas as pd
            excel = pd.read_excel('seoul_transportation.xlsx', sheet_name='철도', engine='openpyxl')
            excel.head()
            ''')
        excel = pd.read_excel('data/서울시대중교통/seoul_transportation.xlsx', 
                                sheet_name='버스', engine='openpyxl')
        st.write(excel.head())
        

        st.divider()

        st.write('**시트명 없이 저장**')
        code = '''excel.to_excel('sample.xlsx', index=True)'''
        st.code(code, language="python")
        st.write('현재 디렉터리에서 sample.xlsx가 저장된 것을 확인할 수 있습니다.')
        st.divider()
        
        st.write('**시트명 지정하여 저장**')
        code = '''excel.to_excel('sample1.xlsx', index=False, sheet_name='샘플')'''
        st.write('현재 디렉터리에서 sample1.xlsx가 저장된 것을 확인할 수 있습니다.')
        st.code(code, language="python")
        st.divider()

        st.header(f"{idx.getHeadIdx()}CSV") ## 소단원02

        st.write('한 줄이 한 개의 행에 해당하며, 열 사이에는 **쉼표(,)를 넣어 구분**합니다.\n')
        st.write('Excel보다 훨씬 가볍고 **차지하는 용량이 적기 때문에 대부분의 파일 데이터는 csv 형태**로 제공됩니다.')
        st.write('- 실습을 위해 **아래의 버튼**을 클릭하여 데이터를 다운로드 해주세요')
        
        with open('data/서울시주민등록인구/seoul_population.csv', "rb") as template_file:
            template_byte = template_file.read()

        st.download_button(label="download data",
                            data=template_byte,
                            type="primary",
                           file_name = "seoul_population.csv")

        st.write('다운 받은 데이터를 현재 작업 중인 jupyter 디렉터리로 이동해주세요')
        st.divider()
        
        st.subheader(f"{idx.getSubIdx()}CSV-불러오기") ## 소단원02- 세부01
        st.code('''
            import pandas as pd
            df = pd.read_csv('seoul_population.csv')
            df
            ''')
        df = pd.read_csv('data/서울시주민등록인구/seoul_population.csv')
        st.write(df)
        st.divider()

        st.subheader(f"{idx.getSubIdx()}CSV-저장하기") ## 소단원02 - 세부02
        st.markdown('저장하는 방법은 excel과 유사합니다.\n'
                    '다만, csv파일 형식에는 sheet_name 옵션은 없습니다.')

        st.code('''
            import pandas as pd
            df = pd.read_csv('seoul_population.csv')
            df
            ''')
        df = pd.read_csv('data/서울시주민등록인구/seoul_population.csv')
        st.divider()

        st.write(''':blue-background[to_csv()]로 csv 파일형식으로 저장할 수 있습니다.''')
        code='''df.to_csv('sample.csv', index=False)'''
        st.code(code, language="python")
        st.write('현재 디렉터리에서 sample.csv가 저장된 것을 확인할 수 있습니다.')
        st.divider()

        st.markdown("읽어드린 **Excel 파일도 csv**로 저장할 수 있습니다.")
        st.code('''
            import pandas as pd
            excel = pd.read_excel('seoul_transportation.xlsx', sheet_name='버스')
                ''')
        # excel = pd.read_excel('data/서울시대중교통/seoul_transportation.xlsx', 
        #                         sheet_name='버스')
        code = '''excel.to_csv('sample1.csv', index=False)'''
        st.code(code, language="python")
        st.write('현재 디렉터리에서 sample1.csv가 저장된 것을 확인할 수 있습니다.')
        st.divider()
    
    elif path == ("Pandas 기초", "Data 전처리"):
        st.header(f"{idx.getHeadIdx()}데이터 복사") ## 소단원01
        
        st.write('Pandas DataFrame의 **복사(Copy), 결측치 처리**, 그리고 row, column의 **추가, 삭제, 컬럼간 연산, 타입의 변환**을 다뤄보겠습니다.')
        st.divider()

        pandas_dataset()

        import seaborn as sns
        df = sns.load_dataset('titanic')

        st.write('DataFrame을 **복제**합니다. 복제한 DataFrame을 수정해도 **원본에는 영향을 미치지 않습니다.**')
        code = '''df.head()'''
        st.code(code)
        st.write(df.head())
        st.divider()

        st.write(':blue-background[copy()]로 DataFrame을 복제합니다.')
        code = '''df_copy = df.copy()'''
        st.code(code)
        code = '''df_copy.head()'''
        st.code(code)
        df_copy = df.copy()
        st.write(df_copy.head())
        st.divider()

        st.write(':blue-background[df_copy]의 :blue-background[age]를 99999로 임의 수정하도록 하겠습니다.')
        code = '''df_copy.loc[0, 'age'] = 99999'''
        st.code(code)
        df_copy.loc[0, 'age'] = 99999
        st.write('수정사항이 반영된 것을 확인할 수 있습니다.')
        code = '''df_copy.head()'''
        st.code(code)
        st.write(df_copy.head())
        st.divider()

        st.write('하지만, 원본 DataFrame의 **데이터는 변경되지 않고 그대로 남아** 있습니다.')
        code = 'df.head()'
        st.code(code)
        st.write(df.head())
        st.divider()

        st.header(f"{idx.getHeadIdx()}데이터 결측치") ## 소단원02

        import seaborn as sns
        df = sns.load_dataset('titanic')


        st.write('결측치는 **비어있는 데이터**를 의미합니다.')
        st.write('결측치에 대한 처리는 매우 중요합니다.')
        st.write('결측치에 대한 처리를 해주려면 **다음의 내용**을 반드시 알아야 합니다.')
        st.write('1. 결측 데이터 확인')
        st.write('2. 결측치가 **아닌** 데이터 확인')
        st.write('3. 결측 데이터 **채우기**')
        st.write('4. 결측 데이터 **제거하기**')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}결측치 확인 - isnull(), isnan()")
        st.write('컬럼(column)별 결측치의 갯수를 확인하기 위해서는 :blue-background[sum()] 함수를 붙혀주면 됩니다.')
        st.write(':blue-background[sum()]은 Pandas의 통계 관련 함수이며, 통계 관련 함수는 **Static** 챕터에서 알 수 있습니다.')
        st.divider()
        st.write('**isnull()**')
        
        code = 'df.isnull().sum()'
        st.code(code)
        st.write(df.isnull().sum())
        st.divider()

        st.write('**isna()**')
        st.write('isnull() 과 동작이 완전 같습니다. 편한 것으로 써주세요. (심지어 도큐먼트도 같습니다)')
        code ='df.isna().sum()'
        st.code(code)
        st.write(df.isna().sum())
        st.divider()

        st.write('DataFrame 전체 결측 데이터의 갯수를 합산하기 위해서는 :blue-background[sum()]을 두 번 사용하면 됩니다.')
        code = 'df.isnull().sum().sum()'
        st.code(code)
        st.write(df.isnull().sum().sum())    
        st.divider()

        st.subheader(f"{idx.getSubIdx()}결측치가 아닌 데이터 확인 - notnull()")
        st.write(':blue-background[notnull()]은 :blue-background[isnull()]과 정확히 **반대** 개념입니다.')
        code = 'df.notnull().sum()'
        st.code(code)
        st.write(df.notnull().sum())
        st.divider()

        st.subheader(f"{idx.getSubIdx()}결측 데이터 필터링")

        st.write(':blue-background[isnull()] 함수가 결측 데이터를 찾는 **boolean index** 입니다.')
        st.write('즉, :blue-background[loc]에 적용하여 조건 필터링을 걸 수 있습니다.')
        code = '''df.loc[df['age'].isnull()]'''
        st.code(code)
        st.write(df.loc[df['age'].isnull()])
        st.divider()

        st.subheader(f"{idx.getSubIdx()}결측치 채우기 - fillna()")
        st.write(':blue-background[fillna()]를 활용하면 결측치에 대하여 일괄적으로 값을 채울 수 있습니다.')
        code = ''' # 다시 원본 DataFrame 로드\ndf = sns.load_dataset('titanic')'''
        st.code(code)
        df = sns.load_dataset('titanic')
        code = '''# 원본을 copy하여 df1 변수에\ndf1 = df.copy()'''
        st.code(code)
        df1 = df.copy()    
        code = '''df1.tail()'''
        st.code(code)
        st.write(df1.tail())
        st.divider()

        st.write('888번 index의 **결측치가 700으로 채워**진 것을 확인할 수 있습니다.')
        code = '''df1['age'].fillna(700).tail()'''
        st.code(code)
        st.write(df1['age'].fillna(700).tail())
        st.divider()

        st.write('df1에 **결측치를 700**으로 채우고 저장합니다.')
        code = '''df1['age'] = df1['age'].fillna(700)'''
        st.code(code)
        df1['age'] = df1['age'].fillna(700)
        code = 'df1.tail()'
        st.code(code)
        st.write(df1.tail())    
        st.divider()

        st.subheader(f"{idx.getSubIdx()}통계값으로 채우기")
        code = '''df1 = df.copy()'''
        st.code(code)
        df1 = df.copy()
        code = 'df1.tail()'
        st.code(code)
        st.write(df1.tail())
        st.divider()

        st.write('**05-1. 평균으로 채우기**')
        code = '''df1['age'].fillna(df1['age'].mean()).tail()'''
        st.code(code)
        st.code(df1['age'].fillna(df1['age'].mean()).tail())
        st.divider()

        st.write('**05-2. 최빈값으로 채우기**')
        code = '''df1['deck'].mode()'''
        st.code(code)
        st.write(df1['deck'].mode())
        st.divider()

        st.write('''최빈값(mode)으로 채울 때에는 반드시 **0번째 index 지정**하여 값을 추출한 후 채워야 합니다.''')
        code = '''df1['deck'].mode()[0]'''
        st.code(code)
        st.write(df1['deck'].mode()[0])
        st.divider()
                    
        code = '''df1['deck'].fillna(df1['deck'].mode()[0]).tail()'''
        st.code(code)
        st.write(df1['deck'].fillna(df1['deck'].mode()[0]).tail())
        
        st.divider()

        st.subheader(f"{idx.getSubIdx()}NaN 값이 있는 데이터 제거하기 (dropna)")
        code = '''df1 = df.copy()
            df1.tail()'''
        st.code(code)
        df1 = df.copy()
        st.write(df1.tail())

        code = 'df1.tail()'
        st.code(code)
        st.write(df1.tail())
        st.divider()

        st.write(''':blue-background[dropna()]로 **1개 라도 NaN 값이 있는 행**은 제거할 수 있습니다. :blue-background[(how='any')]''')
        code = '''df1.dropna()'''
        df1.dropna()
        st.write(df1)
        st.divider()

        st.write('기본 옵션 값은 :blue-background[how=any]로 설정되어 있으며, 다음과 같이 변경할 수 있습니다.')
        st.write('- **any**: 1개 라도 NaN값이 존재시 drop')

        st.write('- **all**: 모두 NaN값이 존재시 drop')
        code = '''df1.dropna(how='all')'''
        st.code(code)
        df1.dropna(how='all')
        st.write(df1)

        st.header(f"{idx.getHeadIdx()}column 추가") ## 소단원03

        st.subheader(f"{idx.getSubIdx()}새로운 column 추가") 

        import seaborn as sns
        df = sns.load_dataset('titanic')
        import numpy as np

        code = '''df1 = df.copy()'''
        st.code(code)
        df1 = df.copy()
        code = '''df1.head()'''
        st.code(code)
        st.write(df1.head())
        st.divider()

        st.write('임의의 값을 대입하여 새로운 컬럼을 추가할 수 있습니다.')
        code = '''df1['VIP'] = True'''
        st.code(code)
        df1['VIP'] = True
        code = '''df1.head()'''
        st.code(code)
        st.write(df1.head())
        st.divider()

        st.write('중간에 컬럼을 추가하고 싶은 경우 :blue-background[insert()]를 활용할 수 있습니다.')
        st.write(':blue-background[insert(컬럼인덱스, 컬럼명, 값)]')
        st.code('''df1.insert(5, 'RICH', df1['fare'] > 100)''')
        st.write('- 5번째 위치에 RICH 컬럼을 추가')
        st.write('- fare 컬럼이 100보다 크면 True, 작으면 False 값을 채웁니다.')
        df1.insert(5, 'RICH', df1['fare'] > 100)
        code = '''df1.head()'''
        st.code(code)
        st.write(df1.head())
        st.divider()

        st.header(f"{idx.getHeadIdx()}데이터 삭제") ## 소단원04
        import seaborn as sns
        df = sns.load_dataset('titanic')
        df1 = df.copy()
        import numpy as np

        st.write('삭제는 **행(row) 삭제와 열(column) 삭제**로 구분할 수 있습니다.')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}행 (row) 삭제")
        st.write('행 삭제시 **index를 지정하여 삭제**합니다.')
        
        code = 'df1.drop(1)'
        st.code(code)
        st.write(df1.drop(1))
        
        st.divider()
        st.write('행 삭제시 **범위를 지정하여 삭제**할 수 있습니다.')
        code = 'df1.drop(np.arange(10))'
        st.code(code)
        st.write(df1.drop(np.arange(10)))

        st.write('**fancy indexing**을 활용하여 삭제할 수 있습니다.')
        code = 'df1.drop([1, 3, 5, 7, 9])'
        st.code(code)
        st.write(df1.drop([1, 3, 5, 7, 9]))
            
        st.divider()

        st.subheader(f"{idx.getSubIdx()}열 (column) 삭제")
        st.code('df1.head()')
        st.write(df1.head())
        st.divider()

        st.write('열 삭제시 **반드시** :blue-background[axis=1] **옵션을 지정**해야 합니다. 2번째 위치에 지정시 :blue-background[axis=]을 생략할 수 있습니다.')
        st.code('''df1.drop('class', axis=1).head()''')
        st.write(df1.drop('class', axis=1).head())
        st.divider()

        st.write('**다수의 컬럼(column) 삭제**도 가능합니다.')
        st.code('''df1.drop(['who', 'deck', 'alive'], axis=1)''')
        st.write(df1.drop(['who', 'deck', 'alive'], axis=1))
        st.divider()

        st.write('삭제된 내용을 바로 적용하려면')
        st.write('1. :blue-background[inplace=True]를 지정합니다.')
        st.write('2. 변수에 **재대입** 하여 결과를 반영합니다.')
        st.code('''df1.drop(['who', 'deck', 'alive'], axis=1, inplace=True)''')
        df1.drop(['who', 'deck', 'alive'], axis=1, inplace=True)
        st.code('df1.head()')
        st.write(df1.head())

        st.header(f"{idx.getHeadIdx()}column 연산")

        st.write('**컬럼(column) 과 컬럼 사이의 연산을 매우 쉽게 적용**할 수 있습니다.')
        
        import seaborn as sns
        df = sns.load_dataset('titanic')
        df1 = df.copy()

        st.code('''# 데이터프레임 복제\ndf1 = df.copy()''')
        st.write('**family(가족)**','의 총합은 **sibsp**컬럼과 **parch**의 합산으로 구할 수 있습니다.')

        st.code('''df1['family'] = df1['sibsp'] + df1['parch']''')
        df1['family'] = df1['sibsp'] + df1['parch']
        st.code('df1.head()')
        st.write(df1.head())
        st.divider()

        st.write('컬럼간 연산시 :blue-background[round()]를 사용하여 소수점 자릿수를 지정할 수 있습니다.')
        st.write('**round(숫자, 소수 몇 째자리)**')
        st.code('''df1['round'] = round(df1['fare'] / df1['age'], 2)''')
        df1['round'] = round(df1['fare'] / df1['age'], 2)
        st.code('df1.head()')
        st.write(df1.head())
        st.divider()

        st.write('연산시 1개의 컬럼이라도 **NaN 값을 포함하고 있다면 결과는 NaN** 이 됩니다.')
        st.code('''df1.loc[df1['age'].isnull(), 'deck':].head()''')
        st.write(df1.loc[df1['age'].isnull(), 'deck':].head())
        st.divider()
    
        st.header(f"{idx.getHeadIdx()}데이터 변환")

        st.write('- 데이터 변환에서는 category 타입으로 변환하는 방법에 대해 알아보겠습니다.')
        st.write('- category로 변경시 사용하는 메모리를 줄일 수 있습니다.')
        import seaborn as sns
        df = sns.load_dataset('titanic')
        import io
        st.divider()

        st.subheader(f"{idx.getSubIdx()}category 타입")
        
        st.code('''df1 = df.copy()\ndf1.head(2)''')
        df1 = df.copy()
        st.write(df1.head(2))
        st.divider()
        st.code('df1.info()')
        buffer = io.StringIO()
        df1.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)
        st.divider()

        st.subheader(f"{idx.getSubIdx()}category로 변경")
        st.write(':blue-background[category]로 변경시에는 Categories가 같이 출력됩니다.')
        st.code('''df1['who'].astype('category').head()''')
        st.write(df1['who'].astype('category').head())
        st.divider()

        st.write('변경사항을 적용합니다.')
        st.code('''df1['who'] = df1['who'].astype('category')''')
        df1['who'] = df1['who'].astype('category')
        st.divider()
        
        st.write(':blue-background[category]로 변경시 사용하는 메모리도 감소합니다.')
        st.code('df1.info()')
        buffer = io.StringIO()
        df1.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)
        st.divider()

    

    elif path == ("Pandas 기초", "Data 연결과 병합"):

        import pandas as pd

        st.header(f"{idx.getHeadIdx()}데이터 연결") ## 소단원01

        st.write('여러 개의 DataFrame으로 이루어진 데이터를 합치는 방법인 concat()(연결), merge()(병합)에 대하여 다뤄보겠습니다.')
        st.write('- :blue-background[concat()]은 2개 이상의 DataFrame을 행 혹은 열 방향으로 연결합니다.')
        st.write('- 실습을 위해 **아래의 버튼**을 클릭하여 2개의 데이터를 다운로드 해주세요')

        with open('data/유가정보/gas_first_2019.csv', "rb") as template_file:
            template_byte = template_file.read()
        with open('data/유가정보/gas_second_2019.csv', "rb") as template_file:
            template_sec = template_file.read()
        but1, but2 = st.columns([2, 6])
        with but1:
            button1 = st.download_button(label="download data",
                            type="primary",
                            data=template_byte,
                           file_name = "gas_first_2019.csv"
            )
        with but2:
            button2 = st.download_button(label="download data",
                            type="primary",
                            data=template_sec,
                           file_name = "gas_second_2019.csv"
            )
        st.write('다운 받은 데이터를 현재 작업 중인 jupyter 디렉터리로 이동해주세요')


        st.divider()

        st.write('**1월부터 6월까지 상반기** 데이터 로드')
        code = '''gas1 = pd.read_csv('gas_first_2019.csv', encoding='euc-kr')'''
        st.code(code)
        st.code('print(gas1.shape)\ngas1.head()')
        gas1 = pd.read_csv('data/유가정보/gas_first_2019.csv', encoding='euc-kr')
        st.write(gas1.shape)
        st.write(gas1.head())
        
        st.write('**7월 부터 12월 까지 하반기** 데이터 로드')
        code =  '''gas2 = pd.read_csv('gas_second_2019.csv', encoding='euc-kr')'''
        st.code(code)
        gas2 = pd.read_csv('data/유가정보/gas_second_2019.csv', encoding='euc-kr')
        code = '''print(gas2.shape)\ngas2.head()'''
        st.code(code)    
        st.write(gas2.shape)
        st.write(gas2.head())

        st.divider()

        st.write(':blue-background[concat()]은 DataFrame을 연결합니다.')
        st.write('단순하게 지정한 DataFrame을 이어서 연결합니다.')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}행 방향으로 연결")
        st.write('기본 값인 :blue-background[axis=0]이 지정되어 있고, 행 방향으로 연결합니다.')
        st.write('또한, 같은 column을 알아서 찾아서 데이터를 연결합니다.')

        st.code('pd.concat([gas1, gas2])')
        st.write(pd.concat([gas1, gas2]))
        st.divider()

        st.write('연결시 위와 같이 index가 초기화가 되지 않아 **전체 DataFrame의 개수와 index가 맞지 않는** 모습입니다.')
        st.code('''pd.concat([gas1, gas2]).iloc[90588:90593]''')
        st.write(pd.concat([gas1, gas2]).iloc[90588:90593])
        st.divider()

        st.write('연결 하면서 **index를 무시하고 연결** 할 수 있습니다.')
        st.code('''gas = pd.concat([gas1, gas2], ignore_index=True)\ngas''')
        gas = pd.concat([gas1, gas2], ignore_index=True)
        st.code('gas')
        st.write(gas)
        st.divider()

        st.write('합치고자 하는 데이터프레임의 **일부 컬럼이 누락되거나 순서가 바뀌어도** 알아서 같은 컬럼끼리 병합합니다.')
        code = '''gas11 = gas1[['지역', '주소', '상호', '상표', '휘발유']]\ngas22 = gas2[['상표', '번호', '지역', '상호', '주소', '경유', '휘발유']]'''
        st.code(code)
        gas11 = gas1[['지역', '주소', '상호', '상표', '휘발유']]
        gas22 = gas2[['상표', '번호', '지역', '상호', '주소', '경유', '휘발유']]
        st.code('gas11.head()')
        st.write(gas11.head())

        st.code('gas22.head()')
        st.write(gas22.head())
        st.divider()
        st.code('pd.concat([gas11, gas22], ignore_index=True)')
        st.write(pd.concat([gas11, gas22], ignore_index=True))
        st.divider()

        st.subheader(f"{idx.getSubIdx()}열 방향으로 연결")
        st.write('열(column) 방향으로 연결 가능하며, :blue-background[axis=1]로 지정합니다.')
        code='''# 실습을 위한 DataFrame 임의 분할\n +
            gas1 = gas.iloc[:, :5]\n +
            gas2 = gas.iloc[:, 5:]'''
        gas1 = gas.iloc[:, :5]
        gas2 = gas.iloc[:, 5:]
        st.code('gas1.head()')
        st.write(gas1.head())
        st.divider()
        st.code('gas2.head()')
        st.write(gas2.head())
        st.divider()

        st.write('같은 index 행끼리 연결됩니다.')
        st.code('pd.concat([gas1, gas2], axis=1)')
        st.write(pd.concat([gas1, gas2], axis=1))
        
        st.header(f"{idx.getHeadIdx()}데이터 병합") ## 소단원02
        import pandas as pd

        st.write('여러 개의 DataFrame으로 이루어진 데이터를 합치는 방법인 concat() - 연결, merge() - 병합에 대하여 알아보겠습니다.')
        st.write('- :blue-background[merge()]는 2개의 DataFrame을 특정 key를 기준으로 병합할 때 활용하는 메서드입니다.')

        st.write('서로 **다른 구성의 DataFrame이지만, 공통된 key값(컬럼)을 가지고 있다면 병합**할 수 있습니다.')
        with st.echo():
            df1 = pd.DataFrame({
            '고객명': ['박세리', '이대호', '손흥민', '김연아', '마이클조던'],
            '생년월일': ['1980-01-02', '1982-02-22', '1993-06-12', '1988-10-16', '1970-03-03'],
            '성별': ['여자', '남자', '남자', '여자', '남자']})
            df1
        

        with st.echo():
            df2 = pd.DataFrame({
            '고객명': ['김연아', '박세리', '손흥민', '이대호', '타이거우즈'],
            '연봉': ['2000원', '3000원', '1500원', '2500원', '3500원']})
            df2
        st.divider()
        with st.echo():
            pd.merge(df1, df2)
        st.write(pd.merge(df1, df2))
        
        st.divider()

        st.subheader(f"{idx.getSubIdx()}병합하는 방법 4가지")

        st.write(':blue-background[how] 옵션 값을 지정하여 4가지 방식으로 병합을 할 수 있으며, 각기 다른 결과를 냅니다.')
        st.write('''- **how** : '{':blue-background[left], :blue-background[right], :blue-background[outer], :blue-background[inner]'}',''')
        st.write('- **default**로 설정된 값은 :blue-background[inner] 입니다.')
        st.code('''# how='inner' 입니다.\npd.merge(df1, df2)''')
        st.write(pd.merge(df1, df2))
        st.divider()

        st.code('''pd.merge(df1, df2, how='left')''')
        st.write(pd.merge(df1, df2, how='left'))
        st.divider()

        st.code('''pd.merge(df1, df2, how='right')''')
        st.write(pd.merge(df1, df2, how='right'))
        st.divider()

        st.code('''pd.merge(df1, df2, how='outer')''')
        st.write(pd.merge(df1, df2, how='outer'))
        st.divider()

        st.subheader(f"{idx.getSubIdx()}병합하려는 컬럼의 이름이 다른 경우")
        with st.echo():
            df1 = pd.DataFrame({
            '이름': ['박세리', '이대호', '손흥민', '김연아', '마이클조던'],
            '생년월일': ['1980-01-02', '1982-02-22', '1993-06-12', '1988-10-16', '1970-03-03'],
            '성별': ['여자', '남자', '남자', '여자', '남자']})
            df1
        st.divider()

        with st.echo():
            df2 = pd.DataFrame({
            '고객명': ['김연아', '박세리', '손흥민', '이대호', '타이거우즈'],
            '연봉': ['2000원', '3000원', '1500원', '2500원', '3500원']})
            df2
        st.divider()

        st.write(':blue-background[left_on]과 :blue-background[right_on]을 지정합니다.')
        st.write('이름과 고객명 컬럼이 모두 drop되지 않고 살아 있음을 확인할 수 있습니다.')
        code = '''pd.merge(df1, df2, left_on='이름', right_on='고객명')'''
        st.code(code)
        st.write(pd.merge(df1, df2, left_on='이름', right_on='고객명'))

    elif path == ("Pandas 기초", "Static"):
        
        st.header(f"{idx.getHeadIdx()}기술 통계") # 소단원01

        st.write('**통계**는 데이터 분석에서 굉장히 중요한 요소입니다.')
        st.write('데이터에 대한 통계 계산식을 Pandas 함수로 제공하기 때문에 쉽게 통계 값을 산출할 수 있습니다.')

        pandas_dataset()

        import pandas as pd
        import seaborn as sns
        df = sns.load_dataset('titanic')
        # for col in df.select_dtypes(include=['object']):
        #     df[col] = df[col].astype('category')

        st.subheader(f"{idx.getSubIdx()}describe() - 요약통계")

        st.write('전반적인 주요 통계를 확인할 수 있습니다.')
        st.write('기본 값으로 **수치형(Numberical) 컬럼**에 대한 통계표를 보여줍니다.')

        st.write('- **count**: 데이터 개수')
        st.write('- **mean**: 평균')
        st.write('- **std**: 표준편차')
        st.write('- **min**: 최솟값')
        st.write('- **max**: 최대값')

        code = 'df.describe()'
        st.code(code)
        st.write(df.describe())
        st.divider()

        st.write('**문자열 컬럼에 대한 통계표**도 확인할 수 있습니다.')
        st.write('- **count**: 데이터 개수')
        st.write('- **unique**: 고유 데이터 값 개수')
        st.write('- **top**: 가장 많이 출현한 데이터 개수')
        st.write('- **freq**: 가장 많이 출현한 데이터의 빈도수')

        ## warning 문 뜸
        # st.header('문자열 칼럼에 대한 요약통계')
        st.code('''df.describe(include='object')''')
        st.write(df.describe(include='object'))
        st.divider()

        import seaborn as sns
        # dataset = sns.load_dataset('titanic')
        # # df 결측치 제거
        # df = dataset.dropna()
        df = sns.load_dataset('titanic')
        # for col in df.select_dtypes(include=['object']):
        #     df[col] = df[col].astype('category')

        st.subheader(f"{idx.getSubIdx()}count() - 개수")

        st.write('데이터의 개수')
        st.write('DataFrame 전체의 개수를 구하는 경우')

        st.code('df.count()')
        st.write(df.count())

        st.write('단일 column의 데이터 개수를 구하는 경우')
        st.code('''df['age'].count()''')
        st.write(df['age'].count())

        st.divider()

        st.subheader(f"{idx.getSubIdx()}mean() - 평균")

        st.write('데이터의 **평균**')
        st.write('DataFrame 평균')

        st.code('df')
        st.write(df)

        st.write(':blue-background[age] 컬럼에 대한 평균')
        st.code('''df['age'].mean()''')
        st.write(df['age'].mean())

        st.divider()

        st.subheader(f"{idx.getSubIdx()}mean - 조건별 평균")
        st.write('성인 남성의 나이의 평균 구하기')
        code = '''condition = (df['adult_male'] == True)\ndf.loc[condition, 'age'].mean()'''
        st.code(code)
        condition = (df['adult_male'] == True)
        st.write(df.loc[condition, 'age'].mean()    )

        st.divider()

        st.subheader(f"{idx.getSubIdx()}median() - 중앙값")
        st.write('데이터의 중앙 값을 출력 합니다. 데이터를 **오름차순 정렬하여 중앙에 위치한 값**입니다.')
        st.write('이상치(outlier)가 존재하는 경우, mean()보다 median()을 대표값으로 더 선호합니다.')

        st.code('pd.Series([1, 2, 3, 4, 5]).median()')
        st.write(pd.Series([1, 2, 3, 4, 5]).median())
        
        st.code('pd.Series([4, 5, 1, 2, 3]).median()')
        st.write(pd.Series([4, 5, 1, 2, 3]).median())

        st.code('pd.Series([1, 2, 3, 4, 5, 6]).median()')
        st.write(pd.Series([1, 2, 3, 4, 5, 6]).median())

        st.write('**짝수** 개의 데이터가 있는 경우에는 **가운데 2개 중앙 데이터의 평균 값을 출력** 합니다.')
        st.code('pd.Series([1, 2, 3, 4, 5, 6]).median()')
        st.write(pd.Series([1, 2, 3, 4, 5, 6]).median())
        st.divider()

        st.write('나이의 평균(mean)과 중앙값(median)은 약간의 **차이가 있음**을 확인할 수 있습니다.')

        code='''print(f"나이 평균: {df['age'].mean():.5f}\n\t나이 중앙값: {df['age'].median()}\n\t차이: {df['age'].mean() - df['age'].median():.5f}")'''
        st.code(code)
        st.write((f"나이 평균: {df['age'].mean():.5f}\n\t나이 중앙값: {df['age'].median()}\n\t차이: {df['age'].mean() - df['age'].median():.5f}"))

        st.divider()

        st.subheader(f"{idx.getSubIdx()}sum() - 합계")

        st.write('데이터의 **합계**입니다. 문자열 column은 모든 데이터가 붙어서 출력될 수 있습니다.')
        st.code('''df.loc[:, ['age', 'fare']].sum()''')
        st.write(df.loc[:, ['age', 'fare']].sum())

        st.write('단일 column에 대한 **합계 출력**')
        st.code('''df['fare'].sum()''')
        st.write(df['fare'].sum())   

        st.divider()

        st.subheader(f"{idx.getSubIdx()}var() - 분산")

        st.latex(r'''
        \text{분산} = \frac{\sum_{i=1}^n (X_i - \bar{X})^2}{n-1}
        ''')

        st.code('''
            # 평균
            fare_mean = df['fare'].values.mean()
            # 분산
            my_var = ((df['fare'].values - fare_mean) ** 2).sum() / (df['fare'].count() - 1)
            my_var''')
        fare_mean = df['fare'].values.mean()
        my_var = ((df['fare'].values - fare_mean) ** 2).sum() / (df['fare'].count() - 1)
        st.write(my_var)
        st.divider()
        st.subheader(f"{idx.getSubIdx()}std() - 표준편차")
        st.latex(r'''
        \text{표준편차} = \sqrt{\text{분산}} = \sqrt{\frac{\sum_{i=1}^n (X_i - \bar{X})^2}{n-1}}
                ''')
        st.write('분산(var)의 제곱근')
        st.code(
            '''import numpy as np\nnp.sqrt(df['fare'].var())''')
        import numpy as np
        st.write(np.sqrt(df['fare'].var()))
        st.code('''df['fare'].std()''')
        st.write(df['fare'].std())
        st.divider()

        st.subheader(f"{idx.getSubIdx()}min() - 최소값, max() - 최대값")
        st.code(
         '''# 최소값
            df['age'].min()
            # 최대값
            df['age'].max()''')
        st.write(df['age'].min())
        st.write(df['age'].max())
        st.divider()

        st.subheader(f"{idx.getSubIdx()}mode() - 최빈값")
        st.write('최빈값은 **가장 많이 출현한 데이터**를 의미합니다.')
        st.code('''df['who'].mode()''')
        st.write(df['who'].mode())   

        st.write('카테고리형 데이터에도 적용 가능합니다.')
        st.code('''df['deck'].mode()''')
        st.write(df['deck'].mode())
        st.divider()
        
        st.header(f"{idx.getHeadIdx()}고급 통계")

        st.write('"고급 통계 함수"는 기술 통계보다 더 복잡한 연산이나 특수한 목적을 가진 함수입니다.')

        pandas_dataset()
        import pandas as pd
        import seaborn as sns
        df = sns.load_dataset('titanic')

        
        st.subheader(f"{idx.getSubIdx()}agg - aggregation: 통합 통계 적용 (복수의 통계 함수 적용)")
        st.write('단일 컬럼에 agg 적용')
        st.code('''df['age'].agg(['min', 'max', 'count','mean'])''')
        st.write(df['age'].agg(['min', 'max', 'count','mean']))       

        st.write('복수의 컬럼에 agg 적용')
        st.code('''df[['age', 'fare']].agg(['min', 'max', 'count', 'mean'])''')
        st.write(df[['age', 'fare']].agg(['min', 'max', 'count', 'mean']))
    
        st.divider()

        st.subheader(f"{idx.getSubIdx()}quantile() - 분위")
        st.write('**Quantile이란 주어진 데이터를 동등한 크기로 분할하는 지점**Quantile이란 주어진 데이터를 동등한 크기로 분할하는 지점을 말합니다.')
        st.write('10%의 경우 0.1을, 80%의 경우 0.8을 대입하여 값을 구합니다.')
        st.code('''# 10% quantile\ndf['age'].quantile(0.1)''')
        st.write(df['age'].quantile(0.1))
        st.divider()
        
        st.code('''# 80% quantile\ndf['age'].quantile(0.8)''')
        st.write(df['age'].quantile(0.8))

        st.divider()

        st.subheader(f"{idx.getSubIdx()}unique() - 고유값, nunique() - 고유값 개수")
        st.write('고유값과 고유값의 개수를 구하고자 할 때 사용합니다.')

        st.write('**unique()**')
        st.code('''df['who'].unique()''')
        st.write(df['who'].unique())   
        st.divider()
        st.write('**nonique()**: 고유값의 개수를 출력합니다.')
        st.code('''df['who'].nunique()''')
        st.write(df['who'].nunique())
        st.divider()

        st.subheader(f"{idx.getSubIdx()}cumsum() - 누적합, cumprod() - 누적곱")

        st.write('누적되는 합계를 구할 수 있습니다.')
        st.code('''df['age'].cumsum()''')
        st.write(df['age'].cumsum())
        st.divider()

        st.write('누적되는 곱도 구할 수 있으나, 일반적으로 **값이 너무 커지므로 잘 활용하지는 않습니다.**')

        st.code('''df['age'].cumprod()''')
        st.write(df['age'].cumprod())
        st.divider()

        st.subheader(f"{idx.getSubIdx()}corr() - 상관관계")
        st.write(':blue-background[corr()]로 컬럼(column)별 **상관관계**를 확인할 수 있습니다.')

        st.write('- **-1~1 사이의 범위**를 가집니다.')
        st.write('- **-1에 가까울수록 반비례** 관계, **1에 가까울수록 정비례** 관계를 의미합니다.')
        code = '''
            numeric_df = df[['survived','age', 'pclass','sibsp', 'parch','fare']]
            numeric_df.corr()'''
        st.code(code)
        numeric_df = df[['survived','age', 'pclass','sibsp', 'parch','fare']]
        st.write(numeric_df.corr())

        st.divider()
        st.write('**특정 컬럼에 대한 상관관계**를 확인할 수 있습니다.')
        st.code('''numeric_df.corr()['survived']''')
        st.write(numeric_df.corr()['survived']) 
        st.divider()
    
    ### Matplotlib 컨텐츠 작성
    elif path == ("Matplotlib 기초", "Matplotlib 기본"):
        st.header(f"{idx.getHeadIdx()}기본 사용")
        st.write("Matplotlib 라이브러리를 이용해서 그래프를 그리는 일반적인 방법에 대해 소개합니다.")
        st.subheader(f"{idx.getSubIdx()}기본 그래프 그리기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4])
            plt.show()
        st.pyplot(plt)
        plt.close()
        st.write("plot() 함수는 리스트의 값들이 y 값들이라고 가정하고, x 값 [0, 1, 2, 3]을 자동으로 만들어냅니다.")
        st.write("matplotlib.pyplot 모듈의 show() 함수는 그래프를 화면에 나타나도록 합니다.")
        st.divider()
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
            plt.show()
        st.write("plot() 함수는 다양한 기능을 포함하고 있어서, 임의의 개수의 인자를 받을 수 있습니다.")
        st.write("예를 들어, 아래와 같이 입력하면, x-y 값을 그래프로 나타낼 수 있습니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}스타일 지정하기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [1, 4, 9, 16], 'ro')
            plt.axis([0, 6, 0, 20])
            plt.show()
        st.write("x, y 값 인자에 대해 선의 색상과 형태를 지정하는 포맷 문자열 (Format string)을 세번째 인자에 입력할 수 있습니다.")
        st.write("포맷 문자열 ‘ro’는 빨간색 (‘red’)의 원형 (‘o’) 마커를 의미합니다. 이후 스타일 관련 단원에서 더 자세하게 학습할 수 있습니다.")
        st.write("matplotlib.pyplot 모듈의 axis() 함수를 이용해서 축의 범위 [xmin, xmax, ymin, ymax]를 지정했습니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}여러 개의 그래프 그리기")
        st.write("이후 다중 그래프 그리기 단원에서 자세히 학습할 수 있습니다.")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            # 200ms 간격으로 균일하게 샘플된 시간
            t = np.arange(0., 5., 0.2)

            # 빨간 대쉬, 파란 사각형, 녹색 삼각형
            plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
            plt.show()
        st.pyplot(plt)
        plt.close()

        st.header(f"{idx.getHeadIdx()}숫자 입력하기")
        st.subheader(f"{idx.getSubIdx()}기본 사용")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([2, 3, 5, 10])
            plt.show()
        st.write("`plot([2, 3, 5, 10])`와 같이 하나의 리스트 형태로 값들을 입력하면 y 값으로 인식합니다.")
        # st.write("**plot((2, 3, 5, 10))** 또는 **plot(np.array(\[2, 3, 5, 10\]))**와 같이 파이썬 튜플 또는 Numpy 어레이의 형태로도 데이터를 입력할 수 있습니다.")
        st.write("""`plot((2, 3, 5, 10))` 또는 `plot(np.array([2, 3, 5, 10]))`와 같이 파이썬 튜플 또는 Numpy 어레이의 형태로도 데이터를 입력할 수 있습니다.""")

        st.write("**x** 값은 기본적으로 **[0, 1, 2, 3]** 이 되어서, **점 (0, 2), (1, 3), (2, 5), (3, 10)** 를 잇는 아래와 같은 꺾은선 그래프가 나타납니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}x, y 값 입력하기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [2, 3, 5, 10])
            plt.show()
        st.write("plot() 함수에 두 개의 리스트를 입력하면 순서대로 x, y 값들로 인식해서 점 (1, 2), (2, 3), (3, 5), (4, 10)를 잇는 꺾은선 그래프가 나타납니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}레이블이 있는 데이터 사용하기")
        with st.echo(): 
            import matplotlib.pyplot as plt

            data_dict = {'data_x': [1, 2, 3, 4, 5], 'data_y': [2, 3, 5, 10, 8]}

            plt.plot('data_x', 'data_y', data=data_dict)
            plt.show()
        st.write("파이썬 딕셔너리와 같이 레이블이 있는 데이터를 그래프로 나타낼 수 있습니다.")
        st.write("예제에서와 같이, 먼저 plot() 함수에 데이터의 레이블 (딕셔너리의 키)을 입력해주고, data 파라미터에 딕셔너리를 지정해줍니다.")
        st.pyplot(plt)
        plt.close()
    
    elif path == ("Matplotlib 기초", "그래프 그리기"):
        st.header(f"{idx.getHeadIdx()}그래프 그리기")
        st.subheader(f"{idx.getSubIdx()}단일 그래프")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            # data 생성
            data = np.arange(1, 100)
            # plot
            plt.plot(data)
            # 그래프를 보여주는 코드
            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}다중 그래프(Multiple graphs)")
        st.write("1개의 canvas 안에 다중 그래프 그리기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            data = np.arange(1, 51)
            plt.plot(data)

            data2 = np.arange(51, 101)
            # plt.figure()
            plt.plot(data2)

            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.write("2개의 figure로 나누어서 다중 그래프 그리기")
        st.write("◾ figure()는 새로운 그래프 canvas를 생성합니다.")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            data = np.arange(100, 201)
            plt.plot(data)

            data2 = np.arange(200, 301)
            # figure()는 새로운 그래프를 생성합니다.
            plt.figure()
            plt.plot(data2)

            plt.show()
        st.pyplot(plt)
        plt.close()

        st.header(f"{idx.getHeadIdx()}여러개의 Plot")
        st.subheader(f"{idx.getSubIdx()}여러개의 Plot을 그리는 방법(Subplot)")
        st.write("subplot(row, column, index)")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            data = np.arange(100, 201)
            plt.subplot(2, 1, 1)
            plt.plot(data)

            data2 = np.arange(200, 301)
            plt.subplot(2, 1, 2)
            plt.plot(data2)

            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.write("위의 코드와 동일하나 , (콤마)를 제거한 상태")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            data = np.arange(100, 201)
            # 콤마를 생략하고 row, column, index로 작성가능
            # 211 -> row: 2, col: 1, index: 1
            plt.subplot(211)
            plt.plot(data)

            data2 = np.arange(200, 301)
            plt.subplot(212)
            plt.plot(data2)

            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()

        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            data = np.arange(100, 201)
            plt.subplot(1, 3, 1)
            plt.plot(data)

            data2 = np.arange(200, 301)
            plt.subplot(1, 3, 2)
            plt.plot(data2)

            data3 = np.arange(300, 401)
            plt.subplot(1, 3, 3)
            plt.plot(data3)

            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}여러개의 plot을 그리는 방법(subplots)")
        st.write("**s가 더 붙습니다.**")
        st.write("plt.subplots(행의 갯수, 열의 갯수)")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            data = np.arange(1, 51)
            # data 생성

            # 밑 그림
            fig, axes = plt.subplots(2, 3)

            axes[0, 0].plot(data)
            axes[0, 1].plot(data * data)
            axes[0, 2].plot(data ** 3)
            axes[1, 0].plot(data % 10)
            axes[1, 1].plot(-data)
            axes[1, 2].plot(data // 20)

            plt.tight_layout()
            plt.show()
        st.pyplot(plt)
        plt.close()

    elif path == ("Matplotlib 기초", "그래프에 text"):
        st.header(f"{idx.getHeadIdx()}Title")
        st.write("**matplotlib.pyplot** 모듈의 **title()** 함수를 이용해서 그래프의 타이틀 (Title)을 설정할 수 있습니다.")
        st.write("그래프의 타이틀을 표시하고 위치를 조절하는 방법, 그리고 타이틀의 폰트와 스타일을 설정하는 방법에 대해 알아봅니다.")
        
        st.subheader(f"{idx.getSubIdx()}기본 사용")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            x = np.arange(0, 2, 0.2)

            plt.plot(x, x, 'bo')
            plt.plot(x, x**2, color='#e35f62', marker='*', linewidth=2)
            plt.plot(x, x**3, color='forestgreen', marker='^', markersize=9)

            plt.tick_params(axis='both', direction='in', length=3, pad=6, labelsize=14)
            plt.title('Graph Title')

            plt.show()
        st.write("**title()** 함수를 이용해서 그래프의 타이틀을 ‘Graph Title’로 설정했습니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}위치와 오프셋 지정하기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            x = np.arange(0, 2, 0.2)

            plt.plot(x, x, 'bo')
            plt.plot(x, x**2, color='#e35f62', marker='*', linewidth=2)
            plt.plot(x, x**3, color='forestgreen', marker='^', markersize=9)

            plt.tick_params(axis='both', direction='in', length=3, pad=6, labelsize=14)
            plt.title('Graph Title', loc='right', pad=20)

            plt.show()
        st.write("**plt.title()** 함수의 **loc** 파라미터를 **‘right’** 로 설정하면, 타이틀이 그래프의 오른쪽 위에 나타나게 됩니다.")
        st.write("{‘left’, ‘center’, ‘right’} 중 선택할 수 있으며 디폴트는 **‘center’** 입니다.")
        st.write("**pad** 파라미터는 **타이틀과 그래프와의 간격을** 포인트 단위로 설정합니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}폰트 지정하기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            x = np.arange(0, 2, 0.2)

            plt.plot(x, x, 'bo')
            plt.plot(x, x**2, color='#e35f62', marker='*', linewidth=2)
            plt.plot(x, x**3, color='forestgreen', marker='^', markersize=9)

            plt.tick_params(axis='both', direction='in', length=3, pad=6, labelsize=14)
            plt.title('Graph Title', loc='right', pad=20)

            title_font = {
                'fontsize': 16,
                'fontweight': 'bold'
            }
            plt.title('Graph Title', fontdict=title_font, loc='left', pad=20)

            plt.show()
        st.write("**fontdict** 파라미터에 딕셔너리 형태로 폰트 스타일을 설정할 수 있습니다.")
        st.write("**‘fontsize’** 를 16으로, **‘fontweight’** 를 ‘bold’로 설정했습니다.")
        st.write("**‘fontsize’** 는 포인트 단위의 숫자를 입력하거나 ‘smaller’, ‘x-large’ 등의 상대적인 설정을 할 수 있습니다.")
        st.write("**‘fontweight’** 에는 {‘normal’, ‘bold’, ‘heavy’, ‘light’, ‘ultrabold’, ‘ultralight’}와 같이 설정할 수 있습니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}타이틀 얻기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            x = np.arange(0, 2, 0.2)

            plt.plot(x, x, 'bo')
            plt.plot(x, x**2, color='#e35f62', marker='*', linewidth=2)
            plt.plot(x, x**3, color='forestgreen', marker='^', markersize=9)

            plt.tick_params(axis='both', direction='in', length=3, pad=6, labelsize=14)
            title_right = plt.title('Graph Title', loc='right', pad=20)

            title_font = {
                'fontsize': 16,
                'fontweight': 'bold'
            }
            title_left = plt.title('Graph Title', fontdict=title_font, loc='left', pad=20)

            print(title_left.get_position())
            print(title_left.get_text())

            print(title_right.get_position())
            print(title_right.get_text())

            plt.show()
        st.write("**plt.title()** 함수는 타이틀을 나타내는 Matplotlib **text** 객체를 반환합니다.")
        st.pyplot(plt)
        plt.close()
        st.write("**get_position()** 과 **get_text()** 메서드를 사용해서 텍스트 위치와 문자열을 얻을 수 있습니다.")
        code = '''(0.0, 1.0)
Graph Title
(1.0, 1.0)
Graph Title'''
        st.code(code, language="python")

        st.header(f"{idx.getHeadIdx()}Text 삽입")
        st.write("matplotlib.pyplot 모듈의 **text()** 함수는 그래프의 적절한 위치에 텍스트를 삽입하도록 합니다.")
        st.write("**text()** 함수를 사용해서 그래프 영역에 텍스트를 삽입하고, 다양하게 꾸미는 방법에 대해 소개합니다.")
        st.write("이 페이지에서 사용하는 히스토그램 예제는 :blue[Histogram] 페이지를 참고하세요.")

        st.subheader(f"{idx.getSubIdx()}기본 사용")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            a = 2.0 * np.random.randn(10000) + 1.0
            b = np.random.standard_normal(10000)
            c = 20.0 * np.random.rand(5000) - 10.0

            plt.hist(a, bins=100, density=True, alpha=0.7, histtype='step')
            plt.text(1.0, 0.35, '2.0*np.random.randn(10000)+1.0')
            plt.hist(b, bins=50, density=True, alpha=0.5, histtype='stepfilled')
            plt.text(2.0, 0.20, 'np.random.standard_normal(10000)')
            plt.hist(c, bins=100, density=True, alpha=0.9, histtype='step')
            plt.text(5.0, 0.08, 'np.random.rand(5000)-10.0')
            plt.show()
        st.write("**text()** 함수를 이용해서 3개의 히스토그램 그래프에 설명을 위한 텍스트를 각각 추가했습니다.")
        st.write("**text()** 에 그래프 상의 x 위치, y 위치, 그리고 삽입할 텍스트를 순서대로 입력합니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}텍스트 스타일 설정하기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            a = 2.0 * np.random.randn(10000) + 1.0
            b = np.random.standard_normal(10000)
            c = 20.0 * np.random.rand(5000) - 10.0

            font1 = {'family': 'serif',
                'color':  'darkred',
                'weight': 'normal',
                'size': 16}

            font2 = {'family': 'Times New Roman',
                'color':  'blue',
                'weight': 'bold',
                'size': 12,
                'alpha': 0.7}

            font3 = {'family': 'Arial',
                'color':  'forestgreen',
                'style': 'italic',
                'size': 14}

            plt.hist(a, bins=100, density=True, alpha=0.7, histtype='step')
            plt.text(1.0, 0.35, 'np.random.randn()', fontdict=font1)
            plt.hist(b, bins=50, density=True, alpha=0.5, histtype='stepfilled')
            plt.text(2.0, 0.20, 'np.random.standard_normal()', fontdict=font2)
            plt.hist(c, bins=100, density=True, alpha=0.9, histtype='step')
            plt.text(5.0, 0.08, 'np.random.rand()', fontdict=font3)

            plt.show()
        st.write("**fontdict** 키워드를 이용하면 font의 종류, 크기, 색상, 투명도, weight 등의 텍스트 스타일을 설정할 수 있습니다.")
        st.write("font1, font2, font3과 같이 미리 지정한 폰트 딕셔너리를 fontdict 키워드에 입력해줍니다.")
        st.write("예제에서는 ‘family’, ‘color’, ‘weight’, ‘size’, ‘alpha’, ‘style’ 등과 같은 텍스트 속성을 사용했습니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}텍스트 회전하기")
        with st.echo():
            plt.hist(a, bins=100, density=True, alpha=0.7, histtype='step')
            plt.text(-3.0, 0.15, 'np.random.randn()', fontdict=font1, rotation=85)
            plt.hist(b, bins=50, density=True, alpha=0.5, histtype='stepfilled')
            plt.text(2.0, 0.0, 'np.random.standard_normal()', fontdict=font2, rotation=-60)
            plt.hist(c, bins=100, density=True, alpha=0.9, histtype='step')
            plt.text(-10.0, 0.08, 'np.random.rand()', fontdict=font3)
            plt.show()
        st.write("rotation 키워드를 이용해서 텍스트를 회전할 수 있습니다.")
        st.pyplot(plt)
        plt.close()
    
    elif path == ("Matplotlib 기초", "그래프 세부 속성"):
        st.header(f"{idx.getHeadIdx()}축 레이블(Label) 설정하기")
        st.write("**matplotlib.pyplot** 모듈의 **xlabel(), ylabel()** 함수를 사용하면 그래프의 x, y 축에 대한 레이블을 표시할 수 있습니다.")
        st.write("xlabel(), ylabel() 함수를 사용해서 그래프의 축에 레이블을 표시하는 방법에 대해 소개합니다.")

        st.subheader(f"{idx.getSubIdx()}기본 사용")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
            plt.xlabel('X-Label')
            plt.ylabel('Y-Label')
            plt.show()
        st.write("**xlabel(), ylabel()** 함수에 문자열을 입력하면, 아래 그림과 같이 각각의 축에 레이블이 표시됩니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}여백 지정하기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [2, 3, 5, 10])
            plt.xlabel('X-Axis', labelpad=15)
            plt.ylabel('Y-Axis', labelpad=20)
            plt.show()
        st.write("**xlabel(), ylabel()** 함수의 **labelpad** 파라미터는 축 레이블의 **여백 (Padding)** 을 지정합니다.")
        st.write("예제에서는 X축 레이블에 대해서 15pt, Y축 레이블에 대해서 20pt 만큼의 여백을 지정했습니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}폰트 설정하기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [2, 3, 5, 10])
            plt.xlabel('X-Axis', labelpad=15, fontdict={'family': 'serif', 'color': 'b', 'weight': 'bold', 'size': 14})
            plt.ylabel('Y-Axis', labelpad=20, fontdict={'family': 'fantasy', 'color': 'deeppink', 'weight': 'normal', 'size': 'xx-large'})
            plt.show()
        st.write("**xlabel(), ylabel()** 함수의 **fontdict** 파라미터를 사용하면 축 레이블의 폰트 스타일을 설정할 수 있습니다.")
        st.write("예제에서는 ‘family’, ‘color’, ‘weight’, ‘size’와 같은 속성을 사용해서 축 레이블 텍스트를 설정했습니다.")
        st.write("아래와 같이 작성하면 폰트 스타일을 편리하게 재사용할 수 있습니다.")
        with st.echo():
            import matplotlib.pyplot as plt

            font1 = {'family': 'serif',
                    'color': 'b',
                    'weight': 'bold',
                    'size': 14
                    }

            font2 = {'family': 'fantasy',
                    'color': 'deeppink',
                    'weight': 'normal',
                    'size': 'xx-large'
                    }

            plt.plot([1, 2, 3, 4], [2, 3, 5, 10])
            plt.xlabel('X-Axis', labelpad=15, fontdict=font1)
            plt.ylabel('Y-Axis', labelpad=20, fontdict=font2)
            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}위치 저장하기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [2, 3, 5, 10])
            plt.xlabel('X-Axis', loc='right')
            plt.ylabel('Y-Axis', loc='top')
            plt.show()
        st.write("**xlabel()** 함수의 **loc** 파라미터는 X축 레이블의 위치를 지정합니다. ({‘left’, ‘center’, ‘right’})")
        st.write("**ylabel()** 함수의 **loc** 파라미터는 Y축 레이블의 위치를 지정합니다. ({‘bottom’, ‘center’, ‘top’})")
        st.write("이 파라미터는 **Matplotlib 3.3** 이후 버전부터 적용되었습니다.")
        st.pyplot(plt)
        plt.close()

        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3], [3, 6, 9])
            plt.plot([1, 2, 3], [2, 4, 9])
            # 타이틀 & font 설정
            plt.title("이것은 타이틀 입니다", fontproperties=prop)

            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()
        
        st.subheader(f"{idx.getSubIdx()}X, Y 축 Tick 설정(rotation)")
        st.write("Tick은 X, Y축에 위치한 눈금을 말합니다.")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            plt.plot(np.arange(10), np.arange(10)*2)
            plt.plot(np.arange(10), np.arange(10)**2)
            plt.plot(np.arange(10), np.log(np.arange(10)))

            # 타이틀 & font 설정
            plt.title('X, Y 틱을 조정합니다', fontsize=10, fontproperties=prop)

            # X축 & Y축 Label 설정
            plt.xlabel('X축', fontsize=10, fontproperties=prop)
            plt.ylabel('Y축', fontsize=10, fontproperties=prop)

            # X tick, Y tick 설정
            plt.xticks(rotation=90)
            plt.yticks(rotation=30)

            plt.show()
        st.pyplot(plt)
        plt.close()

        st.header(f"{idx.getHeadIdx()}범례(Legend) 설정")
        st.write("**범례 (Legend)** 는 그래프에 데이터의 종류를 표시하기 위한 텍스트입니다.")
        st.write("**matplotlib.pyplot** 모듈의 **legend()** 함수를 사용해서 그래프에 범례를 표시할 수 있습니다.")
        st.write("그래프에 다양한 방식으로 범례를 표시하는 방법에 대해 소개합니다.")

        st.subheader(f"{idx.getSubIdx()}기본 사용")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [2, 3, 5, 10], label='Price ($)')
            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')
            plt.legend()

            plt.show()
        st.write("그래프 영역에 범례를 나타내기 위해서는 우선 **plot()** 함수에 **label** 문자열을 지정하고, **matplotlib.pyplot** 모듈의 **legend()** 함수를 호출합니다.")
        st.write("아래와 같이 그래프의 적절한 위치에 데이터를 설명하는 범례가 나타납니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}위치 지정하기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [2, 3, 5, 10], label='Price ($)')
            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')
            # plt.legend(loc=(0.0, 0.0))
            # plt.legend(loc=(0.5, 0.5))
            plt.legend(loc=(1.0, 1.0))

            plt.show()
            st.write("xlabel(), ylabel() 함수의 labelpad 파라미터는 축 레이블의 여백 (Padding)을 지정합니다.")
            st.write("**legend()** 함수의 **loc** 파라미터를 이용해서 범례가 표시될 위치를 설정할 수 있습니다.")
            st.write("**loc** 파라미터를 숫자 쌍 튜플로 지정하면, 해당하는 위치에 범례가 표시됩니다.")
            st.write("**loc=(0.0, 0.0)**은 데이터 영역의 왼쪽 아래, **loc=(1.0, 1.0)**은 데이터 영역의 오른쪽 위 위치입니다.")
            st.write("**loc** 파라미터에 여러 숫자 쌍을 입력하면서 범례의 위치를 확인해보세요.")
        st.pyplot(plt)
        plt.close()
        st.divider()
        
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [2, 3, 5, 10], label='Price ($)')
            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')
            plt.legend(loc='lower right')

            plt.show()
        st.write("**loc** 파라미터는 예제에서와 같이 문자열로 지정할 수도 있고, 숫자 코드를 사용할 수도 있습니다.")
        st.write("**loc=’lower right’** 와 같이 지정하면 아래와 같이 오른쪽 아래에 범례가 표시됩니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}열 개수 지정하기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [2, 3, 5, 10], label='Price ($)')
            plt.plot([1, 2, 3, 4], [3, 5, 9, 7], label='Demand (#)')
            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')
            # plt.legend(loc='best')          # ncol = 1
            plt.legend(loc='best', ncol=2)    # ncol = 2

            plt.show()
        st.write("**legend()** 함수의 **ncol** 파라미터는 범례에 표시될 텍스트의 열의 개수를 지정합니다.")
        st.write("기본적으로 아래 첫번째 그림과 같이 범례 텍스트는 1개의 열로 표시되며, **ncol=2** 로 지정하면 아래 두번째 그림과 같이 표시됩니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}폰트 크기 지정하기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [2, 3, 5, 10], label='Price ($)')
            plt.plot([1, 2, 3, 4], [3, 5, 9, 7], label='Demand (#)')
            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')
            # plt.legend(loc='best')
            plt.legend(loc='best', ncol=2, fontsize=14)

            plt.show()
        st.write("**legend()** 함수의 **fontsize** 파라미터는 범례에 표시될 폰트의 크기를 지정합니다.")
        st.write("폰트 크기를 14로 지정했습니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}범례 테두리 꾸미기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [2, 3, 5, 10], label='Price ($)')
            plt.plot([1, 2, 3, 4], [3, 5, 9, 7], label='Demand (#)')
            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')
            # plt.legend(loc='best')
            plt.legend(loc='best', ncol=2, fontsize=14, frameon=True, shadow=True)

            plt.show()
        st.write("**frameon** 파라미터는 범례 텍스트 상자의 테두리를 표시할지 여부를 지정합니다.")
        st.write("**frameon=False** 로 지정하면 테두리가 표시되지 않습니다.")
        st.write("**shadow** 파라미터를 사용해서 텍스트 상자에 그림자를 표시할 수 있습니다.")
        st.pyplot(plt)
        plt.close()
        st.write("이 외에도 legend() 함수에는 **facecolor, edgecolor, borderpad, labelspacing** 과 같은 다양한 파라미터가 있습니다.")

        st.header(f"{idx.getHeadIdx()}축 범위 지정하기")
        st.write("**matplotlib.pyplot** 모듈의 **xlim(), ylim(), axis()** 함수를 사용하면 그래프의 X, Y축이 표시되는 범위를 지정할 수 있습니다.")
        st.write("◾ xlim() - X축이 표시되는 범위를 지정하거나 반환합니다.")
        st.write("◾ ylim() - Y축이 표시되는 범위를 지정하거나 반환합니다.")
        st.write("◾ axis() - X, Y축이 표시되는 범위를 지정하거나 반환합니다.")
        st.write("그래프의 축의 범위를 지정하고, 확인하는 방법에 대해 소개합니다.")
        
        st.subheader(f"{idx.getSubIdx()}기본 사용 - xlim(), ylim()")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [2, 3, 5, 10])
            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')
            plt.xlim([0, 5])      # X축의 범위: [xmin, xmax]
            plt.ylim([0, 20])     # Y축의 범위: [ymin, ymax]

            plt.show()
        st.write("**xlim()** 함수에 xmin, xmax 값을 각각 입력하거나 리스트 또는 튜플의 형태로 입력합니다.")
        st.write("**ylim()** 함수에 ymin, ymax 값을 각각 입력하거나 리스트 또는 튜플의 형태로 입력합니다.")
        st.write("입력값이 없으면 데이터에 맞게 자동으로 범위를 지정합니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}기본사용 - axis()")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [2, 3, 5, 10])
            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')
            plt.axis([0, 5, 0, 20])  # X, Y축의 범위: [xmin, xmax, ymin, ymax]

            plt.show()
        st.write("**axis()** 함수에 [xmin, xmax, ymin, ymax]의 형태로 X, Y축의 범위를 지정할 수 있습니다.")
        st.write("**axis()** 함수에 입력한 리스트 (또는 튜플)는 반드시 네 개의 값 (xmin, xmax, ymin, ymax)이 있어야 합니다.")
        st.write("입력값이 없으면 데이터에 맞게 자동으로 범위를 지정합니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}옵션 지정하기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [2, 3, 5, 10])
            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')
            plt.axis('square')
            # plt.axis('scaled')

            plt.show()
        st.write("axis() 함수는 아래와 같이 축에 관한 다양한 옵션을 제공합니다.")
        st.write("'on' | 'off' | 'equal' | 'scaled' | 'tight' | 'auto' | 'normal' | 'image' | 'square'")
        st.write("아래의 그림은 ‘square’로 지정했을 때의 그래프입니다. 축의 길이가 동일하게 표시됩니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}축 범위 얻기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [2, 3, 5, 10])
            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')

            x_range, y_range = plt.xlim(), plt.ylim()
            print(x_range, y_range)

            axis_range = plt.axis('scaled')
            print(axis_range)

            plt.show()
        st.pyplot(plt)
        plt.close()
        st.write("xlim(), ylim() 함수는 그래프 영역에 표시되는 X축, Y축의 범위를 각각 반환합니다.")
        st.write("axis() 함수는 그래프 영역에 표시되는 X, Y축의 범위를 반환합니다.")
        code = '''(0.85, 4.15) (1.6, 10.4)
(0.85, 4.15, 1.6, 10.4)'''
        st.code(code, language="python")
        st.write("위의 예제 그림에서 X축은 0.85에서 4.15, Y축은 1.6에서 10.4 범위로 표시되었음을 알 수 있습니다.  ")
    
    elif path == ("Matplotlib 기초", "스타일 세부 설정"):
        st.header(f"{idx.getHeadIdx()}선 종류 지정")
        st.write("데이터를 표현하기 위해 그려지는 선의 종류를 지정하는 방법을 소개합니다.")
        st.write("선 종류를 나타내는 문자열 또는 튜플을 이용해서 다양한 선의 종류를 구현할 수 있습니다.")

        st.subheader(f"{idx.getSubIdx()}기본 사용")
        st.write("데이터를 표현하기 위해 그려지는 선의 종류를 지정하는 방법을 소개합니다.")
        st.write("선 종류를 나타내는 문자열 또는 튜플을 이용해서 다양한 선의 종류를 구현할 수 있습니다.")
        st.write("**< line의 종류 >**")
        st.write("◾ '-' solid line style")
        st.write("◾ '--' dashed line style")
        st.write("◾ '-.' dash-dot line style")
        st.write("◾ ':' dotted line style")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3], [4, 4, 4], '-', color='C0', label='Solid')
            plt.plot([1, 2, 3], [3, 3, 3], '--', color='C0', label='Dashed')
            plt.plot([1, 2, 3], [2, 2, 2], ':', color='C0', label='Dotted')
            plt.plot([1, 2, 3], [1, 1, 1], '-.', color='C0', label='Dash-dot')
            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')
            plt.axis([0.8, 3.2, 0.5, 5.0])
            plt.legend(loc='upper right', ncol=4)
            plt.show()
        st.write("Matplotlib에서 선의 종류를 지정하는 가장 간단한 방법은 포맷 문자열을 사용하는 것입니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}linestyle 지정하기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3], [4, 4, 4], linestyle='solid', color='C0', label="'solid'")
            plt.plot([1, 2, 3], [3, 3, 3], linestyle='dashed', color='C0', label="'dashed'")
            plt.plot([1, 2, 3], [2, 2, 2], linestyle='dotted', color='C0', label="'dotted'")
            plt.plot([1, 2, 3], [1, 1, 1], linestyle='dashdot', color='C0', label="'dashdot'")
            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')
            plt.axis([0.8, 3.2, 0.5, 5.0])
            plt.legend(loc='upper right', ncol=4)
            plt.tight_layout()
            plt.show()
        st.write("**plot()** 함수의 **linestyle** 파라미터 값을 직접 지정할 수 있습니다.")
        st.write("포맷 문자열과 같이 ‘solid’, ‘dashed’, ‘dotted’, dashdot’ 네가지의 선 종류를 지정할 수 있습니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}튜플 사용하기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3], [4, 4, 4], linestyle=(0, (1, 1)), color='C0', label='(0, (1, 1))')
            plt.plot([1, 2, 3], [3, 3, 3], linestyle=(0, (1, 5)), color='C0', label='(0, (1, 5))')
            plt.plot([1, 2, 3], [2, 2, 2], linestyle=(0, (5, 1)), color='C0', label='(0, (5, 1))')
            plt.plot([1, 2, 3], [1, 1, 1], linestyle=(0, (3, 5, 1, 5)), color='C0', label='(0, (3, 5, 1, 5))')
            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')
            plt.axis([0.8, 3.2, 0.5, 5.0])
            plt.legend(loc='upper right', ncol=2)
            plt.tight_layout()
            plt.show()
        st.write("튜플을 사용해서 선의 종류를 커스터마이즈할 수 있습니다.")
        st.write("예를 들어, (0, (1, 1))은 ‘dotted’와 같고, (0, (5, 5))는 ‘dashed’와 같습니다. 또한 (0, (3, 5, 1, 5))는 ‘dashdotted’와 같습니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}선 끝 모양 지정하기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3], [4, 4, 4], linestyle='solid', linewidth=10,
                solid_capstyle='butt', color='C0', label='solid+butt')
            plt.plot([1, 2, 3], [3, 3, 3], linestyle='solid', linewidth=10,
                solid_capstyle='round', color='C0', label='solid+round')

            plt.plot([1, 2, 3], [2, 2, 2], linestyle='dashed', linewidth=10,
                dash_capstyle='butt', color='C1', label='dashed+butt')
            plt.plot([1, 2, 3], [1, 1, 1], linestyle='dashed', linewidth=10,
                dash_capstyle='round', color='C1', label='dashed+round')


            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')
            plt.axis([0.8, 3.2, 0.5, 5.0])
            plt.legend(loc='upper right', ncol=2)
            plt.tight_layout()
            plt.show()
        st.write("**plot()** 함수의 **solid_capstyle, dash_capstyle** 를 사용해서 선의 끝 모양을 지정할 수 있습니다.")
        st.write("각각 ‘butt’, ‘round’로 지정하면 아래 그림과 같이 뭉뚝한, 둥근 끝 모양이 나타납니다.")
        st.pyplot(plt)
        plt.close()

        st.header(f"{idx.getHeadIdx()}마커 지정")
        st.write("특별한 설정이 없으면 그래프가 실선으로 그려지지만, 위의 그림과 같은 마커 형태의 그래프를 그릴 수 있습니다.")
        st.write("**plot()** 함수의 **포맷 문자열 (Format string)** 을 사용해서 그래프의 선과 마커를 지정하는 방법에 대해 알아봅니다.")
        st.subheader(f"{idx.getSubIdx()}기본 사용")
        st.write("**< marker의 종류 >**")
        st.write("◾ '.' point marker")
        st.write("◾ ',' pixel marker")
        st.write("◾ 'o' circle marker")
        st.write("◾ 'v' triangle_down marker")
        st.write("◾ '^' triangle_up marker")
        st.write("◾ '<' triangle_left marker")
        st.write("◾ >' triangle_right marker")
        st.write("◾ '1' tri_down marker")
        st.write("◾ '2' tri_up marker")
        st.write("◾ '3' tri_left marker")
        st.write("◾ '4' tri_right marker")
        st.write("◾ 's ' square marker")
        st.write("◾ 'p' pentagon marker")
        st.write("◾ '*' star marker")
        st.write("◾ 'h' hexagon1 marker")
        st.write("◾ 'H' hexagon2 marker")
        st.write("◾ '+' plus marker")
        st.write("◾ 'x' x marker")
        st.write("◾ 'D' diamond marker")
        st.write("◾ 'd' thin_diamond marker")
        st.write("◾ '|' vline marker")
        st.write("◾ '_' hline marker")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [2, 3, 5, 10], 'bo')
            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')
            plt.show()
        st.write("**plot()** 함수에 **‘bo’** 를 입력해주면 파란색의 원형 마커로 그래프가 표시됩니다.")
        st.write("‘b’는 blue, ‘o’는 circle을 나타내는 문자입니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}선/마커 동시에 나타내기")
        with st.echo():
            import matplotlib.pyplot as plt

            # plt.plot([1, 2, 3, 4], [2, 3, 5, 10], 'bo-')    # 파란색 + 마커 + 실선
            plt.plot([1, 2, 3, 4], [2, 3, 5, 10], 'bo--')     # 파란색 + 마커 + 점선
            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')
            plt.show()
        st.write("**‘bo-‘** 는 파란색의 원형 마커와 실선 (Solid line)을 의미합니다.")
        st.write("또한 **‘bo- -‘** 는 파란색의 원형 마커와 점선 (Dashed line)을 의미합니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}선/마커 표시 형식")
        st.write("선/마커 표시 형식에 대한 예시는 아래와 같습니다.")
        code = '''
'b'     # blue markers with default shape
'ro'    # red circles
'g-'    # green solid line
'--'    # dashed line with default color
'k^:'   # black triangle_up markers connected by a dotted line
'''
        st.code(code, language="python")
        st.divider()

        st.subheader(f"{idx.getSubIdx()}marker 파라미터 사용하기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([4, 5, 6], marker="H")
            plt.plot([3, 4, 5], marker="d")
            plt.plot([2, 3, 4], marker="x")
            plt.plot([1, 2, 3], marker=11)
            plt.plot([0, 1, 2], marker='$Z$')
            plt.show()
        st.write("**plot()** 함수의 marker 파라미터를 사용하면 더욱 다양한 마커 형태를 지정할 수 있습니다.")
        st.write("예제에서 다섯가지 마커를 지정했습니다.")
        st.pyplot(plt)
        plt.close()
    
        st.header(f"{idx.getHeadIdx()}색상 지정")
        st.write("**matplotlib.pyplot** 모듈의 **plot()** 함수를 사용해서 그래프를 나타낼 때, 색상을 지정하는 다양한 방법에 대해 소개합니다.")
        
        st.subheader(f"{idx.getSubIdx()}기본 색상")
        st.write("**< color의 종류 >**")
        st.write("◾ 'b' blue")
        st.write("◾ 'g' green")
        st.write("◾ 'r' red")
        st.write("◾ 'c' cyan")
        st.write("◾ 'm' magenta")
        st.write("◾ 'y' yellow")
        st.write("◾ 'k' black")
        st.write("◾ 'w' white")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            plt.plot(np.arange(10), np.arange(10)*2, marker='o', linestyle='-', color='b')
            plt.plot(np.arange(10), np.arange(10)*2 - 10, marker='v', linestyle='--', color='c')
            plt.plot(np.arange(10), np.arange(10)*2 - 20, marker='+', linestyle='-.', color='y')
            plt.plot(np.arange(10), np.arange(10)*2 - 30, marker='*', linestyle=':', color='r')

            # 타이틀 & font 설정
            plt.title('색상 설정 예제', fontsize=10, fontproperties=prop)

            # X축 & Y축 Label 설정
            plt.xlabel('X축', fontsize=10, fontproperties=prop)
            plt.ylabel('Y축', fontsize=10, fontproperties=prop)

            # X tick, Y tick 설정
            plt.xticks(rotation=90)
            plt.yticks(rotation=30)

            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}color 키워드 인자 사용하기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [2.0, 3.0, 5.0, 10.0], color='limegreen')
            plt.plot([1, 2, 3, 4], [2.0, 2.8, 4.3, 6.5], color='violet')
            plt.plot([1, 2, 3, 4], [2.0, 2.5, 3.3, 4.5], color='dodgerblue')
            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')

            plt.show()
        st.write("**color** 키워드 인자를 사용해서 더 다양한 색상의 이름을 지정할 수 있습니다.")
        st.write("**plot()** 함수에 **color=’limegreen’** 과 같이 입력하면, limegreen에 해당하는 색깔이 표시됩니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}포맷 문자열 사용하기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [2.0, 3.0, 5.0, 10.0], 'r')
            plt.plot([1, 2, 3, 4], [2.0, 2.8, 4.3, 6.5], 'g')
            plt.plot([1, 2, 3, 4], [2.0, 2.5, 3.3, 4.5], 'b')
            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')

            plt.show()
        st.write("**plot()** 함수의 **포맷 문자열 (Format string)** 을 사용해서 실선의 색상을 지정했습니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}Hex code 사용하기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [2, 3, 5, 10], color='#e35f62',
                    marker='o', linestyle='--')
            plt.xlabel('X-Axis')
            plt.ylabel('Y-Axis')

            plt.show()
        st.write("**16진수 코드 (Hex code)** 로 더욱 다양한 색상을 지정할 수 있습니다.")
        st.write("이번에는 **선의 색상** 과 함께 **마커와 선의 종류** 까지 모두 지정해 보겠습니다.")
        st.write("**marker**는 마커 스타일, **linestyle** 는 선의 스타일을 지정합니다.")
        st.write("선의 색상은 Hex code **‘#e35f62’** 로, 마커는 **원형 (Circle)**, 선 종류는 **대시 (Dashed)** 로 지정했습니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}투명도 설정")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            plt.plot(np.arange(10), np.arange(10)*2, color='b', alpha=0.1)
            plt.plot(np.arange(10), np.arange(10)*2 - 10, color='b', alpha=0.3)
            plt.plot(np.arange(10), np.arange(10)*2 - 20, color='b', alpha=0.6)
            plt.plot(np.arange(10), np.arange(10)*2 - 30, color='b', alpha=1.0)

            # 타이틀 & font 설정
            plt.title('투명도 (alpha) 설정 예제', fontsize=10, fontproperties=prop)

            # X축 & Y축 Label 설정
            plt.xlabel('X축', fontsize=10, fontproperties=prop)
            plt.ylabel('Y축', fontsize=10, fontproperties=prop)

            # X tick, Y tick 설정
            plt.xticks(rotation=90)
            plt.yticks(rotation=30)

            plt.show()
        st.pyplot(plt)
        plt.close()

    elif path == ("Matplotlib 기초", "Grid, Annotate"):
        st.header(f"{idx.getHeadIdx()}그리드(Grid)")
        st.write("데이터의 위치를 더 명확하게 나타내기 위해 그래프에 그리드 **(Grid, 격자)** 를 표시할 수 있습니다.")
        st.write("**matplotlib.pyplot** 모듈의 **grid()** 함수를 이용해서 그래프에 다양하게 그리드를 설정해 보겠습니다.")
        st.subheader(f"{idx.getSubIdx()}기본 사용")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            x = np.arange(0, 2, 0.2)

            plt.plot(x, x, 'bo')
            plt.plot(x, x**2, color='#e35f62', marker='*', linewidth=2)
            plt.plot(x, x**3, color='springgreen', marker='^', markersize=9)
            plt.grid(True)

            plt.show()
        st.write("**plt.grid(True)** 와 같이 설정하면, 그래프의 x, y축에 대해 그리드가 표시됩니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}축 지정하기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            x = np.arange(0, 2, 0.2)

            plt.plot(x, x, 'bo')
            plt.plot(x, x**2, color='#e35f62', marker='*', linewidth=2)
            plt.plot(x, x**3, color='forestgreen', marker='^', markersize=9)
            plt.grid(True, axis='y')

            plt.show()
        st.write("**axis=y** 로 설정하면 가로 방향의 그리드만 표시됩니다.")
        st.write("{‘both’, ‘x’, ‘y’} 중 선택할 수 있고 디폴트는 ‘both’입니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}스타일 설정하기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            x = np.arange(0, 2, 0.2)

            plt.plot(x, x, 'bo')
            plt.plot(x, x**2, color='#e35f62', marker='*', linewidth=2)
            plt.plot(x, x**3, color='springgreen', marker='^', markersize=9)
            plt.grid(True, axis='y', color='red', alpha=0.5, linestyle='--')

            plt.show()
        st.write("**color, alpha, linestyle** 파마리터를 사용해서 그리드 선의 스타일을 설정했습니다.")
        st.write("또한 **which** 파라미터를 ‘major’, ‘minor’, ‘both’ 등으로 사용하면 주눈금, 보조눈금에 각각 그리드를 표시할 수 있습니다.")
        st.pyplot(plt)
        plt.close()

        st.header(f"{idx.getHeadIdx()}Annotate 설정")
        st.subheader(f"{idx.getSubIdx()}기본 사용")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            plt.plot(np.arange(10), np.arange(10)*2, marker='o', linestyle='-', color='b')
            plt.plot(np.arange(10), np.arange(10)*2 - 10, marker='v', linestyle='--', color='c')
            plt.plot(np.arange(10), np.arange(10)*2 - 20, marker='+', linestyle='-.', color='y')
            plt.plot(np.arange(10), np.arange(10)*2 - 30, marker='*', linestyle=':', color='r')

            # 타이틀 & font 설정
            plt.title('그리드 설정 예제', fontsize=10, fontproperties=prop)

            # X축 & Y축 Label 설정
            plt.xlabel('X축', fontsize=10, fontproperties=prop)
            plt.ylabel('Y축', fontsize=10, fontproperties=prop)

            # X tick, Y tick 설정
            plt.xticks(rotation=90)
            plt.yticks(rotation=30)

            # annotate 설정
            plt.annotate('코로나 사태 발생 지점', xy=(3, -20), xytext=(3, -25), arrowprops=dict(facecolor='black', shrink=0.05), fontproperties=prop)

            # grid 옵션 추가
            plt.grid()

            plt.show()
        st.pyplot(plt)
        plt.close()

    elif path == ("Matplotlib 기초", "Plot"):
        st.header(f"{idx.getHeadIdx()}Scatterplot")
        st.write("**산점도 (Scatter plot)** 는 두 변수의 상관 관계를 직교 좌표계의 평면에 점으로 표현하는 그래프입니다.")
        st.write("**matplotlib.pyplot** 모듈의 **scatter()** 함수를 이용하면 산점도를 그릴 수 있습니다.")
        st.subheader(f"{idx.getSubIdx()}기본 사용")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            np.random.seed(0)

            n = 50
            x = np.random.rand(n)
            y = np.random.rand(n)

            plt.scatter(x, y)
            plt.show()
        st.write("NumPy의 :blue[random 모듈]에 포함된 rand() 함수를 사용해서 [0, 1) 범위의 난수를 각각 50개씩 생성했습니다.")
        st.write("x, y 데이터를 순서대로 scatter() 함수에 입력하면 x, y 값에 해당하는 위치에 기본 마커가 표시됩니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}색상과 크기 지정하기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            np.random.seed(0)

            n = 50
            x = np.random.rand(n)
            y = np.random.rand(n)
            area = (30 * np.random.rand(n))**2
            colors = np.random.rand(n)

            plt.scatter(x, y, s=area, c=colors)
            plt.show()
        st.write("scatter() 함수의 **s, c** 파라미터는 각각 마커의 크기와 색상을 지정합니다.")
        st.write("마커의 크기는 size**2 의 형태로 지정합니다.")
        st.write("예를 들어 **plot()** 함수에 **markersize=20** 으로 지정하는 것과 scatter() 함수에 s=20**2으로 지정하는 것은 같은 크기의 마커를 표시하도록 합니다.")
        st.write("마커의 색상은 데이터의 길이와 같은 크기의 숫자 시퀀스 또는 rgb, 그리고 Hex code 색상을 입력해서 지정합니다.")
        st.write("마커에 임의의 크기와 색상을 지정했습니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.write("plot() 함수의 markersize 지정과 scatter() 함수의 s (size) 지정에 대해서는 아래의 예제를 참고하세요.")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1], [1], 'o', markersize=20, c='#FF5733')
            plt.scatter([2], [1], s=20**2, c='#33FFCE')

            plt.text(0.5, 1.05, 'plot(markersize=20)', fontdict={'size': 14})
            plt.text(1.6, 1.05, 'scatter(s=20**2)', fontdict={'size': 14})
            plt.axis([0.4, 2.6, 0.8, 1.2])
            plt.show()
        st.write("plot() 함수의 markersize를 20으로, scatter() 함수의 s를 20**2으로 지정했습니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}투명도와 컬러맵 설정하기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            np.random.seed(0)

            n = 50
            x = np.random.rand(n)
            y = np.random.rand(n)
            area = (30 * np.random.rand(n))**2
            colors = np.random.rand(n)

            plt.scatter(x, y, s=area, c=colors, alpha=0.5, cmap='Spectral')
            plt.colorbar()
            plt.show()
        st.write("**alpha** 파라미터는 마커의 투명도를 지정합니다. 0에서 1 사이의 값을 입력합니다.")
        st.write("**cmap** 파라미터에 컬러맵에 해당하는 문자열을 지정할 수 있습니다.")
        st.pyplot(plt)
        plt.close()

        st.header(f"{idx.getHeadIdx()}Line Plot")
        st.subheader(f"{idx.getSubIdx()}기본 lineplot 그리기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np
            
            x = np.arange(0, 10, 0.1)
            y = 1 + np.sin(x)

            plt.plot(x, y)

            plt.xlabel('x value', fontsize=15)
            plt.ylabel('y value', fontsize=15)
            plt.title('sin graph', fontsize=18)

            plt.grid()

            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}2개 이상의 그래프 그리기")
        st.write("◾ color : 컬러 옵션")
        st.write("◾ alpha : 투명도 옵션")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            x = np.arange(0, 10, 0.1)
            y_1 = 1 + np.sin(x)
            y_2 = 1 + np.cos(x)

            plt.plot(x, y_1, label='1+sin', color='blue', alpha=0.3)
            plt.plot(x, y_2, label='1+cos', color='red', alpha=0.7)

            plt.xlabel('x value', fontsize=15)
            plt.ylabel('y value', fontsize=15)
            plt.title('sin and cos graph', fontsize=18)

            plt.grid()
            plt.legend()

            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}마커 스타일링")
        st.write("◾ marker : 마커 옵션")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            x = np.arange(0, 10, 0.1)
            y_1 = 1 + np.sin(x)
            y_2 = 1 + np.cos(x)

            plt.plot(x, y_1, label='1+sin', color='blue', alpha=0.3, marker='o')
            plt.plot(x, y_2, label='1+cos', color='red', alpha=0.7, marker='+')

            plt.xlabel('x value', fontsize=15)
            plt.ylabel('y value', fontsize=15)
            plt.title('sin and cos graph', fontsize=18)

            plt.grid()
            plt.legend()

            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}라인 스타일 변경")
        st.write("◾ linestyle : 라인 스타일 변경 옵션")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            x = np.arange(0, 10, 0.1)
            y_1 = 1 + np.sin(x)
            y_2 = 1 + np.cos(x)

            plt.plot(x, y_1, label='1+sin', color='blue', linestyle=':')
            plt.plot(x, y_2, label='1+cos', color='red', linestyle='-.')

            plt.xlabel('x value', fontsize=15)
            plt.ylabel('y value', fontsize=15)
            plt.title('sin and cos graph', fontsize=18)

            plt.grid()
            plt.legend()

            plt.show()
        st.pyplot(plt)
        plt.close()

        st.header(f"{idx.getHeadIdx()}Areaplot(Filled Area)")
        st.write("matplotlib에서 area plot을 그리고자 할 때는 **fill_between** 함수를 사용합니다.")
        code='''import matplotlib.pyplot as plt
import numpy as np

y = np.random.randint(low=5, high=10, size=20)
y'''
        st.code(code, language="python")
        st.write("**[ 출력 ]**")
        code='''array([9, 8, 9, 5, 7, 6, 8, 7, 6, 5, 6, 6, 9, 7, 7, 5, 7, 8, 5, 7])'''
        st.code(code, language="python")

        st.subheader(f"{idx.getSubIdx()}기본 areaplot 그리기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            x = np.arange(1,21)
            y =  np.random.randint(low=5, high=10, size=20)

            # fill_between으로 색칠하기
            plt.fill_between(x, y, color="green", alpha=0.6)
            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}경계선을 굵게 그리고 area는 옆게 그리는 효과 적용")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.fill_between(x, y, color="green", alpha=0.3)
            plt.plot(x, y, color="green", alpha=0.8)
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}여러 그래프를 겹쳐서 표현")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            x = np.arange(1, 10, 0.05)
            y_1 =  np.cos(x)+1
            y_2 =  np.sin(x)+1
            y_3 = y_1 * y_2 / np.pi

            plt.fill_between(x, y_1, color="green", alpha=0.1)
            plt.fill_between(x, y_2, color="blue", alpha=0.2)
            plt.fill_between(x, y_3, color="red", alpha=0.3)
        st.pyplot(plt)
        plt.close()

        st.header(f"{idx.getHeadIdx()}Box Plot")
        st.write("**박스 플롯 (Box plot)** 또는 **박스-위스커 플롯 (Box-Whisker plot)** 은 수치 데이터를 표현하는 하나의 방식입니다.")
        st.write("샘플 데이터를 생성합니다.")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            # 샘플 데이터 생성
            spread = np.random.rand(50) * 100
            center = np.ones(25) * 50
            flier_high = np.random.rand(10) * 100 + 100
            flier_low = np.random.rand(10) * -100
            data = np.concatenate((spread, center, flier_high, flier_low))
        
        st.subheader(f"{idx.getSubIdx()}기본 박스플롯 생성")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.boxplot(data)
            plt.tight_layout()
            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}Box Plot 축 바꾸기")
        st.write("ax.boxplot()의 vert 파라미터를 False로 지정하면 수평 방향의 박스 플롯이 나타납니다.")
        st.write("디폴트는 수직 방향의 박스 플롯입니다.")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.title('Horizontal Box Plot', fontsize=15)
            plt.boxplot(data, vert=False)

            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}Outlier 마커 심볼과 컬러 변경")
        with st.echo():
            outlier_marker = dict(markerfacecolor='r', marker='D')
        with st.echo():
            import matplotlib.pyplot as plt

            plt.title('Changed Outlier Symbols', fontsize=15)
            plt.boxplot(data, flierprops=outlier_marker)

            plt.show()
        st.pyplot(plt)
        plt.close()

    elif path == ("Matplotlib 기초", "Matplotlib 그래프"):
        st.header(f"{idx.getHeadIdx()}컬러맵 그리기")
        st.write("**matplotlib.pyplot** 모듈은 컬러맵을 간편하게 설정하기 위한 여러 함수를 제공합니다.")
        st.write("아래의 함수들을 사용해서 그래프의 컬러맵을 설정하는 방식에 대해 소개합니다.")
        st.write("**autumn(), bone(), cool(), copper(), flag(), gray(), hot(), hsv(), inferno(), jet(), magma(), nipy_spectral(), pink(), plasma(), prism(), spring(), summer(), viridis(), winter().**")
        st.subheader(f"{idx.getSubIdx()}기본 사용")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            np.random.seed(0)
            arr = np.random.standard_normal((8, 100))

            plt.subplot(2, 2, 1)
            # plt.scatter(arr[0], arr[1], c=arr[1], cmap='spring')
            plt.scatter(arr[0], arr[1], c=arr[1])
            plt.spring()
            plt.title('spring')

            plt.subplot(2, 2, 2)
            plt.scatter(arr[2], arr[3], c=arr[3])
            plt.summer()
            plt.title('summer')

            plt.subplot(2, 2, 3)
            plt.scatter(arr[4], arr[5], c=arr[5])
            plt.autumn()
            plt.title('autumn')

            plt.subplot(2, 2, 4)
            plt.scatter(arr[6], arr[7], c=arr[7])
            plt.winter()
            plt.title('winter')

            plt.tight_layout()
            plt.show()

        st.write("**subplot()** 함수를 이용해서 네 영역에 각각의 그래프를 나타내고,")
        st.write("**spring(), summer(), autumn(), winter()** 함수를 이용해서 컬러맵을 다르게 설정했습니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}컬러바 나타내기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            np.random.seed(0)
            arr = np.random.standard_normal((8, 100))

            plt.subplot(2, 2, 1)
            plt.scatter(arr[0], arr[1], c=arr[1])
            plt.viridis()
            plt.title('viridis')
            plt.colorbar()

            plt.subplot(2, 2, 2)
            plt.scatter(arr[2], arr[3], c=arr[3])
            plt.plasma()
            plt.title('plasma')
            plt.colorbar()

            plt.subplot(2, 2, 3)
            plt.scatter(arr[4], arr[5], c=arr[5])
            plt.jet()
            plt.title('jet')
            plt.colorbar()

            plt.subplot(2, 2, 4)
            plt.scatter(arr[6], arr[7], c=arr[7])
            plt.nipy_spectral()
            plt.title('nipy_spectral')
            plt.colorbar()

            plt.tight_layout()
            plt.show()
        st.write("colorbar() 함수를 사용하면 그래프 영역에 컬러바를 포함할 수 있습니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}컬러맵 종류")
        with st.echo():
            import matplotlib.pyplot as plt
            from matplotlib import cm

            cmaps = plt.colormaps()
            for cm in cmaps:
                print(cm)
        st.write("pyplot 모듈의 **colormaps()** 함수를 사용해서 Matplotlib에서 사용할 수 있는 모든 컬러맵의 이름을 얻을 수 있습니다.")
        st.write("예를 들어, **winter** 와 **winter_r** 은 순서가 앞뒤로 뒤집어진 컬러맵입니다.")

        
    elif path == ("Matplotlib 기초", "막대 그래프"):
        st.header(f"{idx.getHeadIdx()}막대 그래프 그리기")
        st.write("**막대 그래프 (Bar graph, Bar chart)** 는 범주가 있는 데이터 값을 직사각형의 막대로 표현하는 그래프입니다.")
        st.write("Matplotlib에서는 **matplotlib.pyplot** 모듈의 **bar()** 함수를 이용해서 막대 그래프를 간단하게 표현할 수 있습니다.")
        st.subheader(f"{idx.getSubIdx()}기본 사용")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            x = np.arange(3)
            years = ['2018', '2019', '2020']
            values = [100, 400, 900]

            plt.bar(x, values)
            plt.xticks(x, years)

            plt.show()
        st.write("이 예제는 연도별로 변화하는 값을 갖는 데이터를 막대 그래프로 나타냅니다.")
        st.write("NumPy의 **np.arange()** 함수는 주어진 범위와 간격에 따라 균일한 값을 갖는 어레이를 반환합니다.")
        st.write("**years** 는 X축에 표시될 연도이고, **values** 는 막대 그래프의 y 값 입니다.")
        st.write("먼저 **plt.bar()** 함수에 x 값 [0, 1, 2]와 y 값 [100, 400, 900]를 입력해주고,")
        st.write("**xticks()**에 **x** 와 **years** 를 입력해주면, X축의 눈금 레이블에 ‘2018’, ‘2019’, ‘2020’이 순서대로 표시됩니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}비교 그래프 그리기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            x_label = ['Math', 'Programming', 'Data Science', 'Art', 'English', 'Physics']
            x = np.arange(len(x_label))
            y_1 = [66, 80, 60, 50, 80, 10]
            y_2 = [55, 90, 40, 60, 70, 20]

            # 넓이 지정
            width = 0.35

            # subplots 생성
            fig, axes = plt.subplots()

            # 넓이 설정
            axes.bar(x - width/2, y_1, width, align='center', alpha=0.5)
            axes.bar(x + width/2, y_2, width, align='center', alpha=0.8)

            # xtick 설정
            plt.xticks(x)
            axes.set_xticklabels(x_label)
            plt.ylabel('Number of Students')
            plt.title('Subjects')

            plt.legend(['john', 'peter'])

            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}색상 지정하기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            x = np.arange(3)
            years = ['2018', '2019', '2020']
            values = [100, 400, 900]

            plt.bar(x, values, color='y')
            # plt.bar(x, values, color='dodgerblue')
            # plt.bar(x, values, color='C2')
            # plt.bar(x, values, color='#e35f62')
            plt.xticks(x, years)

            plt.show()
        st.write("plt.bar() 함수의 **color** 파라미터를 사용해서 막대의 색상을 지정할 수 있습니다.")
        st.write("예제에서는 네 가지의 색상을 사용했습니다.")
        st.pyplot(plt)
        plt.close()

        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            x = np.arange(3)
            years = ['2018', '2019', '2020']
            values = [100, 400, 900]
            colors = ['y', 'dodgerblue', 'C2']

            plt.bar(x, values, color=colors)
            plt.xticks(x, years)

            plt.show()
        st.write("**plt.bar()** 함수의 **color** 파라미터에 색상의 이름을 리스트의 형태로 입력하면, 막대의 색상을 각각 다르게 지정할 수 있습니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}막대 폭 지정하기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            x = np.arange(3)
            years = ['2018', '2019', '2020']
            values = [100, 400, 900]

            plt.bar(x, values, width=0.4)
            # plt.bar(x, values, width=0.6)
            # plt.bar(x, values, width=0.8)
            # plt.bar(x, values, width=1.0)
            plt.xticks(x, years)

            plt.show()
        st.write("**plt.bar()** 함수의 **width** 파라미터는 막대의 폭을 지정합니다.")
        st.write("예제에서는 막대의 폭을 0.4/0.6/0.8/1.0으로 지정했고, 디폴트는 0.8입니다.")
        st.write("아래 결과는 막대 폭 0.4에 대한 결과입니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}스타일 꾸미기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            x = np.arange(3)
            years = ['2018', '2019', '2020']
            values = [100, 400, 900]

            plt.bar(x, values, align='edge', edgecolor='lightgray',
                    linewidth=5, tick_label=years)

            plt.show()
        st.write("이번에는 막대 그래프의 테두리의 색, 두께 등 스타일을 적용해 보겠습니다.")
        st.write("**align** 은 눈금과 막대의 위치를 조절합니다. 디폴트 값은 ‘center’이며, ‘edge’로 설정하면 막대의 왼쪽 끝에 눈금이 표시됩니다.")
        st.write("**edgecolor** 는 막대 테두리 색, **linewidth** 는 테두리의 두께를 지정합니다.")
        st.write("**tick_label** 을 리스트 또는 어레이 형태로 지정하면, 틱에 문자열을 순서대로 나타낼 수 있습니다.")
        st.pyplot(plt)
        plt.close()

        st.header(f"{idx.getHeadIdx()}수막대 그래프 그리기")
        st.write("**수평 막대 그래프 (Horizontal bar graph)** 는 범주가 있는 데이터 값을 수평 막대로 표현하는 그래프입니다.")
        st.write("**matplotlib.pyplot** 모듈의 **barh()** 함수를 사용해서 수평 막대 그래프를 그리는 방법을 소개합니다.")
        st.subheader(f"{idx.getSubIdx()}기본 사용")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            y = np.arange(3)
            years = ['2018', '2019', '2020']
            values = [100, 400, 900]

            plt.barh(y, values)
            plt.yticks(y, years)

            plt.show()
        st.write("연도별로 변화하는 값을 갖는 데이터를 수평 막대 그래프로 나타냈습니다.")
        st.write("**years** 는 Y축에 표시될 연도이고, **values** 는 막대 그래프의 너비로 표시될 x 값 입니다.")
        st.write("먼저 **barh()** 함수에 NumPy 어레이 [0, 1, 2]와 x 값에 해당하는 리스트 [100, 400, 900]를 입력해줍니다.")
        st.write("다음, **yticks()** 에 y와 years를 입력해주면, Y축의 눈금 레이블에 ‘2018’, ‘2019’, ‘2020’이 순서대로 표시됩니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}비교 그래프 그리기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            x_label = ['Math', 'Programming', 'Data Science', 'Art', 'English', 'Physics']
            x = np.arange(len(x_label))
            y_1 = [66, 80, 60, 50, 80, 10]
            y_2 = [55, 90, 40, 60, 70, 20]

            # 넓이 지정
            width = 0.35

            # subplots 생성
            fig, axes = plt.subplots()

            # 넓이 설정
            axes.barh(x - width/2, y_1, width, align='center', alpha=0.5, color='green')
            axes.barh(x + width/2, y_2, width, align='center', alpha=0.8, color='red')

            # xtick 설정
            plt.yticks(x)
            axes.set_yticklabels(x_label)
            plt.xlabel('Number of Students')
            plt.title('Subjects')

            plt.legend(['john', 'peter'])

            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}막대 높이 지정하기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            y = np.arange(3)
            years = ['2018', '2019', '2020']
            values = [100, 400, 900]

            plt.barh(y, values, height=0.4)
            # plt.barh(y, values, height=0.6)
            # plt.barh(y, values, height=0.8)
            # plt.barh(y, values, height=1.0)
            plt.yticks(y, years)

            plt.show()
        st.write("plt.barh() 함수의 height 파라미터는 막대의 높이를 지정합니다.")
        st.write("예제에서는 막대의 높이를 0.4/0.6/0.8/1.0으로 지정했고, 디폴트는 0.8입니다.")
        st.write("아래 결과는 막대 높이 0.4에 대한 결과입니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}Barplot(축 변환)")
        st.write("barch 함수에서는 **xticks로 설정**했던 부분을 **yticks로 변경**합니다.")
        with st.echo():
            import matplotlib.pyplot as plt

            x = ['Math', 'Programming', 'Data Science', 'Art', 'English', 'Physics']
            y = [66, 80, 60, 50, 80, 10]

            plt.barh(x, y, align='center', alpha=0.7, color='green')
            plt.yticks(x)
            plt.xlabel('Number of Students')
            plt.title('Subjects')

            plt.show()
        st.pyplot(plt)
        plt.close()
    

        st.header(f"{idx.getHeadIdx()}Histogram")
        st.write("**히스토그램 (Histogram)은 도수분포표를 그래프로 나타낸 것으로서, 가로축은 계급, 세로축은 도수 (횟수나 개수 등)** 를 나타냅니다.")
        st.write("이번에는 **matplotlib.pyplot** 모듈의 **hist()** 함수를 이용해서 다양한 히스토그램을 그려 보겠습니다.")
        st.subheader(f"{idx.getSubIdx()}기본 사용")
        with st.echo():
            import matplotlib.pyplot as plt

            weight = [68, 81, 64, 56, 78, 74, 61, 77, 66, 68, 59, 71,
                    80, 59, 67, 81, 69, 73, 69, 74, 70, 65]

            plt.hist(weight)

            plt.show()
        st.write("weight는 몸무게 값을 나타내는 리스트입니다.")
        st.write("**hist()** 함수에 리스트의 형태로 값들을 직접 입력해주면 됩니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}구간 개수 지정하기")
        st.write("**hist()** 함수의 **bins** 파라미터는 히스토그램의 가로축 구간의 개수를 지정합니다.")
        st.write("아래 그림과 같이 구간의 개수에 따라 히스토그램 분포의 형태가 달라질 수 있기 때문에 적절한 구간의 개수를 지정해야 합니다.")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            N = 100000
            bins = 30

            x = np.random.randn(N)

            fig, axs = plt.subplots(1, 3, 
                                    sharey=True, 
                                    tight_layout=True
                                )

            fig.set_size_inches(12, 5)

            axs[0].hist(x, bins=bins)
            axs[1].hist(x, bins=bins*2)
            axs[2].hist(x, bins=bins*4)

            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}누적 히스토그램 그리기")
        with st.echo():
            import matplotlib.pyplot as plt

            weight = [68, 81, 64, 56, 78, 74, 61, 77, 66, 68, 59, 71,
                    80, 59, 67, 81, 69, 73, 69, 74, 70, 65]

            plt.hist(weight, cumulative=True, label='cumulative=True')
            plt.hist(weight, cumulative=False, label='cumulative=False')
            plt.legend(loc='upper left')
            plt.show()
        st.write("**cumulative** 파라미터를 **True**로 지정하면 누적 히스토그램을 나타냅니다.")
        st.write("디폴트는 **False**로 지정됩니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}히스토그램 종류 지정하기")
        with st.echo():
            import matplotlib.pyplot as plt

            weight = [68, 81, 64, 56, 78, 74, 61, 77, 66, 68, 59, 71,
                    80, 59, 67, 81, 69, 73, 69, 74, 70, 65]
            weight2 = [52, 67, 84, 66, 58, 78, 71, 57, 76, 62, 51, 79,
                    69, 64, 76, 57, 63, 53, 79, 64, 50, 61]

            plt.hist((weight, weight2), histtype='bar')
            plt.title('histtype - bar')
            plt.figure()

            plt.hist((weight, weight2), histtype='barstacked')
            plt.title('histtype - barstacked')
            plt.figure()

            plt.hist((weight, weight2), histtype='stepfilled')
            plt.title('histtype - stepfilled')
            plt.figure()

            plt.hist((weight, weight2), histtype='step')
            plt.title('histtype - step')
            plt.show()
        st.write("**histtype** 은 히스토그램의 종류를 지정합니다.")
        st.write("{‘bar’, ‘barstacked’, ‘stepfilled’, ‘step’} 중에서 선택할 수 있으며, 디폴트는 ‘bar’입니다.")
        st.write("예제에서와 같이 두 종류의 데이터를 히스토그램으로 나타냈을 때, **histtype** 의 값에 따라 각기 다른 히스토그램이 그려집니다.")
        st.pyplot(plt)
        plt.clf()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}NumPy 난수의 분포 나타내기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            a = 2.0 * np.random.randn(10000) + 1.0
            b = np.random.standard_normal(10000)
            c = 20.0 * np.random.rand(5000) - 10.0

            plt.hist(a, bins=100, density=True, alpha=0.7, histtype='step')
            plt.hist(b, bins=50, density=True, alpha=0.5, histtype='stepfilled')
            plt.hist(c, bins=100, density=True, alpha=0.9, histtype='step')

            plt.show()
        st.write("Numpy의 np.random.randn(), np.random.standard_normal(), np.random.rand() 함수를 이용해서 임의의 값들을 만들었습니다.")
        st.write("어레이 a는 표준편차 2.0, 평균 1.0을 갖는 정규분포, 어레이 b는 표준정규분포를 따릅니다.")
        st.write("어레이 c는 -10.0에서 10.0 사이의 균일한 분포를 갖는 5000개의 임의의 값입니다.")
        st.write(":red[density=True] 로 설정해주면, 밀도함수가 되어서 막대의 아래 면적이 1이 됩니다.")
        st.write("**alpha**는 투명도를 의미합니다. 0.0에서 1.0 사이의 값을 갖습니다.")
        st.pyplot(plt)
        plt.close()

    elif path == ("Matplotlib 기초", "Pie chart, 3D plot") :
        st.header(f"{idx.getHeadIdx()}Pie Chart")
        st.write("**파이 차트 (Pie chart, 원 그래프)** 는 범주별 구성 비율을 원형으로 표현한 그래프입니다.")
        st.write("위의 그림과 같이 **부채꼴의 중심각을 구성 비율에 비례** 하도록 표현합니다.")
        st.write("**matplotlib.pyplot** 모듈의 **pie()** 함수를 이용해서 파이 차트를 그리는 방법에 대해 소개합니다.")

        st.subheader(f"{idx.getSubIdx()}pie chart 옵션")
        st.write("◾ explode : 파이에서 툭 튀어져 나온 비율")
        st.write("◾ autopct : 퍼센트 자동으로 표기")
        st.write("◾ shadow : 그림자 표시")
        st.write("◾ startangle : 파이를 그리기 시작할 각도")
        st.divider()

        st.subheader(f"{idx.getSubIdx()}기본 사용")
        with st.echo():
            import matplotlib.pyplot as plt

            ratio = [34, 32, 16, 18]
            labels = ['Apple', 'Banana', 'Melon', 'Grapes']

            plt.pie(ratio, labels=labels, autopct='%.1f%%')
            plt.show()
        st.write("우선 각 영역의 비율과 이름을 **ratio** 와 **labels** 로 지정해주고, **pie()** 함수에 순서대로 입력합니다.")
        st.write("**autopct** 는 부채꼴 안에 표시될 숫자의 형식을 지정합니다. 소수점 한자리까지 표시하도록 설정했습니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}시작 각도와 방향 설정하기")
        with st.echo():
            import matplotlib.pyplot as plt

            ratio = [34, 32, 16, 18]
            labels = ['Apple', 'Banana', 'Melon', 'Grapes']

            plt.pie(ratio, labels=labels, autopct='%.1f%%', startangle=260, counterclock=False)
            plt.show()
        st.write("**startangle** 는 부채꼴이 그려지는 시작 각도를 설정합니다.")
        st.write("디폴트는 0도 (양의 방향 x축)로 설정되어 있습니다.")
        st.write("**counterclock=False** 로 설정하면 시계 방향 순서로 부채꼴 영역이 표시됩니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}중심에서 벗어나는 정도 설정하기")
        with st.echo():
            import matplotlib.pyplot as plt

            ratio = [34, 32, 16, 18]
            labels = ['Apple', 'Banana', 'Melon', 'Grapes']
            explode = [0, 0.10, 0, 0.10]

            plt.pie(ratio, labels=labels, autopct='%.1f%%', startangle=260, counterclock=False, explode=explode)
            plt.show()
        st.write("**explode** 는 부채꼴이 파이 차트의 중심에서 벗어나는 정도를 설정합니다.")
        st.write("‘Banana’와 ‘Grapes’ 영역에 대해서 반지름의 10% 만큼 벗어나도록 설정했습니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}그림자 나타내기")
        with st.echo():
            import matplotlib.pyplot as plt

            ratio = [34, 32, 16, 18]
            labels = ['Apple', 'Banana', 'Melon', 'Grapes']
            explode = [0.05, 0.05, 0.05, 0.05]

            plt.pie(ratio, labels=labels, autopct='%.1f%%', startangle=260, counterclock=False, explode=explode, shadow=True)
            plt.show()
        st.write("**shadow** 를 True로 설정하면, 파이 차트에 그림자가 표시됩니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}색상 지정하기")
        with st.echo():
            import matplotlib.pyplot as plt

            ratio = [34, 32, 16, 18]
            labels = ['Apple', 'Banana', 'Melon', 'Grapes']
            explode = [0.05, 0.05, 0.05, 0.05]
            colors = ['silver', 'gold', 'whitesmoke', 'lightgray']

            plt.pie(ratio, labels=labels, autopct='%.1f%%', startangle=260, counterclock=False, explode=explode, shadow=True, colors=colors)
            plt.show()
        st.write("**colors** 를 사용하면 각 영역의 색상을 자유롭게 지정할 수 있습니다.")
        st.write("‘silver’, ‘gold’, ‘lightgray’, ‘whitesmoke’ 등 색상의 이름을 사용해서 각 영역의 색상을 지정했습니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}부채꼴 스타일 지정하기")
        with st.echo():
            import matplotlib.pyplot as plt

            ratio = [34, 32, 16, 18]
            labels = ['Apple', 'Banana', 'Melon', 'Grapes']
            colors = ['#ff9999', '#ffc000', '#8fd9b6', '#d395d0']
            wedgeprops={'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}

            plt.pie(ratio, labels=labels, autopct='%.1f%%', startangle=260, counterclock=False, colors=colors, wedgeprops=wedgeprops)
            plt.show()
        st.write("**wedgeprops** 는 부채꼴 영역의 스타일을 설정합니다.")
        st.write("wedgeprops 딕셔너리의 ‘width’, ‘edgecolor’, ‘linewidth’ 키를 이용해서 각각 부채꼴 영역의 너비 (반지름에 대한 비율), 테두리의 색상, 테두리 선의 너비를 설정했습니다.")
        st.pyplot(plt)
        plt.close()
        
        
        st.header(f"{idx.getHeadIdx()}3D 그래프")
        st.write("3D로 그래프를 그리기 위해서는 mplot3d를 추가로 import 합니다")
        with st.echo():
            from mpl_toolkits import mplot3d

        st.subheader(f"{idx.getSubIdx()}밑그림 그리기(캔버스)")
        with st.echo():
            import matplotlib.pyplot as plt

            fig = plt.figure()
            ax = plt.axes(projection='3d')
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader(f"{idx.getSubIdx()}3D plot 그리기")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            # project=3d로 설정합니다
            ax = plt.axes(projection='3d')

            # x, y, z 데이터를 생성합니다
            z = np.linspace(0, 15, 1000)
            x = np.sin(z)
            y = np.cos(z)

            ax.plot3D(x, y, z, 'gray')
            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()

        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            # project=3d로 설정합니다
            ax = plt.axes(projection='3d')

            sample_size = 100
            x = np.cumsum(np.random.normal(0, 1, sample_size))
            y = np.cumsum(np.random.normal(0, 1, sample_size))
            z = np.cumsum(np.random.normal(0, 1, sample_size))

            # marker 추가
            ax.plot3D(x, y, z, alpha=0.6, marker='o')

            plt.title("ax.plot")
            plt.show()
        st.pyplot(plt)
        plt.close()

    elif path == ("실습 프로젝트", "대기오염 데이터 분석"):
        st.header(f"{idx.getHeadIdx()}서울시 종로구 대기오염")
        st.write("CSV 파일의 2022년 서울시 종로구 대기오염 측정정보를 사용하여 데이터 로드, 분석 및 시각화 결론도출까지 실습을 진행합니다.")

        st.subheader(f"{idx.getSubIdx()}데이터 불러오기")
        st.write('- 실습을 위해 **아래의 버튼**을 클릭하여 데이터를 다운로드 해주세요')
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write("Measurement_item_info.csv")
            with open('data/서울시대기오염측정정보/Measurement_item_info.csv', "rb") as template_file:
                template_byte = template_file.read()

            st.download_button(label="download data",
                                type="primary",
                                data=template_byte,
                            file_name = "Measurement_item_info.csv"
            )
        with col2:
            st.write("Measurement_station_info.csv")
            with open('data/서울시대기오염측정정보/Measurement_station_info.csv', "rb") as template_file:
                template_byte = template_file.read()

            st.download_button(label="download data",
                                type="primary",
                                data=template_byte,
                            file_name = "Measurement_station_info.csv"
            )
        with col3:
            st.write("Measurement_summary.csv")
            with open('data/서울시대기오염측정정보/Measurement_summary.csv', "rb") as template_file:
                template_byte = template_file.read()

            st.download_button(label="download data",
                                type="primary",
                                data=template_byte,
                            file_name = "Measurement_summary.csv"
            )
        with st.echo():
            # 필요한 패키지 설치
            import numpy as np
            import pandas as pd
            import seaborn as sns
            import matplotlib.pyplot as plt

            # 데이터 불러오기
            df_summary = pd.read_csv('data/서울시대기오염측정정보/Measurement_summary.csv')
            df_item = pd.read_csv('data/서울시대기오염측정정보/Measurement_item_info.csv')
            df_station = pd.read_csv('data/서울시대기오염측정정보/Measurement_station_info.csv')

            df_summary.head()
            df_item.head()
            df_station.head()
        st.write("**Measurement_summary**")
        st.write(df_summary.head())
        st.write("**Measurement_item_info**")
        st.write(df_item.head())
        st.write("**Measurement_station_info**")
        st.write(df_station.head())
        st.divider()

        st.subheader(f"{idx.getSubIdx()}데이터 합치기")
        st.write("Measurement data를 data와 time으로 나누고, 일 평균 값으로 합칩니다.")
        code = '''# 'Measurement date' 열을 사용하여 date_time 분리
date_time = df_summary['Measurement date'].str.split(" ", n=1, expand=True)
date_time.head()'''
        st.code(code, language='python')
        date_time = df_summary['Measurement date'].str.split(" ", n=1, expand=True)
        st.write(date_time.head())

        code = '''
# date_time에서 날짜와 시간을 추출하여 새로운 열 추가
df_summary['date'] = date_time[0]
df_summary['time'] = date_time[1]
# 원래의 'Measurement date' 열 삭제
df_summary = df_summary.drop(['Measurement date'], axis=1)
df_summary.head()
'''
        st.code(code, language='python')

        df_summary['date'] = date_time[0]
        df_summary['time'] = date_time[1]
        df_summary = df_summary.drop(['Measurement date'], axis=1)
        st.write(df_summary.head())


        st.subheader(f"{idx.getSubIdx()}데이터 분석")
        st.write("먼저 서울 전체에 대해서 분석해 보기 위해서 data로 groupby하고 분석합니다.")
        with st.echo():
            df_seoul = df_summary.groupby(['date'], as_index=False).agg({'SO2':'mean', 'NO2':'mean', 'O3':'mean', 'CO':'mean', 'PM10':'mean', 'PM2.5':'mean'})
            df_seoul.head()
        df_seoul = df_summary.groupby(['date'], as_index=False).agg({'SO2':'mean', 'NO2':'mean', 'O3':'mean', 'CO':'mean', 'PM10':'mean', 'PM2.5':'mean'})
        st.write(df_seoul.head())

        with st.echo():
            df_seoul.plot(x='date')
            plt.show()
        st.pyplot(plt)
        plt.close()

        code = '''
corr = df_seoul.corr()
f, ax = plt.subplots(figsize=(11, 9))
cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr, cmap=cmap, vmax=1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5})
plt.show() 
'''
        with st.echo():
            df_numeric = df_seoul.drop(columns=['date'])
            # 상관 행렬 계산
            corr = df_numeric.corr()
            # Figure 및 Axes 객체 생성
            fig, ax = plt.subplots(figsize=(11, 9))
            # 색상 맵 생성
            cmap = sns.diverging_palette(220, 10, as_cmap=True)
            # 히트맵 생성
            sns.heatmap(corr, cmap=cmap, vmax=1, center=0,
                        square=True, linewidths=.5, cbar_kws={"shrink": .5})
            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()
        st.write("**PM10 농도**")
        st.write("미세먼지(PM10) 기준으로 좋음, 보통, 나쁨, 매우나쁨으로 구분")
        st.write("대한민국의 미세먼지 환경기준(일평균)")
        st.write("◾ 좋음 0~30")
        st.write("◾ 보통 ~80")
        st.write("◾ 나쁨 ~150")
        st.write("◾ 매우나쁨151~")
        code = '''df_seoul['PM10_class'] = -1
df_seoul.head()'''
        st.code(code, language='python')
        df_seoul['PM10_class'] = -1
        st.write(df_seoul.head())
        st.write("PM10 농도 값을 기준으로 각 행에 대해 클래스를 할당하고, 'PM10_class'라는 새로운 열에 이 값을 저장합니다.")
        st.write("PM10 농도가 특정 범위에 있는 경우에 따라 0,1,2,3 값을 가집니다.")
        code = '''
for (idx, row) in df_seoul.iterrows():
    pm10 = row[5]
    _class = -1
    if pm10 < 0:
        continue
    elif pm10 < 30:
        _class = 0
    elif pm10 < 80:
        _class = 1
    elif pm10 < 150:
        _class = 2
    else:
        _class = 3
    df_seoul.loc[idx, 'PM10_class'] = _class
df_seoul.head()
'''
        for indx, row in df_seoul.iterrows():
            # pm10 = row[5]
            pm10 = row['PM10']
            _class = -1
            if pm10 < 0:
                continue
            elif pm10 < 30:
                _class = 0
            elif pm10 < 80:
                _class = 1
            elif pm10 < 150:
                _class = 2
            else:
                _class = 3
            df_seoul.loc[indx, 'PM10_class'] = _class
        st.write(df_seoul.head())
        df_seoul['PM10_class'].value_counts().plot(kind="bar")
        st.pyplot(plt)
        plt.close()
        st.write("**Examine Strongest Correlation**")
        st.write("seaborn과 jointplot을 사용하여 두 변수 간의 관계를 시각화 하였습니다.")
        st.write("df_seoul 데이터프레임의 'CO'와 'NO2'라는 두 변수 간의 상관관계를 시각화 하였습니다.")
        with st.echo():
            sns.jointplot(x=df_seoul["CO"], y=df_seoul["NO2"], kind='kde', xlim=(0,1),ylim=(0,0.13), color='g')
            plt.show()
        st.pyplot(plt)
        plt.close()

    elif path == ("실습 프로젝트", "지역별 음식점 소비 트렌드 분석"):
        import io
        import numpy as np
        import seaborn as sns

        st.header(f"{idx.getHeadIdx()}지역별 음식점 소비기반 트렌드 데이터")
        st.write("지역별 음식점 소비 데이터를 활용하여 데이터 로드부터, 데이터 탐색 및 분석, 시각화, 결론 도출까지 실습 진행해보겠습니다.")

        st.divider()

        st.subheader(f"{idx.getSubIdx()} 컬럼 설명")
        st.write("- CTPRVN_NM : 시도명칭")
        st.write("- SIGNGU_NM : 시군구 명칭")
        st.write("- FOOD_FCLTY_NM : 음식점업 명칭")
        st.write("- FOOD_FCLTY_CO : 식당수")
        st.write("- POPLTN_CO : 인구수")
        st.divider()

        st.subheader(f"{idx.getSubIdx()}데이터 불러오기")

        st.write('- 실습을 위해 **아래의 버튼**을 클릭하여 데이터를 다운로드 해주세요')
        
        with open('data/음식점소비트렌드/음식점소비트렌드데이터.csv', "rb") as template_file:
            template_csv = template_file.read()

        st.download_button(label="download data",
                            type="primary",
                            data=template_csv,
                           file_name = "음식점소비트렌드데이터.csv"
        )

        st.code("import pandas as pd\n\ndf_map = pd.read_csv('음식점소비트렌드데이터.csv')")
        import pandas as pd
        df_map = pd.read_csv('data/음식점소비트렌드/음식점소비트렌드데이터.csv')

        st.code('df_map')
        st.write(df_map)
        st.divider()

        st.header(f"{idx.getHeadIdx()}데이터 탐색하기(EDA)")
        st.write('데이터 분석에는 **데이터를 탐색**하는 과정이 필요합니다.')
        st.write('- 데이터를 다양한 각도에서 관찰하고 이해하는 과정')
        st.write('- 데이터 분석 전 통계적은 방법으로 자료를 직관적으로 바라보는 과정')

        st.divider()

        st.subheader(f"{idx.getSubIdx()}통계 값으로 데이터 탐색하기")

        st.code('# 행과 열의 수 확인\ndf_map.shape')
        st.write(df_map.shape)

        st.code('# 기본 정보 확인\ndf_map.info()')
        buffer = io.StringIO()
        df_map.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)

        st.code('# 결측치 개수 확인 isnull()\ndf_map.isnull().sum()')
        st.write(df_map.isnull().sum())

        st.code('# 중복 데이터 확인 duplicated()\ndf_map.duplicated().sum()')
        st.write(df_map.duplicated().sum())

        st.code('# 앞의 다섯 개 확인\ndf_map.head()')
        st.write(df_map.head())

        st.code('# 마지막 다섯 개 확인\ndf_map.tail()')
        st.write(df_map.tail())

        st.code('# 통계 데이터 확인\ndf_map.describe()')
        st.write(df_map.describe())

        st.code('# 개별 칼럼 통계치 - 거주자 평균\ndf_map.POPLTN_CO.mean()')
        st.write(df_map.POPLTN_CO.mean())

        st.code('# 전체 식당 수\ndf_map.FOOD_FCLTY_CO.sum()')
        st.write(df_map.FOOD_FCLTY_CO.sum())

        st.code('# 특정 칼럼의 고유한 값 확인 value_counts()\nCTPRVN_NM.value_counts()')  
        st.write(df_map.CTPRVN_NM.value_counts())

        st.code('# SIGNGU_NM의 고유한 값\ndf_map.SIGNGU_NM.value_counts()')
        st.write(df_map.SIGNGU_NM.value_counts())

        st.code('# 특정 칼럼의 고유한 값 개수 확인 nunique() -  CTPRVN_NM\ndf_map.CTPRVN_NM.nunique()')
        st.write(df_map.CTPRVN_NM.nunique())

        st.code('# 식당 종류 확인\ndf_map.FOOD_FCLTY_NM.value_counts()')
        st.write(df_map.FOOD_FCLTY_NM.value_counts())

        st.divider()

        st.subheader(f"{idx.getSubIdx()}조건 인덱싱으로 탐색하기")

        st.code('''# 시군구 이름이 강서구인 데이터\ndf_map[df_map['SIGNGU_NM'] == '강서구']''')
        st.write(df_map[df_map['SIGNGU_NM'] == '강서구'])

        st.code('''# 서울시 강서구만 가져오기 --- 서울시 & 강서구\ndf_map[(df_map.CTPRVN_NM == '서울특별시') & (df_map.SIGNGU_NM == '강서구')]''')
        st.write(df_map[(df_map.CTPRVN_NM == '서울특별시') & (df_map.SIGNGU_NM == '강서구')])

        st.code('''# 서울시 강남구 식당수 --> df_map[강남구 & 서울특별시]['FOOD_FCLTY_NM'].sum()\ndf_map[(df_map.SIGNGU_NM == '강남구')&(df_map.CTPRVN_NM == '서울특별시')].FOOD_FCLTY_CO.sum()''')
        st.write(df_map[(df_map.SIGNGU_NM == '강남구')&(df_map.CTPRVN_NM == '서울특별시')].FOOD_FCLTY_CO.sum())
        st.divider()

        st.subheader(f"{idx.getSubIdx()}피벗 테이블 만들기 :gray-background[pd.pivot_table()]")
        st.markdown("- df : 데이터프레임 \n- index : 기준점이 되는 칼럼 (보통 문자열)\n - values : 계산하려는 칼럼 (보통 숫자)\n - aggfunc : 기초통계함수 (mean, sum 등)")
        
        st.code('''# 피벗테이블 - 시군구별 식당수 합계 데이터프레임만들기
df_식당수 = pd.pivot_table(df_map,
                        index=['CTPRVN_NM', 'SIGNGU_NM'],
                        values= 'FOOD_FCLTY_CO',
                        aggfunc= 'sum')
df_식당수''')
        df_식당수 = pd.pivot_table(df_map,
                        index=['CTPRVN_NM', 'SIGNGU_NM'],
                        values= 'FOOD_FCLTY_CO',
                        aggfunc= 'sum')
        st.write(df_식당수)

        st.code('''# 전체 식당 수 다시 확인
df_식당수.FOOD_FCLTY_CO.sum())''')
        st.write(df_식당수.FOOD_FCLTY_CO.sum())
        st.code('''df_map.FOOD_FCLTY_CO.sum()''')
        st.write(df_map.FOOD_FCLTY_CO.sum())

        st.code('''# 시군구별 인구수 합계 데이터프레임 만들기

df_인구수 = pd.pivot_table(df_map,
                        index=['CTPRVN_NM', 'SIGNGU_NM'],
                        values= 'POPLTN_CO',
                        aggfunc= 'min')
df_인구수''')
        df_인구수 = pd.pivot_table(df_map,
                        index=['CTPRVN_NM', 'SIGNGU_NM'],
                        values= 'POPLTN_CO',
                        aggfunc= 'min')
        st.write(df_인구수)
        st.divider()

        st.header(f"{idx.getHeadIdx()}데이터 전처리")
        st.write('분석을 위해 서울시 데이터만 사용하려고 합니다. 위에서 사용한 피벗 테이블을 활용하여 서울시 데이터만 추출 후 csv 파일로 만들어보겠습니다.')

        st.subheader(f"{idx.getSubIdx()}데이터 프레임 합치기")

        st.code('''df_pivot = pd.concat([df_식당수,df_인구수], axis=1)
df_pivot''')
        df_pivot = pd.concat([df_식당수,df_인구수], axis=1)
        st.write(df_pivot)

        st.code('''df_pivot.info()''')
        buffer = io.StringIO()
        df_pivot.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)
        
        st.subheader(f"{idx.getSubIdx()}컬럼 이름 변경")

        st.code('''# 칼럼이름 변경{'FOOD_FCLTY_CO':'식당수', 'POPLTN_CO':'인구수'}

df_pivot.rename(columns={'FOOD_FCLTY_CO':'식당수', 'POPLTN_CO':'인구수'}, inplace=True)
df_pivot.head()''')
        df_pivot.rename(columns={'FOOD_FCLTY_CO':'식당수', 'POPLTN_CO':'인구수'}, inplace=True)
        st.write(df_pivot.head())

        st.subheader(f"{idx.getSubIdx()}서울시 데이터 csv로 저장")

        st.code('''# 서울시만 저장
df_seoul = df_pivot.loc['서울특별시']
df_seoul.head()''')
        df_seoul = df_pivot.loc['서울특별시']
        st.write(df_seoul.head())

        st.code('''df_seoul.to_csv('seoul.csv')''')
        # df_seoul.to_csv('seoul.csv')
        
        st.divider()

        st.header(f"{idx.getHeadIdx()}데이터 시각화하기")

        st.subheader(f"{idx.getSubIdx()}필요한 라이브러리 로드")

        st.code('''# 시각화 라이브러리 로드 및 설치
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
%matplotlib inline

# 유니코드에서  음수 부호설정
mpl.rc('axes', unicode_minus=False)''')
        
        import pandas as pd
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        
        mpl.rc('axes', unicode_minus=False)

        st.code('''# 한글 지원 라이브러리 설치
!pip install koreanize-matplotlib''')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}서울시 데이터 불러오기")

        st.code('''# 가공한 서울시 데이터 불러오기
df_seoul = pd.read_csv('seoul.csv')''')
        st.code('df_seoul.head()')
        df_seoul = pd.read_csv('data/seoul.csv')
        st.write(df_seoul.head())

        st.divider()

        st.subheader(f"{idx.getSubIdx()}식당수 시각화")
        st.write('서울시 데이터를 활용하여 식당 분포 꺾은선 그래프를 도출해보겠습니다.')

       

        st.code('''# 서울시 식당분포 그리기
plt.title('서울시 식당 분포')
plt.plot(df_seoul['SIGNGU_NM'], df_seoul['식당수'], 'r*-')
plt.show()''')

        
        plt.title('서울시 식당 분포', fontproperties=prop)
        plt.plot(df_seoul['SIGNGU_NM'], df_seoul['식당수'], 'r*-')
        plt.xticks(fontproperties=prop)
        st.pyplot(plt)

        st.write('- 글자가 겹칩니다. **사이즈 조정**하고, **글씨를 회전**해보겠습니다.')

        st.code('''# 화면 사이즈 설정과 글씨 회전
plt.figure(figsize=(20, 4))
plt.title('서울시 식당 분포')
plt.plot(df_seoul['SIGNGU_NM'], df_seoul['식당수'], 'r*-')
plt.show()''')
        
        # 화면 사이즈 설정과 글씨 회전
        plt.figure(figsize=(20, 4))
        plt.title('서울시 식당 분포', fontproperties=prop)
        plt.plot(df_seoul['SIGNGU_NM'], df_seoul['식당수'], 'r*-')
        plt.xticks(fontproperties=prop)
        st.pyplot(plt)
        st.write()
        st.write('- 사이즈가 너무 커졌습니다. **사이즈 조정**하고, **y축에 label**을 붙혀보겠습니다.')
        st.write()

        st.code('''plt.figure(figsize=(8, 4))
plt.title('서울시 식당 분포')
plt.plot(df_seoul['SIGNGU_NM'], df_seoul['식당수'], 'r*-')
# x라벨을 회전
plt.xticks(rotation=60) # 시계 반대방향으로 60도 회전
plt.ylabel('문화체육관광시설 인근 음식점')
plt.show()''')
        
        plt.figure(figsize=(8, 4))
        plt.title('서울시 식당 분포', fontproperties=prop)
        plt.plot(df_seoul['SIGNGU_NM'], df_seoul['식당수'], 'r*-')
        # x라벨을 회전
        plt.xticks(rotation=60, fontproperties=prop) # 시계 반대방향으로 60도 회전
        plt.ylabel('문화체육관광시설 인근 음식점', fontproperties=prop)
        st.pyplot(plt)


        st.write('- **막대 그래프**를 그려보겠습니다. **색을 hotpink**로 설정할 것입니다.')


        st.code('''# 막대 그래프 그리기
plt.figure(figsize=(8, 4))
plt.title('서울시 식당 분포')
# plt.bar()
plt.bar(df_seoul['SIGNGU_NM'], df_seoul['식당수'], color='hotpink')
# x라벨을 회전
plt.xticks(rotation=60)
plt.ylabel('문화체육관광시설 인근 음식점')
plt.show()''')


        plt.figure(figsize=(8, 4))
        plt.title('서울시 식당 분포', fontproperties=prop)
        # plt.bar()
        plt.bar(df_seoul['SIGNGU_NM'], df_seoul['식당수'], color='hotpink')
        # x라벨을 회전
        plt.xticks(rotation=60, fontproperties=prop)
        plt.ylabel('문화체육관광시설 인근 음식점', fontproperties=prop)
        st.pyplot(plt)
        
        st.divider()

        st.subheader(f"{idx.getSubIdx()}인구수 시각화")

        st.write('인구수만 활용하여 그래프를 시각화해보겠습니다.')
        
        st.code('''# 인구수만 포함하는 데이터 프레임 만들기
df_인구 = df_seoul.drop('식당수', axis=1)
df_인구.set_index('SIGNGU_NM', inplace=True)
df_인구''')
        # 인구수만 포함하는 데이터 프레임 만들기
        df_인구 = df_seoul.drop('식당수', axis=1)
        df_인구.set_index('SIGNGU_NM', inplace=True)
        st.write(df_인구)

        st.code('''# 서울시 인구분포 막대그래프 그리기
df_인구.plot(kind='bar', figsize=(10,5), color='orange')
plt.xticks(rotation=60)
plt.xlabel('') # xlabel 이름을 지우기
plt.show()''')
        
        # 서울시 인구분포 막대그래프 그리기
        df_인구.plot(kind='bar', figsize=(10,5), color='orange')
        plt.xticks(rotation=60, fontproperties=prop)
        plt.xlabel('') # xlabel 이름을 지우기
        st.pyplot(plt)

        st.code('''# 수평 막대그래프 그리기 barh
df_인구.plot(kind='barh', figsize=(10,5), color='orange')
# plt.xticks(rotation=60)
plt.ylabel('')
plt.show()''')
        
        # 수평 막대그래프 그리기 barh
        df_인구.plot(kind='barh', figsize=(10,5), color='orange')
        # plt.xticks(rotation=60)
        plt.yticks(fontproperties=prop)
        plt.ylabel('')
        st.pyplot(plt)

        st.divider()

        st.subheader(f"{idx.getSubIdx()}서브플롯 활용하기")

        st.write('- 그래프 2개를 함께 plt에 나타내고 싶습니다.')
        st.write('- 이러한 상황에서 서브플롯을 사용하면 적절합니다.')

        st.code('''# 서브플롯 그리기
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(1,1,1) # 1행 1열 1번째

ax.bar(df_인구.index, df_인구['인구수'], color='orange')
plt.xticks(rotation=60)
plt.show()''')
        
        # 서브플롯 그리기
        fig = plt.figure(figsize=(10,5))
        ax = fig.add_subplot(1,1,1) # 1행 1열 1번째

        ax.bar(df_인구.index, df_인구['인구수'], color='orange')
        plt.xticks(rotation=60, fontproperties=prop)
        st.pyplot(plt)

        st.write('- 수평으로 2개의 그래프를 나타내보겠습니다.')

        st.code('''# 서브 플롯
fig = plt.figure(figsize=(20,5))

ax1 = fig.add_subplot(1,2,1)  # 1행 2열 중 첫번째(왼쪽)
ax2 = fig.add_subplot(1,2,2)  # 1행 2열 중 두번째(오른쪽)
                
# 인구수 막대그래프
ax1.bar(df_인구.index, df_인구['인구수'], color='green')
ax1.set_title('서울시 인구분포')
ax1.set_xticklabels(df_인구.index, rotation=45)

# 식당수 꺽은선그래프
ax2.plot(df_seoul['SIGNGU_NM'], df_seoul['식당수'], 'ro-')
ax2.set_title('서울시 식당분포')
ax2.set_xticklabels(df_seoul['SIGNGU_NM'], rotation=45)

plt.show()''')
        
        # 서브 플롯
        fig = plt.figure(figsize=(20,5))

        ax1 = fig.add_subplot(1,2,1)  # 1행 2열 중 첫번째(왼쪽)
        ax2 = fig.add_subplot(1,2,2)  # 1행 2열 중 두번째(오른쪽)
        # 인구수 막대그래프
        ax1.bar(df_인구.index, df_인구['인구수'], color='green')
        ax1.set_title('서울시 인구분포', fontproperties=prop)
        ax1.set_xticklabels(df_인구.index, rotation=45, fontproperties=prop)

        # 식당수 꺽은선그래프
        ax2.plot(df_seoul['SIGNGU_NM'], df_seoul['식당수'], 'ro-')
        ax2.set_title('서울시 식당분포', fontproperties=prop)
        ax2.set_xticklabels(df_seoul['SIGNGU_NM'], rotation=45, fontproperties=prop)
        st.pyplot(plt)

        st.write('- 수직으로 2개의 그래프를 나타내보겠습니다.')

        st.code('''# 서브 플롯
fig = plt.figure(figsize=(20,10))

ax1 = fig.add_subplot(2,1,1)  # 2행 1열 중 첫번째(위쪽)
ax2 = fig.add_subplot(2,1,2)  # 2행 1열 중 두번째(아래쪽)

# 인구수 막대그래프
ax1.bar(df_인구.index, df_인구['인구수'], color='green')
ax1.set_title('서울시 인구분포')
ax1.set_xticklabels(df_인구.index, rotation=45)

# 식당수 꺽은선그래프
ax2.plot(df_seoul['SIGNGU_NM'], df_seoul['식당수'], 'ro-')
ax2.set_title('서울시 식당분포')
ax2.set_xticklabels(df_seoul['SIGNGU_NM'], rotation=45)

plt.show()''')
        
        # 서브 플롯
        fig = plt.figure(figsize=(20,10))

        ax1 = fig.add_subplot(2,1,1)  # 2행 1열 중 첫번째(위쪽)
        ax2 = fig.add_subplot(2,1,2)  # 2행 1열 중 두번째(아래쪽)

        # 인구수 막대그래프
        ax1.bar(df_인구.index, df_인구['인구수'], color='green')
        ax1.set_title('서울시 인구분포', fontproperties=prop)
        ax1.set_xticklabels(df_인구.index, rotation=45, fontproperties=prop)

        # 식당수 꺽은선그래프
        ax2.plot(df_seoul['SIGNGU_NM'], df_seoul['식당수'], 'ro-')
        ax2.set_title('서울시 식당분포', fontproperties=prop)
        ax2.set_xticklabels(df_seoul['SIGNGU_NM'], rotation=45, fontproperties=prop)

        st.pyplot(plt)

        st.divider()

        st.subheader(f"{idx.getSubIdx()}심화 - 식당 비율 그래프")
        st.write('- 인구 100명당 **식당 수 비율**을 시각화 하고 싶습니다.')
        st.write('- 직관성을 높이기 위해 **서울시 인구수 막대 그래프**와 함께 나타내고 싶습니다.')
        st.write('- 각 그래프를 시각화 하고, **식당 수 비율**과 **인구수**를 함께 나타내보겠습니다.')

        st.code('''# 인구 100명당 식당수 비율 칼럼 생성
df_seoul['식당비율'] = (df_seoul.식당수 / (df_seoul.인구수*0.01))
df_seoul.head()''')
        # 인구 100명당 식당수 비율 칼럼 생성
        df_seoul['식당비율'] = (df_seoul.식당수 / (df_seoul.인구수*0.01))
        st.write(df_seoul.head())

        st.code('''# 식당비율 선그래프

plt.figure(figsize=(8,4))
plt.title('인구 수 대비 식당수')
plt.plot(df_seoul.SIGNGU_NM, df_seoul.식당비율, 'b+-.')
plt.xticks(rotation=45)
plt.show()''')

        plt.figure(figsize=(8,4))
        plt.title('인구 수 대비 식당수', fontproperties=prop)
        plt.plot(df_seoul.SIGNGU_NM, df_seoul.식당비율, 'b+-.')
        plt.xticks(rotation=45, fontproperties=prop)
        st.pyplot(plt)

        st.code('''# 식당 수 막대 그래프도 같이 그리기

plt.figure(figsize=(12,8))
plt.title('서울시 구별 인구수 대비 식당수')
plt.bar(df_seoul.SIGNGU_NM, df_seoul.식당수, color='pink')
plt.plot(df_seoul.SIGNGU_NM, df_seoul.식당비율, 'b*-')
plt.xticks(rotation=45)
plt.show()''')

        plt.figure(figsize=(12,8))
        plt.title('서울시 구별 인구수 대비 식당수', fontproperties=prop)
        plt.bar(df_seoul.SIGNGU_NM, df_seoul.식당수, color='pink')
        plt.plot(df_seoul.SIGNGU_NM, df_seoul.식당비율, 'b*-')
        plt.xticks(rotation=45, fontproperties=prop)
        st.pyplot(plt)

        st.code('''# twinx()함수로 2축 그래프 그리기

plt.figure(figsize=(10,4))
plt.title('서울특별시')
plt.bar(df_seoul.SIGNGU_NM, df_seoul.식당수, color='green', label='음식점수')
plt.legend(bbox_to_anchor=(0.15, 1.22))
plt.xticks(rotation=-45)

y_right = plt.twinx()
y_right.plot(df_seoul.SIGNGU_NM, df_seoul.식당비율, color='purple', marker='o', label='인구 수 대비 음식점')
plt.legend(bbox_to_anchor=(0.23, 1.12))
plt.show()''')


        plt.figure(figsize=(10,4))
        plt.title('서울특별시', fontproperties=prop)
        plt.bar(df_seoul.SIGNGU_NM, df_seoul.식당수, color='green', label='음식점수')
        plt.legend(bbox_to_anchor=(0.15, 1.22), prop=prop)
        plt.xticks(rotation=-45)

        y_right = plt.twinx()
        y_right.plot(df_seoul.SIGNGU_NM, df_seoul.식당비율, color='purple', marker='o', label='인구 수 대비 음식점')
        plt.legend(bbox_to_anchor=(0.23, 1.12), prop=prop)
        st.pyplot(plt)

        st.divider()

        st.subheader(f"{idx.getSubIdx()}심화 - 거주자 원 그래프 그리기")
        st.write('거주자가 많은 순서대로 원 그래프를 그려보겠습니다.')
        st.write('- df를 인구수를 기준으로 정렬하여 저장합니다.')


        st.code('''#거주자순
df_거주자순 = df_seoul.sort_values('인구수', ascending=False, ignore_index=True)
df_거주자순''')
        df_거주자순 = df_seoul.sort_values('인구수', ascending=False, ignore_index=True)
        st.write(df_거주자순)

        st.write('- 비율은 소수점 아래 한 자리까지 나타내도록 하여 원 그래프를 시각화합니다.')

        st.code('''#원그래프 그리기
plt.figure(figsize=(8,8), dpi=100)
df_거주자순['인구수'].plot(kind='pie', label='', autopct='%.1f%%', startangle = 45, labels=df_거주자순['SIGNGU_NM'], cmap='rainbow')
plt.show()''')

        plt.figure(figsize=(8,8), dpi=100)
        df_거주자순['인구수'].plot(kind='pie', label='', autopct='%.1f%%', startangle = 45, labels=df_거주자순['SIGNGU_NM'], cmap='rainbow')
        plt.xticks(fontproperties=prop)
        st.pyplot(plt)
        st.divider()

        st.header(f"{idx.getHeadIdx()}결론 도출")
        
        st.subheader(f"{idx.getSubIdx()}음식점 소비 트렌드 기반 분석 결과")
        st.write('- 서울시에서 식당이 가장 많은 곳은 **강남구**입니다.')
        st.write('- 서울시에서 인구수가 가장 많은 곳은 **송파구**입니다.')
        st.write('- 서울시 인구 100명 당 식당 비율이 가장 높은 곳은 **중구**입니다.')
        st.divider()
        
        st.subheader(f"{idx.getSubIdx()}분석 결과 활용법")
        st.write('- 꺾은선 그래프, 막대 그래프 (식당 수, 인구수)')
        st.write('- 2개의 그래프를 함께 나타내기 (인구수와 식당수)')
        st.write('- 막대 그래프 위에 꺾은 선 그래프 나타내기(인구수와 식당 비율)')
        st.write('- 원 그래프(거주자)')

        st.write('이러한 시각화 자료를 통해 설득력을 더욱 높일 수 있습니다.')


    elif path == ("실습 프로젝트", "날씨별 공공자전거 수요 분석"):
        st.header(f"{idx.getHeadIdx()}날씨별 공공자전거 수요 분석")
        st.write('''
                자전거 대여소는 계절과 날씨에 따라 대여 건수의 변동이 심해, 운영 비용에 큰 영향을 미치고 있습니다. 따라서 날씨예보정보를 활용해 대여건수를 사전에 예측하고, 
                 운영 비용을 조정하기 위한 데이터 분석 및 시각화 실습을 진행합니다.
                 ''')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}데이터 불러오기")
        st.write('- 실습을 위해 **아래의 버튼**을 클릭하여 데이터를 다운로드 해주세요')
        st.write('해당 파일을 압축 해제해 **실습03** 폴더를 :blue-background[data/실습03/]경로로 이동해주세요.')
        with open('data/실습03.zip', "rb") as template_file:
            template_zip = template_file.read()

        st.download_button(label="download data",
                            type="primary",
                            data=template_zip,
                           file_name = "실습03.zip"
        )
        with st.echo():
            # 필요한 패키지 설치
            import numpy as np
            import pandas as pd
            import seaborn as sns
            import matplotlib.pyplot as plt

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

            weather_info.head()
            bike_info.head()

        st.write("**weather_info**")
        st.write(weather_info.head())
        st.write("**bike_info**")
        st.write(bike_info.head())
        st.divider()
        
        st.header(f"{idx.getHeadIdx()}공공자전거 데이터 전처리")
        st.subheader(f"{idx.getSubIdx()}집계 데이터 생성")
        st.write('''날씨 정보와의 결합에 필요한 데이터(**이용건수**)를 생성하기 위해 **대여일자**, **대여시간**으로 집계해줍니다.''')
        st.code('''
                bike_df2 = bike_info.groupby(['대여일자', '대여시간'])['이용건수'].sum()
                bike_df2 = bike_df2.reset_index() #인덱스 재 정렬 , 기존 인덱스를 열로
                
                bike_df2.head()
                ''')
        bike_df2 = bike_info.groupby(['대여일자', '대여시간'])['이용건수'].sum()
        bike_df2 = bike_df2.reset_index() #인덱스 재 정렬 , 기존 인덱스를 열로
        st.write(bike_df2.head())
        st.divider()

        st.subheader(f"{idx.getSubIdx()}파생변수 생성")
        st.write('''대여일자에서 **년도, 월, 일, 요일, 공휴일** 변수를 생성합니다.''')
        st.code('''
                bike_df2['대여일자'] = pd.to_datetime(bike_df2['대여일자'])
                bike_df2['년도'] = bike_df2['대여일자'].dt.year
                bike_df2['월'] = bike_df2['대여일자'].dt.month
                bike_df2['일'] = bike_df2['대여일자'].dt.day
                bike_df2['요일(num)'] = bike_df2['대여일자'].dt.dayofweek
                bike_df2['공휴일'] = 0  #0: 평일 1: 공휴일
                
                # 토요일, 일요일을 공휴일로 설정
                bike_df2.loc[bike_df2['요일(num)'].isin([5,6]),['공휴일']] = 1
                bike_df2.sample(10)
                ''')
        
        bike_df2['대여일자'] = pd.to_datetime(bike_df2['대여일자'])
        bike_df2['년도'] = bike_df2['대여일자'].dt.year
        bike_df2['월'] = bike_df2['대여일자'].dt.month
        bike_df2['일'] = bike_df2['대여일자'].dt.day
        bike_df2['요일(num)'] = bike_df2['대여일자'].dt.dayofweek
        bike_df2['공휴일'] = 0 #0: 평일 1: 공휴일
        
        # 토요일, 일요일을 공휴일로 설정
        bike_df2.loc[bike_df2['요일(num)'].isin([5,6]),['공휴일']] = 1

        st.write(bike_df2.sample(10))
        st.divider()

        st.header(f"{idx.getHeadIdx()}날씨 데이터 전처리")
        st.subheader(f"{idx.getSubIdx()}날짜, 시간 컬럼 생성")
        st.write('''자전거 이용정보와의 결합을 위해 **일시** 칼럼에서 **날짜**와 **시간** 정보를 추출합니다.''')
        st.code('''
                weather_info['날짜'] = weather_info['일시'].str[:10]
                weather_info['시간'] = weather_info['일시'].str[11:13].astype(int)
                ''')
        
        weather_info['날짜'] = weather_info['일시'].str[:10]
        weather_info['시간'] = weather_info['일시'].str[11:13].astype(int)
        st.divider()

        st.subheader(f"{idx.getSubIdx()}컬럼 선택")
        st.write("분석에 사용할 컬럼을 순서대로 가져와서 새 데이터 프레임을 생성합니다.")
        st.code('''
                weather_df = weather_info[['날짜', '시간', '기온(°C)', '강수량(mm)', '풍속(m/s)', '풍향(16방위)', '습도(%)','일조(hr)','일사(MJ/m2)', '적설(cm)','전운량(10분위)', '지면온도(°C)']]
                
                #칼럼명 변경
                weather_df.columns = ['날짜', '시간', '기온', '강수량(mm)', '풍속(m/s)', '풍향(16방위)', '습도(%)','일조','일사', '적설(cm)','전운량',  '지면온도']
                ''')
        weather_df = weather_info[['날짜', '시간', '기온(°C)', '강수량(mm)', '풍속(m/s)', '풍향(16방위)', '습도(%)','일조(hr)','일사(MJ/m2)', '적설(cm)','전운량(10분위)', '지면온도(°C)']]
        weather_df.columns = ['날짜', '시간', '기온', '강수량(mm)', '풍속(m/s)', '풍향(16방위)', '습도(%)','일조','일사', '적설(cm)','전운량',  '지면온도']
        st.divider()
        
        st.subheader(f"{idx.getSubIdx()}결측치 확인")
        st.code('''
                weather_df.isnull().sum()
                ''')
        st.write(weather_df.isnull().sum())
        st.write('''
                **강수량, 적설, 일조, 일사**와 같이 NaN값이 0인 경우는 0으로 fill 해줍니다. **전운량, 기온, 지면온도, 풍향, 풍속**은 같은 일자의 이전시간대의 데이터로 대체합니다.
                ''')
        
        st.write('''
                - NaN 값을 0으로 fill (fillna)
                 ''')
        st.code('''
                weather_df['강수량(mm)'].fillna(0, inplace = True)
                weather_df['적설(cm)'].fillna(0, inplace = True)
                weather_df['일조'].fillna(0, inplace = True)
                weather_df['일사'].fillna(0, inplace = True)
                ''')
        weather_df['강수량(mm)'].fillna(0, inplace = True)
        weather_df['적설(cm)'].fillna(0, inplace = True)
        weather_df['일조'].fillna(0, inplace = True)
        weather_df['일사'].fillna(0, inplace = True)

        st.write('''
                - NaN 값을 직전 데이터의 값으로 fill (ffill)
                 ''')
        st.code('''
                # 날짜 시간으로 정렬
                weather_df = weather_df.sort_values(['날짜','시간'])

                # 전 값으로 
                weather_df['기온'].fillna(method='ffill',inplace = True)
                weather_df['풍속(m/s)'].fillna(method='ffill',inplace = True)
                weather_df['풍향(16방위)'].fillna(method='ffill',inplace = True)
                weather_df['전운량'].fillna(method='ffill',inplace = True)
                weather_df['지면온도'].fillna(method='ffill',inplace = True)
                ''')
        weather_df = weather_df.sort_values(['날짜','시간'])
        weather_df['기온'].fillna(method='ffill',inplace = True)
        weather_df['풍속(m/s)'].fillna(method='ffill',inplace = True)
        weather_df['풍향(16방위)'].fillna(method='ffill',inplace = True)
        weather_df['전운량'].fillna(method='ffill',inplace = True)
        weather_df['지면온도'].fillna(method='ffill',inplace = True)
        
        st.write("결측치를 제거한 결과를 확인해보겠습니다.")
        st.code('''weather_df.isnull().sum()''')
        st.write(weather_df.isnull().sum())
        st.divider()

        st.header(f"{idx.getHeadIdx()}데이터 결합")
        st.write("전처리된 공공자전거 데이터와 날씨 데이터를 결합해 날씨별 자전거 대여 데이터를 만들어보겠습니다.")
        st.code('''
                weather_df['날짜'] = pd.to_datetime(weather_df['날짜'])

                #데이터 타입 맞추기 
                bike_mg = pd.merge (bike_df2, 
                                    weather_df, 
                                    left_on =['대여일자', '대여시간'], 
                                    right_on = ['날짜', '시간']) #default = inner 
                bike_mg.head()
                ''')
        weather_df['날짜'] = pd.to_datetime(weather_df['날짜'])
        #데이터 타입 맞추기 
        bike_mg = pd.merge (bike_df2, 
                            weather_df, 
                            left_on =['대여일자', '대여시간'], 
                            right_on = ['날짜', '시간']) #default = inner 
        st.write(bike_mg.head())

        st.write("**대여일자, 날짜, 시간** 데이터가 중복되는 것을 확인할 수 있습니다. 중복되는 데이터를 제거해보겠습니다.")
        st.code('''
                bike_mg = bike_mg.drop(['대여일자', '날짜', '시간'], axis = 1)
                
                bike_mg.head()
                ''')
        bike_mg = bike_mg.drop(['대여일자', '날짜', '시간'], axis = 1)
        st.write(bike_mg.head())

        ##처리된 데이터 저장 추가할말
        st.divider()

        st.header(f"{idx.getHeadIdx()}데이터 시각화")
        st.write("원본 데이터프레임을 보존하기 위해 복사본을 생성한 후 시각화를 진행하겠습니다.")
        st.code('''data = bike_mg.copy()''')
        data = bike_mg.copy()

        st.subheader(f"{idx.getSubIdx()}데이터 요약 통계")
        st.write("데이터의 요약 통계를 확인해 정상적인 값인지 확인해보겠습니다.")
        st.code('''
                desc_df = data.describe().T
                desc_df
                ''')
        desc_df = data.describe().T
        st.write(desc_df)
        st.divider()

        st.subheader(f"{idx.getSubIdx()}이용건수 분포 시각화")
        st.code('''sns.histplot(data['이용건수'])''')
        fig, ax = plt.subplots()
        sns.histplot(data['이용건수'], ax=ax)
        ax.set_title("이용건수 분포", fontproperties=prop)
        ax.set_xlabel("이용 건수", fontproperties=prop)
        st.pyplot(fig)
        plt.close(fig)

        st.code('''sns.lineplot(x=data['일'], y=data['이용건수'])''')
        fig, ax = plt.subplots()
        sns.lineplot(x=data['일'].map(str), y=data['이용건수'], ax=ax)
        ax.set_xlabel("일", fontproperties=prop)
        ax.set_ylabel("이용 건수", fontproperties=prop)
        st.pyplot(fig)
        plt.close(fig)
        st.divider()
        
        st.subheader(f"{idx.getSubIdx()}피처의 분포 시각화")
        st.write("원하는 컬럼을 선택해 피처의 분포를 확인합니다.")
        st.code('''
                con_cols = ["기온", "강수량(mm)", "풍속(m/s)", "습도(%)", "일조"]
                ''')
        con_cols = ["기온", "강수량(mm)", "풍속(m/s)", "습도(%)", "일조"]
        
        
        st.write("선택된 칼럼에 대한 피처의 분포를 시각화합니다.")
        st.code('''
                fig, axes = plt.subplots(1,5, figsize = (8,8))
                ax = axes.flatten()
                
                # axes = (n,n)형태 / ax = m형태
                for i, col in enumerate(con_cols):
                    sns.histplot(data = data, x = col, ax = ax[i])
                ''')
        
        fig, axes = plt.subplots(1,5, figsize = (8,8))
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
                ''')
        fig, axes = plt.subplots(2,2, figsize = (20,8))
        sns.barplot(data = data, x = '일', y= '이용건수', ax = axes[0,0])
        sns.barplot(data = data, x = '공휴일', y= '이용건수', ax = axes[0,1])
        sns.lineplot(data = data, x = '기온', y= '이용건수', ax = axes[1,0])
        sns.lineplot(data = data, x = '강수량(mm)', y= '이용건수', ax = axes[1,1])
        axes[0,0].set_title('일별 이용건수', fontproperties=prop)
        axes[0,1].set_title('공휴일여부에 따른 이용건수', fontproperties=prop)
        axes[1,0].set_title('기온별 이용건수', fontproperties=prop)
        axes[1,1].set_title('강수량(mm)별 이용건수', fontproperties=prop)
        fig.subplots_adjust(hspace = 0.4)        
        st.pyplot(fig)
        plt.close(fig)

        st.write('''
                공휴일 이용건수보다 평일 이용건수가 더 많음
                -> 분석 결과 작성
                ''')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}평일과 공휴일 이용건수 차이")
        st.write('''평일과 공휴일에는 완전히 다른 이용 현황을 보이는 것을 확인할 수 있습니다.
                 평일의 경우 오전 8시, 오후 6시에 이용건수 피크를 보이는데, 출퇴근으로 인한 영향으로 추측해볼 수 있겠습니다.
                 ''')
        st.code('''plt.figure(figsize = (15,3))
sns.pointplot(x='대여시간', y='이용건수',data = data, hue = '공휴일')
                ''')
        fig, ax = plt.subplots()
        plt.figure(figsize = (15,3))
        sns.pointplot(x='대여시간', y='이용건수',data = data, hue = '공휴일', ax=ax)
        st.pyplot(fig)
        plt.close(fig)
        st.divider()

        st.subheader(f"{idx.getSubIdx()}요일에 따른 이용건수 차이")
        st.write("토요일에 이용건수가 더 많고, 토요일 오후에 전반적으로 이용률이 높은 모습을 보입니다.")
        st.code('''plt.figure(figsize = (15,3))
sns.pointplot(x='대여시간', y='이용건수',data = data, hue = '요일(num)'))
                ''')
        fig, ax = plt.subplots()
        plt.figure(figsize = (15,3))
        sns.pointplot(x='대여시간', y='이용건수',data = data, hue = '요일(num)', ax=ax)
        st.pyplot(fig)
        plt.close(fig)
        st.divider()

        st.subheader(f"{idx.getSubIdx()}요일에 따른 이용건수 차이(box)")
        st.write("휴일은 상대적으로 변동성이 적고, 평일은 변동성이 큰 편입니다.")
        st.code('''
                sns.boxplot(x='요일(num)', y='이용건수',data = data)
                dofw = list('월화수목금토일')
                plt.xticks([0,1,2,3,4,5,6],dofw)
                plt.show()
                ''')
        fig, ax = plt.subplots()
        plt.figure(figsize = (15,3))
        sns.boxplot(x='요일(num)', y='이용건수',data = data, ax=ax)
        # 요일 이름 설정
        dofw = list('월화수목금토일')
        ax.set_xticks([0, 1, 2, 3, 4, 5, 6])
        ax.set_xticklabels(dofw)
        st.pyplot(fig)
        plt.close(fig)
        st.divider()

        #######분석 결과
        
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
