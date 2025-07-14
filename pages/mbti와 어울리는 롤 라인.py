import streamlit as st

st.title("MBTI로 알아보는 LoL 추천 라인")

mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

mbti_lol_roles = {
    "INTJ": {
        "role": "정글",
        "reason": (
            "INTJ는 전략적 사고와 분석 능력이 뛰어난 성격으로, 맵 전체를 조율하며 계획적으로 게임을 풀어나가는 정글 포지션과 잘 어울립니다. "
            "정글은 시야 확보, 오브젝트 타이밍, 갱킹 동선 등 전체적인 흐름을 통제해야 하므로 INTJ의 장기적 사고와 냉철한 판단이 큰 장점으로 작용합니다."
        )
    },
    "INTP": {
        "role": "미드",
        "reason": (
            "INTP는 호기심 많고 창의적인 문제 해결을 즐깁니다. 미드 라인은 다양한 챔피언 풀이 존재하고 라인전, 로밍, 전투 참여 등 다양한 선택지를 요구합니다. "
            "즉흥적이면서도 논리적인 사고를 즐기는 INTP에게 미드는 창의력과 분석력을 발휘하기 좋은 이상적인 포지션입니다."
        )
    },
    "ENTJ": {
        "role": "탑",
        "reason": (
            "ENTJ는 자기주도적이고 리더십이 뛰어난 성격입니다. 탑 라인은 외딴 섬처럼 고립된 라인이지만, 한타에서 큰 역할을 맡거나 스플릿 푸시를 통해 "
            "게임의 흐름을 바꿀 수 있는 중요한 포지션입니다. ENTJ는 스스로 성장한 뒤 강력한 영향력을 행사하는 탑 포지션과 잘 맞습니다."
        )
    },
    "ENTP": {
        "role": "서포터",
        "reason": (
            "ENTP는 커뮤니케이션 능력이 뛰어나고 창의적인 아이디어를 즐깁니다. 서포터는 시야 장악, 한타 이니시, 아군 보호 등 다양한 역할을 수행하면서도, "
            "순간적인 기지와 판단력이 중요한 자리입니다. ENTP의 재치와 순발력은 팀 전체에 활기를 불어넣습니다."
        )
    },
    "INFJ": {
        "role": "서포터",
        "reason": (
            "INFJ는 타인의 감정에 민감하고 헌신적인 성향을 지닌 조용한 조력자입니다. 팀원들의 생존과 성공을 위해 헌신하는 서포터 역할은 INFJ의 내면적인 "
            "가치와 잘 어울립니다. 시야 관리, 힐·쉴드 제공, 팀원 포지션 케어에 능한 INFJ는 훌륭한 서포터 자질을 갖추고 있습니다."
        )
    },
    # 나머지 MBTI 유형도 동일한 형식으로 추가 가능
}

selected_mbti = st.selectbox("당신의 MBTI를 선택하세요", mbti_types)

if selected_mbti:
    result = mbti_lol_roles.get(selected_mbti)
    if result:
        st.subheader(f"🎮 {selected_mbti}에게 추천하는 라인은:")
        st.markdown(f"## 🛡️ {result['role']}")
        st.write(result["reason"])
    else:
        st.warning("이 MBTI에 대한 추천이 아직 준비되지 않았어요.")
