# 라이브러리 불러오기 
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

from shapely.geometry import Point, Polygon, LineString
import matplotlib.pyplot as plt
import matplotlib

# 꽉 찬 화면
st.set_page_config(layout="wide")

# 이미지 가져오기
st.image('https://github.com/8900j/BIG_project/blob/main/Banner.png?raw=true')

# 데이터 가져오기
dt = pd.read_csv('https://raw.githubusercontent.com/8900j/BIG_project/main/test_predict_complete_undummify.csv')
metro = pd.read_csv('https://raw.githubusercontent.com/8900j/BIG_project/main/subway_re.csv')
bus = pd.read_csv('https://raw.githubusercontent.com/8900j/BIG_project/main/JUNG_BUS.csv')

food = pd.read_csv('https://raw.githubusercontent.com/8900j/BIG_project/main/JUNG_FOOD.csv')
munhwa_space = pd.read_csv('https://raw.githubusercontent.com/8900j/BIG_project/main/JUNG_CULTURE_SPACE.csv')
munhwa = pd.read_csv('https://raw.githubusercontent.com/8900j/BIG_project/main/JUNG_CULTURE.csv')
shopping = pd.read_csv('https://raw.githubusercontent.com/8900j/BIG_project/main/JUNG_SHOP.csv')

data = pd.read_csv('https://raw.githubusercontent.com/8900j/BIG_project/main/test_predict_complete_undummify.csv')
data['geometry'] = data.apply(lambda row : Point([row['경도'], row['위도']]), axis=1)
data = gpd.GeoDataFrame(data, geometry='geometry')
data.crs = {'init':'epsg:4326'}
data = data.to_crs({'init':'epsg:5179'})
data['500버퍼'] = data['geometry'].buffer(500)
data['1000버퍼'] = data['geometry'].buffer(1000)

# 데이터 전처리
# 문화공간
munhwa_space['geometry'] = munhwa_space.apply(lambda row : Point([row['경도'], row['위도']]), axis=1)
munhwa_space = gpd.GeoDataFrame(munhwa_space, geometry='geometry')
munhwa_space.crs = {'init':'epsg:4326'}
munhwa_space = munhwa_space.to_crs({'init':'epsg:5179'})
munhwa_space = munhwa_space[['명칭','위도','경도','분류3','geometry']]
munhwa_space.rename(columns = {'분류3' : '분류'}, inplace =True)

# 문화
munhwa['geometry'] = munhwa.apply(lambda row : Point([row['경도'], row['위도']]), axis=1)
munhwa = gpd.GeoDataFrame(munhwa, geometry='geometry')
munhwa.crs = {'init':'epsg:4326'}
munhwa = munhwa.to_crs({'init':'epsg:5179'})
munhwa = munhwa[['명칭','위도','경도','분류3','geometry']]
munhwa.rename(columns = {'분류3' : '분류'}, inplace =True)

# 쇼핑
shopping['geometry'] = shopping.apply(lambda row : Point([row['경도'], row['위도']]), axis=1)
shopping = gpd.GeoDataFrame(shopping, geometry='geometry')
shopping.crs = {'init':'epsg:4326'}
shopping = shopping.to_crs({'init':'epsg:5179'})
shopping = shopping[['명칭','위도','경도','분류3','geometry']]
shopping.rename(columns = {'분류3' : '분류'}, inplace =True)

def mark_at_map(df,i,marker_color, ic): 
    """[‘red’, ‘blue’, ‘green’, ‘purple’, ‘orange’, ‘darkred’,’lightred’, ‘beige’, ‘darkblue’, ‘darkgreen’, 
    ‘cadetblue’, ‘darkpurple’, ‘white’, ‘pink’, ‘lightblue’, ‘lightgreen’, ‘gray’, ‘black’, ‘lightgray’]"""
    if '분류' in df.columns :
        folium.Marker([df['위도'][i], df['경도'][i]] ,
                      tooltip = df.iloc[i]['분류'] + ' : ' + df.iloc[i]['명칭'] ,
                      icon = folium.Icon(color =marker_color, icon=ic, prefix='fa')
                     ).add_to(map)
    else:
        folium.Marker([df['위도'][i],df['경도'][i]] ,
                      tooltip = df.iloc[i]['명칭'],
                      icon = folium.Icon(color =marker_color, icon=ic, prefix='fa')
                     ).add_to(map)
