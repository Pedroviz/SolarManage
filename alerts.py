import datetime
import random
import time
from typing import List, Dict, Any, Optional, Tuple
from models import AlertLevel

# In a real system, this would connect to a database or alerting service

# Store alerts in memory for demo purposes
_ACTIVE_ALERTS = [
    {
        "id": "alert-001",
        "plant_id": "plant-001",
        "level": AlertLevel.WARNING.value,
        "title": "Inverter 2 Efficiency Drop",
        "message": "Inverter 2 is showing 5% lower efficiency than expected. Consider inspection.",
        "timestamp": (datetime.datetime.now() - datetime.timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S"),
        "acknowledged": False
    },
    {
        "id": "alert-002",
        "plant_id": "plant-002",
        "level": AlertLevel.CRITICAL.value,
        "title": "Communication Lost",
        "message": "Communication with monitoring system temporarily lost. Check connection.",
        "timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=45)).strftime("%Y-%m-%d %H:%M:%S"),
        "acknowledged": False
    },
    {
        "id": "alert-003",
        "plant_id": "plant-003",
        "level": AlertLevel.WARNING.value,
        "title": "Panel Group 3 Output Low",
        "message": "Panel group 3 is producing 15% below expected output. Possible shading or dust issue.",
        "timestamp": (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"),
        "acknowledged": False
    },
    {
        "id": "alert-004",
        "plant_id": "plant-003",
        "level": AlertLevel.INFORMATION.value,
        "title": "Maintenance Scheduled",
        "message": "Routine maintenance scheduled for next week. No action required.",
        "timestamp": (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S"),
        "acknowledged": False
    }
]

_ALERT_HISTORY = [
    {
        "id": "hist-001",
        "plant_id": "plant-001",
        "level": AlertLevel.WARNING.value,
        "title": "Grid Connection Instability",
        "message": "Grid connection showing fluctuations. Issue resolved automatically.",
        "timestamp": (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),
        "resolved_at": (datetime.datetime.now() - datetime.timedelta(days=2, hours=-1)).strftime("%Y-%m-%d %H:%M:%S"),
        "resolution": "Self-resolved"
    },
    {
        "id": "hist-002",
        "plant_id": "plant-002",
        "level": AlertLevel.CRITICAL.value,
        "title": "Inverter 1 Failure",
        "message": "Inverter 1 failed and required restart.",
        "timestamp": (datetime.datetime.now() - datetime.timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"),
        "resolved_at": (datetime.datetime.now() - datetime.timedelta(days=4)).strftime("%Y-%m-%d %H:%M:%S"),
        "resolution": "Manually restarted"
    },
    {
        "id": "hist-003",
        "plant_id": "plant-003",
        "level": AlertLevel.INFORMATION.value,
        "title": "System Update",
        "message": "Monitoring system updated to latest version.",
        "timestamp": (datetime.datetime.now() - datetime.timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S"),
        "resolved_at": (datetime.datetime.now() - datetime.timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S"),
        "resolution": "Update completed"
    }
]

def get_active_alerts(
    plant_id: Optional[str] = None, 
    alert_level: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get active alerts, optionally filtered by plant and level
    
    Args:
        plant_id (Optional[str]): Optional plant ID to filter
        alert_level (Optional[str]): Optional alert level to filter
        
    Returns:
        List[Dict[str, Any]]: List of active alerts
    """
    # Filter alerts by plant ID if provided
    filtered_alerts = _ACTIVE_ALERTS
    
    if plant_id:
        filtered_alerts = [a for a in filtered_alerts if a["plant_id"] == plant_id]
    
    # Filter alerts by level if provided
    if alert_level:
        filtered_alerts = [a for a in filtered_alerts if a["level"] == alert_level]
    
    # Sort by timestamp (newest first)
    return sorted(filtered_alerts, key=lambda x: x["timestamp"], reverse=True)

def get_alert_history(
    plant_id: Optional[str] = None, 
    days: int = 30,
    alert_level: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get historical alerts, optionally filtered by plant and level
    
    Args:
        plant_id (Optional[str]): Optional plant ID to filter
        days (int): Number of days to include in history (default 30)
        alert_level (Optional[str]): Optional alert level to filter
        
    Returns:
        List[Dict[str, Any]]: List of historical alerts
    """
    # Filter alerts by plant ID if provided
    filtered_alerts = _ALERT_HISTORY
    
    if plant_id:
        filtered_alerts = [a for a in filtered_alerts if a["plant_id"] == plant_id]
    
    # Filter alerts by level if provided
    if alert_level:
        filtered_alerts = [a for a in filtered_alerts if a["level"] == alert_level]
    
    # Filter by date range
    cutoff_date = (datetime.datetime.now() - datetime.timedelta(days=days))
    filtered_alerts = [
        a for a in filtered_alerts 
        if datetime.datetime.strptime(a["timestamp"], "%Y-%m-%d %H:%M:%S") > cutoff_date
    ]
    
    # Sort by timestamp (newest first)
    return sorted(filtered_alerts, key=lambda x: x["timestamp"], reverse=True)

def acknowledge_alert(alert_id: str) -> bool:
    """
    Acknowledge an active alert
    
    Args:
        alert_id (str): ID of the alert to acknowledge
        
    Returns:
        bool: True if successful, False otherwise
    """
    for alert in _ACTIVE_ALERTS:
        if alert["id"] == alert_id:
            alert["acknowledged"] = True
            
            # Move to history after some time (would be handled by a background process in real implementation)
            # For demo, we'll remove it from active alerts
            _ACTIVE_ALERTS.remove(alert)
            
            # Add to history
            _ALERT_HISTORY.append({
                "id": f"hist-{alert_id}",
                "plant_id": alert["plant_id"],
                "level": alert["level"],
                "title": alert["title"],
                "message": alert["message"],
                "timestamp": alert["timestamp"],
                "resolved_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "resolution": "Acknowledged"
            })
            
            return True
    
    return False

def create_alert(
    plant_id: str, 
    level: str, 
    title: str, 
    message: str
) -> Dict[str, Any]:
    """
    Create a new alert
    
    Args:
        plant_id (str): ID of the plant
        level (str): Alert level (see AlertLevel enum)
        title (str): Alert title
        message (str): Alert message
        
    Returns:
        Dict[str, Any]: The created alert
    """
    # Generate a unique ID
    alert_id = f"alert-{int(time.time())}"
    
    # Create the alert
    alert = {
        "id": alert_id,
        "plant_id": plant_id,
        "level": level,
        "title": title,
        "message": message,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "acknowledged": False
    }
    
    # Add to active alerts
    _ACTIVE_ALERTS.append(alert)
    
    return alert
