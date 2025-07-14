import streamlit as st

st.title("MBTI별 대표적인 장점 3가지")

mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

mbti_strengths = {
    "INTJ": ["논리적 사고", "장기적인 계획 수립", "독립적인 문제 해결"],
    "INTP": ["창의적 사고", "깊은 분석력", "유연한 접근 방식"],
    "ENTJ": ["강한 리더십", "전략적 사고", "목표 지향적 성향"],
    "ENTP": ["빠른 아이디어 생성", "도전 정신", "다양성 수용"],
    "INFJ": ["깊은 공감력", "직관적 통찰력", "의미 중심적 사고"],
    "INFP": ["이상주의적 가치", "감성적 깊이", "창의력 풍부"],
    "ENFJ": ["탁월한 커뮤니케이션", "조화 추구", "리더십 있는 배려심"],
    "ENFP": ["에너지 넘침", "열정적인 태도", "새로움에 대한 호기심"],
    "ISTJ": ["책임감 강함", "체계적인 일처리", "신뢰감 있는 성격"],
    "ISFJ": ["헌신적 태도", "섬세한 배려", "성실함"],
    "ESTJ": ["실용적인 사고", "조직 관리 능력", "결단력"],
    "ESFJ": ["사교적 태도", "타인 중심적 사고", "공감 능력"],
    "ISTP": ["논리적 문제 해결", "차분한 대응력", "기술적 숙련도"],
    "ISFP": ["감성적 감수성", "유연한 태도", "예술적 감각"],
    "ESTP": ["즉흥적 실행력", "위험 감수", "에너지 넘치는 성격"],
    "ESFP": ["사람들과의 친화력", "즐거움을 찾는 능력", "긍정적 사고"]
}

# 사용자 선택
selected_mbti = st.selectbox("당신의 MBTI를 선택하세요", mbti_types)

# 결과 출력
if selected_mbti:
    strengths = mbti_strengths.get(selected_mbti, [])
    st.subheader(f"🌟 {selected_mbti} 유형의 대표 장점:")
    for i, strength in enumerate(strengths, 1):
        st.write(f"{i}. {strength}")

