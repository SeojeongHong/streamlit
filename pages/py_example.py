import streamlit as st
from streamlit_option_menu import option_menu

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
