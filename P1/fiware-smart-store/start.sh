#!/bin/bash

# 1. Matar procesos de Flask previos en el puerto 5005 (Cura el error "Address already in use")
echo "Cleaning up port 5005..."
lsof -ti:5005 | xargs kill -9 2>/dev/null || echo "Port 5005 is already clear."

# 2. Requisito Ticket #8: Tirar abajo contenedores antes de levantarlos 
echo "Stopping and removing existing containers..."
docker-compose down

# 3. Levantar infraestructura en segundo plano
echo "Starting Orion Context Broker and MongoDB..."
docker-compose up -d

# 4. Esperar a que Orion esté listo antes de que Flask intente conectar [cite: 43]
echo "Waiting for Orion Context Broker to initialize..."
sleep 5

# 5. Opcional: Sembrar datos de prueba si el script existe
if [ -f "./seed_orion.py" ]; then
    echo "Initializing Orion Context Broker with test data..."
    python3 ./seed_orion.py
fi

# 6. Activar entorno virtual si existe (No se incluirá en el ZIP según .gitignore )
if [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# 7. Ejecutar la aplicación Flask
echo "Starting Flask Application..."
# Asegúrate de que en app.py el puerto coincida (5005)
python app.py