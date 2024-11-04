# Usa una imagen base de Python ligera
FROM python:latest

# Establece el directorio de trabajo
WORKDIR /app

# Copia las dependencias e instálalas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código y el script
COPY . .

# Da permisos de ejecución al script
RUN chmod +x /app/script.sh

# Crear un usuario sin privilegios para mayor seguridad
RUN useradd -m apiuser
USER apiuser

# Expone el puerto de la API
EXPOSE 5000

# Ejecuta la API
CMD ["python", "app.py"]
