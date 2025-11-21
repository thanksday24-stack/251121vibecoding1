import streamlit as st
import pandas as pd
import altair as alt

# ------------------------
# 데이터 불러오기
# ------------------------
@st.cache_data
def load_data():
    return pd.read_csv("countriesMBTI_16types.csv")

df = load_data()

# ------------------------
# UI 구성
# ------------------------
st.title("🌍 MBTI 국가별 비율 Top/Bottom 10 시각화")

mbti_list = [col for col in df.columns if col != "Country"]
selected = st.selectbox("MBTI 유형을 선택하세요", mbti_list)

# ------------------------
# Top 10
# ------------------------
st.header(f"🔼 {selected} 비율이 가장 높은 10개 국가")

top10 = df.sort_values(by=selected, ascending=False).head(10)

top_chart = (
    alt.Chart(top10)
    .mark_bar()
    .encode(
        x=alt.X(selected, title=f"{selected} 비율"),
        y=alt.Y("Country:N", sort='-x', title="국가"),
        tooltip=["Country", selected]
    )
    .interactive()
)

st.altair_chart(top_chart, use_container_width=True)

# ------------------------
# Bottom 10
# ------------------------
st.header(f"🔽 {selected} 비율이 가장 낮은 10개 국가")

bottom10 = df.sort_values(by=selected, ascending=True).head(10)

bottom_chart = (
    alt.Chart(bottom10)
    .mark_bar()
    .encode(
        x=alt.X(selected, title=f"{selected} 비율"),
        y=alt.Y("Country:N", sort='x', title="국가"),
        tooltip=["Country", selected]
    )
    .interactive()
)

st.altair_chart(bottom_chart, use_container_width=True)
