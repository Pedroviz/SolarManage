import datetime
import random
from typing import Dict, Any, Optional

def format_energy_value(value: float, unit: str = "kWh") -> str:
    """
    Format energy values with appropriate units
    
    Args:
        value (float): The energy value
        unit (str): Base unit (kWh by default)
        
    Returns:
        str: Formatted string with appropriate units
    """
    if unit == "kWh":
        if value >= 1000000:
            return f"{value/1000000:.2f} GWh"
        elif value >= 1000:
            return f"{value/1000:.2f} MWh"
        else:
            return f"{value:.2f} kWh"
    elif unit == "kW":
        if value >= 1000:
            return f"{value/1000:.2f} MW"
        else:
            return f"{value:.2f} kW"
    else:
        return f"{value:.2f} {unit}"

def calculate_efficiency(actual: float, theoretical: float) -> float:
    """
    Calculate efficiency percentage
    
    Args:
        actual (float): Actual energy production
        theoretical (float): Theoretical maximum energy production
        
    Returns:
        float: Efficiency percentage
    """
    if theoretical > 0:
        efficiency = (actual / theoretical) * 100
        return round(efficiency, 1)
    return 0.0

def get_weather_data(location: str) -> Dict[str, Any]:
    """
    Get weather data for a location
    In a real implementation, this would call a weather API
    
    Args:
        location (str): Location string
        
    Returns:
        Dict[str, Any]: Weather data
    """
    # Simulate weather data
    current_hour = datetime.datetime.now().hour
    current_month = datetime.datetime.now().month
    
    # Temperature varies by time of day and month
    base_temp = 15 + (10 if 4 <= current_month <= 9 else 0)  # Higher base in summer
    time_factor = 0 if current_hour < 6 or current_hour > 19 else ((current_hour - 6) / 13 * 10)
    temperature = round(base_temp + time_factor + random.uniform(-3, 3), 1)
    
    # Generate irradiance based on time of day
    if 6 <= current_hour < 19:  # Day time
        hour_factor = 1.0 - abs(current_hour - 12.5) / 8.0
        base_irradiance = 1000 * hour_factor  # Peak around noon
        
        # Weather condition affects irradiance
        weather_rand = random.random()
        
        if weather_rand < 0.6:  # 60% chance of clear
            condition = "Clear"
            irradiance_factor = random.uniform(0.9, 1.0)
        elif weather_rand < 0.8:  # 20% chance of partly cloudy
            condition = "Partly Cloudy"
            irradiance_factor = random.uniform(0.6, 0.8)
        else:  # 20% chance of cloudy
            condition = "Cloudy"
            irradiance_factor = random.uniform(0.2, 0.5)
            
        irradiance = round(base_irradiance * irradiance_factor)
    else:  # Night time
        irradiance = 0
        condition = "Night" if random.random() < 0.8 else "Cloudy Night"
    
    return {
        "temperature": temperature,
        "condition": condition,
        "irradiance": irradiance,
        "humidity": random.randint(30, 80),
        "wind_speed": round(random.uniform(0, 25), 1)
    }
