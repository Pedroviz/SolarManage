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

# Set page configuration
st.set_page_config(
    page_title="Monitoramento de Usinas Solares",
    page_icon="☀️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for improved layout and background
st.markdown("""
<style>
    /* Melhorias gerais de layout */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Fundo gradiente sutil para toda a página */
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #edf6ff 100%);
    }
    
    /* Estilo para os cabeçalhos */
    h1, h2, h3 {
        color: #0c4b8e;
        font-weight: 600;
    }
    
    h1 {
        font-size: 2.2rem;
        margin-bottom: 1.5rem;
        background: linear-gradient(90deg, #1976D2, #64B5F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        font-size: 1.5rem;
        border-bottom: 2px solid #e0e7ff;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        font-size: 1.2rem;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }
    
    /* Estilo para os elementos de dados */
    .dataframe {
        border: none !important;
        border-radius: 5px;
        overflow: hidden;
    }
    
    .dataframe thead tr th {
        background-color: #1976D2;
        color: white !important;
        text-align: center !important;
        padding: 12px 8px !important;
    }
    
    .dataframe tbody tr:nth-child(even) {
        background-color: #f8f9fa;
    }
    
    /* Melhoria nos espaçamentos */
    .stTabs [role="tablist"] {
        gap: 8px;
    }
    
    .stTabs [role="tab"] {
        background-color: rgba(255, 255, 255, 0.7);
        border-radius: 4px 4px 0 0;
        padding: 0.5rem 1rem;
        border: 1px solid #e0e7ff;
        border-bottom: none;
    }
    
    .stTabs [role="tab"][aria-selected="true"] {
        background-color: #1976D2;
        color: white;
        border-color: #1976D2;
    }
    
    /* Estilo para expander */
    .streamlit-expanderHeader {
        font-weight: 600;
        background-color: rgba(25, 118, 210, 0.05);
        border-radius: 4px;
    }
    
    /* Scrollbar personalizada */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c5d8f1;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #1976D2;
    }
</style>
""", unsafe_allow_html=True)

# Page configuration was set at the top of the file

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
    st.title("Monitoramento de Usinas Solares")
    
    # Custom sidebar styles
    st.markdown("""
    <style>
    .sidebar-section {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 10px 15px;
        margin-bottom: 15px;
        border-left: 3px solid #1976D2;
    }
    .sidebar-title {
        color: #1976D2;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Plant selection
    plants = get_plants()
    plant_options = [p['name'] for p in plants]
    st.markdown('<div class="sidebar-section"><div class="sidebar-title">Selecionar Usina</div>', unsafe_allow_html=True)
    selected_plant_name = st.selectbox("", plant_options, label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Find the selected plant ID
    selected_plant = next((p for p in plants if p['name'] == selected_plant_name), None)
    if selected_plant:
        st.session_state.selected_plant = selected_plant['id']
    
    # Refresh rate control
    st.markdown('<div class="sidebar-section"><div class="sidebar-title">Configurações de Atualização</div>', unsafe_allow_html=True)
    refresh_rate = st.slider(
        "Taxa de Atualização (segundos)", 
        min_value=10, 
        max_value=300, 
        value=st.session_state.refresh_rate, 
        step=10
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.session_state.refresh_rate = refresh_rate
    
    # Date range selector for historical data
    st.markdown('<div class="sidebar-section"><div class="sidebar-title">Dados Históricos</div>', unsafe_allow_html=True)
    date_range = st.date_input(
        "Selecionar Período",
        value=(
            st.session_state.date_range[0].date(),
            st.session_state.date_range[1].date()
        ),
        key="date_picker"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        st.session_state.date_range = (
            datetime.datetime.combine(start_date, datetime.time.min),
            datetime.datetime.combine(end_date, datetime.time.max)
        )
    
    # Alert filters
    st.markdown('<div class="sidebar-section"><div class="sidebar-title">Configurações de Alertas</div>', unsafe_allow_html=True)
    alert_filter = st.selectbox(
        "Filtrar Alertas por Nível",
        ["Todos", "Crítico", "Atenção", "Informação"]
    )
    
    # Map alert filter values to English values used in backend
    alert_filter_map = {
        "Todos": "All",
        "Crítico": "Critical",
        "Atenção": "Warning",
        "Informação": "Information"
    }
    st.session_state.alert_filter = alert_filter_map.get(alert_filter, "All")
    
    show_alerts = st.checkbox("Mostrar Painel de Alertas", value=st.session_state.show_alerts)
    st.session_state.show_alerts = show_alerts
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Information
    st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
    st.info("Este painel exibe dados em tempo real e históricos das usinas solares. Selecione uma usina para visualizar suas métricas de desempenho e alertas.")
    st.markdown('</div>', unsafe_allow_html=True)

# Main content
st.title("Painel de Monitoramento de Usinas Solares")

# Check if a plant is selected
if st.session_state.selected_plant is None:
    st.warning("Por favor, selecione uma usina no painel lateral para visualizar os dados de monitoramento.")
else:
    # Get current time and check if data should be refreshed
    current_time = time.time()
    time_diff = current_time - st.session_state.last_refresh
    
    if time_diff >= st.session_state.refresh_rate:
        st.session_state.last_refresh = current_time
    
    # Display last refresh time
    st.caption(f"Última atualização: {datetime.datetime.fromtimestamp(st.session_state.last_refresh).strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Get plant details
    plant_details = get_plant_details(st.session_state.selected_plant)
    
    # Create a card-style container for plant information
    st.markdown("""
    <style>
    .plant-info-container {
        background-color: #f0f7ff;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 25px;
        border-left: 5px solid #1976D2;
    }
    .plant-name {
        color: #1976D2;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 15px;
    }
    .info-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 15px;
    }
    .info-item {
        margin-bottom: 8px;
    }
    .info-label {
        color: #666;
        font-size: 0.9rem;
        margin-bottom: 3px;
    }
    .info-value {
        color: #1E293B;
        font-size: 1.1rem;
        font-weight: 500;
    }
    .weather-icon {
        margin-right: 5px;
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Get weather data for the plant location
    weather = get_weather_data(plant_details['location'])
    
    # Determine weather icon
    weather_icon = "☀️"
    if "Cloud" in weather['condition']:
        weather_icon = "⛅"
    elif "Rain" in weather['condition']:
        weather_icon = "🌧️"
    elif "Night" in weather['condition']:
        weather_icon = "🌙"
    
    # Create the plant info card
    html_content = f"""
    <div class="plant-info-container">
        <div class="plant-name">{plant_details['name']}</div>
        <div class="info-grid">
            <div>
                <div class="info-item">
                    <div class="info-label">Localização</div>
                    <div class="info-value">📍 {plant_details['location']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Capacidade</div>
                    <div class="info-value">⚡ {plant_details['capacity']} kW</div>
                </div>
            </div>
            <div>
                <div class="info-item">
                    <div class="info-label">Painéis</div>
                    <div class="info-value">🔋 {plant_details['panels_count']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Instalação</div>
                    <div class="info-value">📅 {plant_details['installation_date']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Status</div>
                    <div class="info-value">🔌 {plant_details['status']}</div>
                </div>
            </div>
            <div>
                <div class="info-item">
                    <div class="info-label">Clima Atual</div>
                    <div class="info-value"><span class="weather-icon">{weather_icon}</span> {weather['condition']}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Temperatura</div>
                    <div class="info-value">🌡️ {weather['temperature']}°C</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Irradiância</div>
                    <div class="info-value">☀️ {weather['irradiance']} W/m²</div>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)
    
    # Get current plant data
    plant_data = get_plant_data(st.session_state.selected_plant)
    
    # Display KPI metrics
    st.subheader("Indicadores-Chave de Desempenho")
    
    # Use the custom KPI metrics function 
    create_kpi_metrics(plant_data, plant_details)
    
    # Create tabs for different visualizations
    tab1, tab2, tab3 = st.tabs([
        "Monitoramento em Tempo Real", 
        "Desempenho Histórico", 
        "Status da Usina"
    ])
    
    with tab1:
        # Real-time power gauge
        st.subheader("Saída de Energia em Tempo Real")
        gauge_cols = st.columns([2, 1])
        
        with gauge_cols[0]:
            create_power_gauge(
                current_value=plant_data['current_production'],
                max_value=plant_details['capacity']
            )
        
        with gauge_cols[1]:
            # Custom styled box for power statistics
            st.markdown("""
            <style>
            .stats-box {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 15px;
                margin-bottom: 15px;
                border-left: 4px solid #1976D2;
            }
            .stats-title {
                color: #1976D2;
                font-weight: 600;
                font-size: 1rem;
                margin-bottom: 10px;
            }
            .stats-item {
                margin-bottom: 8px;
                font-size: 0.95rem;
            }
            .online-status {
                color: #4CAF50;
                font-weight: 500;
            }
            .offline-status {
                color: #F44336;
                font-weight: 500;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Power statistics
            peak_power = plant_data['peak_power']
            avg_power = plant_data['average_power']
            
            stats_html = f"""
            <div class="stats-box">
                <div class="stats-title">Estatísticas de Energia</div>
                <div class="stats-item">Pico Hoje: <strong>{peak_power} kW</strong></div>
                <div class="stats-item">Média Hoje: <strong>{avg_power} kW</strong></div>
            </div>
            """
            st.markdown(stats_html, unsafe_allow_html=True)
            
            # Inverter status indicators
            inverter_html = '<div class="stats-box"><div class="stats-title">Status dos Inversores</div>'
            
            for i, status in enumerate(plant_data['inverter_status']):
                status_class = "online-status" if status == "Online" else "offline-status"
                status_label = "Online" if status == "Online" else "Offline"
                inverter_html += f'<div class="stats-item">Inversor {i+1}: <span class="{status_class}">{status_label}</span></div>'
            
            inverter_html += '</div>'
            st.markdown(inverter_html, unsafe_allow_html=True)
        
        # Today's energy production chart
        st.subheader("Produção de Energia Hoje")
        hourly_data = plant_data['hourly_production']
        plot_energy_production(hourly_data)
    
    with tab2:
        # Historical performance
        st.subheader("Desempenho Histórico")
        
        # Get historical data based on the selected date range
        start_date, end_date = st.session_state.date_range
        historical_data = get_historical_data(
            st.session_state.selected_plant,
            start_date,
            end_date
        )
        
        # Daily production chart
        st.subheader("Produção Diária de Energia")
        plot_comparison_chart(
            historical_data['dates'],
            historical_data['daily_production'],
            historical_data['daily_target'],
            "Energia (kWh)",
            "Produção Diária vs Meta"
        )
        
        # Efficiency chart
        st.subheader("Tendência de Eficiência")
        plot_efficiency_chart(
            historical_data['dates'],
            historical_data['efficiency']
        )
    
    with tab3:
        # Plant status and components
        st.subheader("Status dos Componentes da Usina")
        
        # Create status table
        components = plant_data['components_status']
        
        # Translate component names and column names
        component_map = {
            "PV Panels": "Painéis Fotovoltaicos",
            "Inverters": "Inversores",
            "Mounting System": "Sistema de Montagem",
            "AC Subsystem": "Subsistema AC",
            "Communications": "Comunicações"
        }
        
        status_map = {
            "Normal": "Normal",
            "Warning": "Atenção",
            "Critical": "Crítico"
        }
        
        # Translate component data
        for comp in components:
            if comp["component"] in component_map:
                comp["component"] = component_map[comp["component"]]
            if comp["status"] in status_map:
                comp["status"] = status_map[comp["status"]]
            comp["last_check"] = "Última Verificação: " + comp["last_check"]
        
        # Create a DataFrame for the status
        status_df = pd.DataFrame(components)
        status_df.rename(columns={
            "component": "Componente",
            "status": "Status",
            "last_check": "Última Verificação"
        }, inplace=True)
        
        # Color code the status column
        def highlight_status(val):
            if val == "Normal":
                return 'background-color: #c6efce; color: #006100'
            elif val == "Atenção":
                return 'background-color: #ffeb9c; color: #9c5700'
            else:  # Critical
                return 'background-color: #ffc7ce; color: #9c0006'
        
        # Display the styled DataFrame with custom CSS
        st.markdown("""
        <style>
        .component-table {
            font-family: 'Arial', sans-serif;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.dataframe(
            status_df.style.applymap(
                highlight_status, 
                subset=['Status']
            ),
            use_container_width=True,
            height=250
        )
        
        # Maintenance Schedule
        st.subheader("Agenda de Manutenção")
        maintenance_data = plant_details['maintenance_schedule']
        
        if maintenance_data:
            # Translate maintenance data
            for item in maintenance_data:
                if item.get("task") == "Panel Cleaning":
                    item["task"] = "Limpeza de Painéis"
                elif item.get("task") == "Inverter Inspection":
                    item["task"] = "Inspeção de Inversores"
                elif item.get("task") == "Inverter Replacement":
                    item["task"] = "Substituição de Inversores"
                elif item.get("task") == "Wiring Check":
                    item["task"] = "Verificação de Fiação"
                elif item.get("task") == "Annual Maintenance":
                    item["task"] = "Manutenção Anual"
                elif item.get("task") == "Site Inspection":
                    item["task"] = "Inspeção do Local"
                
                if item.get("status") == "Scheduled":
                    item["status"] = "Agendado"
                elif item.get("status") == "In Progress":
                    item["status"] = "Em Andamento"
                elif item.get("status") == "Completed":
                    item["status"] = "Concluído"
            
            maintenance_df = pd.DataFrame(maintenance_data)
            maintenance_df.rename(columns={
                "task": "Tarefa",
                "date": "Data",
                "status": "Status"
            }, inplace=True)
            
            st.dataframe(maintenance_df, use_container_width=True)
        else:
            st.info("Não há atividades de manutenção agendadas.")

# Alert panel (conditional)
if st.session_state.show_alerts:
    st.sidebar.divider()
    st.sidebar.markdown('<div class="sidebar-section"><div class="sidebar-title">Alertas Ativos</div>', unsafe_allow_html=True)
    
    # Get active alerts based on filter
    alerts = get_active_alerts(
        st.session_state.selected_plant,
        alert_level=st.session_state.alert_filter if st.session_state.alert_filter != "All" else None
    )
    
    # Custom alert styling
    st.sidebar.markdown("""
    <style>
    .alert-item {
        margin-bottom: 10px;
        border-radius: 4px;
        overflow: hidden;
    }
    .alert-critical {
        border-left: 4px solid #F44336;
    }
    .alert-warning {
        border-left: 4px solid #FF9800;
    }
    .alert-info {
        border-left: 4px solid #2196F3;
    }
    .alert-header {
        padding: 8px 12px;
        font-weight: 500;
        font-size: 0.9rem;
        cursor: pointer;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .alert-critical .alert-header {
        background-color: rgba(244, 67, 54, 0.1);
        color: #d32f2f;
    }
    .alert-warning .alert-header {
        background-color: rgba(255, 152, 0, 0.1);
        color: #e65100;
    }
    .alert-info .alert-header {
        background-color: rgba(33, 150, 243, 0.1);
        color: #0277bd;
    }
    .alert-timestamp {
        font-size: 0.75rem;
        opacity: 0.7;
        margin-top: 4px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Translate alert levels
    alert_level_map = {
        "Critical": "Crítico",
        "Warning": "Atenção",
        "Information": "Informação"
    }
    
    if alerts:
        for alert in alerts:
            # Translate alert level
            translated_level = alert_level_map.get(alert['level'], alert['level'])
            
            # Determine alert class and color
            alert_class = alert['level'].lower()
            if alert_class == "warning":
                alert_class = "warning"
            elif alert_class == "information":
                alert_class = "info"
            else:
                alert_class = "critical"
                
            alert_color = {
                "Critical": "#d32f2f",
                "Warning": "#e65100",
                "Information": "#0277bd"
            }.get(alert['level'], "gray")
            
            # Create alert expander with custom styling
            with st.sidebar.expander(f"{translated_level}: {alert['title']}"):
                st.markdown(f"<div style='color:{alert_color}'>{alert['message']}</div>", unsafe_allow_html=True)
                st.caption(f"Horário: {alert['timestamp']}")
                
                # Acknowledge button
                if st.button("Confirmar", key=f"ack_{alert['id']}"):
                    acknowledge_alert(alert['id'])
                    st.success("Alerta confirmado")
                    # Refresh the page after a short delay
                    time.sleep(1)
                    st.rerun()
    else:
        # Display message when no alerts
        if st.session_state.alert_filter == "All":
            st.sidebar.success("Não há alertas ativos!")
        else:
            # Map back from English to Portuguese for display
            filter_display = {
                "Critical": "críticos",
                "Warning": "de atenção",
                "Information": "informativos"
            }.get(st.session_state.alert_filter, st.session_state.alert_filter.lower())
            st.sidebar.info(f"Não há alertas {filter_display} ativos.")
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
