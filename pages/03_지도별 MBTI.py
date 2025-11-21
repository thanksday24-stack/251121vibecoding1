# 2511211700_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import requests
import json
from folium.features import GeoJson
from folium import IFrame
import base64

# ---------------------------
# 설정
# ---------------------------
CSV_PATH = "countriesMBTI_16types.csv"  # 업로드된 CSV 경로 (변경 불필요)
GEOJSON_URL = "https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson"
# ---------------------------

st.set_page_config(layout="wide", page_title="MBTI × 국가 (지도 + 파이차트)")

st.title("🌍 국가별 MBTI 지도 & 13-18세 남/여 MBTI 파이차트")

# ---------------------------
# 데이터 로드
# ---------------------------
@st.cache_data
def load_mbti_df(path):
    df = pd.read_csv(path)
    # 컬럼 공백 제거
    df.columns = [c.strip() for c in df.columns]
    return df

@st.cache_data
def load_geojson(url):
    res = requests.get(url)
    res.raise_for_status()
    return res.json()

df = load_mbti_df(CSV_PATH)
geojson = load_geojson(GEOJSON_URL)

# MBTI 목록 (Country 제외)
mbti_cols = [c for c in df.columns if c.lower() != "country"]

# ---------------------------
# 사이드바 컨트롤
# ---------------------------
with st.sidebar:
    st.header("설정")
    selected_mbti_for_choropleth = st.selectbox("지도로 표시할 MBTI 선택", mbti_cols, index=0)
    st.markdown("---")
    country_choice = st.selectbox("세부 보기 국가 선택", ["(선택 없음)"] + sorted(df["Country"].tolist()))
    st.markdown("**가정**: CSV의 비율은 전체 인구 대비 분포이며, 13~18세의 성별 분포는 동일 비율로 가정함(성비 50:50).")

# ---------------------------
# 지도 만들기 (폴리움)
# ---------------------------
m = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodbpositron")

# 국가별 MBTI 값을 빠르게 조회할 dict 생성
value_map = dict(zip(df["Country"], df[selected_mbti_for_choropleth]))

# 스타일 함수: GeoJSON feature의 이름(다양한 프로퍼티 키 시도)을 찾아 색 지정
def style_function(feature):
    # GeoJSON에 저장된 국가명 키 확인
    props = feature.get("properties", {})
    name = props.get("ADMIN") or props.get("NAME") or props.get("name") or props.get("country")
    val = None
    if name in value_map:
        val = value_map[name]
    # 색상 단계 (간단한 연속색)
    if val is None:
        return {"fillColor": "#ededed", "color": "#999999", "weight": 0.5, "fillOpacity": 0.5}
    # val은 0~1 사이라고 가정
    if val >= 0.12:
        color = "#800026"
    elif val >= 0.09:
        color = "#BD0026"
    elif val >= 0.07:
        color = "#E31A1C"
    elif val >= 0.05:
        color = "#FC4E2A"
    elif val >= 0.03:
        color = "#FD8D3C"
    else:
        color = "#FEB24C"
    return {"fillColor": color, "color": "#444444", "weight": 0.3, "fillOpacity": 0.7}

# 툴팁 텍스트(국가명 + 값 요약)
def tooltip_function(feature):
    props = feature.get("properties", {})
    name = props.get("ADMIN") or props.get("NAME") or props.get("name") or props.get("country")
    val = value_map.get(name, None)
    if val is None:
        return f"{name}: 데이터 없음"
    else:
        return f"{name}: {selected_mbti_for_choropleth} 비율 {val:.3f}"

# GeoJson 추가 (클릭 이벤트는 Streamlit에서 selectbox로 처리)
gj = GeoJson(
    geojson,
    name="countries",
    style_function=style_function,
    tooltip=folium.GeoJsonTooltip(fields=["ADMIN", "NAME", "name"], aliases=["ADMIN","NAME","name"], labels=False, sticky=False),
)
# 각 feature에 tooltip text를 대체로 설정 (fallback)
for feature in gj.data["features"]:
    props = feature.get("properties", {})
    # set a popup/tooltip string into properties for display
    props["__tooltip__"] = tooltip_function(feature)

# GeoJson에 추가
gj.add_to(m)

# 지도 표시
st.subheader("인터랙티브 세계지도 (지도 클릭 → 사이드바에서 국가 선택으로 상세 보기)")
with st.expander("지도 보기 (확대/축소 가능)"):
    st_folium(m, width=1000, height=600)

