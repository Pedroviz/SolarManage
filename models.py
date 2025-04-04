from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime, date

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

class PanelType(Enum):
    """Enum for solar panel types"""
    MONOCRYSTALLINE = "Monocristalino"
    POLYCRYSTALLINE = "Policristalino"
    THIN_FILM = "Filme Fino"
    BIFACIAL = "Bifacial"
    PERC = "PERC"

class ProblemSeverity(Enum):
    """Enum for problem severity levels"""
    LOW = "Baixa"
    MEDIUM = "Média"
    HIGH = "Alta"
    CRITICAL = "Crítica"

class DirtLevel(Enum):
    """Enum for dirt/soiling levels"""
    NONE = "Nenhum"
    LIGHT = "Leve"
    MODERATE = "Moderado"
    HEAVY = "Pesado"
    SEVERE = "Severo"

class MaintenanceType(Enum):
    """Enum for maintenance types"""
    CLEANING = "Limpeza"
    INSPECTION = "Inspeção"
    REPAIR = "Reparo"
    REPLACEMENT = "Substituição"
    ADJUSTMENT = "Ajuste"

class ProblemType(Enum):
    """Enum for common solar panel problems"""
    HOTSPOT = "Ponto Quente"
    MICROFRACTURE = "Microfissura"
    PID = "Degradação Induzida por Potencial"
    DELAMINATION = "Delaminação"
    CORROSION = "Corrosão"
    DISCOLORATION = "Descoloração"
    SNAIL_TRAIL = "Trilha de Caracol"
    JUNCTION_BOX = "Falha na Caixa de Junção"
    BYPASS_DIODE = "Falha no Diodo de Bypass"
    CELL_INTERCONNECTION = "Falha na Interconexão de Células"

@dataclass
class MaintenanceRecord:
    """Class for maintenance record data"""
    data: str
    tipo: MaintenanceType
    observacao: str
    tecnico: Optional[str] = None
    custo: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "data": self.data,
            "tipo": self.tipo.value if isinstance(self.tipo, MaintenanceType) else self.tipo,
            "observacao": self.observacao,
            "tecnico": self.tecnico,
            "custo": self.custo
        }

@dataclass
class PanelProblem:
    """Class for solar panel problem data"""
    tipo: ProblemType
    gravidade: ProblemSeverity
    data: str
    descricao: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "tipo": self.tipo.value if isinstance(self.tipo, ProblemType) else self.tipo,
            "gravidade": self.gravidade.value if isinstance(self.gravidade, ProblemSeverity) else self.gravidade,
            "data": self.data,
            "descricao": self.descricao
        }

@dataclass
class SolarPanel:
    """Class for solar panel data"""
    id: str
    tipo: PanelType
    fabricante: str
    modelo: str
    data_instalacao: str
    potencia_nominal: float
    eficiencia_atual: float
    eficiencia_inicial: float
    producao_atual: float
    producao_esperada: float
    temperatura_operacao: float
    irradiacao_media: float
    temperatura_ambiente: float
    umidade: float
    nivel_sujeira: DirtLevel
    historico_manutencao: List[MaintenanceRecord]
    problemas_detectados: List[PanelProblem]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for AI analysis"""
        return {
            "id": self.id,
            "tipo": self.tipo.value if isinstance(self.tipo, PanelType) else self.tipo,
            "fabricante": self.fabricante,
            "modelo": self.modelo,
            "data_instalacao": self.data_instalacao,
            "potencia_nominal": self.potencia_nominal,
            "eficiencia_atual": self.eficiencia_atual,
            "eficiencia_inicial": self.eficiencia_inicial,
            "producao_atual": self.producao_atual,
            "producao_esperada": self.producao_esperada,
            "temperatura_operacao": self.temperatura_operacao,
            "irradiacao_media": self.irradiacao_media,
            "temperatura_ambiente": self.temperatura_ambiente,
            "umidade": self.umidade,
            "nivel_sujeira": self.nivel_sujeira.value if isinstance(self.nivel_sujeira, DirtLevel) else self.nivel_sujeira,
            "historico_manutencao": [m.to_dict() for m in self.historico_manutencao],
            "problemas_detectados": [p.to_dict() for p in self.problemas_detectados]
        }
