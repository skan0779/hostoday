# Hostoday

![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-DataFrame-150458?logo=pandas&logoColor=white)
![GeoPandas](https://img.shields.io/badge/GeoPandas-Geospatial-0E4D92)
![Folium](https://img.shields.io/badge/Folium-Map-77B829)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-Model-FF6F00)
![RandomForest](https://img.shields.io/badge/RandomForest-Model-228B22)
![CatBoost](https://img.shields.io/badge/CatBoost-Model-FFCC00)


> 국내 아파트 매물을 Airbnb 호스트로 전환 시 수익을 예측해주는 PoC 서비스 (수익 예측 기반 호스트 유치 솔루션)

<p align="center">
  <img src="./thumbnail.jpg"
       alt="Thumbnail.jpg"
       style="width: 30%; height: auto;">
</p>

---


## 1. 프로젝트 개요
**Hostoday**는 Airbnb 사업자로 전환할때 예상 수익을 계산해주는 PoC 서비스입니다. (월세 아파트를 에어비앤비 호스트로 전환시 얻는 월수익 차액을 예측하여 신규 호스트로의 전환을 유도합니다) 사업자가 등록하고자 하는 매물과 주변 편의시설 정보를, Airbnb 사이트의 실제 숙박가격 및 부대시설 정보를 기반으로 Fine-tuning 한 ML 모델에 넣어, 사업자 전환 시 수익을 예측합니다. 또한 국토교통부 최근 5년간 아파트 실거래 데이터를 기반으로 추천하는 전환 사업자를 선정하여 Pre-sales를 지원합니다. 본 프로젝트는 KT AIVLE School 프로젝트에서 우수상을 수상하였습니다.

**Service Design**

<p align="center">
  <img src="./project_design.png"
       alt="Project Design"
       style="width: 80%; height: auto;">
</p>

**주요 기능:**
- **잠재 고객 추천:** 국토교통부 최근 5년간 등록된 매물 중 가장 수입성이 높은 매물을 추천하여 제공합니다.
- **예상 월 수입액 산정:** 매물의 Airbnb 전화 시 월세 수입을 예측하여 제공합니다.
- **주변 인프라 지도 제공:** 매물 반경 1km 네 관광 및 교통 인프라 지도를 제공합니다.

**처리 흐름:**
- **1차 데이터 수집:** Airbnb 사이트 웹 스크래핑을 통해 데이터를 수집합니다.
- **2차 데이터 수집:** 국토교통부 5년 아파트 실거래 데이터를 수집합니다.
- **ML 모델 학습:** XGBoost, RandomForest, CatBoost 모델을 Fine-tuning을 진행합니다. (파라미터 튜닝 포함)
- **기타 서비스 학습:** 주변 편의시설 시각화를 시킵니다.
- **UI 구성:** Streamlit 기반 웹사이트를 구성합니다.


---


## 2. 기술 스택
> XGBoost, RandomForest, CatBoost 모델을 사용하여 집값을 예측하는 ML 기반 PoC 서비스입니다.

| 구분        | 기술 |
|------------|------|
| Language   | Python 3.12 |
| Web UI     | Streamlit, streamlit-folium |
| Data       | pandas, numpy, GeoPandas |
| Visualization | Plotly Express, Folium, Matplotlib |
| Geo/Spatial   | Shapely, Geopy |
| ML Model | XGBoost, RandomForest, CatBoost |


---


## 3. 실행 방법
> 기본 포트: http://localhost:8501

```sh
# 1. 가상환경 설치
python -m venv venv
source venv/bin/activate

# 2. 필수 라이브러리 설치
pip install streamlit pandas numpy plotly folium streamlit-folium geopandas geopy shapely matplotlib

# 3. 어플리케이션 실행
streamlit run hostoday_streamlit_ui.py
```


---


## 4. 주요 모듈 구성 및 기능

```
hostoday/
├── README.md                       # 서비스 개요
├── hostoday_streamlit_ui.py        # Streamlit UI 소스코드
├── Data/                           # 데이터셋
└── Settings/                       # 설정파일
    ├── .gitignore
    └── requirements.txt
```

