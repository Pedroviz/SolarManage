# 🌞 SolarManage - Painel de Monitoramento de Usinas Solares

Aplicação para monitoramento em tempo real de usinas solares com visualização de dados e assistente de IA integrado.

## 🚀 Começando

### Pré-requisitos

- Git ([instalação](https://git-scm.com/))
- Python 3.8+ ([instalação](https://www.python.org/downloads/))
- Conta em [Anthropic](https://console.anthropic.com/) ou [OpenAI](https://platform.openai.com/) (para o assistente de IA)

### 📥 Instalação

1. **Clonar o repositório**:

   ```bash
   git clone https://github.com/Pedroviz/SolarManage.git
   cd SolarManage

   ```

2. **Configurar ambiente virtual**:

   ```bash

   ```

# Windows

python -m venv .venv
.venv\Scripts\activate

# Linux/macOS

python -m venv .venv
source .venv/bin/activate

3.  **Instalar dependências**:

        ```bash

    pip install -r requirements.txt

4.  **Configurar variáveis de ambiente**:

Crie um arquivo .env na raiz do projeto:

    ```ini

# Chave da API (Anthropic ou OpenAI)

ANTHROPIC_API_KEY=sua_chave_aqui

# OU

OPENAI_API_KEY=sua_chave_aqui

# Configurações do servidor

PORT=8501

**▶️Execução**
```bash

streamlit run app.py --server.address=localhost --server.port=8501
O aplicativo estará disponível em:
👉 http://localhost:8501

🛠 Estrutura do Projeto

SolarManage/
├── .venv/ # Ambiente virtual
├── assets/ # Arquivos estáticos (imagens, etc)
├── app.py # Aplicação principal
├── data_handler.py # Lógica de manipulação de dados
├── visualization.py # Visualizações e gráficos
├── ai_chatbot.py # Integração com IA
├── .env # Variáveis de ambiente
└── requirements.txt # Dependências

🔧 Troubleshooting

    Erros comuns
    1. Porta em uso:
        # Linux/macOS
        lsof -i :8501
        kill -9 <PID>

        # Windows
        netstat -ano | findstr :8501
        taskkill /PID <PID> /F

    2. Problemas com dependências:

        bash
        Copy
        pip install --upgrade -r requirements.txt

    3. Erros no assistente de IA:

        Verifique se a chave API está correta no .env

        Confira os limites de uso da API

🤝 Como Contribuir
Faça um fork do projeto

Crie uma branch (git checkout -b feature/nova-feature)

Commit suas mudanças (git commit -m 'Adiciona nova feature')

Push para a branch (git push origin feature/nova-feature)

Abra um Pull Request
