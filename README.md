# Sincronizador de Catálogo de Productos
Sistema de sincronización de catálogo de productos que permite la actualización de productos y  relaciones con portales de venta en una base de datos PostgresSQL. El proyecto permite procesar y validar datos desde archivos CSV y mantener la sincronización en dos fuentes de datos: catálogo de productos y portales donde estos estan publicados.

## Funcionalidad general
Esta aplicación ha sido diseñada en python y permite:
- **Sincronizar productos**: a partir de archivos CSV con datos actualizados a una base de datos:
    - `--catalog`: Actualiza los productos del catálogo del cliente
    - `--portal`: Sincroniza los productos del portal
- **Gestionar relaciones**: entre productos y portales de venta (N:N)
- **Validar datos**: a tráves de Pydantic para mantener la integridad de la información
- **Logs**: sobre todas las operaciones de la aplicación y separados en aplicación y operaciones sobre la base de datos

## Arquitectura
La aplicación sigue una arquitectura basada en capas:
- **Capa de datos (bd)**: Modelos SQLAlchemy y gestión de la base de datos
- **Capa de servicios**: Lógica principal para el procesamiento de los productos
- **Capa de repositorios**: Acceso y manipulación de la base de datos
- **Capa de esquemas**: Validación de datos usando Pydantic
- **Configuración**: Centralización de la configuración

## Dependencias principales
- **SQLAlchemy 2.0.44**: ORM para gestión de base de datos
- **Pydantic 2.12.4**: Validación de datos
- **psycopg2 2.9.11**: Adaptador de PostgreSQL
- **python-dotenv 1.2.1**: Gestión de variables de entorno
- **pydantic-settings 2.12.0**: Configuración basada en Pydantic

## Instalación y configuración

### Requisitos previos

- **Python 3.10+**
- **Docker y Docker Compose**
- **PostgreSQL 17**

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd product-catalog-sync
```

### 2. Crear entorno virtual
```bash
python -m venv venv

# En linux/macOS
source venv/bin/activate

# En Windows
venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Copia el archivo de ejemplo y modifica las variables con tus datos:
```bash
cp .env.example .env
```
Edita el archivo `.env` con tus datos:

```env
DB_NAME=product_catalog
DB_USER=admin
DB_PASSWORD=admin
DB_PORT=5432
DB_HOST=localhost
```

### 5. Iniciar la base de datos con Docker
```bash
docker-compose up -d
```
Esto iniciará un contenedor de PostgreSQL 17 con:
- Base de datos configurada según el archivo `.env`
- A través del puerto 5432
- Con persistencia de datos a través de volúmenes Docker

Para verificar que el contenedor está funcionando:
```bash
docker ps
```

Para ver los logs de la base de datos:
```bash
docker logs catalog_db
```

Para detener la base de datos:
```bash
docker-compose down
```

### 6. Crear tablas
Antes de poder hacer nada se **deben** crear las tablas:
```bash
python -m src.main --initdb
```

### 7. Datos de entrada
El sistema espera archivos CSV en el directorio `data/`. Crea el directorio si no existe:

```bash
mkdir -p data
```

El formato esperado es el siguiente (feed_items.csv y portal_items.csv):
```csv
product_id,title,price,store_id
1,Producto Ejemplo,29.99,1|2|3
2,Otro Producto,15.50,1
```

Donde:
- `product_id`: ID único del producto (entero)
- `store_id`: IDs de tiendas separados por `|` (ejemplo: `1|2|3`)
- `title`: Nombre del producto
- `price`: Precio del producto

## Ejecución

### Inicializar la base de datos
El programa crea y inicializa las tablas automáticamente.

### Modo catálogo

Actualiza el catálogo de productos desde `data/feed_items.csv` o una ruta específicada.

Ruta por defecto (`data/feed_items.csv`)
```bash
python -m src.main --catalog
```

Ruta personalizada:
```bash
python -m src.main --catalog --file data/custom_file.csv
```

