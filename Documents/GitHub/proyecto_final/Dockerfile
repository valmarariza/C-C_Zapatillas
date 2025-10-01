FROM python:3.13-alpine

# Variables de entorno para evitar problemas de buffering y pyc
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar dependencias de Python
RUN apk add --no-cache build-base mariadb-connector-c-dev

# Copiar requirements.txt e instalar dependencias
COPY requirements.txt .
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto (Gunicorn lo usará)
EXPOSE 5000

# Comando de arranque (Gunicorn para producción)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--forwarded-allow-ips=*", "run:app"]
