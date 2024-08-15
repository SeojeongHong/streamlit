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
import pandas as pd

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
    st.title(chapter)
    path = (topic, chapter)

    ### Python 컨텐츠 작성
    if path == ("파이썬 기초", "자료형") :
        st.header(f"{idx.getHeadIdx()}숫자형")
        st.write("숫자형에는 정수형(Integer)과 실수형(Float)이 있습니다. 정수는 양의 정수와 음의 정수, 0이 될 수 있는 숫자입니다. 실수는 소수점이 포함된 숫자를 의미합니다.")
        
###############################################################################################################
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
        st.code('''
                # 필요한 패키지 설치
                import numpy as np
                import pandas as pd
                import seaborn as sns
                import matplotlib.pyplot as plt

                # #한글 표시 -> 캐싱
                plt.rcParams['font.family'] = 'NanumGothic'
                plt.rc('font', family='NanumGothic')
                ''', line_numbers=True)

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
        #------------------------------------------------------------
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
        #------------------------------------------------------------
        st.write("**weather_info**")
        st.code('''weather_info.sample(5)''', line_numbers=True)
        st.write(weather_info.sample(5))
        
        st.write("**bike_info**")
        st.code('''bike_info.sample(5)''', line_numbers=True)
        st.write(bike_info.sample(5))
        st.divider()
        
        st.header(f"{idx.getHeadIdx()}공공자전거 데이터 전처리")
        st.subheader(f"{idx.getSubIdx()}집계 데이터 생성")
        st.write('''날씨 정보와의 결합에 필요한 데이터(**이용건수**)를 생성하기 위해 **대여일자**, **대여시간**으로 집계해줍니다.''')
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
                **강수량, 적설, 일조, 일사**와 같이 NaN값이 0인 경우는 0으로 fill 해줍니다. **전운량, 기온, 지면온도, 풍향, 풍속**은 같은 일자의 이전시간대의 데이터로 대체합니다.
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
        # NaN 값을 직전 데이터의 값으로 fill (ffill)
        # 날짜 시간으로 정렬
        weather_df = weather_df.sort_values(['날짜','시간'])

        # 전 값으로 
        weather_df['기온'] = weather_df['기온'].ffill()
        weather_df['풍속(m/s)']= weather_df['풍속(m/s)'].ffill()
        weather_df['풍향(16방위)'] = weather_df['풍향(16방위)'].ffill()
        weather_df['전운량'] = weather_df['전운량'].ffill()
        weather_df['지면온도'] = weather_df['지면온도'].ffill()
        
        st.write("결측치를 제거한 결과를 확인해보겠습니다.")
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
        #데이터 결합
        weather_df['날짜'] = pd.to_datetime(weather_df['날짜'])

        #데이터 타입 맞추기 
        bike_mg = pd.merge (bike_df2, 
                            weather_df, 
                            left_on =['대여일자', '대여시간'], 
                            right_on = ['날짜', '시간']) #default = inner 
        st.write(bike_mg.head())

        st.write("**대여일자, 날짜, 시간** 데이터가 중복되는 것을 확인할 수 있습니다. 중복되는 데이터를 제거해보겠습니다.")
        st.code('''
                #중복데이터 제거
                bike_mg = bike_mg.drop(['대여일자', '날짜', '시간'], axis = 1)

                bike_mg.head()
                ''',line_numbers=True)
        #중복데이터 제거
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

        st.subheader(f"{idx.getSubIdx()}데이터 요약 통계")
        st.write("데이터의 요약 통계를 확인해 정상적인 값인지 확인해보겠습니다.")
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
        ax.set_xlabel('이용건수', fontproperties=prop)
        st.pyplot(fig)
        plt.close(fig)
        

        st.code('''
                sns.lineplot(x=data['일'], y=data['이용건수'])

                plt.show()
                ''',line_numbers=True)
        fig, ax = plt.subplots()
        sns.lineplot(x=data['일'], y=data['이용건수'], ax=ax)
        ax.set_xlabel('일', fontproperties=prop)
        ax.set_ylabel('이용건수', fontproperties=prop)
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
        ax[0].set_xlabel('기온', fontproperties=prop)
        ax[1].set_xlabel('강수량(mm)', fontproperties=prop)
        ax[2].set_xlabel('풍속(m/s)', fontproperties=prop)
        ax[3].set_xlabel('습도(%)', fontproperties=prop)
        ax[4].set_xlabel('일조', fontproperties=prop)
        
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
        axes[0,0].set_xlabel('일', fontproperties=prop)
        axes[0,0].set_ylabel('이용건수', fontproperties=prop)
        
        axes[0,1].set_title('공휴일여부에 따른 이용건수', fontproperties=prop)
        axes[0,1].set_xlabel('공휴일', fontproperties=prop)
        axes[0,1].set_ylabel('이용건수', fontproperties=prop)
        
        axes[1,0].set_title('기온별 이용건수', fontproperties=prop)
        axes[1,0].set_xlabel('기온', fontproperties=prop)
        axes[1,0].set_ylabel('이용건수', fontproperties=prop)
        
        axes[1,1].set_title('강수량(mm)별 이용건수', fontproperties=prop)
        axes[1,1].set_xlabel('강수량(mm)', fontproperties=prop)
        axes[1,1].set_ylabel('이용건수', fontproperties=prop)

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

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, title='공휴일', title_fontproperties=prop, prop=prop)
        ax.set_xlabel('대여시간', fontproperties=prop)
        ax.set_ylabel('이용건수', fontproperties=prop)

        st.pyplot(fig)
        plt.close(fig)
        st.write('''평일과 공휴일에는 완전히 다른 이용 현황을 보이는 것을 확인할 수 있습니다.
                 평일의 경우 오전 8시, 오후 6시에 이용건수 피크를 보이는데, 출퇴근으로 인한 영향으로 추측해볼 수 있겠습니다.
                 ''')
        st.divider()

        st.subheader(f"{idx.getSubIdx()}요일에 따른 이용건수 차이")
        st.code('''
                sns.pointplot(x='대여시간', y='이용건수',data = data, hue = '요일(num)')

                plt.show()
                ''',line_numbers=True)
        fig, ax = plt.subplots()
        sns.pointplot(x='대여시간', y='이용건수',data = data, hue = '요일(num)', ax=ax)

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, title='요일(num)', title_fontproperties=prop, prop=prop)
        ax.set_xlabel('대여시간', fontproperties=prop)
        ax.set_ylabel('이용건수', fontproperties=prop)


        st.pyplot(fig)
        plt.close(fig)
        st.write("토요일에 이용건수가 더 많고, 토요일 오후에 전반적으로 이용률이 높은 모습을 보입니다.")
        
        st.divider()

        st.subheader(f"{idx.getSubIdx()}요일에 따른 이용건수 차이(box)")
        st.code('''
                sns.boxplot(x='요일(num)', y='이용건수',data = data)
                dofw = list('월화수목금토일')
                plt.xticks([0,1,2,3,4,5,6],dofw, fontproperties=prop)
                
                plt.show()
                ''',line_numbers=True)
        fig, ax = plt.subplots()
        sns.boxplot(x='요일(num)', y='이용건수',data = data, ax=ax)
        dofw = list('월화수목금토일')
        plt.xticks([0,1,2,3,4,5,6],dofw, fontproperties=prop)
        ax.set_xlabel('요일(num)', fontproperties=prop)
        ax.set_ylabel('이용건수', fontproperties=prop)
        
        st.pyplot(fig)
        plt.close(fig)
        st.write("공휴일은 상대적으로 변동성이 적고, 평일은 변동성이 큰 편입니다.")
        
        st.divider()
        
        st.header(f"{idx.getHeadIdx()}결론 도출")
        st.subheader(f"{idx.getSubIdx()}시간대 및 공휴일여부에 따른 특성")
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
