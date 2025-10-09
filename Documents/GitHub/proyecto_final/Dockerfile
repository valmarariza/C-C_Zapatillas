# Imagen base ligera con Python
FROM python:3.13-alpine

# Evitar archivos pyc y asegurar logs en consola
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar extensiones de Python
RUN apk add --no-cache build-base libffi-dev openssl-dev

# Copiar e instalar dependencias del proyecto
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt

# Copiar todo el código de la app
COPY . .

# Exponer el puerto de la aplicación
EXPOSE 5000

# Comando de inicio con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--forwarded-allow-ips=*", "run:app"]
