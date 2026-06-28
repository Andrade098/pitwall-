git clone https://github.com/Andrade098/pitwall-.git ///////
cd pitwall-

# Entrar na pasta do backend
cd backend

# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual (Windows Git Bash)
source .venv/Scripts/activate

# Instalar as dependências
pip install -r requirements.txt

# Iniciar o servidor
uvicorn app.main:app --reload

# Voltar para a pasta raiz do projeto
cd ~/OneDrive/Pictures/f1-projeto/pitwall  # ou onde você clonou

# Iniciar o Live Server para servir o HTML
npx live-server

# Em outro terminal, na raiz do projeto
npx live-server
# ou
python -m http.server 8080

http://127.0.0.1:8080/test_ws.html
