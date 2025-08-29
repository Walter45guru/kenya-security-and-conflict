import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from streamlit_folium import folium_static
import numpy as np
from datetime import datetime
import warnings
import geopandas as gpd
warnings.filterwarnings('ignore')

def standardize_county_names(county_name):
    """Standardize county names to match shapefile"""
    county_mapping = {
        'Elgeyo Marakwet': 'Elgeyo-Marakwet',
        'Muranga': "Murang'a",
        'Tharaka-Nithi': 'Tharaka Nithi'
    }
    return county_mapping.get(county_name, county_name)

# Page configuration
st.set_page_config(
    page_title="Kenya Security Dashboard",
    page_icon="🇰🇪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    /* Sidebar styling */
    .css-1d391kg, .css-1lcbmhc, .css-1cypcdb, .css-1wivap2 {
        background-color: #000080 !important;
    }
    
    /* Target all possible sidebar selectors */
    [data-testid="stSidebar"] > div:first-child {
        background-color: #000080 !important;
    }
    
    /* Additional sidebar background targeting */
    .css-1d391kg > div:first-child,
    .css-1lcbmhc > div:first-child {
        background-color: #000080 !important;
    }
    
    /* Force sidebar background */
    section[data-testid="stSidebar"] {
        background-color: #000080 !important;
    }
    
    /* Sidebar content background */
    .css-1d391kg .css-1lcbmhc {
        background-color: #000080 !important;
    }
    
    /* Consistent sidebar width across devices */
    [data-testid="stSidebar"] {
        min-width: 300px !important;
        max-width: 300px !important;
    }
    
    /* Ensure sidebar content fits properly */
    [data-testid="stSidebar"] .css-1d391kg {
        width: 300px !important;
    }
    
    /* Sidebar text styling for better readability */
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: white !important;
    }
    
    /* Sidebar selectbox and slider styling */
    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.9) !important;
    }
    
    [data-testid="stSidebar"] .stSlider > div > div > div {
        background-color: rgba(255, 255, 255, 0.9) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 4px 4px 0px 0px;
        color: #262730;
        padding: 10px 16px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF3B1D;
        color: white;
    }
    .kpi-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        border: 1px solid #e0e0e0;
        margin: 0.5rem;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: bold;
        color: #FF3B1D;
        margin: 8px 0;
    }
    .kpi-label {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 8px;
    }
    .kpi-icon {
        font-size: 1.5rem;
        margin-bottom: 8px;
    }
    .insight-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-left: 4px solid #FF3B1D;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .insight-title {
        font-weight: bold;
        color: #FF3B1D;
        margin-bottom: 0.5rem;
        font-size: 1.1rem;
    }
    .insight-text {
        color: #495057;
        line-height: 1.6;
    }
    
    /* Map container styling to prevent cutoff */
    .map-container {
        margin: 0;
        padding: 0;
        width: 100%;
        overflow: visible;
    }
    
    /* Ensure Plotly maps fit properly */
    .js-plotly-plot {
        width: 100% !important;
        height: 100% !important;
    }
    
    /* Map legend positioning */
    .mapboxgl-ctrl-bottom-right {
        right: 10px !important;
    }
    
    .mapboxgl-ctrl-bottom-left {
        left: 10px !important;
    }
    
    /* Responsive map sizing */
    .stPlotlyChart {
        width: 100% !important;
        max-width: none !important;
    }
    
    /* Ensure maps don't overflow */
    .element-container {
        max-width: 100% !important;
        overflow: visible !important;
    }
    
    /* Map container full width */
    .map-container > div {
        width: 100% !important;
        max-width: 100% !important;
    }
