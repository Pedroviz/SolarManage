import datetime
import os
import json
from typing import List, Dict, Any, Optional, Union
from models import (
    SolarPanel, PanelType, DirtLevel, MaintenanceRecord, PanelProblem,
    MaintenanceType, ProblemType, ProblemSeverity
)

# Dados de exemplo para painéis solares
# Em um sistema real, isso viria de um banco de dados ou API
SAMPLE_PANELS = [
    {
        "id": "P001",
        "tipo": PanelType.MONOCRYSTALLINE,
        "fabricante": "SunPower",
        "modelo": "Maxeon 3",
        "data_instalacao": "2022-05-10",
        "potencia_nominal": 400.0,
        "eficiencia_atual": 20.1,
        "eficiencia_inicial": 22.0,
        "producao_atual": 1.8,
        "producao_esperada": 2.0,
        "temperatura_operacao": 48.5,
        "irradiacao_media": 5.7,
        "temperatura_ambiente": 28.0,
        "umidade": 65.0,
        "nivel_sujeira": DirtLevel.LIGHT,
        "historico_manutencao": [
            MaintenanceRecord(
                data="2023-01-15",
                tipo=MaintenanceType.CLEANING,
                observacao="Limpeza de rotina",
                tecnico="Carlos Silva",
                custo=120.0
            ),
            MaintenanceRecord(
                data="2023-07-22",
                tipo=MaintenanceType.INSPECTION,
                observacao="Inspeção semestral",
                tecnico="Maria Oliveira",
                custo=80.0
            )
        ],
        "problemas_detectados": [
            PanelProblem(
                tipo=ProblemType.HOTSPOT,
                gravidade=ProblemSeverity.LOW,
                data="2023-05-02",
                descricao="Pequeno ponto quente detectado no canto superior direito"
            )
        ]
    },
    {
        "id": "P002",
        "tipo": PanelType.POLYCRYSTALLINE,
        "fabricante": "Canadian Solar",
        "modelo": "CS6K-300MS",
        "data_instalacao": "2021-08-18",
        "potencia_nominal": 300.0,
        "eficiencia_atual": 15.2,
        "eficiencia_inicial": 17.8,
        "producao_atual": 1.2,
        "producao_esperada": 1.5,
        "temperatura_operacao": 52.0,
        "irradiacao_media": 5.7,
        "temperatura_ambiente": 28.0,
        "umidade": 65.0,
        "nivel_sujeira": DirtLevel.MODERATE,
        "historico_manutencao": [
            MaintenanceRecord(
                data="2022-02-10",
                tipo=MaintenanceType.CLEANING,
                observacao="Limpeza após tempestade de poeira",
                tecnico="Pedro Costa",
                custo=150.0
            ),
            MaintenanceRecord(
                data="2023-02-15",
                tipo=MaintenanceType.REPAIR,
                observacao="Reparo de conectores danificados",
                tecnico="João Almeida",
                custo=220.0
            )
        ],
        "problemas_detectados": [
            PanelProblem(
                tipo=ProblemType.CORROSION,
                gravidade=ProblemSeverity.MEDIUM,
                data="2023-01-30",
                descricao="Corrosão nas bordas do painel"
            ),
            PanelProblem(
                tipo=ProblemType.JUNCTION_BOX,
                gravidade=ProblemSeverity.LOW,
                data="2023-02-15",
                descricao="Pequenas rachaduras na caixa de junção"
            )
        ]
    },
    {
        "id": "P003",
        "tipo": PanelType.BIFACIAL,
        "fabricante": "Longi Solar",
        "modelo": "LR4-60HPB-365M",
        "data_instalacao": "2023-01-05",
        "potencia_nominal": 365.0,
        "eficiencia_atual": 20.5,
        "eficiencia_inicial": 21.0,
        "producao_atual": 1.9,
        "producao_esperada": 2.0,
        "temperatura_operacao": 45.0,
        "irradiacao_media": 5.7,
        "temperatura_ambiente": 28.0,
        "umidade": 65.0,
        "nivel_sujeira": DirtLevel.NONE,
        "historico_manutencao": [
            MaintenanceRecord(
                data="2023-06-20",
                tipo=MaintenanceType.INSPECTION,
                observacao="Inspeção de rotina",
                tecnico="Ana Santos",
                custo=80.0
            )
        ],
        "problemas_detectados": []
    },
    {
        "id": "P004",
        "tipo": PanelType.THIN_FILM,
        "fabricante": "First Solar",
        "modelo": "Series 6",
        "data_instalacao": "2020-11-22",
        "potencia_nominal": 420.0,
        "eficiencia_atual": 16.2,
        "eficiencia_inicial": 18.0,
        "producao_atual": 1.6,
        "producao_esperada": 1.9,
        "temperatura_operacao": 50.0,
        "irradiacao_media": 5.7,
        "temperatura_ambiente": 28.0,
        "umidade": 65.0,
        "nivel_sujeira": DirtLevel.HEAVY,
        "historico_manutencao": [
            MaintenanceRecord(
                data="2021-05-10",
                tipo=MaintenanceType.CLEANING,
                observacao="Limpeza de poeira acumulada",
                tecnico="Roberto Lima",
                custo=180.0
            ),
            MaintenanceRecord(
                data="2022-05-15",
                tipo=MaintenanceType.CLEANING,
                observacao="Limpeza anual",
                tecnico="Roberto Lima",
                custo=180.0
            ),
            MaintenanceRecord(
                data="2023-04-02",
                tipo=MaintenanceType.REPAIR,
                observacao="Reparo de selante deteriorado",
                tecnico="Carlos Silva",
                custo=250.0
            )
        ],
        "problemas_detectados": [
            PanelProblem(
                tipo=ProblemType.DELAMINATION,
                gravidade=ProblemSeverity.MEDIUM,
                data="2023-03-28",
                descricao="Delaminação detectada na borda inferior"
            ),
            PanelProblem(
                tipo=ProblemType.DISCOLORATION,
                gravidade=ProblemSeverity.MEDIUM,
                data="2023-03-28",
                descricao="Descoloração em aproximadamente 10% da área"
            )
        ]
    },
    {
        "id": "P005",
        "tipo": PanelType.PERC,
        "fabricante": "JinkoSolar",
        "modelo": "Eagle 66TR G4",
        "data_instalacao": "2021-03-15",
        "potencia_nominal": 380.0,
        "eficiencia_atual": 17.8,
        "eficiencia_inicial": 19.5,
        "producao_atual": 1.7,
        "producao_esperada": 1.85,
        "temperatura_operacao": 49.0,
        "irradiacao_media": 5.7,
        "temperatura_ambiente": 28.0,
        "umidade": 65.0,
        "nivel_sujeira": DirtLevel.MODERATE,
        "historico_manutencao": [
            MaintenanceRecord(
                data="2022-01-20",
                tipo=MaintenanceType.CLEANING,
                observacao="Limpeza de rotina",
                tecnico="Maria Oliveira",
                custo=120.0
            ),
            MaintenanceRecord(
                data="2022-07-12",
                tipo=MaintenanceType.INSPECTION,
                observacao="Inspeção semestral",
                tecnico="Pedro Costa",
                custo=80.0
            ),
            MaintenanceRecord(
                data="2023-01-18",
                tipo=MaintenanceType.CLEANING,
                observacao="Limpeza de rotina",
                tecnico="Maria Oliveira",
                custo=120.0
            )
        ],
        "problemas_detectados": [
            PanelProblem(
                tipo=ProblemType.PID,
                gravidade=ProblemSeverity.LOW,
                data="2022-12-05",
                descricao="Sinais iniciais de PID detectados"
            ),
            PanelProblem(
                tipo=ProblemType.SNAIL_TRAIL,
                gravidade=ProblemSeverity.LOW,
                data="2023-01-18",
                descricao="Pequenas trilhas de caracol visíveis na inspeção"
            )
        ]
    }
]

