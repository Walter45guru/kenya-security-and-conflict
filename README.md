# 🇰🇪 Kenya Security & Conflict Dashboard

A comprehensive Streamlit-based dashboard for analyzing security events, fatalities, and conflict patterns across Kenya's 47 counties, with special focus on election-related violence patterns.

## 🚀 Features

### 📊 **Overview Tab**
- **Key Performance Indicators (KPIs)**: Total events, average events/week, total fatalities, average fatalities/week
- **Event Type Distribution**: Interactive pie chart showing breakdown of security events
- **Summary Statistics**: Population exposure, unique counties, data coverage
- **Critical Election Security Analysis**: Historical context and recurring patterns

### ⏰ **Time Analysis Tab**
- **Events Over Time**: Line charts showing temporal trends with election cycle correlation
- **Fatalities Over Time**: Analysis of lethal incidents over time
- **Monthly Trends**: Seasonal patterns and election-related security challenges
- **Election Violence Patterns**: 2008 post-election violence and subsequent cycles

### 🗺️ **Geographic Tab**
- **Top Counties by Events**: Bar charts of high-incident areas
- **Top Counties by Fatalities**: Geographic distribution of lethal incidents
- **County Choropleth Maps**: Interactive maps showing events and fatalities by county
- **Election Violence Hotspots**: Identification of high-risk areas during electoral periods

### 🎯 **Event Types Tab**
- **Event Type Distribution**: Analysis of different security incident categories
- **Fatalities by Event Type**: Lethality analysis across incident categories
- **Sub-Event Analysis**: Detailed breakdown of specific incident types
- **Interactive Data Table**: Searchable and downloadable event data

## 🔧 Technical Features

- **County Name Standardization**: Automatic mapping between CSV data and shapefile counties
- **Interactive Visualizations**: Plotly charts with hover information and zoom capabilities
- **Responsive Design**: Optimized for different screen sizes and devices
- **Data Filtering**: Year range, region, event type, and county-based filtering
- **Export Functionality**: Download filtered data as CSV
- **Professional Styling**: Custom CSS for enhanced user experience

## 📁 Repository Structure

```
kenya-security-and-conflict/
├── kenya_dashboard.py          # Main Streamlit application
├── kenya_data.csv             # Security events dataset
├── group 1 logo.png           # Dashboard logo
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Walter45guru/kenya-security-and-conflict.git
   cd kenya-security-and-conflict
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the dashboard**
   ```bash
   python -m streamlit run kenya_dashboard.py
   ```

4. **Access the dashboard**
   - Local URL: http://localhost:8501
   - Network URL: http://[your-ip]:8501

## 📊 Data Sources

### Primary Dataset: `kenya_data.csv`
- **Security Events**: Comprehensive database of security incidents
- **Geographic Coverage**: All 47 Kenyan counties
- **Temporal Range**: Multi-year security event tracking
- **Event Categories**: Various types of security incidents and sub-events
- **Demographic Data**: Population exposure and fatality statistics

### Geographic Data: Kenya Counties Shapefile
- **County Boundaries**: Official administrative boundaries
- **Population Data**: County-level demographic information
- **Coordinate System**: WGS 1984 (EPSG:4326)
- **Coverage**: All 47 counties with complete geographic data

## 🗳️ Election Security Analysis

### Historical Context
The dashboard provides comprehensive analysis of Kenya's electoral security challenges, including:

- **2008 Post-Election Violence**: Watershed moment with 1,000+ fatalities and 600,000 displaced persons
- **Recurring Patterns**: Elevated security incidents during 2013, 2017, and 2022 elections
- **Risk Periods**: Pre and post-election security challenges
- **Geographic Hotspots**: Counties most affected during electoral periods

### Key Insights
- **Election Cycle Correlation**: Clear patterns linking electoral periods to security incidents
- **Risk Assessment**: Identification of high-risk areas and time periods
- **Policy Implications**: Recommendations for electoral security frameworks
- **Conflict Prevention**: Strategies for mitigating election-related violence

## 🎨 Customization

### Styling
- **Sidebar**: Navy blue theme (#000080) with white text
- **KPIs**: Red accent color (#FF3B1D) for key metrics
- **Insights**: Styled information boxes with gradient backgrounds
- **Responsive Design**: Optimized for various screen sizes

### Data Integration
- **County Mapping**: Automatic standardization of county names
- **Shapefile Integration**: Seamless geographic data visualization
- **Filter System**: Comprehensive data filtering capabilities
- **Export Options**: Data download functionality

## 🔍 Usage Examples

### Security Analysis
- **Temporal Patterns**: Identify peak periods of security incidents
- **Geographic Distribution**: Map security challenges across counties
- **Event Classification**: Analyze different types of security incidents
- **Population Impact**: Assess demographic exposure to security events

### Policy Development
- **Resource Allocation**: Target high-risk areas and time periods
- **Prevention Strategies**: Develop early warning systems
- **Electoral Security**: Design comprehensive electoral security frameworks
- **Conflict Resolution**: Implement conflict prevention mechanisms

## 📈 Future Enhancements

- **Real-time Data Integration**: Live updates from security databases
- **Predictive Analytics**: Machine learning models for risk assessment
- **Mobile Application**: Cross-platform mobile dashboard
- **API Integration**: RESTful API for external data access
- **Multi-language Support**: Localization for different regions

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Add comprehensive documentation for new features
- Include tests for new functionality
- Update requirements.txt for new dependencies

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Author

**Walter45guru**
- GitHub: [@Walter45guru](https://github.com/Walter45guru)
- Repository: [kenya-security-and-conflict](https://github.com/Walter45guru/kenya-security-and-conflict)

## 🙏 Acknowledgments

- **Data Sources**: Kenya security events dataset and county shapefiles
- **Open Source Libraries**: Streamlit, Plotly, Pandas, GeoPandas, Folium
- **Community**: Contributors and users of the dashboard

## 📞 Support

For questions, issues, or support:
- Create an issue on GitHub
- Contact the maintainer through GitHub
- Check the documentation and examples

---

**🇰🇪 Empowering Kenya's security analysis through data-driven insights and interactive visualization.**
