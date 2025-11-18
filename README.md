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