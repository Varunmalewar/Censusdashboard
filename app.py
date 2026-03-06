import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="India Census Dashboard",
    page_icon="bar_chart",
    layout='wide',
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    /* Main header styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A5F;
        text-align: center;
        margin-bottom: 0.5rem;
        padding-top: 1rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    /* Metric card styling */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
    }
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    /* Sidebar styling */
    .sidebar-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: inherit;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #667eea;
    }
    /* Info box */
    .info-box {
        background-color: #f0f7ff;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    /* Footer */
    .footer {
        text-align: center;
        color: #888;
        padding: 2rem 0 1rem 0;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv('india.csv')

df = load_data()

# Header
st.markdown('<h1 class="main-header">India Census Data Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Explore demographic insights across Indian states and districts</p>', unsafe_allow_html=True)

# Prepare state list
list_of_states = list(df['State'].unique())
list_of_states.insert(0, 'Overall India')

# Sidebar configuration
with st.sidebar:
    st.markdown('<p class="sidebar-header">Dashboard Controls</p>', unsafe_allow_html=True)
    
    st.markdown("#### Region Selection")
    selected_state = st.selectbox(
        'Select a State/Territory',
        list_of_states,
        help="Choose 'Overall India' to view all districts or select a specific state"
    )
    
    st.markdown("---")
    st.markdown("#### Parameter Configuration")
    
    parameter_options = ['Population', 'Households_with_Internet', 'sex_ratio', 'literacy_rate']
    parameter_labels = {
        'Population': 'Population',
        'Households_with_Internet': 'Internet Access',
        'sex_ratio': 'Sex Ratio',
        'literacy_rate': 'Literacy Rate'
    }
    
    primary = st.selectbox(
        'Primary Parameter (Size)',
        sorted(parameter_options),
        format_func=lambda x: parameter_labels.get(x, x),
        help="This parameter controls the size of markers on the map"
    )
    
    secondary = st.selectbox(
        'Secondary Parameter (Color)',
        sorted(parameter_options),
        index=1,
        format_func=lambda x: parameter_labels.get(x, x),
        help="This parameter controls the color intensity of markers"
    )
    
    st.markdown("---")
    
    # Color scheme selection
    color_scheme = st.selectbox(
        'Color Scheme',
        ['Viridis', 'Plasma', 'Inferno', 'Turbo', 'Blues', 'Reds', 'Greens'],
        help="Select the color palette for the visualization"
    )
    
    st.markdown("---")
    
    plot = st.button('Generate Visualization', use_container_width=True, type="primary")
    
   

# Main content area
if plot:
    # Filter data based on selection
    if selected_state == 'Overall India':
        filtered_df = df
        zoom_level = 3.5
        center_lat = 20.5937
        center_lon = 78.9629
    else:
        filtered_df = df[df['State'] == selected_state]
        zoom_level = 6
        center_lat = filtered_df['Latitude'].mean()
        center_lon = filtered_df['Longitude'].mean()
    
    # Display metrics
    st.markdown("### Key Statistics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_pop = filtered_df['Population'].sum()
        st.metric(
            label="Total Population",
            value=f"{total_pop:,.0f}",
            delta=None
        )
    
    with col2:
        avg_literacy = filtered_df['literacy_rate'].mean()
        st.metric(
            label="Avg. Literacy Rate",
            value=f"{avg_literacy:.1f}%",
            delta=None
        )
    
    with col3:
        avg_sex_ratio = filtered_df['sex_ratio'].mean()
        st.metric(
            label="Avg. Sex Ratio",
            value=f"{avg_sex_ratio:.0f}",
            delta=None
        )
    
    with col4:
        total_internet = filtered_df['Households_with_Internet'].sum()
        st.metric(
            label="Internet Households",
            value=f"{total_internet:,.0f}",
            delta=None
        )
    
    st.markdown("---")
    
    # Map visualization
    st.markdown("### Geographic Distribution")
    st.markdown(f"""
    <div class="info-box">
        <strong>Visualization Guide:</strong> Marker <strong>size</strong> represents <em>{parameter_labels.get(primary, primary)}</em> 
        and marker <strong>color</strong> represents <em>{parameter_labels.get(secondary, secondary)}</em>
    </div>
    """, unsafe_allow_html=True)
    
    # Create the map
    fig = px.scatter_map(
        filtered_df,
        lat="Latitude",
        lon="Longitude",
        size=primary,
        size_max=40,
        color=secondary,
        color_continuous_scale=color_scheme.lower(),
        zoom=zoom_level,
        hover_name="District",
        hover_data={
            'State': True,
            'Population': ':,.0f',
            'literacy_rate': ':.1f',
            'sex_ratio': ':.0f',
            'Households_with_Internet': ':,.0f',
            'Latitude': False,
            'Longitude': False
        },
        center={"lat": center_lat, "lon": center_lon}
    )
    
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=600,
        coloraxis_colorbar=dict(
            title=parameter_labels.get(secondary, secondary),
            thickness=15,
            len=0.7
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Data table section
    with st.expander("View Detailed Data", expanded=False):
        st.dataframe(
            filtered_df[['State', 'District', 'Population', 'literacy_rate', 'sex_ratio', 'Households_with_Internet']]
            .sort_values(by=primary, ascending=False)
            .reset_index(drop=True),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Population": st.column_config.NumberColumn(format="%d"),
                "literacy_rate": st.column_config.NumberColumn("Literacy Rate (%)", format="%.1f"),
                "sex_ratio": st.column_config.NumberColumn("Sex Ratio", format="%.0f"),
                "Households_with_Internet": st.column_config.NumberColumn("Internet Households", format="%d")
            }
        )

else:
    # Welcome message when no visualization is generated
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        ### Welcome to the India Census Dashboard
        
        This interactive tool allows you to explore demographic data across Indian states and districts.
        
        **Getting Started:**
        1. Select a state or choose "Overall India" from the sidebar
        2. Choose your primary and secondary parameters
        3. Select a color scheme that suits your preference
        4. Click **Generate Visualization** to see the results
        
        **Available Parameters:**
        - **Population**: Total population count
        - **Literacy Rate**: Percentage of literate population
        - **Sex Ratio**: Females per 100 males
        - **Internet Access**: Households with internet connectivity
        """)
        
        # Quick stats preview
        st.markdown("### 📊 Quick Overview")
        
    # Display overall India stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total States/UTs", f"{df['State'].nunique()}")
    with col2:
        st.metric("Total Districts", f"{len(df)}")
    with col3:
        st.metric("Total Population", f"{df['Population'].sum():,.0f}")
    with col4:
        st.metric("Avg. Literacy", f"{df['literacy_rate'].mean():.1f}%")

# Footer
st.markdown("---")
st.markdown('<p class="footer">India Census Data Dashboard | Built with Streamlit & Plotly</p>', unsafe_allow_html=True)      