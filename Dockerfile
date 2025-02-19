# Usando Python 3.11 para evitar problemas de compatibilidade
FROM python:3.11-slim  

# Definindo o diretório de trabalho
WORKDIR /app  

# Instalando dependências do PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev

# Copiando os arquivos do projeto
COPY . .

# Instalando as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt  

# Expondo a porta usada pelo Django
EXPOSE 8000  

# Comando para rodar o servidor Django usando Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mycash.wsgi:application"]