def get_panel_by_id(panel_id: str) -> Optional[Dict[str, Any]]:
    """
    Recupera dados de um painel solar específico
    
    Args:
        panel_id (str): ID do painel solar
        
    Returns:
        Optional[Dict[str, Any]]: Dados do painel ou None se não encontrado
    """
    for panel in SAMPLE_PANELS:
        if panel["id"] == panel_id:
            if isinstance(panel, SolarPanel):
                return panel.to_dict()
            else:
                # Converter objetos embutidos para dicionários
                panel_dict = panel.copy()
                
                # Converter enumerações para seus valores
                if isinstance(panel_dict["tipo"], PanelType):
                    panel_dict["tipo"] = panel_dict["tipo"].value
                
                if isinstance(panel_dict["nivel_sujeira"], DirtLevel):
                    panel_dict["nivel_sujeira"] = panel_dict["nivel_sujeira"].value
                
                # Converter listas de registros
                panel_dict["historico_manutencao"] = [
                    m.to_dict() if hasattr(m, "to_dict") else m 
                    for m in panel_dict["historico_manutencao"]
                ]
                
                panel_dict["problemas_detectados"] = [
                    p.to_dict() if hasattr(p, "to_dict") else p 
                    for p in panel_dict["problemas_detectados"]
                ]
                
                return panel_dict
    return None

