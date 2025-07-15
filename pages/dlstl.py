import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Page configuration
st.set_page_config(
    page_title="🌐 Global Cybersecurity Threats Dashboard",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
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

# Generate sample data (replace with actual data loading)
@st.cache_data
def load_sample_data():
    """Generate sample cybersecurity threat data"""
    np.random.seed(42)
    
    # Countries and regions
    countries = ['USA', 'China', 'Russia', 'Germany', 'UK', 'India', 'Brazil', 'Japan', 'France', 'South Korea',
                'Australia', 'Canada', 'Netherlands', 'Israel', 'Iran', 'North Korea', 'Ukraine', 'Turkey']
    
    # Attack types
    attack_types = ['Malware', 'Phishing', 'Ransomware', 'DDoS', 'Data Breach', 'Social Engineering', 
                   'SQL Injection', 'Zero-day Exploit', 'Insider Threat', 'APT']
    
    # Sectors
    sectors = ['Finance', 'Healthcare', 'Government', 'Education', 'Technology', 'Energy', 'Retail', 
              'Manufacturing', 'Transportation', 'Telecommunications']
    
    # Severity levels
    severity_levels = ['Low', 'Medium', 'High', 'Critical']
    
    # Generate data for 2015-2024
    data = []
    for year in range(2015, 2025):
        # More incidents in recent years
        num_incidents = 800 + (year - 2015) * 150 + np.random.randint(-100, 200)
        
        for _ in range(num_incidents):
            # Generate random date within the year
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

# Load data
df = load_sample_data()

# Sidebar
st.sidebar.markdown("### 🔧 Filters")

# Year filter
years = sorted(df['year'].unique())
selected_years = st.sidebar.multiselect(
    "Select Years", 
    years, 
    default=years[-3:],
    help="Choose years to analyze"
)

# Country filter
countries = sorted(df['country'].unique())
selected_countries = st.sidebar.multiselect(
    "Select Countries", 
    countries, 
    default=countries[:5],
    help="Choose countries to analyze"
)

# Attack type filter
attack_types = sorted(df['attack_type'].unique())
selected_attacks = st.sidebar.multiselect(
    "Select Attack Types", 
    attack_types, 
    default=attack_types,
    help="Choose attack types to analyze"
)

# Severity filter
severity_levels = ['Low', 'Medium', 'High', 'Critical']
selected_severity = st.sidebar.multiselect(
    "Select Severity Levels", 
    severity_levels, 
    default=severity_levels,
    help="Choose severity levels to analyze"
)

# Filter data
filtered_df = df[
    (df['year'].isin(selected_years)) &
    (df['country'].isin(selected_countries)) &
    (df['attack_type'].isin(selected_attacks)) &
    (df['severity'].isin(selected_severity))
]

# Main dashboard
st.markdown('<h1 class="main-header">🌐 Global Cybersecurity Threats Dashboard</h1>', unsafe_allow_html=True)

# Key metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_incidents = len(filtered_df)
    st.metric("Total Incidents", f"{total_incidents:,}")

with col2:
    avg_financial_impact = filtered_df['financial_impact'].mean()
    st.metric("Avg Financial Impact", f"${avg_financial_impact:,.0f}")

with col3:
    total_affected_users = filtered_df['affected_users'].sum()
    st.metric("Total Affected Users", f"{total_affected_users:,.0f}")

with col4:
    critical_incidents = len(filtered_df[filtered_df['severity'] == 'Critical'])
    st.metric("Critical Incidents", f"{critical_incidents:,}")

st.markdown("---")

# Charts section
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Threats Over Time")
    
    # Time series chart
    time_series = filtered_df.groupby('year').size().reset_index(name='incidents')
    fig_time = px.line(
        time_series, 
        x='year', 
        y='incidents',
        title='Cybersecurity Incidents by Year',
        markers=True
    )
    fig_time.update_layout(
        xaxis_title="Year",
        yaxis_title="Number of Incidents",
        hovermode='x unified'
    )
    st.plotly_chart(fig_time, use_container_width=True)

with col2:
    st.subheader("🎯 Attack Types Distribution")
    
    # Attack types pie chart
    attack_dist = filtered_df['attack_type'].value_counts().reset_index()
    attack_dist.columns = ['attack_type', 'count']
    
    fig_pie = px.pie(
        attack_dist, 
        values='count', 
        names='attack_type',
        title='Distribution of Attack Types'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Geographic analysis
st.subheader("🌍 Geographic Distribution")

col1, col2 = st.columns(2)

with col1:
    # Top countries by incidents
    country_stats = filtered_df.groupby('country').agg({
        'attack_type': 'count',
        'financial_impact': 'mean',
        'affected_users': 'sum'
    }).round(2)
    country_stats.columns = ['Incidents', 'Avg Financial Impact', 'Total Affected Users']
    country_stats = country_stats.sort_values('Incidents', ascending=False)
    
    fig_country = px.bar(
        country_stats.head(10).reset_index(),
        x='country',
        y='Incidents',
        title='Top 10 Countries by Incidents',
        color='Incidents',
        color_continuous_scale='Reds'
    )
    fig_country.update_layout(xaxis_title="Country", yaxis_title="Number of Incidents")
    st.plotly_chart(fig_country, use_container_width=True)

with col2:
    # Severity distribution by country
    severity_country = filtered_df.groupby(['country', 'severity']).size().reset_index(name='count')
    
    fig_severity = px.bar(
        severity_country,
        x='country',
        y='count',
        color='severity',
        title='Severity Distribution by Country',
        color_discrete_map={
            'Low': '#2ecc71',
            'Medium': '#f39c12',
            'High': '#e74c3c',
            'Critical': '#8e44ad'
        }
    )
    fig_severity.update_layout(xaxis_title="Country", yaxis_title="Number of Incidents")
    st.plotly_chart(fig_severity, use_container_width=True)

# Sector analysis
st.subheader("🏢 Sector Analysis")

col1, col2 = st.columns(2)

with col1:
    # Sector incidents
    sector_stats = filtered_df.groupby('sector').agg({
        'attack_type': 'count',
        'financial_impact': 'mean'
    }).round(2)
    sector_stats.columns = ['Incidents', 'Avg Financial Impact']
    sector_stats = sector_stats.sort_values('Incidents', ascending=True)
    
    fig_sector = px.bar(
        sector_stats.reset_index(),
        x='Incidents',
        y='sector',
        title='Incidents by Sector',
        orientation='h',
        color='Avg Financial Impact',
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_sector, use_container_width=True)

with col2:
    # Monthly trend
    monthly_trend = filtered_df.groupby('month').size().reset_index(name='incidents')
    monthly_trend['month_name'] = monthly_trend['month'].apply(
        lambda x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][x-1]
    )
    
    fig_monthly = px.line(
        monthly_trend,
        x='month_name',
        y='incidents',
        title='Monthly Incident Pattern',
        markers=True
    )
    fig_monthly.update_layout(xaxis_title="Month", yaxis_title="Number of Incidents")
    st.plotly_chart(fig_monthly, use_container_width=True)

# Advanced analysis
st.subheader("🔍 Advanced Analysis")

tab1, tab2, tab3 = st.tabs(["Financial Impact", "Correlation Analysis", "Trend Prediction"])

with tab1:
    # Financial impact analysis
    col1, col2 = st.columns(2)
    
    with col1:
        # Financial impact by attack type
        financial_impact = filtered_df.groupby('attack_type')['financial_impact'].agg(['mean', 'sum']).round(2)
        financial_impact.columns = ['Average Impact', 'Total Impact']
        financial_impact = financial_impact.sort_values('Average Impact', ascending=False)
        
        fig_financial = px.bar(
            financial_impact.reset_index(),
            x='attack_type',
            y='Average Impact',
            title='Average Financial Impact by Attack Type',
            color='Average Impact',
            color_continuous_scale='Reds'
        )
        fig_financial.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig_financial, use_container_width=True)
    
    with col2:
        # Scatter plot: Financial impact vs affected users
        fig_scatter = px.scatter(
            filtered_df.sample(min(1000, len(filtered_df))),
            x='affected_users',
            y='financial_impact',
            color='severity',
            size='affected_users',
            hover_data=['country', 'attack_type'],
            title='Financial Impact vs Affected Users',
            color_discrete_map={
                'Low': '#2ecc71',
                'Medium': '#f39c12',
                'High': '#e74c3c',
                'Critical': '#8e44ad'
            }
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

with tab2:
    # Correlation heatmap
    st.write("### Attack Type and Sector Correlation")
    
    correlation_data = pd.crosstab(filtered_df['attack_type'], filtered_df['sector'])
    
    fig_heatmap = px.imshow(
        correlation_data,
        title='Attack Type vs Sector Heatmap',
        color_continuous_scale='RdYlBu_r',
        aspect='auto'
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)

with tab3:
    # Simple trend prediction
    st.write("### Incident Trend Prediction")
    
    yearly_trend = filtered_df.groupby('year').size().reset_index(name='incidents')
    
    # Simple linear regression for prediction
    from sklearn.linear_model import LinearRegression
    
    X = yearly_trend['year'].values.reshape(-1, 1)
    y = yearly_trend['incidents'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next 2 years
    future_years = np.array([[2025], [2026]])
    predictions = model.predict(future_years)
    
    # Create prediction chart
    extended_years = list(yearly_trend['year']) + [2025, 2026]
    extended_incidents = list(yearly_trend['incidents']) + list(predictions)
    
    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(
        x=yearly_trend['year'],
        y=yearly_trend['incidents'],
        mode='lines+markers',
        name='Historical Data',
        line=dict(color='blue')
    ))
    fig_pred.add_trace(go.Scatter(
        x=[2025, 2026],
        y=predictions,
        mode='lines+markers',
        name='Prediction',
        line=dict(color='red', dash='dash')
    ))
    fig_pred.update_layout(
        title='Cybersecurity Incidents Trend Prediction',
        xaxis_title='Year',
        yaxis_title='Number of Incidents'
    )
    st.plotly_chart(fig_pred, use_container_width=True)
    
    st.info(f"Predicted incidents for 2025: {int(predictions[0]):,}")
    st.info(f"Predicted incidents for 2026: {int(predictions[1]):,}")

# Data table
st.subheader("📊 Detailed Data")

# Display sample data
st.dataframe(
    filtered_df.head(1000),
    use_container_width=True,
    column_config={
        "date": st.column_config.DateColumn("Date"),
        "financial_impact": st.column_config.NumberColumn("Financial Impact", format="$%.0f"),
        "affected_users": st.column_config.NumberColumn("Affected Users", format="%.0f")
    }
)

# Download data
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="📥 Download Filtered Data as CSV",
    data=csv,
    file_name="cybersecurity_threats_filtered.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🔒 Global Cybersecurity Threats Dashboard | Built with Streamlit</p>
    <p>Data visualization for cybersecurity threat analysis and monitoring</p>
</div>
""", unsafe_allow_html=True)
