# Sincronizador de Catálogo de Productos
Sistema de sincronización de catálogo de productos que permite la actualización de productos y relaciones con portales de venta en una base de datos PostgreSQL.  
Además, incluye una API REST construida con FastAPI que permite consultar los productos y sus tiendas asociadas.

## Funcionalidad general
Esta aplicación ha sido diseñada en python y permite:
- **Sincronizar productos**: a partir de archivos CSV con datos actualizados a una base de datos:
    - `--catalog`: Actualiza los productos del catálogo del cliente
    - `--portal`: Sincroniza los productos del portal
- **Gestionar relaciones**: entre productos y portales de venta (N:N)
- **FastAPI** para consultar el catálogo de productos y las tiendas asociadas
- **Validar datos**: a tráves de Pydantic para mantener la integridad de la información
- **Logs**: sobre todas las operaciones de la aplicación y separados en aplicación y operaciones sobre la base de datos

## Arquitectura
La aplicación sigue una arquitectura basada en capas:
- **Capa de API**: Endpoints de lectura sobre FastAPI
- **Capa de datos (bd)**: Modelos SQLAlchemy y gestión de la base de datos
- **Capa de servicios**: Lógica principal para el procesamiento de los productos
- **Capa de repositorios**: Acceso y manipulación de la base de datos
- **Capa de esquemas**: Validación de datos usando Pydantic
- **Configuración**: Centralización de la configuración

## Instalación y configuración

### Requisitos previos

- **Python 3.10+**
- **Docker y Docker Compose**
- **Make** (Opcional para la instalación rápida)

### Instalación manual

#### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd product-catalog-sync
```

#### 2. Crear entorno virtual
```bash
python -m venv venv

# En linux/macOS
source venv/bin/activate

# En Windows
venv\Scripts\activate
```

#### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

#### 4. Configurar variables de entorno
Copia los archivos de ejemplo y modifica las variables con tus datos:
```bash
cp .env.example .env
cp docker.env.example .docker.env
```
Edita el archivo `.env` con tus datos:

```env
DB_NAME=product_catalog
DB_USER=admin
DB_PASSWORD=admin
DB_PORT=5432
DB_HOST=localhost
API_PORT=8000
```

Edita el archivo `docker.env` con tus datos:
```docker.env
DB_NAME=product_catalog
DB_USER=admin
DB_PASSWORD=admin
DB_PORT=5432
DB_HOST=db
API_PORT=8000
```
**NOTA**: Para que funcione el contenedor de FastAPI **DB_HOST** debe ser igual al nombre del servicio en `docker-compose.yaml`

#### 5. Iniciar la base de datos y FastAPI con Docker
```bash
docker-compose up -d
```
Esto iniciará un contenedor de PostgreSQL 17 con:
- Base de datos configurada según el archivo `.env`
- A través del puerto 5432
- Con persistencia de datos a través de volúmenes Docker

Y además un contenedor de FastAPI, que:
- Levanta la API en `http://localhost:8000`
- Se conecta directamente al contenedor de PostgreSQL
- Proporciona un endpoint para obtener todos los productos

Para verificar que el contenedor está funcionando:
```bash
docker ps
```

Para ver los logs:
```bash
docker logs catalog_db
docker logs product_catalog_app
```

Para detener los contenedores:
```bash
docker-compose down
```

#### 6. Crear tablas
Antes de poder hacer nada se **deben** crear las tablas:
```bash
python -m product_catalog_sync.main --initdb
```

#### 7. Datos de entrada
El sistema espera archivos CSV en el directorio por defecto `data/`. Crea el directorio si no existe:
La configuración de la ruta se puede cambiar en `product_catalog_sync/config/app_config.py`
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

### Instalación rápida
La forma más sencilla de instalar y preparar todo el entorno (entorno virtual, dependencias, variables de entorno, base de datos Docker, tablas y estructura de directorios) es ejecutar:
```bash
make -f Makefile.windows setup # para Windows
make -f Makefile.linux setup   # para Linux
```
**NOTA**: Se recomienda crear el archivo `.env` y `docker.env` con tus datos a partir de los ejemplos `.env.example` y `docker.env.example` antes de ejecutar este comando
Este comando realiza automáticamente los siguientes pasos:

1. Crea un entorno virtual (`venv/`)
2. Instala todas las dependencias desde `requirements.txt`
3. Crea el archivo `.env` y `docker.env` a partir de `.env.example` y `docker.env.example` si no existe 
4. Levanta el contenedor Docker de PostgreSQL y FastAPI
5. Inicializa las tablas de la base de datos
6. Crea el directorio `data/` si no existe

Cuando la instalación termine verás un mensaje como:

```
Instalación completa.
```

## Ejecución

### Usar el entorno virtual
Antes de ejecutar cualquier comando, asegúrate de activar el entorno virtual creado durante la instalación.
Linux / macOS
```bash
source .venv/bin/activate
```
Windows (cmd)
```bash
venv\Scripts\activate
```
Windows (Powershell)
```bash
.\.venv\Scripts\Activate.ps1
```

