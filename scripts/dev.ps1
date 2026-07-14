# Start development environment and tail logs
docker compose -f compose.yaml -f compose.dev.yaml up -d
docker compose logs -f
