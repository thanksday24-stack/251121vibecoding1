import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# 데이터 로드
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("countriesMBTI_16types.csv")
    return df

df = load_data()

# ---------------------------------------------------------
# 사이드바 : MBTI 선택
# ---------------------------------------------------------
st.title("🌍 MBTI 국가별 비율 시각화 웹앱")

mbti_list = df.columns[1:]  # Country 제외한 16개 MBTI 유형
selected_mbti = st.sidebar.selectbox("MBTI 유형을 선택하세요", mbti_list)

st.subheader(f"📌 선택한 MBTI : **{selected_mbti}**")

# ---------------------------------------------------------
# 상위 10개 & 하위 10개 나라 계산
# ---------------------------------------------------------
top10 = df.nlargest(10, selected_mbti)[["Country", selected_mbti]]
bottom10 = df.nsmallest(10, selected_mbti)[["Country", selected_mbti]]

# ---------------------------------------------------------
# 상위 10개 나라 plotly 막대그래프
# ---------------------------------------------------------
st.markdown("## 🔼 가장 **높은** 비율 TOP 10")

fig_top = px.bar(
    top10,
    x=selected_mbti,
    y="Country",
    orientation="h",
    title=f"{selected_mbti} 비율이 높은 TOP 10 국가",
)

st.plotly_chart(fig_top, use_container_width=True)

# ---------------------------------------------------------
# 하위 10개 plotly 막대그래프
# ---------------------------------------------------------
st.markdown("## 🔽 가장 **낮은** 비율 BOTTOM 10")

fig_bottom = px.bar(
    bottom10,
    x=selected_mbti,
    y="Country",
    orientation="h",
    title=f"{selected_mbti} 비율이 낮은 BOTTOM 10 국가",
)

st.plotly_chart(fig_bottom, use_container_width=True)

st.markdown("---")
st.markdown("데이터 출처: 업로드한 CSV 파일")
