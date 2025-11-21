import streamlit as st

# -------------------------------
# MBTI별 고전문학 추천 데이터
# -------------------------------
book_data = {
    "ISTJ": {
        "title": "논어",
        "author": "공자",
        "desc": "원칙과 규율을 중시하는 당신에게 절제와 품격의 지혜를 전함 📘"
    },
    "ISFJ": {
        "title": "어린 왕자",
        "author": "생텍쥐페리",
        "desc": "배려심 깊고 따뜻한 당신에게 마음을 울리는 순수함을 선사함 🌟"
    },
    "INFJ": {
        "title": "죄와 벌",
        "author": "도스토예프스키",
        "desc": "깊은 통찰과 의미를 찾는 당신에게 인간의 내면을 탐구하는 작품 💫"
    },
    "INTJ": {
        "title": "군주론",
        "author": "마키아벨리",
        "desc": "전략가형 당신에게 현실적인 권력과 인간 이해의 방향을 제시함 🧠"
    },
    "ISTP": {
        "title": "손자병법",
        "author": "손자",
        "desc": "분석적이고 실전적인 당신에게 압축된 지혜와 전략을 제공함 ⚔️"
    },
    "ISFP": {
        "title": "데미안",
        "author": "헤르만 헤세",
        "desc": "감성적이고 자기 탐색이 강한 당신에게 성장의 의미를 건네줌 🎨"
    },
    "INFP": {
        "title": "월든",
        "author": "헨리 데이비드 소로",
        "desc": "이상주의자인 당신에게 자연 속 성찰의 여정을 안내함 🌲"
    },
    "INTP": {
        "title": "국부론",
        "author": "애덤 스미스",
        "desc": "지적 호기심이 강한 당신에게 인간 사회의 원리를 분석함 📙"
    },
    "ESTP": {
        "title": "삼국지",
        "author": "나관중",
        "desc": "모험심 강하고 행동파인 당신에게 영웅들의 전략과 승부의 서사 ⚡"
    },
    "ESFP": {
        "title": "오셀로",
        "author": "셰익스피어",
        "desc": "감정 표현이 풍부한 당신에게 인간 감정의 극적 드라마 🎭"
    },
    "ENFP": {
        "title": "동물농장",
        "author": "조지 오웰",
        "desc": "열정적이고 독창적인 당신에게 상징과 풍자의 깊이를 전함 🔥"
    },
    "ENTP": {
        "title": "변신",
        "author": "프란츠 카프카",
        "desc": "새로운 관점을 즐기는 당신에게 기괴함 속 진실을 탐구하는 경험 🌀"
    },
    "ESTJ": {
        "title": "국가",
        "author": "플라톤",
        "desc": "정돈된 체계를 중시하는 당신에게 이상 국가의 모델을 제시함 🏛️"
    },
    "ESFJ": {
        "title": "작은 아씨들",
        "author": "루이자 메이 올콧",
        "desc": "사람을 중시하는 당신에게 가족과 관계의 따뜻함을 전함 💞"
    },
    "ENFJ": {
        "title": "홍루몽",
        "author": "조설근",
        "desc": "타인을 돕는 데 열정적인 당신에게 인간의 군상을 깊게 바라보는 경험 🌺"
    },
    "ENTJ": {
        "title": "짜라투스트라는 이렇게 말했다",
        "author": "니체",
        "desc": "리더형인 당신에게 강렬한 사유와 의지를 불어넣음 🔱"
    }
}

# -------------------------------
# UI 구성
# -------------------------------
st.set_page_config(page_title="MBTI 고전문학 추천", page_icon="📚")

st.title("📚 MBTI 기반 고전문학 추천 웹앱")
st.write("당신의 MBTI를 선택하면, 성향에 잘 맞는 고전문학을 추천드릴게요! 😊")

# MBTI 선택
selected_mbti = st.selectbox("MBTI 유형을 선택하세요:", list(book_data.keys()))

# 추천 결과 출력
if selected_mbti:
    book = book_data[selected_mbti]
    st.subheader(f"📖 추천 도서: **{book['title']}**")
    st.write(f"👤 **저자:** {book['author']}")
    st.write(f"✨ **추천 이유:** {book['desc']}")
