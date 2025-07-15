# cyber_dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(
    page_title="🌐 글로벌 사이버보안 위협 대시보드",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 커스텀 CSS 스타일
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #ff6b6b, #4ecdc4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# 샘플 데이터 생성 함수
@st.cache_data
def load_sample_data():
    np.random.seed(42)
    countries = ['미국', '중국', '러시아', '독일', '영국', '인도', '브라질', '일본', '프랑스', '한국',
                '호주', '캐나다', '네덜란드', '이스라엘', '이란', '북한', '우크라이나', '터키']
    attack_types = ['악성코드', '피싱', '랜섬웨어', 'DDoS', '데이터 유출', '사회공학', 
                   'SQL 인젝션', '제로데이 익스플로잇', '내부자 위협', 'APT']
    sectors = ['금융', '의료', '정부', '교육', '기술', '에너지', '소매', 
              '제조', '교통', '통신']
    severity_levels = ['낮음', '보통', '높음', '치명적']
    
    data = []
    for year in range(2015, 2025):
        num_incidents = 800 + (year - 2015) * 150 + np.random.randint(-100, 200)
        for _ in range(num_incidents):
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31)
            random_date = start_date + timedelta(days=np.random.randint(0, 365))
            data.append({
                'date': random_date,
                'year': year,
                'month': random_date.month,
                'country': np.random.choice(countries),
                'attack_type': np.random.choice(attack_types),
                'sector': np.random.choice(sectors),
                'severity': np.random.choice(severity_levels, p=[0.3, 0.4, 0.2, 0.1]),
                'financial_impact': np.random.exponential(50000) * (1 + (year - 2015) * 0.1),
                'affected_users': np.random.exponential(1000) * (1 + (year - 2015) * 0.2)
            })
    return pd.DataFrame(data)

# 데이터 불러오기
df = load_sample_data()

# 사이드바 필터
st.sidebar.markdown("### 🔧 필터")
years = sorted(df['year'].unique())
selected_years = st.sidebar.multiselect("연도 선택", years, default=years[-3:])
countries = sorted(df['country'].unique())
selected_countries = st.sidebar.multiselect("국가 선택", countries, default=countries[:5])
attack_types = sorted(df['attack_type'].unique())
selected_attacks = st.sidebar.multiselect("공격 유형 선택", attack_types, default=attack_types)
severity_levels = ['낮음', '보통', '높음', '치명적']
selected_severity = st.sidebar.multiselect("심각도 수준 선택", severity_levels, default=severity_levels)

# 필터링
filtered_df = df[
    (df['year'].isin(selected_years)) &
    (df['country'].isin(selected_countries)) &
    (df['attack_type'].isin(selected_attacks)) &
    (df['severity'].isin(selected_severity))
]

# 헤더
st.markdown('<h1 class="main-header">🌐 글로벌 사이버보안 위협 대시보드</h1>', unsafe_allow_html=True)

# 주요 지표
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("총 사고 건수", f"{len(filtered_df):,}")
with col2:
    st.metric("평균 재정 피해", f"${filtered_df['financial_impact'].mean():,.0f}")
with col3:
    st.metric("총 피해자 수", f"{filtered_df['affected_users'].sum():,.0f}")
with col4:
    st.metric("치명적 사고", f"{len(filtered_df[filtered_df['severity'] == '치명적']):,}")

st.markdown("---")

# 그래프 1: 연도별 사고
st.subheader("📈 시간별 위협 추이")
time_series = filtered_df.groupby('year').size().reset_index(name='incidents')
fig1 = px.line(time_series, x='year', y='incidents', markers=True, title='연도별 사이버보안 사고')
st.plotly_chart(fig1, use_container_width=True)

# 그래프 2: 공격 유형 분포
st.subheader("🎯 공격 유형 분포")
attack_dist = filtered_df['attack_type'].value_counts().reset_index()
attack_dist.columns = ['attack_type', 'count']
fig2 = px.pie(attack_dist, values='count', names='attack_type', title='공격 유형 분포')
st.plotly_chart(fig2, use_container_width=True)

# 상세 테이블
st.subheader("📊 상세 데이터")
st.dataframe(
    filtered_df.head(1000),
    use_container_width=True,
    column_config={
        "date": st.column_config.DateColumn("날짜"),
        "financial_impact": st.column_config.NumberColumn("재정 피해", format="$%.0f"),
        "affected_users": st.column_config.NumberColumn("피해자 수", format="%.0f")
    }
)

# 다운로드 버튼
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="📥 필터링된 데이터 CSV 다운로드",
    data=csv,
    file_name="cybersecurity_threats_filtered.csv",
    mime="text/csv"
)

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🔒 글로벌 사이버보안 위협 대시보드 | Streamlit으로 구축</p>
    <p>사이버보안 위협 분석 및 모니터링을 위한 데이터 시각화</p>
</div>
""", unsafe_allow_html=True)
