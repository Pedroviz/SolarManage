import os
import sys
import anthropic
from anthropic import Anthropic
from typing import Dict, List, Any, Optional

#the newest Anthropic model is "claude-3-5-sonnet-20241022" which was released October 22, 2024

class SolarPanelHealthChatbot:
    """
    Chatbot para análise de saúde de painéis solares usando IA
    """
    
    def __init__(self):
        """
        Inicializa o chatbot
        """
        # Inicializa o cliente Anthropic
        anthropic_key = os.environ.get('ANTHROPIC_API_KEY')
        if not anthropic_key:
            raise ValueError("ANTHROPIC_API_KEY não encontrada nas variáveis de ambiente")
            
        self.client = Anthropic(api_key=anthropic_key)
        self.model = "claude-3-5-sonnet-20241022"
        
        # Sistema de contexto para fornecer conhecimento especializado ao modelo
        self.system_prompt = """
        Você é um assistente especialista em painéis solares e sistemas fotovoltaicos.
        
        Seu papel é analisar dados de desempenho de painéis solares e fornecer:
        1. Diagnósticos de possíveis problemas
        2. Recomendações para otimização
        3. Previsões de quando a manutenção será necessária
        4. Estimativas de vida útil restante dos painéis
        
        Conhecimento específico que você possui:
        - Degradação normal de painéis solares (0.5-1% ao ano)
        - Problemas comuns: pontos quentes, microfissuras, PID (degradação induzida por potencial)
        - Efeitos da sujeira e condições climáticas no desempenho
        - Padrões de deterioração em diferentes tipos de painéis (monocristalino, policristalino, filme fino)
        - Métricas ideais de desempenho em diferentes condições
        
        Ao responder a perguntas, forneça:
        - Análises baseadas em evidências dos dados apresentados
        - Explicações claras e concisas
        - Recomendações práticas e acionáveis
        - Estimativas de confiança em suas previsões
        
        Responda sempre em português, a menos que solicitado em outro idioma.
        """
        
        # Histórico de conversas para contexto
        self.conversation_history = []
        
    def analyze_panel_health(self, panel_data: Dict[str, Any]) -> str:
        """
        Analisa os dados de saúde de um painel solar e retorna insights
        
        Args:
            panel_data: Dicionário contendo dados do painel solar
            
        Returns:
            str: Análise detalhada da saúde do painel
        """
        # Formata os dados do painel para o prompt
        prompt = self._format_panel_data(panel_data)
        
        # Adiciona instruções específicas
        prompt += """
        Com base nos dados acima:
        1. Qual é o estado atual de saúde deste painel solar?
        2. Existem sinais de degradação anormal ou problemas emergentes?
        3. Quando provavelmente será necessária a próxima manutenção?
        4. Quais ações específicas podem melhorar o desempenho?
        5. Qual é a estimativa de vida útil restante?
        """
        
        # Adiciona ao histórico de conversas
        self.conversation_history.append({"role": "user", "content": prompt})
        
        # Chama a API do Anthropic
        response = self.client.messages.create(
            model=self.model,
            system=self.system_prompt,
            messages=self.conversation_history,
            max_tokens=1024
        )
        
        # Adiciona a resposta ao histórico
        self.conversation_history.append({"role": "assistant", "content": response.content[0].text})
        
        # Retorna a resposta
        return response.content[0].text
    
    def ask_question(self, question: str, panel_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Permite ao usuário fazer perguntas sobre painéis solares
        
        Args:
            question: Pergunta do usuário
            panel_data: Dados opcionais do painel para contexto
            
        Returns:
            str: Resposta do chatbot
        """
        prompt = question
        
        # Se houver dados do painel, adiciona ao prompt
        if panel_data:
            prompt = self._format_panel_data(panel_data) + "\n\n" + question
        
        # Adiciona ao histórico de conversas
        self.conversation_history.append({"role": "user", "content": prompt})
        
        # Chama a API do Anthropic
        response = self.client.messages.create(
            model=self.model,
            system=self.system_prompt,
            messages=self.conversation_history,
            max_tokens=1024
        )
        
        # Adiciona a resposta ao histórico
        self.conversation_history.append({"role": "assistant", "content": response.content[0].text})
        
        # Retorna a resposta
        return response.content[0].text
    
    def _format_panel_data(self, panel_data: Dict[str, Any]) -> str:
        """
        Formata os dados do painel para o prompt
        
        Args:
            panel_data: Dicionário contendo dados do painel solar
            
        Returns:
            str: Dados formatados para o prompt
        """
        formatted_data = "DADOS DO PAINEL SOLAR:\n\n"
        
        # Informações básicas
        if 'id' in panel_data:
            formatted_data += f"ID: {panel_data.get('id')}\n"
        if 'tipo' in panel_data:
            formatted_data += f"Tipo: {panel_data.get('tipo')}\n"
        if 'fabricante' in panel_data:
            formatted_data += f"Fabricante: {panel_data.get('fabricante')}\n"
        if 'modelo' in panel_data:
            formatted_data += f"Modelo: {panel_data.get('modelo')}\n"
        if 'data_instalacao' in panel_data:
            formatted_data += f"Data de Instalação: {panel_data.get('data_instalacao')}\n"
        if 'potencia_nominal' in panel_data:
            formatted_data += f"Potência Nominal: {panel_data.get('potencia_nominal')} W\n"
        
        # Métricas de desempenho
        formatted_data += "\nMÉTRICAS DE DESEMPENHO:\n"
        if 'eficiencia_atual' in panel_data:
            formatted_data += f"Eficiência Atual: {panel_data.get('eficiencia_atual')}%\n"
        if 'eficiencia_inicial' in panel_data:
            formatted_data += f"Eficiência Inicial: {panel_data.get('eficiencia_inicial')}%\n"
        if 'producao_atual' in panel_data:
            formatted_data += f"Produção Atual: {panel_data.get('producao_atual')} kWh\n"
        if 'producao_esperada' in panel_data:
            formatted_data += f"Produção Esperada: {panel_data.get('producao_esperada')} kWh\n"
        if 'temperatura_operacao' in panel_data:
            formatted_data += f"Temperatura de Operação: {panel_data.get('temperatura_operacao')}°C\n"
        
        # Histórico de manutenção
        if 'historico_manutencao' in panel_data and panel_data['historico_manutencao']:
            formatted_data += "\nHISTÓRICO DE MANUTENÇÃO:\n"
            for manutencao in panel_data['historico_manutencao']:
                formatted_data += f"- Data: {manutencao.get('data')}, Tipo: {manutencao.get('tipo')}, Observação: {manutencao.get('observacao')}\n"
        
        # Problemas detectados
        if 'problemas_detectados' in panel_data and panel_data['problemas_detectados']:
            formatted_data += "\nPROBLEMAS DETECTADOS:\n"
            for problema in panel_data['problemas_detectados']:
                formatted_data += f"- Tipo: {problema.get('tipo')}, Gravidade: {problema.get('gravidade')}, Data: {problema.get('data')}\n"
        
        # Condições ambientais
        formatted_data += "\nCONDIÇÕES AMBIENTAIS:\n"
        if 'irradiacao_media' in panel_data:
            formatted_data += f"Irradiação Média: {panel_data.get('irradiacao_media')} kWh/m²\n"
        if 'temperatura_ambiente' in panel_data:
            formatted_data += f"Temperatura Ambiente: {panel_data.get('temperatura_ambiente')}°C\n"
        if 'umidade' in panel_data:
            formatted_data += f"Umidade: {panel_data.get('umidade')}%\n"
        if 'nivel_sujeira' in panel_data:
            formatted_data += f"Nível de Sujeira: {panel_data.get('nivel_sujeira')}\n"
        
        return formatted_data
    
    def clear_conversation_history(self):
        """
        Limpa o histórico de conversas
        """
        self.conversation_history = []

# Função para criar uma instância do chatbot
def get_chatbot():
    """
    Retorna uma instância do chatbot
    
    Returns:
        SolarPanelHealthChatbot: Instância do chatbot
    """
    return SolarPanelHealthChatbot()