# --------------------------------------------------------------------------------------------------------------------------------------------

tab1, tab2, tab3 = st.tabs(['에어비앤비 직원용','호스트 희망 임대인용', '데이터베이스'])

with tab1:
    # 실제 기능 구현된 프로토타입에 해당되는 탭
    
    st.markdown('#### 고객 리스트')
    show_df=dt[['단지명','주소','예측월세가격', '기존월세가격', '월수입차액']]
    show_df['예측월세가격']=(show_df['예측월세가격']*10000).astype('int')
    show_df['기존월세가격']=(show_df['기존월세가격']*10000).astype('int')
    show_df['월수입차액']=(show_df['월수입차액']*10000).astype('int')
 
    st.dataframe(show_df)

    st.markdown('#### 고객 정보 검색')
    a,b,c = st.columns(3)

    idx = a.text_input(f'index 번호(0~{len(dt)-1})를 입력하세요') # 유저한테 글자 입력받기

    if idx :
        i=int(idx)
        a,b,c,d=st.columns([0.4,0.1,0.8,0.4])
        # 정류장, 지하철 역 표현을 위한 df
        tmp=dt.iloc[[i]]
        
        # 기타 인프라 추가를 위한 df
        tmpo =data.iloc[[i]]
        
        tmpo['geometry'] = tmpo.apply(lambda row : Point([row['경도'], row['위도']]), axis=1)
        tmpo = gpd.GeoDataFrame(tmpo, geometry='geometry')
        tmpo.crs = {'init':'epsg:4326'}
        tmpo = tmpo.to_crs({'init':'epsg:5179'})
        tmpo['500버퍼'] = tmpo['geometry'].buffer(500)
        tmpo['1000버퍼'] = tmpo['geometry'].buffer(1000)
        
        # 선택된 문화공간
        munhwa_space_remain = munhwa_space.loc[munhwa_space.geometry.within(tmpo['1000버퍼'][i]),:]
        munhwa_space_remain.reset_index(drop = True, inplace= True)
        
        # 선택된 문화재
        munhwa_remain = munhwa.loc[munhwa.geometry.within(tmpo['1000버퍼'][i]),:]
        munhwa_remain.reset_index(drop =True, inplace= True)
        
        # 선택된 쇼핑
        shopping_remain = shopping.loc[shopping.geometry.within(tmpo['1000버퍼'][i]),:]
        shopping_remain.reset_index(drop =True, inplace= True)

        
            # *************************************************************************************
        
        with a:
            # 1-2. 가격 정보(차트): 예측월세가격, 기존월세가격, 월수입차액
            m=['기존월세가격','예측월세가격']
            n=[int(tmp['기존월세가격'][i]),int(tmp['예측월세가격'][i])]
            price=pd.DataFrame({'구분':m,'가격':n})
            fig = px.bar(price, x='구분', y='가격',text_auto=True, width=300, height=600) # text_auto=True 값 표시 여부, title='제목' 
            st.plotly_chart(fig)

            # *************************************************************************************
        
        ten1=tmp[['맛집', '문화공간', '문화재', '쇼핑']]
        
        with b:
            txt1=ten1['쇼핑'].values[0]
            img1="https://github.com/8900j/BIG_project/blob/main/logo_shop.png?raw=true"
            st.markdown(f'<h1 style="font-size: 20px;">{txt1}개</h1><img style="width:40px" src={img1}/>', unsafe_allow_html=True)

            txt2=ten1['문화공간'].values[0]
            img2="https://github.com/8900j/BIG_project/blob/main/logo_space.png?raw=true"
            st.markdown(f'<h1 style="font-size: 20px;">{txt2}개</h1><img style="width:45px" src={img2}/>', unsafe_allow_html=True)

            txt3=ten1['문화재'].values[0]
            img3="https://github.com/8900j/BIG_project/blob/main/logo_culture.png?raw=true"
            st.markdown(f'<h1 style="font-size: 20px;">{txt3}개</h1><img style="width:45px" src={img3}/>', unsafe_allow_html=True)

            txt4=ten1['맛집'].values[0]
            img4="https://github.com/8900j/BIG_project/blob/main/logo_food.png?raw=true"
            st.markdown(f'<h1 style="font-size: 20px;">{txt4}개</h1><img style="width:40px" src={img4}/>', unsafe_allow_html=True)
  
            # *************************************************************************************   
        
        with c:
            #지도

            home_lat = tmp['위도'] # 위도
            home_lng = tmp['경도'] # 경도

            for k in range(len(metro)):
                if dt.loc[i, '지하철역'] == metro.loc[k, '역명']:
                    metro_station = metro.loc[k, '역명']
                    # print([metro.loc[i, '역사위치위도'], metro.loc[i, '역사위치경도']])
                    metro_lat = metro.loc[k,'역사위치위도']
                    metro_lng = metro.loc[k,'역사위치경도']
                    break

            for k in range(len(bus)):
                if dt.loc[i, '버스정류장'] == bus.loc[k, '정류장명']:
                    bus_station = bus.loc[k, '정류장명']
                    bus_lat = bus.loc[k,'정류장_위도']
                    bus_lng = bus.loc[k,'정류장_경도']
                    break

            # 배경지도 map (center 위치)
            baegyeong = folium.Figure(width=400, height=400)
            map = folium.Map(location=[home_lat, home_lng],
                             zoom_start=15).add_to(baegyeong)

            # 지도 map에 Marker 추가하기
            folium.Marker([home_lat, home_lng],tooltip = dt.iloc[i]['단지명'],icon=folium.Icon(color='red',icon='home')).add_to(map)

            # 지하철역 marker 추가
            folium.Marker(location=[metro_lat,metro_lng],tooltip=metro_station,zoom_start=15,icon=folium.Icon(color='blue', icon='subway', prefix='fa')).add_to(map)

            # 버스정류장 marker 추가
            folium.Marker(location=[bus_lat, bus_lng],tooltip=bus_station,zoom_start=15,icon=folium.Icon(color='blue',icon='bus', prefix='fa')).add_to(map)
            
