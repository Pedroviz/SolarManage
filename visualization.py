import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Dict, Any, Union, Tuple

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
        name="Actual Production",
        marker_color='#2ca02c'
    ))
    
    # Add projected production with different color
    fig.add_trace(go.Bar(
        x=hours[current_hour:],
        y=values[current_hour:],
        name="Projected Production",
        marker_color='rgba(44, 160, 44, 0.5)'  # Same color but transparent
    ))
    
    # Update layout
    fig.update_layout(
        xaxis_title="Hour",
        yaxis_title="Energy (kWh)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=40, t=40, b=40),
        height=400
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
        name="Efficiency",
        line=dict(color='#1f77b4', width=2),
        mode='lines+markers'
    ))
    
    # Add horizontal reference line at 95% - good performance
    fig.add_shape(
        type="line",
        x0=dates[0],
        y0=95,
        x1=dates[-1],
        y1=95,
        line=dict(
            color="green",
            width=1,
            dash="dash",
        )
    )
    
    # Add annotation for reference line
    fig.add_annotation(
        x=dates[0],
        y=95,
        text="Good Performance (95%)",
        showarrow=False,
        yshift=10,
        font=dict(size=10, color="green")
    )
    
    # Update layout
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Efficiency (%)",
        yaxis=dict(range=[85, 100]),  # Set y-axis range to focus on relevant values
        margin=dict(l=40, r=40, t=40, b=40),
        height=400
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
    cols = st.columns(4)
    
    # Current production
    with cols[0]:
        current_production = plant_data['current_production']
        st.metric(
            "Current Production", 
            f"{current_production} kW",
            f"{round((current_production / plant_details['capacity']) * 100, 1)}% of capacity"
        )
    
    # Daily energy
    with cols[1]:
        daily_production = plant_data['daily_production']
        daily_target = plant_details['daily_target']
        daily_percentage = (daily_production / daily_target) * 100 if daily_target > 0 else 0
        st.metric(
            "Today's Energy", 
            f"{daily_production} kWh", 
            f"{round(daily_percentage, 1)}% of target"
        )
    
    # Efficiency
    with cols[2]:
        efficiency = plant_data['efficiency']
        efficiency_delta = efficiency - plant_data['efficiency_yesterday']
        st.metric(
            "Current Efficiency", 
            f"{efficiency}%", 
            f"{round(efficiency_delta, 1)}% from yesterday"
        )
    
    # Performance ratio
    with cols[3]:
        performance_ratio = plant_data['performance_ratio']
        performance_delta = performance_ratio - plant_data['performance_ratio_yesterday']
        st.metric(
            "Performance Ratio", 
            f"{performance_ratio}%", 
            f"{round(performance_delta, 1)}% from yesterday"
        )

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
        name="Actual",
        line=dict(color='#2ca02c', width=2),
        mode='lines+markers'
    ))
    
    # Add target values line
    fig.add_trace(go.Scatter(
        x=dates,
        y=target_values,
        name="Target",
        line=dict(color='#d62728', width=2, dash='dash'),
        mode='lines'
    ))
    
    # Calculate achievement percentage
    achievement = [100 * a / t if t > 0 else 0 for a, t in zip(actual_values, target_values)]
    
    # Add achievement percentage line on secondary y-axis
    fig.add_trace(go.Scatter(
        x=dates,
        y=achievement,
        name="Achievement %",
        line=dict(color='#1f77b4', width=1.5),
        mode='lines',
        yaxis="y2"
    ))
    
    # Update layout with secondary y-axis
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title=y_label,
        yaxis2=dict(
            title="Achievement %",
            titlefont=dict(color='#1f77b4'),
            tickfont=dict(color='#1f77b4'),
            anchor="x",
            overlaying="y",
            side="right",
            range=[0, 120]
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=40, r=40, t=40, b=40),
        height=400
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
    
    # Create the gauge chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=current_value,
        number={"suffix": " kW"},
        domain={"x": [0, 1], "y": [0, 1]},
        title={"text": "Power Output"},
        delta={"reference": max_value, "relative": True, "valueformat": ".1%"},
        gauge={
            "axis": {"range": [None, max_value], "tickwidth": 1, "tickcolor": "darkblue"},
            "bar": {"color": "#19d3f3" if percentage >= 70 else "#2ca02c"},
            "bgcolor": "white",
            "borderwidth": 2,
            "bordercolor": "gray",
            "steps": [
                {"range": [0, max_value * 0.3], "color": "#ffec81"},
                {"range": [max_value * 0.3, max_value * 0.7], "color": "#a4e175"},
                {"range": [max_value * 0.7, max_value], "color": "#19d3f3"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": max_value * 0.95
            }
        }
    ))
    
    # Update layout
    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=50, b=10)
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True)
