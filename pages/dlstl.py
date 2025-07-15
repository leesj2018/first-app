import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# 페이지 설정
st.set_page_config(
    page_title="🌐 글로벌 사이버보안 위협 대시보드",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 스타일링을 위한 커스텀 CSS
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
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
    }
</style>
""", unsafe_allow_html=True)

# 샘플 데이터 생성 (실제 데이터 로딩으로 대체)
@st.cache_data
def load_sample_data():
    """샘플 사이버보안 위협 데이터 생성"""
    np.random.seed(42)
    
    # 국가 및 지역
    countries = ['미국', '중국', '러시아', '독일', '영국', '인도', '브라질', '일본', '프랑스', '한국',
                '호주', '캐나다', '네덜란드', '이스라엘', '이란', '북한', '우크라이나', '터키']
    
    # 공격 유형
    attack_types = ['악성코드', '피싱', '랜섬웨어', 'DDoS', '데이터 유출', '사회공학', 
                   'SQL 인젝션', '제로데이 익스플로잇', '내부자 위협', 'APT']
    
    # 산업군
    sectors = ['금융', '의료', '정부', '교육', '기술', '에너지', '소매', 
              '제조', '교통', '통신']
    
    # 심각도 수준
    severity_levels = ['낮음', '보통', '높음', '치명적']
    
    # 2015-2024년 데이터 생성
    data = []
    for year in range(2015, 2025):
        # 최근 연도일수록 더 많은 사고
        num_incidents = 800 + (year - 2015) * 150 + np.random.randint(-100, 200)
        
        for _ in range(num_incidents):
            # 연도 내 무작위 날짜 생성
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31)
            random_date = start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days))
            
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

# 데이터 로드
df = load_sample_data()

# 사이드바
st.sidebar.markdown("### 🔧 필터")

# 연도 필터
years = sorted(df['year'].unique())
selected_years = st.sidebar.multiselect(
    "연도 선택", 
    years, 
    default=years[-3:],
    help="분석할 연도를 선택하세요"
)

# 국가 필터
countries = sorted(df['country'].unique())
selected_countries = st.sidebar.multiselect(
    "국가 선택", 
    countries, 
    default=countries[:5],
    help="분석할 국가를 선택하세요"
)

# 공격 유형 필터
attack_types = sorted(df['attack_type'].unique())
selected_attacks = st.sidebar.multiselect(
    "공격 유형 선택", 
    attack_types, 
    default=attack_types,
    help="분석할 공격 유형을 선택하세요"
)

# 심각도 필터
severity_levels = ['낮음', '보통', '높음', '치명적']
selected_severity = st.sidebar.multiselect(
    "심각도 수준 선택", 
    severity_levels, 
    default=severity_levels,
    help="분석할 심각도 수준을 선택하세요"
)

# 데이터 필터링
filtered_df = df[
    (df['year'].isin(selected_years)) &
    (df['country'].isin(selected_countries)) &
    (df['attack_type'].isin(selected_attacks)) &
    (df['severity'].isin(selected_severity))
]

# 메인 대시보드
st.markdown('<h1 class="main-header">🌐 글로벌 사이버보안 위협 대시보드</h1>', unsafe_allow_html=True)

# 주요 지표
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_incidents = len(filtered_df)
    st.metric("총 사고 건수", f"{total_incidents:,}")

with col2:
    avg_financial_impact = filtered_df['financial_impact'].mean()
    st.metric("평균 재정 피해", f"${avg_financial_impact:,.0f}")

with col3:
    total_affected_users = filtered_df['affected_users'].sum()
    st.metric("총 피해자 수", f"{total_affected_users:,.0f}")

with col4:
    critical_incidents = len(filtered_df[filtered_df['severity'] == '치명적'])
    st.metric("치명적 사고", f"{critical_incidents:,}")

st.markdown("---")

# 차트 섹션
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 시간별 위협 추이")
    
    # 시계열 차트
    time_series = filtered_df.groupby('year').size().reset_index(name='incidents')
    fig_time = px.line(
        time_series, 
        x='year', 
        y='incidents',
        title='연도별 사이버보안 사고',
        markers=True
    )
    fig_time.update_layout(
        xaxis_title="연도",
        yaxis_title="사고 건수",
        hovermode='x unified'
    )
    st.plotly_chart(fig_time, use_container_width=True)

with col2:
    st.subheader("🎯 공격 유형 분포")
    
    # 공격 유형 파이 차트
    attack_dist = filtered_df['attack_type'].value_counts().reset_index()
    attack_dist.columns = ['attack_type', 'count']
    
    fig_pie = px.pie(
        attack_dist, 
        values='count', 
        names='attack_type',
        title='공격 유형 분포'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# 지역별 분석
st.subheader("🌍 지역별 분포")

col1, col2 = st.columns(2)

with col1:
    # 사고 건수 기준 상위 국가
    country_stats = filtered_df.groupby('country').agg({
        'attack_type': 'count',
        'financial_impact': 'mean',
        'affected_users': 'sum'
    }).round(2)
    country_stats.columns = ['사고 건수', '평균 재정 피해', '총 피해자 수']
    country_stats = country_stats.sort_values('사고 건수', ascending=False)
    
    fig_country = px.bar(
        country_stats.head(10).reset_index(),
        x='country',
        y='사고 건수',
        title='사고 건수 기준 상위 10개국',
        color='사고 건수',
        color_continuous_scale='Reds'
    )
    fig_country.update_layout(xaxis_title="국가", yaxis_title="사고 건수")
    st.plotly_chart(fig_country, use_container_width=True)

with col2:
    # 국가별 심각도 분포
    severity_country = filtered_df.groupby(['country', 'severity']).size().reset_index(name='count')
    
    fig_severity = px.bar(
        severity_country,
        x='country',
        y='count',
        color='severity',
        title='국가별 심각도 분포',
        color_discrete_map={
            '낮음': '#2ecc71',
            '보통': '#f39c12',
            '높음': '#e74c3c',
            '치명적': '#8e44ad'
        }
    )
    fig_severity.update_layout(xaxis_title="국가", yaxis_title="사고 건수")
    st.plotly_chart(fig_severity, use_container_width=True)

# 산업군 분석
st.subheader("🏢 산업군 분석")

col1, col2 = st.columns(2)

with col1:
    # 산업군별 사고
    sector_stats = filtered_df.groupby('sector').agg({
        'attack_type': 'count',
        'financial_impact': 'mean'
    }).round(2)
    sector_stats.columns = ['사고 건수', '평균 재정 피해']
    sector_stats = sector_stats.sort_values('사고 건수', ascending=True)
    
    fig_sector = px.bar(
        sector_stats.reset_index(),
        x='사고 건수',
        y='sector',
        title='산업군별 사고 건수',
        orientation='h',
        color='평균 재정 피해',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_sector, use_container_width=True)

with col2:
    # 월별 추이
    monthly_trend = filtered_df.groupby('month').size().reset_index(name='incidents')
    monthly_trend['month_name'] = monthly_trend['month'].apply(
        lambda x: ['1월', '2월', '3월', '4월', '5월', '6월',
                  '7월', '8월', '9월', '10월', '11월', '12월'][x-1]
    )
    
    fig_monthly = px.line(
        monthly_trend,
        x='month_name',
        y='incidents',
        title='월별 사고 패턴',
        markers=True
    )
    fig_monthly.update_layout(xaxis_title="월", yaxis_title="사고 건수")
    st.plotly_chart(fig_monthly, use_container_width=True)

# 고급 분석
st.subheader("🔍 고급 분석")

tab1, tab2, tab3 = st.tabs(["재정 피해", "상관관계 분석", "추세 예측"])

with tab1:
    # 재정 피해 분석
    col1, col2 = st.columns(2)
    
    with col1:
        # 공격 유형별 재정 피해
        financial_impact = filtered_df.groupby('attack_type')['financial_impact'].agg(['mean', 'sum']).round(2)
        financial_impact.columns = ['평균 피해', '총 피해']
        financial_impact = financial_impact.sort_values('평균 피해', ascending=False)
        
        fig_financial = px.bar(
            financial_impact.reset_index(),
            x='attack_type',
            y='평균 피해',
            title='공격 유형별 평균 재정 피해',
            color='평균 피해',
            color_continuous_scale='Reds'
        )
        fig_financial.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_financial, use_container_width=True)
    
    with col2:
        # 산점도: 재정 피해 vs 피해자 수
        fig_scatter = px.scatter(
            filtered_df.sample(min(1000, len(filtered_df))),
            x='affected_users',
            y='financial_impact',
            color='severity',
            size='affected_users',
            hover_data=['country', 'attack_type'],
            title='재정 피해 vs 피해자 수',
            color_discrete_map={
                '낮음': '#2ecc71',
                '보통': '#f39c12',
                '높음': '#e74c3c',
                '치명적': '#8e44ad'
            }
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

with tab2:
    # 상관관계 히트맵
    st.write("### 공격 유형과 산업군 상관관계")
    
    correlation_data = pd.crosstab(filtered_df['attack_type'], filtered_df['sector'])
    
    fig_heatmap = px.imshow(
        correlation_data,
        title='공격 유형 vs 산업군 히트맵',
        color_continuous_scale='RdYlBu_r',
        aspect='auto'
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

with tab3:
    # 간단한 추세 예측
    st.write("### 사고 추세 예측")
    
    yearly_trend = filtered_df.groupby('year').size().reset_index(name='incidents')
    
    # sklearn 없이 간단한 선형 회귀
    if len(yearly_trend) > 1:
        X = yearly_trend['year'].values
        y = yearly_trend['incidents'].values
        
        # 기울기와 절편 수동 계산
        n = len(X)
        sum_x = np.sum(X)
        sum_y = np.sum(y)
        sum_xy = np.sum(X * y)
        sum_x2 = np.sum(X * X)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        intercept = (sum_y - slope * sum_x) / n
        
        # 향후 2년 예측
        pred_2025 = slope * 2025 + intercept
        pred_2026 = slope * 2026 + intercept
        predictions = [pred_2025, pred_2026]
        
        # 예측 차트 생성
        fig_pred = go.Figure()
        fig_pred.add_trace(go.Scatter(
            x=yearly_trend['year'],
            y=yearly_trend['incidents'],
            mode='lines+markers',
            name='과거 데이터',
            line=dict(color='blue')
        ))
        fig_pred.add_trace(go.Scatter(
            x=[2025, 2026],
            y=predictions,
            mode='lines+markers',
            name='예측',
            line=dict(color='red', dash='dash')
        ))
        fig_pred.update_layout(
            title='사이버보안 사고 추세 예측',
            xaxis_title='연도',
            yaxis_title='사고 건수'
        )
        st.plotly_chart(fig_pred, use_container_width=True)
        
        st.info(f"2025년 예상 사고 건수: {int(predictions[0]):,}")
        st.info(f"2026년 예상 사고 건수: {int(predictions[1]):,}")
    else:
        st.warning("추세 예측을 위한 데이터가 부족합니다. 더 많은 연도를 선택해주세요.")

# 데이터 테이블
st.subheader("📊 상세 데이터")

# 샘플 데이터 표시
st.dataframe(
    filtered_df.head(1000),
    use_container_width=True,
    column_config={
        "date": st.column_config.DateColumn("날짜"),
        "financial_impact": st.column_config.NumberColumn("재정 피해", format="$%.0f"),
        "affected_users": st.column_config.NumberColumn("피해자 수", format="%.0f")
    }
)

# 데이터 다운로드
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
