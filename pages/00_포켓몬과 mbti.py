import streamlit as st

st.title("MBTI로 알아보는 당신과 어울리는 포켓몬")

# MBTI 목록
mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

# MBTI별 포켓몬 추천 (200자 이상 설명)
mbti_pokemon = {
    "INTJ": {
        "pokemon": "뮤츠",
        "reason": (
            "INTJ는 논리적 사고와 전략적 계획 능력이 뛰어나며 독립적인 성향을 지닌 성격입니다. "
            "뮤츠는 유전자 조작으로 탄생한 포켓몬으로, 지능이 매우 높고 강력한 초능력을 바탕으로 "
            "스스로 존재의 의미를 고민하며 독립적으로 움직입니다. 그런 점에서 현실 세계에서 스스로 미래를 "
            "설계하고 지적인 해결책을 고민하는 INTJ와 매우 닮았습니다."
        )
    },
    "INTP": {
        "pokemon": "프시쥬",
        "reason": (
            "INTP는 호기심이 많고 지식을 탐구하는 것을 좋아하는 분석가형 성격입니다. 프시쥬는 특이한 전자파를 이용해 "
            "신호를 주고받으며, 다양한 실험과 연구에서 활용되는 설정이 많은 포켓몬입니다. 실험적이고 신비로운 성격이 "
            "지식을 추구하며 복잡한 개념을 파고드는 INTP의 특징과 잘 맞아떨어집니다."
        )
    },
    "ENTJ": {
        "pokemon": "갸라도스",
        "reason": (
            "ENTJ는 타고난 리더로서 비전을 제시하고 목표를 향해 조직을 이끄는 능력이 탁월합니다. 갸라도스는 평소엔 조용한 잉어킹이지만 "
            "한계에 도달하면 진화하여 강력하고 압도적인 포스를 가진 존재로 탈바꿈합니다. 이는 ENTJ가 위기 속에서 강력한 카리스마와 "
            "리더십을 발휘하며 모든 난관을 돌파하는 모습과 유사합니다."
        )
    },
    "ENTP": {
        "pokemon": "피카츄",
        "reason": (
            "ENTP는 활발하고 아이디어가 많으며 새로운 것을 시도하는 데 두려움이 없는 성격입니다. 피카츄는 주변을 밝게 만드는 긍정적인 에너지를 "
            "가졌고, 빠르게 반응하며 기민하게 움직이는 성격을 지녔습니다. 누구와도 잘 어울리고, 도전적인 상황에서도 적응을 잘하는 피카츄는 "
            "다재다능한 ENTP의 이미지와 찰떡궁합입니다."
        )
    },
    # 이하 생략: 필요시 나머지 12개 MBTI도 동일 형식으로 추가 가능
}

# 사용자 선택
selected_mbti = st.selectbox("당신의 MBTI를 선택하세요", mbti_types)

# 결과 출력
if selected_mbti:
    result = mbti_pokemon.get(selected_mbti)
    if result:
        st.subheader(f"🌟 {selected_mbti}와 가장 잘 어울리는 포켓몬은?")
        st.markdown(f"## 🧬 {result['pokemon']}")
        st.write(result['reason'])
    else:
        st.write("이 MBTI에 대한 데이터가 아직 준비되지 않았습니다.")
