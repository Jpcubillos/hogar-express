# Guía de Despliegue en VM

## Estructura Recomendada del Servidor
```
/srv/hogar-express/
├── compose.yaml
├── compose.prod.yaml
├── .env
├── postgres/ (Volumen DB)
├── media/ (Archivos cargados)
└── backups/ (Copias diarias)
```

## Comandos de Despliegue
```bash
docker compose -f compose.yaml -f compose.prod.yaml up -d --build
```