# ---------------------------
# 국가 선택 시: 파이차트 + 취미추천
# ---------------------------
def make_pies_for_country(country_name):
    row = df[df["Country"] == country_name]
    if row.empty:
        st.warning("해당 국가 데이터 없음.")
        return

    # MBTI 비율(합이 1에 가깝다고 가정)
    mbti_series = row.iloc[0][mbti_cols]
    # 가정: 13-18세 전체 인구를 예시 수치로 잡음 (male_total, female_total)
    # 비율만 중요하므로 임의의 스케일을 사용 (예: 성별 각각 5000명)
    male_total = 5000
    female_total = 5000

    # 동일 분포를 성별로 나눔 (50:50 가정)
    male_counts = mbti_series * male_total
    female_counts = mbti_series * female_total

    # plotly 파이차트 (두 개 옆으로)
    fig_m = px.pie(values=male_counts.values, names=male_counts.index,
                   title=f"{country_name} — 13-18세 남자 MBTI 분포 (가정된 인원: {male_total})")
    fig_f = px.pie(values=female_counts.values, names=female_counts.index,
                   title=f"{country_name} — 13-18세 여자 MBTI 분포 (가정된 인원: {female_total})")

    return fig_m, fig_f, mbti_series.sort_values(ascending=False)

def recommend_hobbies_for_mbti(mbti_code):
    # MBTI별 추천 취미(창의적으로 구성). 각 MBTI마다 3개 취미와 장단점(체언형 종결) 표기
    recs = {
        "INFP": [
            ("창작 글쓰기", "감정표현의 통로 가능함", "내적세계에 몰입함", "현실실현이 느림"),
            ("일러스트/스케치", "창의성 발현 가능함", "집중력 향상 가능함", "완성에 시간 소요됨"),
            ("자연 속 산책", "정서 안정에 도움됨", "아이디어 촉진됨", "외부자극 부족시 지루함")
        ],
        "ENTP": [
            ("토론 동호회", "아이디어 교류 가능함", "논리력 증대 가능함", "집중 유지 어려움"),
            ("스타트업 프로젝트 참여", "실험적 시도 가능함", "네트워크 확장 가능함", "불확실성 높음"),
            ("임기응변형 보드게임", "전략적 사고 촉진됨", "사회적 교류 가능함", "긴 게임은 지루함")
        ],
        "ISFJ": [
            ("정리·수납 DIY", "실용적 성취감 발생함", "생활 개선 가능함", "창의성 제약됨"),
            ("봉사활동", "사회적 유대감 형성됨", "보람감 증대됨", "시간적 제약 존재함"),
            ("가드닝(정원가꾸기)", "심리 안정에 도움됨", "책임감 향상됨", "초기관리 필요함")
        ],
        # 기본 추천 (기타 MBTI)
    }
    # 기본 fallback 추천 (창의적 혼합)
    fallback = [
        ("독서 클럽", "지식 확장 가능함", "비판적 사고 증진됨", "외향적 네트워킹 제한됨"),
        ("요리 실습", "성취감 즉시 발생함", "창의적 표현 가능함", "재료 비용 발생함"),
        ("사진 촬영", "관찰력 향상 가능함", "기억 저장 가능함", "장비 학습 필요함")
    ]
    return recs.get(mbti_code, fallback)

# 상세 표시
if country_choice and country_choice != "(선택 없음)":
    st.markdown(f"## 🇺🇳 {country_choice} — 13~18세 남/여 MBTI 파이차트")
    res = make_pies_for_country(country_choice)
    if res:
        fig_m, fig_f, sorted_series = res
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(fig_m, use_container_width=True)
        with col2:
            st.plotly_chart(fig_f, use_container_width=True)

        st.markdown("---")
        st.markdown("### 🔝 상위 3개 MBTI 및 취미 추천(각 MBTI별 3개) — 장점/단점")
        top3 = list(sorted_series.index[:3])
        for mbti in top3:
            st.markdown(f"**{mbti} — 추천 취미 및 장단점**")
            recs = recommend_hobbies_for_mbti(mbti)
            # recs: list of tuples (취미, 장점, 장점2, 단점) or fallback with single description fields
            for i, item in enumerate(recs, start=1):
                if len(item) >= 4:
                    hobby, advantage1, advantage2, downside = item
                    st.write(f"- **{i}. {hobby}**  — 장점: {advantage1}; {advantage2}. 단점: {downside}.")
                else:
                    # fallback tuple (hobby, shortadv, shortdown)
                    hobby, shortadv, shortdown = item
                    st.write(f"- **{i}. {hobby}**  — 장점: {shortadv}. 단점: {shortdown}.")
else:
    st.info("왼쪽 사이드바에서 국가를 선택하면 해당 국가의 13~18세 남/여 MBTI 파이차트와 상위 MBTI 취미 추천을 표시함.")

st.markdown("---")
st.caption("참고: 본 앱은 CSV의 MBTI 비율을 기반으로 시각화하며, 13~18세 성별 분포는 동일비율로 가정했음. 실제 연령·성별 분포가 있는 데이터로 대체하면 보다 정확한 분석 가능함.")