</style>
""", unsafe_allow_html=True)

def standardize_county_names(county_name):
    """Standardize county names to match shapefile"""
    county_mapping = {
        'Elgeyo Marakwet': 'Elgeyo-Marakwet',
        'Muranga': "Murang'a",
        'Tharaka-Nithi': 'Tharaka Nithi'
    }
    return county_mapping.get(county_name, county_name)

@st.cache_data
def load_county_shapefile():
    """Load Kenya counties shapefile"""
    try:
        gdf = gpd.read_file('../Downloads/Counties_data/Counties_data/Kenya_Counties.shp')
        return gdf
    except Exception as e:
        st.error(f"Error loading shapefile: {e}")
        return None

@st.cache_data
def load_data():
    """Load and preprocess the Kenya data"""
    try:
        df = pd.read_csv('kenya_data.csv')
        
        # Convert WEEK to datetime
        df['WEEK'] = pd.to_datetime(df['WEEK'])
        
        # Extract year for easier analysis
        df['YEAR'] = df['WEEK'].dt.year
        
        # Fill missing values
        df['FATALITIES'] = df['FATALITIES'].fillna(0)
        df['POPULATION_EXPOSURE'] = df['POPULATION_EXPOSURE'].fillna(0)
        df['EVENTS'] = df['EVENTS'].fillna(1)
        
        # Standardize county names to match shapefile
        df['ADMIN1_STANDARDIZED'] = df['ADMIN1'].apply(standardize_county_names)
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

@st.cache_data
def load_county_shapefile():
    """Load Kenya counties shapefile"""
    try:
        gdf = gpd.read_file('../Downloads/Counties_data/Counties_data/Kenya_Counties.shp')
        return gdf
    except Exception as e:
        st.error(f"Error loading shapefile: {e}")
        return None

def display_insight(title, text):
    """Helper function to display insights in a styled box"""
    st.markdown(f"""
    <div class="insight-box">
        <div class="insight-title">{title}</div>
        <div class="insight-text">{text}</div>
    </div>
    """, unsafe_allow_html=True)

def overview_tab(filtered_df):
    """Overview tab with KPIs and summary metrics"""
    st.header("📊 Overview")
    
    # Calculate additional metrics
    total_weeks = filtered_df['WEEK'].nunique()
    avg_events_per_week = filtered_df['EVENTS'].sum() / total_weeks if total_weeks > 0 else 0
    avg_fatalities_per_week = filtered_df['FATALITIES'].sum() / total_weeks if total_weeks > 0 else 0
    
    # KPI Cards in single horizontal line
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">📅</div>
            <div class="kpi-label">Total Events</div>
            <div class="kpi-value">{:,}</div>
        </div>
        """.format(filtered_df['EVENTS'].sum()), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">📈</div>
            <div class="kpi-label">Avg Events/Week</div>
            <div class="kpi-value">{:.1f}</div>
        </div>
        """.format(avg_events_per_week), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">⚠️</div>
            <div class="kpi-label">Total Fatalities</div>
            <div class="kpi-value">{:,}</div>
        </div>
        """.format(filtered_df['FATALITIES'].sum()), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-icon">👥</div>
            <div class="kpi-label">Avg Fatalities/Week</div>
            <div class="kpi-value">{:.1f}</div>
        </div>
        """.format(avg_fatalities_per_week), unsafe_allow_html=True)
    
    # Overview insights
    total_events = filtered_df['EVENTS'].sum()
    total_fatalities = filtered_df['FATALITIES'].sum()
    fatality_rate = (total_fatalities / total_events * 100) if total_events > 0 else 0
    
    display_insight(
        "📊 Dashboard Overview Insights",
        f"The dashboard shows {total_events:,} total security events with {total_fatalities:,} fatalities across {filtered_df['ADMIN1'].nunique()} counties. "
        f"On average, {avg_events_per_week:.1f} events occur per week with {avg_fatalities_per_week:.1f} fatalities. "
        f"The fatality rate is {fatality_rate:.1f}% of total events. "
        f"Data covers {total_weeks} weeks, providing comprehensive coverage of security patterns in Kenya."
    )
    
    # Special Election Violence Insight
    display_insight(
        "🗳️ Critical Election Security Analysis",
        f"<strong>Historical Context:</strong> Kenya's security landscape has been significantly shaped by electoral cycles. "
        f"The 2008 post-election violence was a watershed moment, resulting in over 1,000 fatalities and 600,000 displaced persons. "
        f"<strong>Recurring Pattern:</strong> Subsequent general elections (2013, 2017, 2022) have continued to experience "
        f"elevated security incidents, though with varying intensity. <strong>Key Risk Periods:</strong> Security challenges "
        f"typically peak in the months leading up to elections and immediately following results announcement. "
        f"<strong>Policy Implications:</strong> This pattern underscores the critical need for robust electoral security frameworks, "
        f"early warning systems, and conflict prevention mechanisms to safeguard democratic processes and national stability."
    )
    
    # Event Type Distribution Pie Chart
    st.subheader("📊 Event Type Distribution")
    event_type_summary = filtered_df.groupby('EVENT_TYPE')['EVENTS'].sum().reset_index()
    
    # Create pie chart
    fig_pie = px.pie(
        event_type_summary, 
        values='EVENTS', 
        names='EVENT_TYPE',
        title='Breakdown of events by type',
        color_discrete_sequence=['#2E8B57', '#DC143C', '#FF8C00', '#9370DB', '#808080']
    )
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Additional summary metrics
    st.subheader("📋 Summary Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Population Exposure", f"{filtered_df['POPULATION_EXPOSURE'].sum():,}")
    
    with col2:
        st.metric("Unique Counties", filtered_df['ADMIN1'].nunique())
    
    with col3:
        st.metric("Data Coverage", f"{total_weeks} weeks")

def time_analysis_tab(filtered_df):
    """Time analysis tab with temporal charts"""
    st.header("⏰ Time Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Events over time
        events_by_year = filtered_df.groupby('YEAR')['EVENTS'].sum().reset_index()
        fig_events = px.line(events_by_year, x='YEAR', y='EVENTS', 
                           title='Events Over Time',
                           markers=True)
        fig_events.update_layout(height=400)
        st.plotly_chart(fig_events, use_container_width=True)
        
        # Events over time insights
        max_events_year = events_by_year.loc[events_by_year['EVENTS'].idxmax()]
        min_events_year = events_by_year.loc[events_by_year['EVENTS'].idxmin()]
        events_trend = "increasing" if events_by_year['EVENTS'].iloc[-1] > events_by_year['EVENTS'].iloc[0] else "decreasing"
        
        display_insight(
            "📈 Events Over Time Analysis",
            f"Security events show a {events_trend} trend over time. The peak year was {int(max_events_year['YEAR'])} with {int(max_events_year['EVENTS']):,} events, "
            f"while {int(min_events_year['YEAR'])} had the lowest activity with {int(min_events_year['EVENTS']):,} events. "
            f"<strong>Critical Insight:</strong> Kenya has experienced significant security challenges around general elections, "
            f"particularly the devastating 2008 post-election violence that resulted in widespread fatalities and displacement. "
            f"This pattern of election-related security incidents continues to pose challenges for national stability and requires "
            f"proactive measures to prevent violence during electoral periods."
        )
    
    with col2:
        # Fatalities over time
        fatalities_by_year = filtered_df.groupby('YEAR')['FATALITIES'].sum().reset_index()
        fig_fatalities = px.line(fatalities_by_year, x='YEAR', y='FATALITIES',
                               title='Fatalities Over Time',
                               markers=True)
        fig_fatalities.update_layout(height=400)
        st.plotly_chart(fig_fatalities, use_container_width=True)
        
        # Fatalities over time insights
        max_fatalities_year = fatalities_by_year.loc[fatalities_by_year['FATALITIES'].idxmax()]
        min_fatalities_year = fatalities_by_year.loc[fatalities_by_year['FATALITIES'].idxmin()]
        fatalities_trend = "increasing" if fatalities_by_year['FATALITIES'].iloc[-1] > fatalities_by_year['FATALITIES'].iloc[0] else "decreasing"
        
        display_insight(
            "⚠️ Fatalities Over Time Analysis",
            f"Fatalities display a {fatalities_trend} trend, with {int(max_fatalities_year['YEAR'])} being the deadliest year ({int(max_fatalities_year['FATALITIES']):,} fatalities). "
            f"The safest year was {int(min_fatalities_year['YEAR'])} with {int(min_fatalities_year['FATALITIES']):,} fatalities. "
            f"<strong>Election Violence Pattern:</strong> Kenya's electoral cycles have been marked by recurring security challenges. "
            f"The 2008 post-election violence was particularly devastating, with over 1,000 fatalities and 600,000 displaced persons. "
            f"Subsequent elections (2013, 2017, 2022) have also seen increased security incidents, highlighting the need for "
            f"comprehensive electoral security frameworks and conflict prevention mechanisms."
        )
    
    # Monthly trends
    st.subheader("📅 Monthly Trends")
    filtered_df['MONTH'] = filtered_df['WEEK'].dt.month
    monthly_events = filtered_df.groupby('MONTH')['EVENTS'].sum().reset_index()
    monthly_fatalities = filtered_df.groupby('MONTH')['FATALITIES'].sum().reset_index()
    
    fig_monthly = make_subplots(rows=1, cols=2, subplot_titles=('Events by Month', 'Fatalities by Month'))
    
    fig_monthly.add_trace(
        go.Bar(x=monthly_events['MONTH'], y=monthly_events['EVENTS'], name='Events'),
        row=1, col=1
    )
    
    fig_monthly.add_trace(
        go.Bar(x=monthly_fatalities['MONTH'], y=monthly_fatalities['FATALITIES'], name='Fatalities'),
        row=1, col=2
    )
    
    fig_monthly.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_monthly, use_container_width=True)
    
    # Monthly trends insights
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    peak_month_events = month_names[monthly_events['MONTH'].iloc[monthly_events['EVENTS'].idxmax()] - 1]
    peak_month_fatalities = month_names[monthly_fatalities['MONTH'].iloc[monthly_fatalities['FATALITIES'].idxmax()] - 1]
    
    display_insight(
        "📅 Monthly Pattern Analysis",
        f"Monthly analysis reveals seasonal patterns in security events. {peak_month_events} experiences the highest number of events, "
        f"while {peak_month_fatalities} sees the most fatalities. <strong>Election Cycle Correlation:</strong> These patterns "
        f"strongly correlate with Kenya's electoral cycles, with increased security incidents typically occurring in the months "
        f"leading up to and following general elections. The 2008 post-election violence peaked in January-February, while "
        f"2017 and 2022 elections also saw heightened security challenges. Understanding these electoral security patterns "
        f"enables better resource allocation and preventive measures during high-risk electoral periods."
    )

def geographic_tab(filtered_df, county_gdf):
    """Geographic analysis tab with maps and location-based charts"""
    st.header("🗺️ Geographic Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Top counties by events
        top_counties = filtered_df.groupby('ADMIN1')['EVENTS'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_top_counties = px.bar(top_counties, x='ADMIN1', y='EVENTS',
                                title='Top 10 Counties by Events')
        fig_top_counties.update_layout(height=400)
        fig_top_counties.update_xaxes(tickangle=45)
        st.plotly_chart(fig_top_counties, use_container_width=True)
        
        # Top counties insights
        top_county = top_counties.iloc[0]
        top_3_counties = ", ".join(top_counties['ADMIN1'].head(3).tolist())
        events_concentration = (top_counties['EVENTS'].head(3).sum() / top_counties['EVENTS'].sum() * 100)
        
        display_insight(
            "🏛️ Geographic Concentration of Events",
            f"{top_county['ADMIN1']} leads with {int(top_county['EVENTS']):,} events, followed by {top_3_counties}. "
            f"The top 3 counties account for {events_concentration:.1f}% of all events, indicating significant geographic concentration. "
            f"<strong>Election Violence Hotspots:</strong> Several of these high-incident counties have been particularly "
            f"affected during electoral periods, including the 2008 post-election violence and subsequent election cycles. "
            f"<strong>Risk Factors:</strong> These areas often experience heightened tensions due to political polarization, "
            f"ethnic dynamics, and historical grievances that become amplified during elections. "
            f"This geographic concentration suggests the need for targeted security interventions in these high-risk areas "
            f"and analysis of underlying factors contributing to their vulnerability."
        )
    
    with col2:
        # Top counties by fatalities
        top_fatalities = filtered_df.groupby('ADMIN1')['FATALITIES'].sum().sort_values(ascending=False).head(10).reset_index()
        fig_top_fatalities = px.bar(top_fatalities, x='ADMIN1', y='FATALITIES',
                                  title='Top 10 Counties by Fatalities')
        fig_top_fatalities.update_layout(height=400)
        fig_top_fatalities.update_xaxes(tickangle=45)
        st.plotly_chart(fig_top_fatalities, use_container_width=True)
        
        # Top fatalities insights
        top_fatality_county = top_fatalities.iloc[0]
        top_3_fatality_counties = ", ".join(top_fatalities['ADMIN1'].head(3).tolist())
        fatalities_concentration = (top_fatalities['FATALITIES'].head(3).sum() / top_fatalities['FATALITIES'].sum() * 100)
        
        display_insight(
            "💀 Geographic Distribution of Fatalities",
            f"{top_fatality_county['ADMIN1']} experiences the highest fatalities ({int(top_fatality_county['FATALITIES']):,}), "
            f"followed by {top_3_fatality_counties}. The top 3 counties account for {fatalities_concentration:.1f}% of all fatalities. "
            f"This concentration highlights critical areas requiring immediate attention and suggests potential correlations "
            f"with factors like population density, economic conditions, or historical conflict patterns."
        )
    
    # County Choropleth Map
    st.subheader("🗺️ County-Level Security Events Map")
    
    if county_gdf is not None:
        # Create a container for better map display
        map_container = st.container()
        # Prepare data for choropleth
        county_events = filtered_df.groupby('ADMIN1_STANDARDIZED')['EVENTS'].sum().reset_index()
        county_fatalities = filtered_df.groupby('ADMIN1_STANDARDIZED')['FATALITIES'].sum().reset_index()
        
        # Merge with shapefile
        county_gdf_events = county_gdf.merge(county_events, left_on='COUNTY', right_on='ADMIN1_STANDARDIZED', how='left')
        county_gdf_fatalities = county_gdf.merge(county_fatalities, left_on='COUNTY', right_on='ADMIN1_STANDARDIZED', how='left')
        
        # Fill NaN values with 0
        county_gdf_events['EVENTS'] = county_gdf_events['EVENTS'].fillna(0)
        county_gdf_fatalities['FATALITIES'] = county_gdf_fatalities['FATALITIES'].fillna(0)
        
        # Create choropleth map for events
        fig_choropleth_events = px.choropleth_mapbox(
            county_gdf_events,
            geojson=county_gdf_events.geometry.__geo_interface__,
            locations=county_gdf_events.index,
            color='EVENTS',
            hover_name='COUNTY',
            hover_data=['EVENTS', 'TotalCount'],
            color_continuous_scale='Reds',
            mapbox_style='carto-positron',
            zoom=5,
            center={'lat': 0.0236, 'lon': 37.9062},
            title='Security Events by County'
        )
        fig_choropleth_events.update_layout(
            height=500,
            margin=dict(l=0, r=0, t=50, b=0),
            mapbox=dict(
                center=dict(lat=0.0236, lon=37.9062),
                zoom=5.5,
                style='carto-positron'
            )
        )
        
        with map_container:
            st.plotly_chart(fig_choropleth_events, use_container_width=True, config={'displayModeBar': True})
        
        # Create choropleth map for fatalities
        fig_choropleth_fatalities = px.choropleth_mapbox(
            county_gdf_fatalities,
            geojson=county_gdf_fatalities.geometry.__geo_interface__,
            locations=county_gdf_fatalities.index,
            color='FATALITIES',
            hover_name='COUNTY',
            hover_data=['FATALITIES', 'TotalCount'],
            color_continuous_scale='Reds',
            mapbox_style='carto-positron',
            zoom=5,
            center={'lat': 0.0236, 'lon': 37.9062},
            title='Fatalities by County'
        )
        fig_choropleth_fatalities.update_layout(
            height=500,
            margin=dict(l=0, r=0, t=50, b=0),
            mapbox=dict(
                center=dict(lat=0.0236, lon=37.9062),
                zoom=5.5,
                style='carto-positron'
            )
        )
        
        with map_container:
            st.plotly_chart(fig_choropleth_fatalities, use_container_width=True, config={'displayModeBar': True})
        
        # Map insights
        total_mapped_counties = len(county_gdf_events[county_gdf_events['EVENTS'] > 0])
        high_events_counties = len(county_gdf_events[county_gdf_events['EVENTS'] >= county_gdf_events['EVENTS'].quantile(0.75)])
        
        display_insight(
            "🗺️ County-Level Geographic Analysis",
            f"The choropleth maps show security events and fatalities across {total_mapped_counties} counties with recorded incidents. "
            f"{high_events_counties} counties fall in the high-incident category (75th percentile). "
            f"Counties with darker colors indicate higher security challenges, enabling targeted resource allocation "
            f"and intervention strategies based on geographic risk patterns."
        )
    else:
        st.warning("County shapefile not available. Please ensure the shapefile is in the correct location.")
        
        # Fallback to original map
        st.subheader("📍 Interactive Map (Fallback)")
        
        # Create map centered on Kenya
        m = folium.Map(location=[0.0236, 37.9062], zoom_start=6, tiles='OpenStreetMap')
        
        # Add markers for events with fatalities
        events_with_fatalities = filtered_df[filtered_df['FATALITIES'] > 0]
        
        for idx, row in events_with_fatalities.iterrows():
            if pd.notna(row['CENTROID_LATITUDE']) and pd.notna(row['CENTROID_LONGITUDE']):
                popup_text = f"""
                <b>County:</b> {row['ADMIN1']}<br>
                <b>Event:</b> {row['EVENT_TYPE']}<br>
                <b>Sub-Event:</b> {row['SUB_EVENT_TYPE']}<br>
                <b>Fatalities:</b> {row['FATALITIES']}<br>
                <b>Date:</b> {row['WEEK'].strftime('%Y-%m-%d')}<br>
                <b>Population Exposure:</b> {row['POPULATION_EXPOSURE']:,.0f}
                """
                
                # Color code by fatalities
                if row['FATALITIES'] >= 10:
                    color = 'red'
                elif row['FATALITIES'] >= 5:
                    color = 'orange'
                else:
                    color = 'yellow'
                
                folium.CircleMarker(
                    location=[row['CENTROID_LATITUDE'], row['CENTROID_LONGITUDE']],
                    radius=row['FATALITIES'] * 2 + 5,
                    popup=folium.Popup(popup_text, max_width=300),
                    color=color,
                    fill=True,
                    fillOpacity=0.7
                ).add_to(m)
        
        # Display the map
        folium_static(m, width=800, height=500)

def event_types_tab(filtered_df):
    """Event types analysis tab with event distribution charts"""
    st.header("🎯 Event Type Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Event type distribution
        event_type_counts = filtered_df.groupby('EVENT_TYPE')['EVENTS'].sum().reset_index()
        fig_event_types = px.pie(event_type_counts, values='EVENTS', names='EVENT_TYPE',
                               title='Distribution of Event Types')
        fig_event_types.update_layout(height=400)
        st.plotly_chart(fig_event_types, use_container_width=True)
        
        # Event type distribution insights
        dominant_event_type = event_type_counts.iloc[event_type_counts['EVENTS'].idxmax()]
        dominant_percentage = (dominant_event_type['EVENTS'] / event_type_counts['EVENTS'].sum() * 100)
        
        display_insight(
            "🎯 Event Type Distribution Analysis",
            f"{dominant_event_type['EVENT_TYPE']} is the most common event type, accounting for {dominant_percentage:.1f}% of all events. "
            f"This dominance suggests specific security challenges that require targeted intervention strategies. "
            f"Understanding the nature of these events helps develop appropriate response mechanisms and preventive measures "
            f"tailored to the specific threat profile."
        )
    
    with col2:
        # Fatalities by event type
        fatalities_by_type = filtered_df.groupby('EVENT_TYPE')['FATALITIES'].sum().reset_index()
        fig_fatalities_type = px.bar(fatalities_by_type, x='EVENT_TYPE', y='FATALITIES',
                                   title='Fatalities by Event Type')
        fig_fatalities_type.update_layout(height=400)
        st.plotly_chart(fig_fatalities_type, use_container_width=True)
        
        # Fatalities by event type insights
        deadliest_event_type = fatalities_by_type.iloc[fatalities_by_type['FATALITIES'].idxmax()]
        deadliest_percentage = (deadliest_event_type['FATALITIES'] / fatalities_by_type['FATALITIES'].sum() * 100)
        
        display_insight(
            "💀 Fatalities by Event Type Analysis",
            f"{deadliest_event_type['EVENT_TYPE']} causes the highest number of fatalities ({int(deadliest_event_type['FATALITIES']):,}), "
            f"representing {deadliest_percentage:.1f}% of all fatalities. This indicates that while some event types "
            f"may be more frequent, others have higher lethality rates. This insight is crucial for prioritizing "
            f"security resources and developing appropriate response protocols for different types of incidents."
        )
    
    # Sub-event type analysis
    st.subheader("🔍 Sub-Event Type Analysis")
    sub_event_counts = filtered_df.groupby('SUB_EVENT_TYPE')['EVENTS'].sum().sort_values(ascending=False).head(15).reset_index()
    
    fig_sub_events = px.bar(sub_event_counts, x='SUB_EVENT_TYPE', y='EVENTS',
                           title='Top 15 Sub-Event Types')
    fig_sub_events.update_layout(height=400)
    fig_sub_events.update_xaxes(tickangle=45)
    st.plotly_chart(fig_sub_events, use_container_width=True)
    
    # Sub-event insights
    top_sub_event = sub_event_counts.iloc[0]
    top_3_sub_events = ", ".join(sub_event_counts['SUB_EVENT_TYPE'].head(3).tolist())
    
    display_insight(
        "🔍 Sub-Event Type Deep Dive",
        f"{top_sub_event['SUB_EVENT_TYPE']} is the most frequent sub-event type with {int(top_sub_event['EVENTS']):,} occurrences, "
        f"followed by {top_3_sub_events}. This granular analysis reveals specific incident patterns that may not be "
        f"apparent at the broader event type level. Understanding these sub-categories enables more precise "
        f"security planning and resource allocation for specific threat scenarios."
    )
    
    # Detailed data table
    st.subheader("📋 Detailed Event Data")
    search_term = st.text_input("Search in data (County, Event Type, etc.)")
    
    if search_term:
        search_df = filtered_df[
            filtered_df['ADMIN1'].str.contains(search_term, case=False, na=False) |
            filtered_df['EVENT_TYPE'].str.contains(search_term, case=False, na=False) |
            filtered_df['SUB_EVENT_TYPE'].str.contains(search_term, case=False, na=False)
        ]
    else:
        search_df = filtered_df
    
    # Display filtered data
    st.dataframe(
        search_df[['WEEK', 'ADMIN1', 'EVENT_TYPE', 'SUB_EVENT_TYPE', 'EVENTS', 'FATALITIES', 'POPULATION_EXPOSURE']]
        .sort_values('WEEK', ascending=False),
        use_container_width=True
    )
    
    # Download button
    csv = search_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name=f"kenya_security_data.csv",
        mime="text/csv"
    )
    
    # Data table insights
    display_insight(
        "📊 Data Exploration Insights",
        f"The detailed data table contains {len(search_df):,} records with comprehensive information about each security event. "
        f"Use the search functionality to explore specific patterns by county, event type, or sub-event type. "
        f"This granular data enables detailed analysis for policy development, resource planning, and "
        f"understanding the complex dynamics of security challenges across different regions and time periods."
    )

def main():
    # Sidebar with logo and filters
    with st.sidebar:
        # Logo at the top
        st.image("group 1 logo.png", width=200)
        st.markdown("---")
        
        st.header("📊 Dashboard Filters")
        
        # Load data
        df = load_data()
        
        if df is None:
            st.error("Failed to load data. Please check if 'kenya_data.csv' exists.")
            return
        
        # Load county shapefile
        county_gdf = load_county_shapefile()
        
        # Year range filter
        year_range = st.sidebar.slider(
            "Select Year Range",
            min_value=int(df['YEAR'].min()),
            max_value=int(df['YEAR'].max()),
            value=(int(df['YEAR'].min()), int(df['YEAR'].max())),
            step=1
        )
        
        # Region filter
        regions = ['All'] + sorted(df['REGION'].unique().tolist())
        selected_region = st.sidebar.selectbox("Select Region", regions)
        
        # Event type filter
        event_types = ['All'] + sorted(df['EVENT_TYPE'].unique().tolist())
        selected_event_type = st.sidebar.selectbox("Select Event Type", event_types)
        
        # Admin1 (County) filter
        admin1_options = ['All'] + sorted(df['ADMIN1'].unique().tolist())
        selected_admin1 = st.sidebar.selectbox("Select County", admin1_options)
        
        # Apply filters
        filtered_df = df.copy()
        filtered_df = filtered_df[(filtered_df['YEAR'] >= year_range[0]) & (filtered_df['YEAR'] <= year_range[1])]
        
        if selected_region != 'All':
            filtered_df = filtered_df[filtered_df['REGION'] == selected_region]
        
        if selected_event_type != 'All':
            filtered_df = filtered_df[filtered_df['EVENT_TYPE'] == selected_event_type]
        
        if selected_admin1 != 'All':
            filtered_df = filtered_df[filtered_df['ADMIN1'] == selected_admin1]
    
    # Main content area
    st.markdown('<h1 class="main-header">🇰🇪 Kenya Security & Conflict Dashboard</h1>', unsafe_allow_html=True)
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "⏰ Time Analysis", "🗺️ Geographic", "🎯 Event Types"])
    
    with tab1:
        overview_tab(filtered_df)
    
    with tab2:
        time_analysis_tab(filtered_df)
    
    with tab3:
        geographic_tab(filtered_df, county_gdf)
    
    with tab4:
        event_types_tab(filtered_df)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Dashboard created with Streamlit | Data source: Kenya Security Events Dataset | County boundaries: Kenya Counties Shapefile</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
