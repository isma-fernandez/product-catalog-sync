# Tests Documentation

Esta carpeta contiene la suite completa de tests para el proyecto product-catalog-sync.

## Estructura de Tests

### tests/conftest.py
Contiene las fixtures compartidas por todos los tests:
- `setup_test_environment`: Configura variables de entorno necesarias
- `db_session`: Proporciona una sesión de base de datos SQLite en memoria para tests
- `sample_product_data`: Datos de ejemplo para productos
- `sample_csv_row`: Fila de ejemplo de CSV

### Tests por Módulo

#### test_product_input.py (15 tests)
Tests para el schema de validación ProductInput:
- Validación de productos con una o múltiples tiendas
- Validación de IDs negativos (debe fallar)
- Validación de títulos vacíos (debe fallar)
- Validación de precios cero o negativos (debe fallar)
- Validación de formato de store_id
- Representación en string

#### test_product_repository.py (7 tests)
Tests para operaciones CRUD de productos:
- Crear producto
- Obtener producto existente y no existente
- Actualizar producto
- Eliminar producto
- Obtener todos los productos

#### test_store_repository.py (5 tests)
Tests para operaciones de tiendas:
- Crear tienda
- Obtener tienda existente y no existente
- get_or_create con tienda nueva y existente

#### test_product_store_repository.py (8 tests)
Tests para relaciones producto-tienda:
- Añadir relación producto-tienda
- Obtener tiendas de un producto
- Obtener relación específica
- Eliminar relación por objeto y por IDs

#### test_csv_reader.py (6 tests)
Tests para lectura de archivos CSV:
- Leer CSV válido
- Manejar filas inválidas (deben ser omitidas)
- Manejar archivo vacío
- Manejar archivo no encontrado
- Validar precios inválidos
- Validar títulos vacíos

#### test_product_service.py (8 tests)
Tests para lógica de negocio:
- Procesar producto nuevo
- Procesar producto existente sin cambios
- Procesar producto existente con cambios
- Sincronizar tiendas (añadir y eliminar)
- Detectar cambios en productos

## Cobertura de Código

Cobertura actual: **51%**

Áreas con alta cobertura:
- Schemas: 100%
- Repositorios: 100%
- Services (product_service): 100%
- Models: 100%

Áreas con baja cobertura:
- database.py: 0% (funciones de conexión a DB no testeadas)
- healthcheck.py: 0% (verificación de DB no testeada)
- main.py: 0% (punto de entrada no testeado)
- update_catalog.py y update_portal.py: 0% (flujos completos no testeados)

## Ejecutar Tests

### Todos los tests
```bash
./run_tests.sh
```

### Tests específicos por marcador
```bash
# Solo tests unitarios
pytest tests/ -m unit -v

# Solo tests de integración (si existieran)
pytest tests/ -m integration -v
```

### Tests específicos por archivo
```bash
pytest tests/test_product_input.py -v
```

### Test específico
```bash
pytest tests/test_product_input.py::TestProductInput::test_valid_product_single_store -v
```

## Añadir Nuevos Tests

1. Crear archivo `test_<modulo>.py` en la carpeta tests/
2. Importar pytest y el módulo a testear
3. Crear clase `Test<NombreModulo>` con marcador `@pytest.mark.unit` o `@pytest.mark.integration`
4. Escribir funciones de test con nombres descriptivos `test_<descripcion>`
5. Usar fixtures disponibles en conftest.py cuando sea necesario
6. Ejecutar tests para verificar que pasan

## Fixtures Disponibles

### db_session
Sesión de base de datos SQLite en memoria. Se limpia automáticamente después de cada test.

```python
def test_example(db_session):
    # Usar db_session para operaciones de DB
    product = create_product(db_session, ...)
```

### sample_product_data
Diccionario con datos de ejemplo para un producto.

```python
def test_example(sample_product_data):
    product = ProductInput(**sample_product_data)
```

### tmp_path (fixture de pytest)
Directorio temporal para crear archivos en tests.

```python
def test_example(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("content")
```

## Buenas Prácticas

1. **Nombres descriptivos**: Los nombres de tests deben describir claramente qué se está probando
2. **Arrange-Act-Assert**: Organizar tests en tres secciones claras
3. **Tests independientes**: Cada test debe ser independiente y no depender de otros
4. **Usar fixtures**: Reutilizar fixtures para setup común
5. **Tests atómicos**: Cada test debe probar una sola cosa
6. **Documentación**: Agregar docstrings explicando qué se prueba

## Mejoras Futuras

Áreas que podrían beneficiarse de más tests:
- Tests de integración para flujos completos (update_catalog, update_portal)
- Tests para manejo de errores de conexión a base de datos
- Tests de rendimiento para grandes volúmenes de datos
- Tests para el healthcheck
- Mocks de loggers para verificar mensajes de log
