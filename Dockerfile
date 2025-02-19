# Usar uma imagem do Python 3.11 Slim para um ambiente leve e otimizado
FROM python:3.11-slim  

# Definir o diretório de trabalho dentro do contêiner
WORKDIR /app  

# Instalar dependências do PostgreSQL necessárias para o psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev

# Copiar os arquivos do projeto para o contêiner
COPY . .

# Instalar as dependências do projeto Django
RUN pip install --no-cache-dir -r requirements.txt  

# Expor a porta que o Django usará (8000)
EXPOSE 8000  

# Comando para rodar o servidor Django usando Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "MyCash.wsgi:application"]

