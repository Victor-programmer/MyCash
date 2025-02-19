# Usar uma imagem leve do Python 3.11
FROM python:3.11-slim  

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app  

# Instalar dependências do PostgreSQL para psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev  

# Copiar os arquivos do projeto para o contêiner
COPY . .  

# Instalar as dependências do Django
RUN pip install --no-cache-dir -r requirements.txt  

# Expor a porta do Django (8000)
EXPOSE 8000  

# Comando para rodar o servidor Django com Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "MyCash.wsgi:application"]
