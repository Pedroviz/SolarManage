import streamlit as st
import pandas as pd
import time
import datetime
from data_handler import get_plant_data, get_plants, get_plant_details, get_historical_data
from visualization import (
    plot_energy_production, 
    plot_efficiency_chart, 
    create_kpi_metrics,
    plot_comparison_chart,
    create_power_gauge
)
from alerts import get_active_alerts, get_alert_history, acknowledge_alert
from models import PlantStatus, AlertLevel
from utils import format_energy_value, calculate_efficiency, get_weather_data

# Page configuration
st.set_page_config(
    page_title="Solar Plant Monitoring System",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state if it doesn't exist
if 'selected_plant' not in st.session_state:
    st.session_state.selected_plant = None
if 'refresh_rate' not in st.session_state:
    st.session_state.refresh_rate = 60  # Default refresh rate in seconds
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = time.time()
if 'show_alerts' not in st.session_state:
    st.session_state.show_alerts = False
if 'alert_filter' not in st.session_state:
    st.session_state.alert_filter = "All"
if 'date_range' not in st.session_state:
    st.session_state.date_range = (
        datetime.datetime.now() - datetime.timedelta(days=7),
        datetime.datetime.now()
    )

# Sidebar
with st.sidebar:
    st.title("Solar Plant Monitoring")
    
    # Plant selection
    plants = get_plants()
    plant_options = [p['name'] for p in plants]
    selected_plant_name = st.selectbox("Select Plant", plant_options)
    
    # Find the selected plant ID
    selected_plant = next((p for p in plants if p['name'] == selected_plant_name), None)
    if selected_plant:
        st.session_state.selected_plant = selected_plant['id']
    
    # Refresh rate control
    st.divider()
    st.subheader("Data Refresh Settings")
    refresh_rate = st.slider(
        "Refresh Rate (seconds)", 
        min_value=10, 
        max_value=300, 
        value=st.session_state.refresh_rate, 
        step=10
    )
    st.session_state.refresh_rate = refresh_rate
    
    # Date range selector for historical data
    st.divider()
    st.subheader("Historical Data")
    date_range = st.date_input(
        "Select Date Range",
        value=(
            st.session_state.date_range[0].date(),
            st.session_state.date_range[1].date()
        ),
        key="date_picker"
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        st.session_state.date_range = (
            datetime.datetime.combine(start_date, datetime.time.min),
            datetime.datetime.combine(end_date, datetime.time.max)
        )
    
    # Alert filters
    st.divider()
    st.subheader("Alert Settings")
    alert_filter = st.selectbox(
        "Filter Alerts by Level",
        ["All", "Critical", "Warning", "Information"]
    )
    st.session_state.alert_filter = alert_filter
    
    show_alerts = st.checkbox("Show Alert Panel", value=st.session_state.show_alerts)
    st.session_state.show_alerts = show_alerts
    
    # Information
    st.divider()
    st.info("This dashboard displays real-time and historical data from solar plants. Select a plant to view its performance metrics and alerts.")

# Main content
st.title("Solar Plant Monitoring Dashboard")

# Check if a plant is selected
if st.session_state.selected_plant is None:
    st.warning("Please select a plant from the sidebar to view its monitoring data.")
else:
    # Get current time and check if data should be refreshed
    current_time = time.time()
    time_diff = current_time - st.session_state.last_refresh
    
    if time_diff >= st.session_state.refresh_rate:
        st.session_state.last_refresh = current_time
    
    # Display last refresh time
    st.caption(f"Last updated: {datetime.datetime.fromtimestamp(st.session_state.last_refresh).strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get plant details
    plant_details = get_plant_details(st.session_state.selected_plant)
    
    # Display plant information
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader(plant_details['name'])
        st.write(f"Location: {plant_details['location']}")
        st.write(f"Capacity: {plant_details['capacity']} kW")
    
    with col2:
        st.write(f"Panels: {plant_details['panels_count']}")
        st.write(f"Installation Date: {plant_details['installation_date']}")
        st.write(f"Status: {plant_details['status']}")
    
    with col3:
        # Get weather data for the plant location
        weather = get_weather_data(plant_details['location'])
        st.write(f"Current Weather: {weather['condition']}")
        st.write(f"Temperature: {weather['temperature']}°C")
        st.write(f"Irradiance: {weather['irradiance']} W/m²")
    
    # Get current plant data
    plant_data = get_plant_data(st.session_state.selected_plant)
    
    # Display KPI metrics
    st.subheader("Key Performance Indicators")
    metrics_cols = st.columns(4)
    
    # Energy production
    with metrics_cols[0]:
        current_production = plant_data['current_production']
        daily_production = plant_data['daily_production']
        st.metric(
            "Current Production", 
            f"{current_production} kW",
            f"{round((current_production / plant_details['capacity']) * 100, 1)}% of capacity"
        )
    
    # Daily energy
    with metrics_cols[1]:
        daily_target = plant_details['daily_target']
        daily_percentage = (daily_production / daily_target) * 100 if daily_target > 0 else 0
        delta = f"{round(daily_percentage, 1)}% of target"
        delta_color = "normal" if daily_percentage >= 90 else "off"
        st.metric(
            "Today's Energy", 
            f"{daily_production} kWh", 
            delta,
            delta_color=delta_color
        )
    
    # Efficiency
    with metrics_cols[2]:
        efficiency = plant_data['efficiency']
        efficiency_delta = efficiency - plant_data['efficiency_yesterday']
        st.metric(
            "Current Efficiency", 
            f"{efficiency}%", 
            f"{round(efficiency_delta, 1)}% from yesterday"
        )
    
    # Performance ratio
    with metrics_cols[3]:
        performance_ratio = plant_data['performance_ratio']
        performance_delta = performance_ratio - plant_data['performance_ratio_yesterday']
        st.metric(
            "Performance Ratio", 
            f"{performance_ratio}%", 
            f"{round(performance_delta, 1)}% from yesterday"
        )
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs([
        "Real-time Monitoring", 
        "Historical Performance", 
        "Plant Status"
    ])
    
    with tab1:
        # Real-time power gauge
        st.subheader("Real-time Power Output")
        gauge_cols = st.columns([2, 1])
        
        with gauge_cols[0]:
            create_power_gauge(
                current_value=plant_data['current_production'],
                max_value=plant_details['capacity']
            )
        
        with gauge_cols[1]:
            st.write("**Power Statistics**")
            st.write(f"Peak Today: {plant_data['peak_power']} kW")
            st.write(f"Average Today: {plant_data['average_power']} kW")
            
            # Simple inverter status indicators
            st.write("**Inverter Status**")
            for i, status in enumerate(plant_data['inverter_status']):
                status_color = "green" if status == "Online" else "red"
                st.markdown(f"Inverter {i+1}: <span style='color:{status_color}'>{status}</span>", unsafe_allow_html=True)
        
        # Today's energy production chart
        st.subheader("Today's Energy Production")
        hourly_data = plant_data['hourly_production']
        plot_energy_production(hourly_data)
    
    with tab2:
        # Historical performance
        st.subheader("Historical Performance")
        
        # Get historical data based on the selected date range
        start_date, end_date = st.session_state.date_range
        historical_data = get_historical_data(
            st.session_state.selected_plant,
            start_date,
            end_date
        )
        
        # Daily production chart
        st.subheader("Daily Energy Production")
        plot_comparison_chart(
            historical_data['dates'],
            historical_data['daily_production'],
            historical_data['daily_target'],
            "Energy (kWh)",
            "Daily Production vs Target"
        )
        
        # Efficiency chart
        st.subheader("Efficiency Trend")
        plot_efficiency_chart(
            historical_data['dates'],
            historical_data['efficiency']
        )
    
    with tab3:
        # Plant status and components
        st.subheader("Plant Components Status")
        
        # Create status table
        components = plant_data['components_status']
        
        # Create a DataFrame for the status
        status_df = pd.DataFrame(components)
        
        # Color code the status column
        def highlight_status(val):
            if val == "Normal":
                return 'background-color: #c6efce; color: #006100'
            elif val == "Warning":
                return 'background-color: #ffeb9c; color: #9c5700'
            else:  # Critical
                return 'background-color: #ffc7ce; color: #9c0006'
        
        # Display the styled DataFrame
        st.dataframe(
            status_df.style.applymap(
                highlight_status, 
                subset=['status']
            ),
            use_container_width=True
        )
        
        # Maintenance Schedule
        st.subheader("Maintenance Schedule")
        maintenance_data = plant_details['maintenance_schedule']
        
        if maintenance_data:
            maintenance_df = pd.DataFrame(maintenance_data)
            st.dataframe(maintenance_df, use_container_width=True)
        else:
            st.info("No scheduled maintenance activities.")

# Alert panel (conditional)
if st.session_state.show_alerts:
    st.sidebar.divider()
    st.sidebar.subheader("Active Alerts")
    
    # Get active alerts based on filter
    alerts = get_active_alerts(
        st.session_state.selected_plant,
        alert_level=st.session_state.alert_filter if st.session_state.alert_filter != "All" else None
    )
    
    if alerts:
        for alert in alerts:
            # Determine alert color based on level
            alert_color = {
                "Critical": "red",
                "Warning": "orange",
                "Information": "blue"
            }.get(alert['level'], "gray")
            
            with st.sidebar.expander(f"{alert['level']}: {alert['title']}"):
                st.markdown(f"<span style='color:{alert_color}'>{alert['message']}</span>", unsafe_allow_html=True)
                st.caption(f"Timestamp: {alert['timestamp']}")
                
                if st.button("Acknowledge", key=f"ack_{alert['id']}"):
                    acknowledge_alert(alert['id'])
                    st.success("Alert acknowledged")
                    # Refresh the page after a short delay
                    time.sleep(1)
                    st.rerun()
    else:
        if st.session_state.alert_filter == "All":
            st.sidebar.success("No active alerts!")
        else:
            st.sidebar.info(f"No {st.session_state.alert_filter.lower()} alerts active.")
