# Entrar na pasta do backend
cd backend

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# No Windows (Git Bash):
source .venv/Scripts/activate
# No Windows (PowerShell):
.venv\Scripts\Activate.ps1
# No Mac/Linux:
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Iniciar o servidor
uvicorn app.main:app --reload


resumo
cd backend
python -m venv .venv
source .venv/Scripts/activate  # Windows Git Bash
pip install -r requirements.txt
uvicorn app.main:app --reload
