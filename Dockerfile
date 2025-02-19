FROM python:3.11-slim  

WORKDIR /app  

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev

COPY . .  

RUN pip install --no-cache-dir -r requirements.txt  

**WORKDIR /app/MyCash**  # Ajuste conforme o nome do seu projeto Django

EXPOSE 8000  

# Comando para rodar o servidor Django usando Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "MyCash.wsgi:application"]