#             for k in range(len(munhwa_remain)):
#                 mark_at_map(munhwa_remain,k,'green', 'ticket')

#             for k in range(len(munhwa_space_remain)):
#                 mark_at_map(munhwa_space_remain,k,'orange', 'hashtag')

#             for k in range(len(shopping_remain)):
#                 mark_at_map(shopping_remain,k,'pink', 'shopping-bag')
                
            for k in range(len(munhwa_remain)):
                mark_at_map(munhwa_remain,k,'green', 'ticket')

            for k in range(len(munhwa_space_remain)):
                mark_at_map(munhwa_space_remain,k,'orange', 'hashtag')

            for k in range(len(shopping_remain)):
                mark_at_map(shopping_remain,k,'pink', 'shopping-bag')

            # 1000m 반경 원 추가하기
            folium.Circle(
                location=[home_lat, home_lng],
                radius=1000,
                popup="반경 1000m",
                color="red", # 다른 색깔: #3186cc
                fill=True,
                fill_color="red",
            ).add_to(map)

            # call to render Folium map in Streamlit
            st.st_data = st_folium(baegyeong, width=600, height=550)
            
            # *************************************************************************************
        
        with d:
            ten2=tmp[['지하철역', '지하철역까지(m)', '버스정류장', '버스정류장까지(m)']]
            # 기본 정보: 단지명, 전용면적
            basic=pd.DataFrame({'단지명':tmp['단지명'],'전용면적(㎡)':tmp['전용면적'],'주소':tmp['주소']})
            name=basic['단지명'].values[0]
            size=basic['전용면적(㎡)'].values[0]
            st.markdown('### 단지명: {}'.format(name))
            st.markdown('### 전용면적: {}㎡'.format(size))

            txt = '<p style="font-family:Malgun Gothic; color:cornflowerblue; font-size: 40px;">{}만 원 UP</p>'
            st.markdown(txt.format(int(dt.iloc[i]['월수입차액'])), unsafe_allow_html=True)          

