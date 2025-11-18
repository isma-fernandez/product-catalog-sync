#!/bin/bash
# Script para ejecutar los tests del proyecto

# Configurar variables de entorno para tests
export DB_NAME=test_db
export DB_USER=test_user
export DB_PASSWORD=test_password
export DB_PORT=5432
export DB_HOST=localhost

# Ejecutar pytest
python -m pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
