import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any, Union, Tuple

# Define a custom color palette for better visual appeal
COLOR_PALETTE = {
    "primary": "#1976D2",       # Primary blue
    "secondary": "#FF9800",     # Orange
    "success": "#4CAF50",       # Green
    "warning": "#FFC107",       # Amber
    "danger": "#F44336",        # Red
    "info": "#03A9F4",          # Light Blue
    "background": "#FFFFFF",    # White
    "text": "#1E293B",          # Dark blue-gray
    "grid": "#E0E0E0"           # Light gray
}

def plot_energy_production(hourly_data: Dict[str, List[Any]]) -> None:
    """
    Plot hourly energy production chart
    
    Args:
        hourly_data (Dict[str, List[Any]]): Dictionary with 'hours' and 'values' lists
    """
    hours = hourly_data['hours']
    values = hourly_data['values']
    
    # Determine current hour for splitting actual vs forecast
    current_hour = len([v for v in values if v > 0])
    
    # Create figure
    fig = go.Figure()
    
    # Add actual production
    fig.add_trace(go.Bar(
        x=hours[:current_hour],
        y=values[:current_hour],
        name="Produção Real",
        marker_color=COLOR_PALETTE["success"],
        hovertemplate='%{y:.1f} kWh<extra></extra>'
    ))
    
    # Add projected production with different color
    fig.add_trace(go.Bar(
        x=hours[current_hour:],
        y=values[current_hour:],
        name="Produção Projetada",
        marker_color='rgba(76, 175, 80, 0.5)',  # Semi-transparent green
        hovertemplate='%{y:.1f} kWh<extra></extra>'
    ))
    
    # Update layout with improved styling
    fig.update_layout(
        xaxis_title="Hora",
        yaxis_title="Energia (kWh)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=40, t=40, b=40),
        height=400,
        plot_bgcolor='rgba(240, 247, 255, 0.5)',
        paper_bgcolor='rgba(255, 255, 255, 0)',
        font=dict(color=COLOR_PALETTE["text"]),
        xaxis=dict(
            gridcolor=COLOR_PALETTE["grid"],
            tickfont=dict(size=10)
        ),
        yaxis=dict(
            gridcolor=COLOR_PALETTE["grid"],
            tickfont=dict(size=10)
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="sans-serif"
        )
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

def plot_efficiency_chart(dates: List[str], efficiency_values: List[float]) -> None:
    """
    Plot efficiency trend over time
    
    Args:
        dates (List[str]): List of date strings
        efficiency_values (List[float]): List of efficiency values
    """
    # Create figure
    fig = go.Figure()
    
    # Add efficiency line
    fig.add_trace(go.Scatter(
        x=dates,
        y=efficiency_values,
        name="Eficiência",
        line=dict(color=COLOR_PALETTE["primary"], width=3),
        mode='lines+markers',
        marker=dict(size=8, symbol='circle', line=dict(width=2, color=COLOR_PALETTE["primary"])),
        hovertemplate='%{y:.1f}%<extra></extra>'
    ))
    
    # Add horizontal reference line at 95% - good performance
    fig.add_shape(
        type="line",
        x0=dates[0],
        y0=95,
        x1=dates[-1],
        y1=95,
        line=dict(
            color=COLOR_PALETTE["success"],
            width=1.5,
            dash="dash",
        )
    )
    
    # Add annotation for reference line
    fig.add_annotation(
        x=dates[0],
        y=95,
        text="Desempenho Ideal (95%)",
        showarrow=False,
        yshift=10,
        font=dict(size=10, color=COLOR_PALETTE["success"])
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Eficiência (%)",
        yaxis=dict(
            range=[85, 100],  # Set y-axis range to focus on relevant values
            gridcolor=COLOR_PALETTE["grid"],
            tickfont=dict(size=10)
        ),
        xaxis=dict(
            gridcolor=COLOR_PALETTE["grid"],
            tickfont=dict(size=10)
        ),
        plot_bgcolor='rgba(240, 247, 255, 0.5)',
        paper_bgcolor='rgba(255, 255, 255, 0)',
        font=dict(color=COLOR_PALETTE["text"]),
        margin=dict(l=40, r=40, t=40, b=40),
        height=400,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="sans-serif"
        )
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

def create_kpi_metrics(
    plant_data: Dict[str, Any],
    plant_details: Dict[str, Any]
) -> None:
    """
    Create KPI metrics display
    
    Args:
        plant_data (Dict[str, Any]): Current plant data
        plant_details (Dict[str, Any]): Plant details
    """
    # Use CSS to create more attractive metrics
    st.markdown("""
    <style>
    .metric-container {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
        transition: all 0.3s cubic-bezier(.25,.8,.25,1);
        margin-bottom: 20px;
    }
    .metric-container:hover {
        box-shadow: 0 3px 6px rgba(0,0,0,0.16), 0 3px 6px rgba(0,0,0,0.23);
    }
    .metric-title {
        color: #1E293B;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .metric-value {
        color: #1976D2;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .metric-delta {
        font-size: 0.9rem;
        font-weight: 500;
    }
    .metric-delta-positive {
        color: #4CAF50;
    }
    .metric-delta-negative {
        color: #F44336;
    }
    .metric-delta-neutral {
        color: #FF9800;
    }
    </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    
    # Current production
    with cols[0]:
        current_production = plant_data['current_production']
        capacity_percentage = round((current_production / plant_details['capacity']) * 100, 1)
        delta_class = "positive" if capacity_percentage >= 50 else "neutral"
        
        html_content = f"""
        <div class="metric-container">
            <div class="metric-title">Produção Atual</div>
            <div class="metric-value">{current_production} kW</div>
            <div class="metric-delta metric-delta-{delta_class}">{capacity_percentage}% da capacidade</div>
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
    
    # Daily energy
    with cols[1]:
        daily_production = plant_data['daily_production']
        daily_target = plant_details['daily_target']
        daily_percentage = round((daily_production / daily_target) * 100, 1) if daily_target > 0 else 0
        delta_class = "positive" if daily_percentage >= 90 else ("neutral" if daily_percentage >= 70 else "negative")
        
        html_content = f"""
        <div class="metric-container">
            <div class="metric-title">Energia Hoje</div>
            <div class="metric-value">{daily_production} kWh</div>
            <div class="metric-delta metric-delta-{delta_class}">{daily_percentage}% da meta</div>
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
    
    # Efficiency
    with cols[2]:
        efficiency = plant_data['efficiency']
        efficiency_delta = round(efficiency - plant_data['efficiency_yesterday'], 1)
        delta_class = "positive" if efficiency_delta > 0 else ("negative" if efficiency_delta < 0 else "neutral")
        delta_symbol = "↑" if efficiency_delta > 0 else ("↓" if efficiency_delta < 0 else "→")
        
        html_content = f"""
        <div class="metric-container">
            <div class="metric-title">Eficiência Atual</div>
            <div class="metric-value">{efficiency}%</div>
            <div class="metric-delta metric-delta-{delta_class}">{delta_symbol} {abs(efficiency_delta)}% em relação a ontem</div>
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
    
    # Performance ratio
    with cols[3]:
        performance_ratio = plant_data['performance_ratio']
        performance_delta = round(performance_ratio - plant_data['performance_ratio_yesterday'], 1)
        delta_class = "positive" if performance_delta > 0 else ("negative" if performance_delta < 0 else "neutral")
        delta_symbol = "↑" if performance_delta > 0 else ("↓" if performance_delta < 0 else "→")
        
        html_content = f"""
        <div class="metric-container">
            <div class="metric-title">Índice de Desempenho</div>
            <div class="metric-value">{performance_ratio}%</div>
            <div class="metric-delta metric-delta-{delta_class}">{delta_symbol} {abs(performance_delta)}% em relação a ontem</div>
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)

def plot_comparison_chart(
    dates: List[str], 
    actual_values: List[float], 
    target_values: List[float],
    y_label: str,
    title: str
) -> None:
    """
    Plot comparison chart between actual and target values
    
    Args:
        dates (List[str]): List of date strings
        actual_values (List[float]): List of actual values
        target_values (List[float]): List of target values
        y_label (str): Label for y-axis
        title (str): Chart title
    """
    # Create figure
    fig = go.Figure()
    
    # Add actual values line
    fig.add_trace(go.Scatter(
        x=dates,
        y=actual_values,
        name="Produção Real",
        line=dict(color=COLOR_PALETTE["success"], width=3),
        mode='lines+markers',
        marker=dict(size=7, symbol='circle'),
        hovertemplate='%{y:.1f} kWh<extra></extra>'
    ))
    
    # Add target values line
    fig.add_trace(go.Scatter(
        x=dates,
        y=target_values,
        name="Meta",
        line=dict(color=COLOR_PALETTE["secondary"], width=2.5, dash='dash'),
        mode='lines',
        hovertemplate='%{y:.1f} kWh<extra></extra>'
    ))
    
    # Calculate achievement percentage
    achievement = [100 * a / t if t > 0 else 0 for a, t in zip(actual_values, target_values)]
    
    # Add achievement percentage line on secondary y-axis
    fig.add_trace(go.Scatter(
        x=dates,
        y=achievement,
        name="Desempenho (%)",
        line=dict(color=COLOR_PALETTE["primary"], width=2),
        mode='lines',
        yaxis="y2",
        hovertemplate='%{y:.1f}%<extra></extra>'
    ))
    
    # Fill area between actual and target
    fill_value = []
    for a, t in zip(actual_values, target_values):
        if a > t:
            fill_value.append(a)
        else:
            fill_value.append(t)
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=actual_values,
        name='Área de Comparação',
        showlegend=False,
        line=dict(width=0),
        hoverinfo='skip'
    ))
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=target_values,
        name='Área de Comparação',
        fillcolor='rgba(0, 150, 136, 0.1)',
        fill='tonexty',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Update layout with secondary y-axis
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, color=COLOR_PALETTE["text"])
        ),
        xaxis_title="Data",
        yaxis_title=y_label,
        yaxis2=dict(
            title="Desempenho (%)",
            titlefont=dict(color=COLOR_PALETTE["primary"]),
            tickfont=dict(color=COLOR_PALETTE["primary"]),
            anchor="x",
            overlaying="y",
            side="right",
            range=[0, 120],
            gridcolor=COLOR_PALETTE["grid"]
        ),
        yaxis=dict(
            gridcolor=COLOR_PALETTE["grid"],
            tickfont=dict(size=10)
        ),
        xaxis=dict(
            gridcolor=COLOR_PALETTE["grid"],
            tickfont=dict(size=10)
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(255, 255, 255, 0.7)",
            bordercolor=COLOR_PALETTE["grid"],
            borderwidth=1
        ),
        plot_bgcolor='rgba(240, 247, 255, 0.5)',
        paper_bgcolor='rgba(255, 255, 255, 0)',
        font=dict(color=COLOR_PALETTE["text"]),
        margin=dict(l=40, r=40, t=60, b=40),
        height=400,
        hoverlabel=dict(
            bgcolor="white",
            font_size=12,
            font_family="sans-serif"
        )
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)

def create_power_gauge(current_value: float, max_value: float) -> None:
    """
    Create a gauge chart for power output visualization
    
    Args:
        current_value (float): Current power output
        max_value (float): Maximum power capacity
    """
    # Calculate percentage
    percentage = (current_value / max_value) * 100 if max_value > 0 else 0
    
    # Determine color based on percentage
    if percentage >= 70:
        gauge_color = COLOR_PALETTE["primary"]
    elif percentage >= 40:
        gauge_color = COLOR_PALETTE["success"]
    else:
        gauge_color = COLOR_PALETTE["warning"]
    
    # Create the gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current_value,
        number={"suffix": " kW", "font": {"size": 24, "color": COLOR_PALETTE["text"]}},
        domain={"x": [0, 1], "y": [0, 1]},
        title={
            "text": "Potência Atual", 
            "font": {"size": 18, "color": COLOR_PALETTE["text"]}
        },
        delta={
            "reference": max_value, 
            "relative": True, 
            "valueformat": ".1%",
            "font": {"size": 14}
        },
        gauge={
            "axis": {
                "range": [None, max_value], 
                "tickwidth": 1, 
                "tickcolor": COLOR_PALETTE["grid"],
                "tickfont": {"size": 12, "color": COLOR_PALETTE["text"]}
            },
            "bar": {"color": gauge_color},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": COLOR_PALETTE["grid"],
            "steps": [
                {"range": [0, max_value * 0.3], "color": "rgba(255, 193, 7, 0.2)"},  # Amarelo claro
                {"range": [max_value * 0.3, max_value * 0.7], "color": "rgba(76, 175, 80, 0.2)"},  # Verde claro
                {"range": [max_value * 0.7, max_value], "color": "rgba(25, 118, 210, 0.2)"}  # Azul claro
            ],
            "threshold": {
                "line": {"color": COLOR_PALETTE["secondary"], "width": 4},
                "thickness": 0.75,
                "value": max_value * 0.95
            }
        }
    ))
    
    # Add a subtle grid background and improve overall appearance
    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=50, b=10),
        paper_bgcolor='rgba(255, 255, 255, 0)',
        font=dict(family="Arial, sans-serif"),
        shapes=[
            # Add an outer circle for better aesthetics
            dict(
                type="circle",
                xref="paper", yref="paper",
                x0=0.05, y0=0.05, x1=0.95, y1=0.95,
                line=dict(color="rgba(240, 240, 240, 0.5)", width=1)
            )
        ]
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
