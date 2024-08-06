import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False
import numpy as np

@st.cache_data
def load_contents() :
    #topic - chapter - section
    contents = {
        "파이썬 기초": {
            "자료형": ["숫자형", "문자열", "불", "리스트", "튜플", "딕셔너리", "집합"],
            "제어문": ["if문", "while문", "for문"],
            "고급": ["함수", "클래스", "모듈", "패키지"]
        },
        "Pandas 기초": {
            "대단원 01": ["소단원01", "소단원02", "소단원03"],
            "대단원 02": ["소단원01", "소단원02"],
            "대단원 03": ["소단원01"],
            "대단원 04": ["소단원01", "소단원02", "소단원03", "소단원04"],
            "대단원 05": ["소단원01", "소단원02"]
        },
        "Matplotlib 기초": {
            "Matplotlib 기본" : ["기본 사용", "숫자 입력하기", "타이틀"],
            "Matplotlib 스타일": ["단일/다중 그래프", "여러개의 Plot을 그리는 방법(Subplot)", "주요 스타일 옵션", "축 레이블(Label) 설정하기", "범례(Legend) 설정", "축 범위 지정하기", "스타일 세부 설정 - 선 종류 지정", "스타일 세부 설정 - 마커 지정", "스타일 세부 설정 - 색상 지정", "그리드(Grid)", "Annotate 설정"],
            "Matplotlib 그래프": ["Scatterplot", "컬러맵 그리기", "막대 그래프 그리기", "수평 막대 그래프 그리기", "Line Plot", "Areaplot(Filled Area)", "Histogram", "Pie Chart", "Box Plot", "3D 그래프", "Text 삽입"]
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
            "Matplotlib 기초" : '''matplotlib.pyplot 모듈은 명령어 스타일로 동작하는 함수의 모음입니다.\n
matplotlib.pyplot 모듈의 각각의 함수를 사용해서 그래프 영역을 만들고, 몇 개의 선을 표현하고, 레이블로 꾸미는 등 간편하게 그래프를 만들고 변화를 줄 수 있습니다.''',
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
    path = (topic, chapter, section)

    ### 컨텐츠 작성
    if path == ("파이썬 기초", "자료형", "숫자형") :
        st.subheader("숫자형이란")
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

        st.subheader("숫자형의 연산 - 산술 연산자")
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

        st.subheader("숫자형의 연산 - 복합 연산자")
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
    elif path == ("파이썬 기초", "자료형", "문자열") :
        st.subheader("문자열이란")
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
        st.subheader("문자열 길이 구하기")
        st.write("문자열의 길이는 다음과 같이 len 함수를 사용하면 구할 수 있습니다.")
        st.code('''
                a = "Life is too short"
                print(len(a))
                #출력 : 17
                ''')
        st.divider()
        st.subheader("문자열 인덱싱")
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

        st.subheader("문자열 슬라이싱")
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

        st.subheader("문자열 관련 함수")
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
    elif path == ("파이썬 기초", "자료형", "불") :
        st.subheader("불이란")
        st.write('''
                불(bool)이란 참(True)과 거짓(False)을 나타내는 자료형입니다. 불 자료형은 다음 2가지 값만을 가질 수 있습니다.

                - True: 참을 의미한다.
                - False: 거짓을 의미한다.
                
                True나 False는 파이썬의 예약어로, true, false와 같이 작성하면 안 되고 첫 문자를 항상 대문자로 작성해야 합니다.
                 ''')
        st.divider()
        st.subheader("불 자료형 사용법")
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
        st.subheader("자료형의 참과 거짓")
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
    elif path == ("파이썬 기초", "자료형", "리스트") :
        st.subheader("리스트란")
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
        st.subheader("리스트의 인덱싱")
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

        st.subheader("리스트의 슬라이싱")
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
        st.subheader("리스트 길이 구하기")
        st.write("리스트 길이를 구하기 위해서는 다음처럼 len 함수를 사용해야 합니다.")
        st.code('''
                a = [1, 2, 3]
                print(len(a))
                #출력 : 3
                ''')
        st.write("len은 문자열, 리스트 외에 앞으로 배울 튜플과 딕셔너리에도 사용할 수 있는 함수입니다.")
        
        st.divider()
        st.subheader("리스트 값 수정하기")
        st.write("리스트의 인덱스를 통해 요소에 접근하고 값을 수정할 수 있습니다.")
        st.code('''
                a = [1, 2, 3]
                a[2] = 4

                print(a)
                #출력 : [1, 2, 4]
                ''')
        st.divider()
        st.subheader("리스트 요소 삭제하기")
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
        st.subheader("리스트 관련 함수")
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
    elif path == ("파이썬 기초", "자료형", "튜플") :
        st.subheader("튜플이란")
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

        st.subheader("튜플의 인덱싱")
        st.write("문자열, 리스트와 마찬가지로 튜플 또한 인덱싱이 가능합니다.")
        st.code('''
                t1 = (1, 2, 'a', 'b')

                print(t1[0])
                # 출력 : 1

                print(t1[3])
                # 출력 : 'b'
                ''')
        st.divider()

        st.subheader("튜플의 슬라이싱")
        st.code('''
                t1 = (1, 2, 'a', 'b')

                print(t1[1:])
                # 출력 : (2, 'a', 'b')
                ''')
        st.divider()

        st.subheader("튜플 길이 구하기")
        st.code('''
                t1 = (1, 2, 'a', 'b')
                print(len(t1))
                #출력 : 4
                ''')   
    elif path == ("파이썬 기초", "자료형", "딕셔너리") :
        st.subheader("딕셔너리란")
        st.write('''
                딕셔너리(dictionary)란 단어 그대로 '사전'이라는 뜻입니다. 딕셔너리의 기본 구조는 아래와 같이 Key와 Value를 한 쌍으로 가지며, 리스트나 튜플처럼 순차적으로 해당 요솟값을 구하지 않고 Key를 통해 Value를 얻는 특징을 가집니다.
        
                    {Key1: Value1, Key2: Value2, Key3: Value3, ...}
                
                ''')
        st.divider()

        st.subheader("딕셔너리 생성하기")
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
        st.subheader("딕셔너리 쌍 추가, 삭제하기")
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

        st.subheader("딕셔너리 관련 함수")
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
    elif path == ("파이썬 기초", "자료형", "집합") :
        st.subheader("집합이란")
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
        st.subheader("집합의 연산")
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

        st.subheader("집합 관련 함수")
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
    #"제어문": ["if문", "while문", "for문"]
    elif path == ("파이썬 기초", "제어문", "if문") :
        st.subheader("if문 기본 구조")
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
        st.subheader("조건문 유형 - 비교 연산자")
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
        st.subheader("조건문 유형 - and, or, not")
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

        st.subheader("조건문 유형 - in, not in")
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
    elif path == ("파이썬 기초", "제어문", "while문") :
        st.subheader("while문이란")
        st.write("문장을 반복해서 수행해야 할 경우 while 문을 사용합니다. 그래서 while 문을 ‘반복문’이라고도 부릅니다.")
        st.divider()

        st.subheader("while문의 기본 구조")
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

        st.subheader("while 문 강제로 빠져나가기")
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
        st.subheader("while 문의 맨 처음으로 돌아가기")
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
    elif path == ("파이썬 기초", "제어문", "for문") :
        st.subheader("for문이란")
        st.write('''
                 for문은 정해진 횟수나 범위 안에서 차례대로 대입하며 반복을 수행하는 반복문입니다. 아래와 같은 기본 구조를 가집니다.
                 
                        for 변수 in 리스트(또는 튜플, 문자열):
                            수행할_문장1
                            수행할_문장2
                            ...

                리스트나 튜플, 문자열의 첫 번째 요소부터 마지막 요소까지 차례로 변수에 대입되어 for문 내 문장들이 수행됩니다.

                 ''')
        st.divider()
        st.subheader("for문 사용법")
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

        st.subheader("for문과 continue문")
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

        st.subheader("for문과 함께 자주 사용하는 range 함수")
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
    #  "고급": ["함수", "클래스", "모듈", "패키지"]
    elif path == ("파이썬 기초", "고급", "함수") :
        st.subheader("함수란")
        st.write("코드의 반복을 줄이거나 어떠한 용도를 위해 특정 코드들을 모아둔 것입니다. 한 번 작성해두면 해당 코드가 필요할 때 함수를 호출해서 쉽게 재사용 할 수 있고, 용도에 따라 분리가 가능해 가독성이 좋습니다.")
        st.divider()

        st.subheader("함수의 구조")
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

        st.subheader("매개변수와 인수")
        st.write("매개변수는 함수에 입력으로 전달된 값을 받는 변수, 인수는 함수를 호출할 때 전달하는 입력값을 의미합니다.")

        st.code('''
                def add(a, b):  # a, b는 매개변수
                    return a+b

                print(add(3, 4))  # 3, 4는 인수
                ''')
        st.divider()
        st.subheader("return(반환값)")
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
        st.subheader("lambda")
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
    ### 박은수
    ### Matplotlib 컨텐츠 작성
    elif path == ("Matplotlib 기초", "Matplotlib 기본", "기본 사용"):
        st.header("기본 사용")
        st.write("Matplotlib 라이브러리를 이용해서 그래프를 그리는 일반적인 방법에 대해 소개합니다.")
        
        st.subheader("기본 그래프 그리기")
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

        st.subheader("스타일 지정하기")
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

        st.subheader("여러 개의 그래프 그리기")
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


    elif path == ("Matplotlib 기초", "Matplotlib 기본", "숫자 입력하기"):
        st.header("숫자 입력하기")
        st.subheader("기본 사용")
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

        st.subheader("x, y 값 입력하기")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3, 4], [2, 3, 5, 10])
            plt.show()
        st.write("plot() 함수에 두 개의 리스트를 입력하면 순서대로 x, y 값들로 인식해서 점 (1, 2), (2, 3), (3, 5), (4, 10)를 잇는 꺾은선 그래프가 나타납니다.")
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader("레이블이 있는 데이터 사용하기")
        with st.echo(): 
            import matplotlib.pyplot as plt

            data_dict = {'data_x': [1, 2, 3, 4, 5], 'data_y': [2, 3, 5, 10, 8]}

            plt.plot('data_x', 'data_y', data=data_dict)
            plt.show()
        st.write("파이썬 딕셔너리와 같이 레이블이 있는 데이터를 그래프로 나타낼 수 있습니다.")
        st.write("예제에서와 같이, 먼저 plot() 함수에 데이터의 레이블 (딕셔너리의 키)을 입력해주고, data 파라미터에 딕셔너리를 지정해줍니다.")
        st.pyplot(plt)
        plt.close()
    
    elif path == ("Matplotlib 기초", "Matplotlib 기본", "타이틀"):
        st.header("타이틀")
        st.write("**matplotlib.pyplot** 모듈의 **title()** 함수를 이용해서 그래프의 타이틀 (Title)을 설정할 수 있습니다.")
        st.write("이 페이지에서는 그래프의 타이틀을 표시하고 위치를 조절하는 방법, 그리고 타이틀의 폰트와 스타일을 설정하는 방법에 대해 알아봅니다.")
        
        st.subheader("기본 사용")
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

        st.subheader("위치와 오프셋 지정하기")
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

        st.subheader("폰트 지정하기")
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

        st.subheader("타이틀 얻기")
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

    elif path == ("Matplotlib 기초", "Matplotlib 스타일", "단일/다중 그래프"):
        st.header("단일/다중 그래프 생성")
        st.subheader("단일 그래프 생성")
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

        st.subheader("다중 그래프(Multiple graphs)")
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

    elif path == ("Matplotlib 기초", "Matplotlib 스타일", "여러개의 Plot을 그리는 방법(Subplot)"):
        st.header("여러개의 Plot을 그리는 방법(Subplot)")
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

        st.subheader("여러개의 plot을 그리는 방법(subplots) - s가 더 붙습니다.")
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

    elif path == ("Matplotlib 기초", "Matplotlib 스타일", "주요 스타일 옵션"):
        st.header("주요 스타일 옵션")
        st.write("subplot(row, column, index)")
        with st.echo():
            import matplotlib.pyplot as plt
            from IPython.display import Image

            # 출처: matplotlib.org
            Image('https://matplotlib.org/_images/anatomy.png')

        st.pyplot(plt)
        plt.close()
    
    elif path == ("Matplotlib 기초", "Matplotlib 스타일", "축 레이블(Label) 설정하기"):
        st.header("축 레이블(Label) 설정하기")
        st.write("**matplotlib.pyplot** 모듈의 **xlabel(), ylabel()** 함수를 사용하면 그래프의 x, y 축에 대한 레이블을 표시할 수 있습니다.")
        st.write("이 페이지에서는 xlabel(), ylabel() 함수를 사용해서 그래프의 축에 레이블을 표시하는 방법에 대해 소개합니다.")

        st.subheader("기본 사용")
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

        st.subheader("여백 지정하기")
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

        st.subheader("폰트 설정하기")
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

        st.subheader("위치 저장하기")
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
            plt.title("이것은 타이틀 입니다")

            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()
        
        st.subheader("X, Y 축 Tick 설정(rotation)")
        st.write("Tick은 X, Y축에 위치한 눈금을 말합니다.")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            plt.plot(np.arange(10), np.arange(10)*2)
            plt.plot(np.arange(10), np.arange(10)**2)
            plt.plot(np.arange(10), np.log(np.arange(10)))

            # 타이틀 & font 설정
            plt.title('X, Y 틱을 조정합니다', fontsize=10)

            # X축 & Y축 Label 설정
            plt.xlabel('X축', fontsize=10)
            plt.ylabel('Y축', fontsize=10)

            # X tick, Y tick 설정
            plt.xticks(rotation=90)
            plt.yticks(rotation=30)

            plt.show()
        st.pyplot(plt)
        plt.close()

    elif path == ("Matplotlib 기초", "Matplotlib 스타일", "범례(Legend) 설정"):
        st.header("범례(Legend) 설정")
        st.write("**범례 (Legend)** 는 그래프에 데이터의 종류를 표시하기 위한 텍스트입니다.")
        st.write("**matplotlib.pyplot** 모듈의 **legend()** 함수를 사용해서 그래프에 범례를 표시할 수 있습니다.")
        st.write("이 페이지에서는 그래프에 다양한 방식으로 범례를 표시하는 방법에 대해 소개합니다.")

        st.subheader("기본 사용")
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

        st.subheader("위치 지정하기")
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

        st.subheader("열 개수 지정하기")
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

        st.subheader("폰트 크기 지정하기")
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

        st.subheader("범례 테두리 꾸미기")
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

    elif path == ("Matplotlib 기초", "Matplotlib 스타일", "축 범위 지정하기"):
        st.header("축 범위 지정하기")
        st.write("**matplotlib.pyplot** 모듈의 **xlim(), ylim(), axis()** 함수를 사용하면 그래프의 X, Y축이 표시되는 범위를 지정할 수 있습니다.")
        st.write("◾ xlim() - X축이 표시되는 범위를 지정하거나 반환합니다.")
        st.write("◾ ylim() - Y축이 표시되는 범위를 지정하거나 반환합니다.")
        st.write("◾ axis() - X, Y축이 표시되는 범위를 지정하거나 반환합니다.")
        st.write("이 페이지에서는 그래프의 축의 범위를 지정하고, 확인하는 방법에 대해 소개합니다.")
        
        st.subheader("기본 사용 - xlim(), ylim()")
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

        st.subheader("기본사용 - axis()")
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

        st.subheader("옵션 지정하기")
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

        st.subheader("축 범위 얻기")
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



    
    elif path == ("Matplotlib 기초", "Matplotlib 스타일", "스타일 세부 설정 - 선 종류 지정"):
        st.header("스타일 세부 설정 - 선 종류 지정")
        st.write("데이터를 표현하기 위해 그려지는 선의 종류를 지정하는 방법을 소개합니다.")
        st.write("선 종류를 나타내는 문자열 또는 튜플을 이용해서 다양한 선의 종류를 구현할 수 있습니다.")

        st.subheader("기본 사용")
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

        st.subheader("linestyle 지정하기")
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

        st.subheader("튜플 사용하기")
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

        st.subheader("선 끝 모양 지정하기")
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

    elif path == ("Matplotlib 기초", "Matplotlib 스타일", "스타일 세부 설정 - 마커 지정"):
        st.header("스타일 세부 설정 - 마커 지정")
        st.write("특별한 설정이 없으면 그래프가 실선으로 그려지지만, 위의 그림과 같은 마커 형태의 그래프를 그릴 수 있습니다.")
        st.write("**plot()** 함수의 **포맷 문자열 (Format string)** 을 사용해서 그래프의 선과 마커를 지정하는 방법에 대해 알아봅니다.")
        st.subheader("기본 사용")
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

        st.subheader("선/마커 동시에 나타내기")
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

        st.subheader("선/마커 표시 형식")
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

        st.subheader("marker 파라미터 사용하기")
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
    
    elif path == ("Matplotlib 기초", "Matplotlib 스타일", "스타일 세부 설정 - 색상 지정"):
        st.header("스타일 세부 설정 - 색상 지정")
        st.write("**matplotlib.pyplot** 모듈의 **plot()** 함수를 사용해서 그래프를 나타낼 때, 색상을 지정하는 다양한 방법에 대해 소개합니다.")
        
        st.subheader("기본 색상")
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
            plt.title('색상 설정 예제', fontsize=10)

            # X축 & Y축 Label 설정
            plt.xlabel('X축', fontsize=10)
            plt.ylabel('Y축', fontsize=10)

            # X tick, Y tick 설정
            plt.xticks(rotation=90)
            plt.yticks(rotation=30)

            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader("color 키워드 인자 사용하기")
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

        st.subheader("포맷 문자열 사용하기")
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

        st.subheader("Hex code 사용하기")
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

        st.subheader("투명도 설정")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            plt.plot(np.arange(10), np.arange(10)*2, color='b', alpha=0.1)
            plt.plot(np.arange(10), np.arange(10)*2 - 10, color='b', alpha=0.3)
            plt.plot(np.arange(10), np.arange(10)*2 - 20, color='b', alpha=0.6)
            plt.plot(np.arange(10), np.arange(10)*2 - 30, color='b', alpha=1.0)

            # 타이틀 & font 설정
            plt.title('투명도 (alpha) 설정 예제', fontsize=10)

            # X축 & Y축 Label 설정
            plt.xlabel('X축', fontsize=10)
            plt.ylabel('Y축', fontsize=10)

            # X tick, Y tick 설정
            plt.xticks(rotation=90)
            plt.yticks(rotation=30)

            plt.show()
        st.pyplot(plt)
        plt.close()

    elif path == ("Matplotlib 기초", "Matplotlib 스타일", "그리드(Grid)"):
        st.header("그리드(Grid)")
        st.write("데이터의 위치를 더 명확하게 나타내기 위해 그래프에 그리드 **(Grid, 격자)** 를 표시할 수 있습니다.")
        st.write("이 페이지에서는 **matplotlib.pyplot** 모듈의 **grid()** 함수를 이용해서 그래프에 다양하게 그리드를 설정해 보겠습니다.")
        st.subheader("기본 사용")
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

        st.subheader("축 지정하기")
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

        st.subheader("스타일 설정하기")
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
    
    elif path == ("Matplotlib 기초", "Matplotlib 스타일", "Annotate 설정"):
        st.header("Annotate 설정")
        with st.echo():
            import matplotlib.pyplot as plt
            import numpy as np

            plt.plot(np.arange(10), np.arange(10)*2, marker='o', linestyle='-', color='b')
            plt.plot(np.arange(10), np.arange(10)*2 - 10, marker='v', linestyle='--', color='c')
            plt.plot(np.arange(10), np.arange(10)*2 - 20, marker='+', linestyle='-.', color='y')
            plt.plot(np.arange(10), np.arange(10)*2 - 30, marker='*', linestyle=':', color='r')

            # 타이틀 & font 설정
            plt.title('그리드 설정 예제', fontsize=10)

            # X축 & Y축 Label 설정
            plt.xlabel('X축', fontsize=10)
            plt.ylabel('Y축', fontsize=10)

            # X tick, Y tick 설정
            plt.xticks(rotation=90)
            plt.yticks(rotation=30)

            # annotate 설정
            plt.annotate('코로나 사태 발생 지점', xy=(3, -20), xytext=(3, -25), arrowprops=dict(facecolor='black', shrink=0.05))

            # grid 옵션 추가
            plt.grid()

            plt.show()
        st.pyplot(plt)
        plt.close()

    elif path == ("Matplotlib 기초", "Matplotlib 그래프", "Scatterplot"):
        st.header("Scatterplot")
        st.write("**산점도 (Scatter plot)** 는 두 변수의 상관 관계를 직교 좌표계의 평면에 점으로 표현하는 그래프입니다.")
        st.write("**matplotlib.pyplot** 모듈의 **scatter()** 함수를 이용하면 산점도를 그릴 수 있습니다.")
        st.subheader("기본 사용")
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

        st.subheader("색상과 크기 지정하기")
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

        st.subheader("투명도와 컬러맵 설정하기")
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

    elif path == ("Matplotlib 기초", "Matplotlib 그래프", "컬러맵 그리기"):
        st.header("컬러맵 그리기")
        st.write("**matplotlib.pyplot** 모듈은 컬러맵을 간편하게 설정하기 위한 여러 함수를 제공합니다.")
        st.write("아래의 함수들을 사용해서 그래프의 컬러맵을 설정하는 방식에 대해 소개합니다.")
        st.write("**autumn(), bone(), cool(), copper(), flag(), gray(), hot(), hsv(), inferno(), jet(), magma(), nipy_spectral(), pink(), plasma(), prism(), spring(), summer(), viridis(), winter().**")
        st.subheader("기본 사용")
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

        st.subheader("컬러바 나타내기")
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

        st.subheader("컬러맵 종류")
        with st.echo():
            import matplotlib.pyplot as plt
            from matplotlib import cm

            cmaps = plt.colormaps()
            for cm in cmaps:
                print(cm)
        st.write("pyplot 모듈의 **colormaps()** 함수를 사용해서 Matplotlib에서 사용할 수 있는 모든 컬러맵의 이름을 얻을 수 있습니다.")
        st.write("예를 들어, **winter** 와 **winter_r** 은 순서가 앞뒤로 뒤집어진 컬러맵입니다.")

    elif path == ("Matplotlib 기초", "Matplotlib 그래프", "막대 그래프 그리기") :
        st.header("막대 그래프 그리기")
        st.write("**막대 그래프 (Bar graph, Bar chart)** 는 범주가 있는 데이터 값을 직사각형의 막대로 표현하는 그래프입니다.")
        st.write("Matplotlib에서는 **matplotlib.pyplot** 모듈의 **bar()** 함수를 이용해서 막대 그래프를 간단하게 표현할 수 있습니다.")
        st.subheader("기본 사용")
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

        st.subheader("비교 그래프 그리기")
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

        st.subheader("색상 지정하기")
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

        st.subheader("막대 폭 지정하기")
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

        st.subheader("스타일 꾸미기")
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

    elif path == ("Matplotlib 기초", "Matplotlib 그래프", "수평 막대 그래프 그리기") :
        st.header("수막대 그래프 그리기")
        st.write("**수평 막대 그래프 (Horizontal bar graph)** 는 범주가 있는 데이터 값을 수평 막대로 표현하는 그래프입니다.")
        st.write("**matplotlib.pyplot** 모듈의 **barh()** 함수를 사용해서 수평 막대 그래프를 그리는 방법을 소개합니다.")
        st.subheader("기본 사용")
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

        st.subheader("비교 그래프 그리기")
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

        st.subheader("막대 높이 지정하기")
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

        st.subheader("Barplot(축 변환)")
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

    elif path == ("Matplotlib 기초", "Matplotlib 그래프", "Line Plot") :
        st.header("Line Plot")
        st.subheader("기본 lineplot 그리기")
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

        st.subheader("2개 이상의 그래프 그리기")
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

        st.subheader("마커 스타일링")
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

        st.subheader("라인 스타일 변경")
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
    
    elif path == ("Matplotlib 기초", "Matplotlib 그래프", "Areaplot(Filled Area)") :
        st.header("Areaplot(Filled Area)")
        st.write("matplotlib에서 area plot을 그리고자 할 때는 **fill_between** 함수를 사용합니다.")
        code='''import matplotlib.pyplot as plt
import numpy as np

y = np.random.randint(low=5, high=10, size=20)
y'''
        st.code(code, language="python")
        st.write("**[ 출력 ]**")
        code='''array([9, 8, 9, 5, 7, 6, 8, 7, 6, 5, 6, 6, 9, 7, 7, 5, 7, 8, 5, 7])'''
        st.code(code, language="python")

        st.subheader("기본 areaplot 그리기")
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

        st.subheader("경계선을 굵게 그리고 area는 옆게 그리는 효과 적용")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.fill_between(x, y, color="green", alpha=0.3)
            plt.plot(x, y, color="green", alpha=0.8)
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader("여러 그래프를 겹쳐서 표현")
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

    elif path == ("Matplotlib 기초", "Matplotlib 그래프", "Histogram") :
        st.header("Histogram")
        st.write("**히스토그램 (Histogram)은 도수분포표를 그래프로 나타낸 것으로서, 가로축은 계급, 세로축은 도수 (횟수나 개수 등)** 를 나타냅니다.")
        st.write("이번에는 **matplotlib.pyplot** 모듈의 **hist()** 함수를 이용해서 다양한 히스토그램을 그려 보겠습니다.")
        st.subheader("기본 사용")
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

        st.subheader("구간 개수 지정하기")
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

        st.subheader("누적 히스토그램 그리기")
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

        st.subheader("히스토그램 종류 지정하기")
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

        st.subheader("NumPy 난수의 분포 나타내기")
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

    elif path == ("Matplotlib 기초", "Matplotlib 그래프", "Pie Chart") :
        st.header("Pie Chart")
        st.write("**파이 차트 (Pie chart, 원 그래프)** 는 범주별 구성 비율을 원형으로 표현한 그래프입니다.")
        st.write("위의 그림과 같이 **부채꼴의 중심각을 구성 비율에 비례** 하도록 표현합니다.")
        st.write("**matplotlib.pyplot** 모듈의 **pie()** 함수를 이용해서 파이 차트를 그리는 방법에 대해 소개합니다.")
        st.subheader("pie chart 옵션")
        st.write("◾ explode : 파이에서 툭 튀어져 나온 비율")
        st.write("◾ autopct : 퍼센트 자동으로 표기")
        st.write("◾ shadow : 그림자 표시")
        st.write("◾ startangle : 파이를 그리기 시작할 각도")
        st.divider()

        st.subheader("기본 사용")
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

        st.subheader("시작 각도와 방향 설정하기")
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

        st.subheader("중심에서 벗어나는 정도 설정하기")
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

        st.subheader("그림자 나타내기")
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

        st.subheader("색상 지정하기")
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

        st.subheader("부채꼴 스타일 지정하기")
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

    elif path == ("Matplotlib 기초", "Matplotlib 그래프", "Box Plot") :
        st.header("Box Plot")
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
        
        st.subheader("기본 박스플롯 생성")
        with st.echo():
            import matplotlib.pyplot as plt

            plt.boxplot(data)
            plt.tight_layout()
            plt.show()
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader("Box Plot 축 바꾸기")
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

        st.subheader("Outlier 마커 심볼과 컬러 변경")
        with st.echo():
            outlier_marker = dict(markerfacecolor='r', marker='D')
        with st.echo():
            import matplotlib.pyplot as plt

            plt.title('Changed Outlier Symbols', fontsize=15)
            plt.boxplot(data, flierprops=outlier_marker)

            plt.show()
        st.pyplot(plt)
        plt.close()
        
    elif path == ("Matplotlib 기초", "Matplotlib 그래프", "3D 그래프") :
        st.header("3D 그래프")
        st.write("3D로 그래프를 그리기 위해서는 mplot3d를 추가로 import 합니다")
        with st.echo():
            from mpl_toolkits import mplot3d

        st.subheader("밑그림 그리기(캔버스)")
        with st.echo():
            import matplotlib.pyplot as plt

            fig = plt.figure()
            ax = plt.axes(projection='3d')
        st.pyplot(plt)
        plt.close()
        st.divider()

        st.subheader("3D plot 그리기")
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

    elif path == ("Matplotlib 기초", "Matplotlib 그래프", "Text 삽입") :
        st.header("Text 삽입")
        st.write("matplotlib.pyplot 모듈의 **text()** 함수는 그래프의 적절한 위치에 텍스트를 삽입하도록 합니다.")
        st.write("이 페이지에서는 **text()** 함수를 사용해서 그래프 영역에 텍스트를 삽입하고, 다양하게 꾸미는 방법에 대해 소개합니다.")
        st.write("이 페이지에서 사용하는 히스토그램 예제는 :blue[Histogram] 페이지를 참고하세요.")

        st.subheader("기본 사용")
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

        st.subheader("텍스트 스타일 설정하기")
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

        st.subheader("텍스트 회전하기")
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

    else :
        st.error("Content Not Found !")

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
