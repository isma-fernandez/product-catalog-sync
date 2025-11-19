# Dockerfile para la aplicación FastAPI
FROM python:3.11-slim

WORKDIR /app

# Necesario para psycopg2
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Requisitos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto al contenedor
# No es lo ideal, pero no tengo tiempo para hacer un COPY selectivo
COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
