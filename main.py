import streamlit as st

st.title("MBTI 기반 직업 추천 웹앱")

# MBTI 유형 리스트
mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# MBTI별 직업 추천 사전
mbti_jobs = {
    "INTJ": ["전략기획가", "데이터 과학자", "시스템 설계자"],
    "INTP": ["이론 물리학자", "프로그래머", "UX 리서처"],
    "ENTJ": ["경영 컨설턴트", "프로젝트 매니저", "CEO"],
    "ENTP": ["창업가", "마케팅 전략가", "혁신 디자이너"],
    "INFJ": ["상담가", "작가", "인권 변호사"],
    "INFP": ["예술가", "심리학자", "문학 작가"],
    "ENFJ": ["교사", "HR 매니저", "공공 관계 전문가"],
    "ENFP": ["브랜드 디자이너", "기획자", "방송 작가"],
    "ISTJ": ["회계사", "공무원", "품질 관리자"],
    "ISFJ": ["간호사", "초등 교사", "사서"],
    "ESTJ": ["군인", "프로젝트 관리자", "행정가"],
    "ESFJ": ["사회복지사", "고객 서비스 관리자", "이벤트 플래너"],
    "ISTP": ["기계공", "파일럿", "응급 구조대원"],
    "ISFP": ["패션 디자이너", "사진작가", "요리사"],
    "ESTP": ["영업사원", "기업가", "응급 구조요원"],
    "ESFP": ["배우", "퍼포먼스 아티스트", "이벤트 코디네이터"]
}

# 사용자 입력
selected_mbti = st.selectbox("당신의 MBTI를 선택하세요", mbti_types)

# 추천 직업 출력
if selected_mbti:
    st.subheader(f"{selected_mbti} 유형을 위한 추천 직업")
    jobs = mbti_jobs.get(selected_mbti, [])
    for i, job in enumerate(jobs, 1):
        st.write(f"{i}. {job}")
