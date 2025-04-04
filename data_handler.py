import pandas as pd
import numpy as np
import datetime
import random
from typing import List, Dict, Any, Tuple, Optional
from models import PlantStatus, AlertLevel

# This module handles all data operations for the solar plant monitoring system
# In a real implementation, this would connect to APIs, databases, or IoT devices

# Simulated plant data - in a real implementation, this would come from a database or API
SAMPLE_PLANTS = [
    {
        "id": "plant-001",
        "name": "SolarField Alpha",
        "location": "Phoenix, AZ",
        "capacity": 500,  # kW
        "panels_count": 1500,
        "installation_date": "2019-06-15",
        "status": PlantStatus.OPERATIONAL.value,
        "daily_target": 2500,  # kWh
        "maintenance_schedule": [
            {"task": "Panel Cleaning", "date": "2023-11-15", "status": "Scheduled"},
            {"task": "Inverter Inspection", "date": "2023-12-01", "status": "Scheduled"},
        ]
    },
    {
        "id": "plant-002",
        "name": "SunPower Beta",
        "location": "Las Vegas, NV",
        "capacity": 750,  # kW
        "panels_count": 2250,
        "installation_date": "2020-03-20",
        "status": PlantStatus.OPERATIONAL.value,
        "daily_target": 3750,  # kWh
        "maintenance_schedule": [
            {"task": "Wiring Check", "date": "2023-11-10", "status": "Completed"},
            {"task": "Annual Maintenance", "date": "2023-12-15", "status": "Scheduled"},
        ]
    },
    {
        "id": "plant-003",
        "name": "EcoSolar Gamma",
        "location": "San Diego, CA",
        "capacity": 300,  # kW
        "panels_count": 900,
        "installation_date": "2021-01-10",
        "status": PlantStatus.PARTIAL.value,
        "daily_target": 1500,  # kWh
        "maintenance_schedule": [
            {"task": "Inverter Replacement", "date": "2023-11-05", "status": "In Progress"},
            {"task": "Site Inspection", "date": "2023-11-25", "status": "Scheduled"},
        ]
    }
]

def get_plants() -> List[Dict[str, Any]]:
    """
    Retrieve the list of all solar plants
    
    Returns:
        List[Dict[str, Any]]: List of solar plants with basic information
    """
    # In a real implementation, this would fetch from a database or API
    return SAMPLE_PLANTS

def get_plant_details(plant_id: str) -> Dict[str, Any]:
    """
    Get detailed information about a specific plant
    
    Args:
        plant_id (str): The ID of the plant
        
    Returns:
        Dict[str, Any]: Detailed plant information
    """
    # Find the plant in our sample data
    plant = next((p for p in SAMPLE_PLANTS if p["id"] == plant_id), None)
    
    if not plant:
        return {
            "name": "Unknown Plant",
            "location": "Unknown",
            "capacity": 0,
            "panels_count": 0,
            "installation_date": "Unknown",
            "status": PlantStatus.OFFLINE.value,
            "daily_target": 0,
            "maintenance_schedule": []
        }
    
    return plant

