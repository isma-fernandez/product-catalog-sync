"# product-catalog-sync

Sistema de sincronización de catálogo de productos desde archivos CSV a base de datos.

## Instalación

### Dependencias principales
```bash
pip install -r requirements.txt
```

### Dependencias de desarrollo (para tests)
```bash
pip install -r requirements-dev.txt
```

## Tests

Este proyecto incluye una suite completa de tests unitarios que cubren:
- Validación de schemas (ProductInput)
- Repositorios (product, store, product_store)
- Servicios (csv_reader, product_service)

### Ejecutar todos los tests

#### Opción 1: Usando el script incluido
```bash
./run_tests.sh
```

#### Opción 2: Directamente con pytest
```bash
export DB_NAME=test_db
export DB_USER=test_user
export DB_PASSWORD=test_password
export DB_PORT=5432
export DB_HOST=localhost

python -m pytest tests/ -v
```

### Ejecutar tests con cobertura
```bash
./run_tests.sh
```

El reporte de cobertura se genera en formato HTML en el directorio `htmlcov/`.

### Ejecutar tests específicos

Por marcador (unit/integration):
```bash
python -m pytest tests/ -m unit -v
```

Por archivo:
```bash
python -m pytest tests/test_product_input.py -v
```

Por clase o función:
```bash
python -m pytest tests/test_product_input.py::TestProductInput::test_valid_product_single_store -v
```

## Estructura del proyecto

```
src/
├── config/          # Configuración de la aplicación
├── db/              # Modelos de base de datos
│   └── models/
├── repositories/    # Capa de acceso a datos
├── schemas/         # Schemas de validación (Pydantic)
├── services/        # Lógica de negocio
└── utils/           # Utilidades

tests/
├── conftest.py               # Fixtures compartidos
├── test_product_input.py     # Tests del schema ProductInput
├── test_product_repository.py
├── test_store_repository.py
├── test_product_store_repository.py
├── test_csv_reader.py        # Tests del lector CSV
└── test_product_service.py   # Tests del servicio de productos
```" 
