# Almacenamiento de Archivos y Documentos

## Estructura de Persistencia
Los archivos nunca se guardan directamente en PostgreSQL. La base de datos almacena los metadatos y la ruta cifrada en un volumen persistente:

```
/media/documents/{entity_type}/{year}/{month}/{uuid}.{extension}
```

## Acceso Privado
- Las descargas se gestionan mediante `/api/v1/documents/{id}/content/`.
- Se requiere el permiso `documents.view_private_document`.
- En producción, Nginx está preparado para servir los archivos de forma eficiente usando `X-Accel-Redirect` sin exponer el directorio real.