Este modo:
- Lee productos del archivo CSV
- Crea o actualiza productos existentes
- **Mantiene** productos no presentes en el CSV
- Gestiona las relaciones producto-tienda

### Modo portal

Sincroniza productos desde `data/portal_items.csv`:

Ruta por defecto (`data/feed_items.csv`)
```bash
python -m src.main --portal
```

Ruta personalizada:
```bash
python -m src.main --portal --file data/custom_file.csv
```

Este modo:
- Lee productos del archivo CSV
- Crea o actualiza productos existentes
- **Elimina** productos que no están en el CSV
- Sincroniza completamente el portal con el archivo


### Verificación de logs
Los logs se almacenan en el directorio `/logs`. Están divididos en dos archivos:
- **app.log**: registra todo lo que ocurre relacionado directamente con la aplicación
- **db.log**: registra todas las operaciones realizadas sobre la base de datos incluido COMMITS y ROLLBACKS

## Estructura del código
```
product-catalog-sync/
│
├── src/
│   ├── api/                    # API (TODO)
│   ├── config/                
│   │   ├── app_config.py      # Configuración principal
│   │   └── logging.conf       # Configuración de logging
│   │
│   ├── db/                     # Capa de base de datos
│   │   ├── models/            
│   │   │   ├── product.py        # Modelo Product
│   │   │   ├── store.py          # Modelo Store
│   │   │   └── product_store.py  # Tabla de relación many-to-many
│   │   ├── base.py           
│   │   ├── database.py       # Configuración y gestión de sesiones
│   │   └── healthcheck.py    # Verificación de conexión a DB
│   │
│   ├── repositories/          # Capa de acceso a datos
│   │   ├── product_repository.py       # CRUD de productos
│   │   ├── store_repository.py         # CRUD de tiendas
│   │   └── product_store_repository.py # CRUD de relaciones
│   │
│   ├── schemas/               # Esquemas de validación
│   │   └── product_input.py   # Schema para datos de entrada
│   │
│   ├── services/              # Lógica principal
│   │   ├── csv_reader.py      # Lectura y validación de CSV
│   │   ├── product_service.py # Procesamiento de productos
│   │   ├── update_catalog.py  # Servicio de actualización de catálogo
│   │   └── update_portal.py   # Servicio de actualización de portal
│   │
│   ├── utils/                 # Utilidades
│   │   ├── logging.py          # Configuración de logging
│   │   └── logging_handlers.py # Handlers personalizados
│   │
│   └── main.py               # Punto de entrada de la aplicación
│
├── data/                      # Archivos CSV de entrada
│   ├── feed_items.csv        # Datos del catálogo
│   └── portal_items.csv      # Datos del portal
│
├── docker-compose.yaml       # Configuración de Docker para PostgreSQL
├── requirements.txt          # Dependencias de Python
├── .env.example             # Ejemplo de variables de entorno
└── README.md                # Esta documentación
```

## Modelo de datos
El sistema utiliza tres tablas principales

### 1. Products
- `product_id` (PK): Identificador único del producto
- `title`: Título del producto
- `price`: Precio del producto

### 2. Stores
- `store_id` (PK): Identificador único de la tienda

### 3. Product_Store (N:N)
- `product_id` (FK, PK): Referencia a Products
- `store_id` (FK, PK): Referencia a Stores

## Ejemplos de uso

### Ejemplo 1: Actualización del catálogo
```bash
# 1. Asegúrate que la base de datos está funcionando
docker-compose up -d

# 2. Verifica tu archivo CSV
cat data/feed_items.csv
# o
cat data/custom_file.csv

# 3. Ejecuta la actualización del catálogo
python -m src.main --catalog    # ruta por defecto
# o
python -m src.main --catalog --file data/custom_file.csv
```

### Ejemplo 2: Sincronización del portal
```bash
#1. Verifica tu archivo CSV
cat data/portal_items.csv
# o
cat data/custom_file.csv

# 2. Ejecuta la actualización del catálogo
python -m src.main --portal    # ruta por defecto
# o
python -m src.main --portal --file data/custom_file.csv
```
