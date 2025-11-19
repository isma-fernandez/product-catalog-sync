PYTHON := python3
VENV := venv
ENV_FILE := .env
ENV_EXAMPLE := .env.example

install:
	@echo "Creando entorno virtual..."
	$(PYTHON) -m venv $(VENV)

	@echo "Instalando dependencias..."
	. $(VENV)/bin/activate && pip install -r requirements.txt

	@echo "Configurando variables de entorno..."
	@if [ ! -f "$(ENV_FILE)" ]; then \
		cp $(ENV_EXAMPLE) $(ENV_FILE); \
		echo "Archivo .env creado desde .env.example"; \
		echo ""; \
		echo "Credenciales por defecto:"; \
		sed 's/^/  /' $(ENV_EXAMPLE); \
		echo ""; \
		echo "Por favor, revisa y actualiza las variables de entorno en el archivo .env según sea necesario."; \
	else \
		echo "Archivo .env ya existe"; \
	fi

	@echo "Iniciando PostgreSQL y FastAPI con Docker..."
	docker-compose up -d

	@echo "Creando tablas en la base de datos..."
	. $(VENV)/bin/activate && python -m src.main --initdb

	@echo "Creando directorio de datos si no existe..."
	mkdir -p data
	@echo "Creando directorio de logs si no existe..."
	mkdir -p logs

	@echo "Instalación completa."
	@echo ""
	@echo "Puedes empezar ejecutando:"
	@echo "  python -m src.main --portal"
	@echo "  python -m src.main --catalog"
	@echo "  opcional: --file <ruta_del_archivo>"
	@echo ""
	@echo "O accediendo al endpoint a través de:"
	@echo "  localhost:8000/api/products"