def get_plant_data(plant_id: str) -> Dict[str, Any]:
    """
    Get current performance data for a specific plant
    
    Args:
        plant_id (str): The ID of the plant
        
    Returns:
        Dict[str, Any]: Current plant performance data
    """
    # Get the plant details
    plant = get_plant_details(plant_id)
    capacity = plant["capacity"]
    
    # Generate realistic data based on time of day
    current_hour = datetime.datetime.now().hour
    
    # Simulating solar production curve - peak around noon, zero at night
    if 6 <= current_hour < 19:  # Daylight hours (6 AM to 7 PM)
        # Create a bell curve with peak around noon
        hour_factor = 1.0 - abs(current_hour - 12.5) / 8.0
        # Add some randomness (weather effects, cloud cover, etc.)
        variability = random.uniform(0.8, 1.2)
        # Calculate current production as a percentage of capacity
        production_percentage = max(0, hour_factor * variability)
    else:
        # Night time - no production
        production_percentage = 0
    
    # Calculate the current production from the percentage and capacity
    current_production = round(production_percentage * capacity, 1)
    
    # Generate hourly production data for today
    now = datetime.datetime.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    
    hours = []
    hourly_values = []
    
    for hour in range(24):
        hour_time = start_of_day + datetime.timedelta(hours=hour)
        hours.append(hour_time.strftime("%H:%M"))
        
        if hour <= now.hour:
            # For past hours today, generate data
            if 6 <= hour < 19:
                # Daylight hours - generate production data
                hour_factor = 1.0 - abs(hour - 12.5) / 8.0
                random_factor = random.uniform(0.8, 1.2)
                hourly_value = max(0, hour_factor * random_factor * capacity * 0.9)  # 90% factor to account for inefficiencies
            else:
                # Night time - no production
                hourly_value = 0
            
            hourly_values.append(round(hourly_value, 1))
        else:
            # For future hours, use projected values
            if 6 <= hour < 19:
                # Daylight hours - generate projected data
                hour_factor = 1.0 - abs(hour - 12.5) / 8.0
                projected_value = hour_factor * capacity * 0.85  # 85% factor for conservative projection
            else:
                # Night time - no production
                projected_value = 0
                
            hourly_values.append(round(projected_value, 1))
    
    # Calculate daily production (sum of hourly values)
    daily_production = sum(hourly_values[:now.hour + 1])
    
    # Generate efficiency and performance data
    # Efficiency is affected by temperature, dust, etc.
    # Higher temperature reduces efficiency
    hour_temp = 20 + 10 * (1.0 - abs(current_hour - 14) / 8.0)  # Peak temperature around 2 PM
    base_efficiency = 96.0  # Base efficiency percentage
    temp_effect = max(0, (hour_temp - 25) * 0.4)  # Efficiency drop with higher temperatures
    current_efficiency = round(base_efficiency - temp_effect, 1)
    
    # Yesterday's efficiency for comparison
    efficiency_yesterday = round(base_efficiency - random.uniform(0, 6), 1)
    
    # Performance ratio (PR) - ratio of actual to theoretically possible energy output
    performance_ratio = round(current_efficiency * random.uniform(0.94, 0.99), 1)
    performance_ratio_yesterday = round(performance_ratio - random.uniform(-1.5, 1.5), 1)
    
    # Peak and average power for today
    peak_power = round(max(hourly_values), 1)
    valid_values = [v for v in hourly_values[:now.hour + 1] if v > 0]
    average_power = round(sum(valid_values) / len(valid_values), 1) if valid_values else 0
    
    # Inverter status
    num_inverters = max(1, capacity // 100)  # Approximate 1 inverter per 100 kW
    inverter_status = []
    
    for i in range(num_inverters):
        # Small random chance of inverter being offline
        if random.random() < 0.05 and plant["status"] == PlantStatus.PARTIAL.value:
            inverter_status.append("Offline")
        else:
            inverter_status.append("Online")
    
    # Component status
    components_status = [
        {"component": "PV Panels", "status": "Normal", "last_check": (now - datetime.timedelta(days=3)).strftime("%Y-%m-%d")},
        {"component": "Inverters", "status": "Normal" if all(s == "Online" for s in inverter_status) else "Warning", 
         "last_check": (now - datetime.timedelta(days=2)).strftime("%Y-%m-%d")},
        {"component": "Mounting System", "status": "Normal", "last_check": (now - datetime.timedelta(days=10)).strftime("%Y-%m-%d")},
        {"component": "AC Subsystem", "status": "Normal", "last_check": (now - datetime.timedelta(days=5)).strftime("%Y-%m-%d")},
        {"component": "Communications", "status": "Normal", "last_check": now.strftime("%Y-%m-%d")},
    ]
    
    # If the plant is in PARTIAL status, add an issue to a component
    if plant["status"] == PlantStatus.PARTIAL.value:
        # Add a warning to one of the components
        components_status[1]["status"] = "Warning"  # Inverter warning
    
    # Return the complete data structure
    return {
        "current_production": current_production,
        "daily_production": round(daily_production, 1),
        "efficiency": current_efficiency,
        "efficiency_yesterday": efficiency_yesterday,
        "performance_ratio": performance_ratio,
        "performance_ratio_yesterday": performance_ratio_yesterday,
        "hourly_production": {
            "hours": hours,
            "values": hourly_values
        },
        "peak_power": peak_power,
        "average_power": average_power,
        "inverter_status": inverter_status,
        "components_status": components_status
    }

def get_historical_data(
    plant_id: str, 
    start_date: datetime.datetime, 
    end_date: datetime.datetime
) -> Dict[str, Any]:
    """
    Get historical performance data for a specific plant
    
    Args:
        plant_id (str): The ID of the plant
        start_date (datetime.datetime): Start date for historical data
        end_date (datetime.datetime): End date for historical data
        
    Returns:
        Dict[str, Any]: Historical plant performance data
    """
    # Get the plant details
    plant = get_plant_details(plant_id)
    capacity = plant["capacity"]
    daily_target = plant["daily_target"]
    
    # Calculate the number of days in the range
    delta = end_date - start_date
    num_days = delta.days + 1
    
    # Generate date list
    dates = [(start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d") 
             for i in range(num_days)]
    
    # Generate daily production data
    daily_production = []
    daily_target_values = []
    efficiency_values = []
    
    for i in range(num_days):
        current_date = start_date + datetime.timedelta(days=i)
        # Production depends on season, cloudiness, etc.
        
        # Determine season factor (summer produces more)
        month = current_date.month
        if 5 <= month <= 8:  # Summer
            season_factor = random.uniform(0.85, 0.95)
        elif month in [4, 9]:  # Spring/Fall
            season_factor = random.uniform(0.7, 0.85)
        else:  # Winter
            season_factor = random.uniform(0.5, 0.7)
        
        # Weekend effect (slight reduction in performance due to less maintenance)
        weekday = current_date.weekday()
        weekend_factor = 0.98 if weekday >= 5 else 1.0
        
        # Random variation (weather, etc.)
        random_factor = random.uniform(0.85, 1.15)
        
        # Calculate actual production
        daily_prod = round(daily_target * season_factor * weekend_factor * random_factor, 1)
        daily_production.append(daily_prod)
        
        # Target is constant based on plant specifications
        daily_target_values.append(daily_target)
        
        # Efficiency is affected by temperature, dust, etc.
        # Base efficiency is higher in cooler months
        base_efficiency = 96.0 if month in [11, 12, 1, 2] else 94.0
        daily_efficiency = round(base_efficiency * random.uniform(0.95, 1.02), 1)
        efficiency_values.append(daily_efficiency)
    
    return {
        "dates": dates,
        "daily_production": daily_production,
        "daily_target": daily_target_values,
        "efficiency": efficiency_values
    }