def get_all_panels() -> List[Dict[str, Any]]:
    """
    Recupera a lista de todos os painéis solares
    
    Returns:
        List[Dict[str, Any]]: Lista de painéis solares
    """
    # Converter objetos para dicionários
    panels = []
    for panel in SAMPLE_PANELS:
        if isinstance(panel, SolarPanel):
            panels.append(panel.to_dict())
        else:
            # Converter objetos embutidos para dicionários
            panel_dict = panel.copy()
            
            # Converter enumerações para seus valores
            if isinstance(panel_dict["tipo"], PanelType):
                panel_dict["tipo"] = panel_dict["tipo"].value
            
            if isinstance(panel_dict["nivel_sujeira"], DirtLevel):
                panel_dict["nivel_sujeira"] = panel_dict["nivel_sujeira"].value
            
            # Converter listas de registros
            panel_dict["historico_manutencao"] = [
                m.to_dict() if hasattr(m, "to_dict") else m 
                for m in panel_dict["historico_manutencao"]
            ]
            
            panel_dict["problemas_detectados"] = [
                p.to_dict() if hasattr(p, "to_dict") else p 
                for p in panel_dict["problemas_detectados"]
            ]
            
            panels.append(panel_dict)
    
    return panels

def add_maintenance_record(panel_id: str, maintenance_record: MaintenanceRecord) -> bool:
    """
    Adiciona um registro de manutenção a um painel
    
    Args:
        panel_id (str): ID do painel
        maintenance_record (MaintenanceRecord): Registro de manutenção
        
    Returns:
        bool: True se adicionado com sucesso, False caso contrário
    """
    for panel in SAMPLE_PANELS:
        if panel["id"] == panel_id:
            panel["historico_manutencao"].append(maintenance_record)
            return True
    return False

def add_problem_record(panel_id: str, problem: PanelProblem) -> bool:
    """
    Adiciona um registro de problema a um painel
    
    Args:
        panel_id (str): ID do painel
        problem (PanelProblem): Problema detectado
        
    Returns:
        bool: True se adicionado com sucesso, False caso contrário
    """
    for panel in SAMPLE_PANELS:
        if panel["id"] == panel_id:
            panel["problemas_detectados"].append(problem)
            return True
    return False

def update_panel_data(panel_id: str, data_updates: Dict[str, Any]) -> bool:
    """
    Atualiza dados de um painel específico
    
    Args:
        panel_id (str): ID do painel
        data_updates (Dict[str, Any]): Atualizações a serem aplicadas
        
    Returns:
        bool: True se atualizado com sucesso, False caso contrário
    """
    for panel in SAMPLE_PANELS:
        if panel["id"] == panel_id:
            for key, value in data_updates.items():
                if key in panel:
                    panel[key] = value
            return True
    return False