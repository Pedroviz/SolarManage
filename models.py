from enum import Enum

class PlantStatus(Enum):
    """Enum for solar plant status values"""
    OPERATIONAL = "Operational"
    PARTIAL = "Partially Operational"
    MAINTENANCE = "Under Maintenance"
    OFFLINE = "Offline"

class AlertLevel(Enum):
    """Enum for alert levels"""
    CRITICAL = "Critical"
    WARNING = "Warning"
    INFORMATION = "Information"

class MaintenanceStatus(Enum):
    """Enum for maintenance status values"""
    SCHEDULED = "Scheduled"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class ComponentStatus(Enum):
    """Enum for component status values"""
    NORMAL = "Normal"
    WARNING = "Warning"
    CRITICAL = "Critical"
