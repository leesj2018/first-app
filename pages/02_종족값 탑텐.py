import streamlit as st
import plotly.express as px
import pandas as pd

st.title("포켓몬 종족값 TOP 10 시각화")

# 예시 데이터 (종족값 합 기준)
pokemon_data = [
    {"name": "뮤츠", "total": 680},
    {"name": "루기아", "total": 680},
    {"name": "칠색조", "total": 680},
    {"name": "레쿠쟈", "total": 680},
    {"name": "디아루가", "total": 680},
    {"name": "펄기아", "total": 680},
    {"name": "기라티나", "total": 680},
    {"name": "제르네아스", "total": 680},
    {"name": "이벨타르", "total": 680},
    {"name": "자시안(검의 왕)", "total": 720}  # 종족값 최고
]

# 데이터프레임으로 변환
df = pd.DataFrame(pokemon_data)

# Plotly 그래프 생성
fig = px.bar(
    df.sort_values(by="total", ascending=False),
    x="name",
    y="total",
    title="종족값이 가장 높은 포켓몬 TOP 10",
    labels={"name": "포켓몬 이름", "total": "종족값 총합"},
    text="total"
)

fig.update_traces(marker_color="royalblue", textposition="outside")
fig.update_layout(yaxis=dict(range=[600, 750]))

# 그래프 출력
st.plotly_chart(fig)
