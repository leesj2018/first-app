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