#             if int(dt.iloc[i]['월수입차액'])>=0:
#                 txt = '<p style="font-family:Malgun Gothic; color:cornflowerblue; font-size: 40px;">{}만 원 UP</p>'
#                 st.markdown(txt.format(int(dt.iloc[i]['월수입차액'])), unsafe_allow_html=True)
#             else:
#                 txt = '<p style="font-family:Malgun Gothic; color:red; font-size: 30px;">{}만 원 down</p>'
#                 st.markdown(txt.format(int(dt.iloc[i]['월수입차액']), unsafe_allow_html=True)
                            
            txt5=ten2['버스정류장'].values[0]
            txt6=int(ten2['버스정류장까지(m)'].values[0])
            img5="https://github.com/8900j/BIG_project/blob/main/logo_bus.png?raw=true"
            st.markdown(f'<h1 style="font-size: 20px;">{txt5},{txt6}m</h1><img style="width:50px" src={img5}/>', unsafe_allow_html=True)

            txt7=ten2['지하철역'].values[0]
            txt8=int(ten2['지하철역까지(m)'].values[0])
            img6="https://github.com/8900j/BIG_project/blob/main/logo_metro.png?raw=true"
            st.markdown(f'<h1 style="font-size: 20px;">{txt7},{txt8}m</h1><img style="width:50px" src={img6}/>', unsafe_allow_html=True)
                        
        # 5. 고객 연락수단

        st.markdown('#### 고객 연락수단 (email, sns 등)')
        a,b,c,d = st.columns([0.3,0.3,0.5,1])
        a.markdown(f'##### [📨e-mail](mailto:ktaivle@kt.com)') # 에이블스쿨 이메일
        insta_url='https://www.instagram.com/aivlestory/?igshid=YmMyMTA2M2Y%3D' # 에이블스쿨 인스타그램
        b.markdown(f'##### [⭐instagram]({insta_url})')

    else:
        txt = '<p style="font-family:Malgun Gothic; color:cornflowerblue; font-size: 15px;">▲ index 번호를 입력해주세요</p>'
        st.markdown(txt, unsafe_allow_html=True)