### Inicializar la base de datos
En caso de no haberlo hecho durante la instalación manual, crea las tablas usando: 
```bash
python -m product_catalog_sync.main --initdb
```
La instalación rápida las crea automáticamente.

### Modo catálogo

Actualiza el catálogo de productos desde `data/feed_items.csv` o una ruta específicada.

Ruta por defecto (`data/feed_items.csv`)
```bash
python -m product_catalog_sync.main --catalog
```

Ruta personalizada:
```bash
python -m product_catalog_sync.main --catalog --file data/custom_file.csv
```

Las rutas por defecto pueden ser modificadas en `product_catalog_sync/config/app_config.py`

Este modo:
- Lee productos del archivo CSV
- Crea o actualiza productos existentes
- **Mantiene** productos no presentes en el CSV
- Gestiona las relaciones producto-tienda

### Modo portal

Sincroniza productos desde `data/portal_items.csv`:

Ruta por defecto (`data/feed_items.csv`)
```bash
python -m product_catalog_sync.main --portal
```

Ruta personalizada:
```bash
python -m product_catalog_sync.main --portal --file data/custom_file.csv
```

Las rutas por defecto pueden ser modificadas en `product_catalog_sync/config/app_config.py`

Este modo:
- Lee productos del archivo CSV
- Crea o actualiza productos existentes
- **Elimina** productos que no están en el CSV
- Sincroniza completamente el portal con el archivo

### Verificación de logs
Los logs se almacenan en el directorio por defecto `/logs`. Están divididos en dos archivos:
- **app.log**: registra todo lo que ocurre relacionado directamente con la aplicación
- **db.log**: registra todas las operaciones realizadas sobre la base de datos incluido COMMITS y ROLLBACKS

Las rutas por defecto pueden ser modificadas en `product_catalog_sync/config/app_config.py`

## Estructura del código
```
product-catalog-sync/
│
├── product_catalog_sync/
│   ├── api/  
│   │   ├── app.py             # Punto de entrada de la API
│   │   └── routers.py         # Endpoints         
│   │
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
│   │   ├── product_queries.py        # Consultas SQL
│   │   ├── product_repository.py     # CRUD de productos
│   │   ├── store_repository.py       # CRUD de tiendas
│   │   └── product_store_repository.py # CRUD de relaciones
│   │
│   ├── schemas/               # Esquemas de validación
│   │   ├── product_input.py   # Schema para datos de entrada
│   │   └── product_response.py# Schema para respuestas
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
│
├── docker-compose.yaml       # Configuración de Docker para PostgreSQL
├── docker.env.example        # Variables de entorno para Docker (ejemplo)
├── Dockerfile                # Imagen de la aplicación
│
├── makefile.linux            # Makefile para Linux
├── makefile.windows          # Makefile para Windows
│
├── requirements.txt          # Dependencias de Python
│
├── .env.example             # Ejemplo de variables de entorno
├── .gitignore               # Exclusiones de Git
│
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
Asegúrate de estar siempre dentro del entorno virtual:
Linux / macOS
```bash
source .venv/bin/activate
```
Windows (cmd)
```bash
venv\Scripts\activate
```
Windows (Powershell)
```bash
.\.venv\Scripts\Activate.ps1
```
### Ejemplo 1: Actualización del catálogo

```bash
# 1. Asegúrate que la base de datos está funcionando
docker-compose up -d

# 2. Verifica tener los datos CSV en data/, específicado con --file o en la ruta que hayas configurado

# 3. Ejecuta la actualización del catálogo
python -m product_catalog_sync.main --catalog    # ruta por defecto
# o
python -m product_catalog_sync.main --catalog --file data/custom_file.csv
```

### Ejemplo 2: Sincronización del portal
```bash
# 1. Verifica tener los datos CSV en data/, específicado con --file o en la ruta que hayas configurado

# 2. Ejecuta la actualización del catálogo
python -m product_catalog_sync.main --portal    # ruta por defecto
# o
python -m product_catalog_sync.main --portal --file data/custom_file.csv
```

### Ejemplo 3: Uso de endpoints
```bash
# 1. Asegúrate que FastAPI está funcionando
docker-compose up -d

# Alternativa: ejecutar localmente sin Docker (asegúrate que Docker no este activo)
uvicorn product_catalog_sync.api.app:app --reload
```
Una vez la API este disponible en `http://localhost:8000`
```bash
# Consultar productos via cURL
curl http://localhost:8000/api/products
```

Este es un ejemplo de respuesta:
```json
[
  {
    "product_id": 1084,
    "title": "PORTATIL MACBOOK AIR 2017",
    "price": 599.95,
    "stores": [1, 3]
  },
  {
    "product_id": 1946,
    "title": "GOOGLE CHROMECAST 3GEN",
    "price": 29.95,
    "stores": [4, 2]
  }
]
```

También puedes consultar la documentación de los endpoints en `http://localhost:8000/docs` o `http://localhost:8000/redoc`