# --------------------------------------------------------------------------------------------------------------------------------------------
with tab2:

    new_title = '<p style="font-family:Malgun Gothic; color:lightcoral; font-size: 30px;">당신의 공간을 에어비앤비하세요!</p>'
    temp_title = '<p style="font-family:Malgun Gothic; color:black; font-size: 30px;">- 향후 서비스 추가를 위한 탭 -</p>'
    
    st.markdown(temp_title, unsafe_allow_html=True)
    st.markdown(new_title, unsafe_allow_html=True)

    st.markdown('#### 정보를 입력해주세요.')
    a,b,c,d = st.columns([1,1,1,1])
    a.markdown('**단지명**')
    name=a.text_input('예시) 마이홈') # 유저한테 글자 입력받기
    b.markdown('**전용면적(㎡)**')
    size=b.text_input('예시) 100') # 유저한테 글자 입력받기
    c.markdown('**층수**')
    floor=c.text_input('예시) 1') # 유저한테 글자 입력받기
    d.markdown('**도로명 주소**')
    address=d.text_input('예시) 중구 명동10길 29') # 유저한테 글자 입력받기
    
    test1=pd.read_csv('https://raw.githubusercontent.com/8900j/BIG_project/main/example_1.csv')
    test2=pd.read_csv('https://raw.githubusercontent.com/8900j/BIG_project/main/example_2.csv')
    test3=pd.read_csv('https://raw.githubusercontent.com/8900j/BIG_project/main/example_3.csv')
    
    if address=='중구 명동10길 29':
        a,b,c,d=st.columns([0.06,0.55,0.3,0.3])
        ten1=test1[['1000m맛집', '1000m문화공간', '1000m문화재', '1000m쇼핑']]
        with a:
            txt1=ten1['1000m쇼핑'].values[0]
            img1="https://github.com/8900j/BIG_project/blob/main/logo_shop.png?raw=true"
            st.markdown(f'<h1 style="font-size: 20px;">{txt1}개</h1><img style="width:40px" src={img1}/>', unsafe_allow_html=True)

            txt2=ten1['1000m문화공간'].values[0]
            img2="https://github.com/8900j/BIG_project/blob/main/logo_space.png?raw=true"
            st.markdown(f'<h1 style="font-size: 20px;">{txt2}개</h1><img style="width:45px" src={img2}/>', unsafe_allow_html=True)

            txt3=ten1['1000m문화재'].values[0]
            img3="https://github.com/8900j/BIG_project/blob/main/logo_culture.png?raw=true"
            st.markdown(f'<h1 style="font-size: 20px;">{txt3}개</h1><img style="width:45px" src={img3}/>', unsafe_allow_html=True)

            txt4=ten1['1000m맛집'].values[0]
            img4="https://github.com/8900j/BIG_project/blob/main/logo_food.png?raw=true"
            st.markdown(f'<h1 style="font-size: 20px;">{txt4}개</h1><img style="width:40px" src={img4}/>', unsafe_allow_html=True)

        with b:
            # 지도
            
            home_lat = test1['위도'] # 위도
            home_lng = test1['경도'] # 경도

            for k in range(len(metro)):
                if test1.loc[0,'가장 가까운 지하철역'] == metro.loc[k, '역명']:
                    metro_station = metro.loc[k, '역명']
                    # print([metro.loc[i, '역사위치위도'], metro.loc[i, '역사위치경도']])
                    metro_lat = metro.loc[k,'역사위치위도']
                    metro_lng = metro.loc[k,'역사위치경도']
                    break

            for k in range(len(bus)):
                if test1.loc[0,'가장 가까운 버스정류장'] == bus.loc[k, '정류장명']:
                    bus_station = bus.loc[k, '정류장명']
                    bus_lat = bus.loc[k,'정류장_위도']
                    bus_lng = bus.loc[k,'정류장_경도']
                    break

            # 배경지도 map (center 위치)
            baegyeong = folium.Figure(width=400, height=400)
            map = folium.Map(location=[home_lat, home_lng],
                             zoom_start=15).add_to(baegyeong)

            # 지도 map에 Marker 추가하기
            folium.Marker([home_lat, home_lng],tooltip = test1.iloc[0]['단지명'],icon=folium.Icon(color='red',icon='home')).add_to(map)

            # 지하철역 marker 추가
            folium.Marker(location=[metro_lat,metro_lng],tooltip=metro_station,zoom_start=15,icon=folium.Icon(color='blue', icon='subway', prefix='fa')).add_to(map)

            # 버스정류장 marker 추가
            folium.Marker(location=[bus_lat, bus_lng],tooltip=bus_station,zoom_start=15,icon=folium.Icon(color='blue',icon='bus', prefix='fa')).add_to(map)

            # 500m 반경 원 추가하기
            folium.Circle(
                location=[home_lat, home_lng],
                radius=1000,
                popup="반경 1000m",
                color="red", # 다른 색깔: #3186cc
                fill=True,
                fill_color="red",
            ).add_to(map)

            # call to render Folium map in Streamlit
            st.st_data = st_folium(baegyeong, width=600, height=550)

            with c:
                # 기본 정보: 단지명, 전용면적
                basic=pd.DataFrame({'단지명':test1['단지명'],'전용면적(㎡)':test1['전용면적'],'주소':test1['도로명주소']})
                name=basic['단지명'].values[0]
                size=basic['전용면적(㎡)'].values[0]
                st.markdown('### 단지명: {}'.format(name))
                st.markdown('### 전용면적: {}㎡'.format(size))         
                
                ten2=test1[['가장 가까운 지하철역까지 거리(m)','가장 가까운 지하철역','가장 가까운 버스정류장까지 거리(m)','가장 가까운 버스정류장']]
                
                txt5=ten2['가장 가까운 버스정류장'].values[0]
                txt6=int(ten2['가장 가까운 버스정류장까지 거리(m)'].values[0])
                img5="https://github.com/8900j/BIG_project/blob/main/logo_bus.png?raw=true"
                st.markdown(f'<h1 style="font-size: 20px;">{txt5},{txt6}m</h1><img style="width:50px" src={img5}/>', unsafe_allow_html=True)

                txt7=ten2['가장 가까운 지하철역'].values[0]
                txt8=int(ten2['가장 가까운 지하철역까지 거리(m)'].values[0])
                img6="https://github.com/8900j/BIG_project/blob/main/logo_metro.png?raw=true"
                st.markdown(f'<h1 style="font-size: 20px;">{txt7},{txt8}m</h1><img style="width:50px" src={img6}/>', unsafe_allow_html=True)
            
    elif address=='중구 삼일대로 302':
        st.dataframe(test2)
    elif address=='중구 소월로 50':
        st.dataframe(test3)
    elif address=='중구 소공로 106':
        st.dataframe(test4)
    
# --------------------------------------------------------------------------------------------------------------------------------------------

with tab3:
    temp_title = '<p style="font-family:Malgun Gothic; color:black; font-size: 30px;">- 향후 서비스 추가를 위한 탭 -</p>'
    st.markdown(temp_title, unsafe_allow_html=True)
    
    full_test=pd.read_csv('https://raw.githubusercontent.com/8900j/BIG_project/main/example_full.csv')
    st.dataframe(full_test[:3])
