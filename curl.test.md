# 🧪 Ejemplos de Prueba

Una vez que tengas tu API corriendo, prueba estos comandos:

## Crear usuario

```bash
curl -X POST "http://localhost:8000/users/" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "johndoe",
       "email": "john@example.com",
       "full_name": "John Doe"
     }'
```

## Listar usuarios

```bash
curl -X GET "http://localhost:8000/users/?skip=0&limit=10"
```

## Importar película desde TMDB

```bash
# Fight Club (TMDB ID: 550)
curl -X POST "http://localhost:8000/movies/import/550"
```

## Buscar películas en TMDB

```bash
curl -X GET "http://localhost:8000/movies/search/matrix"
```

## Importar películas populares

```bash
curl -X POST "http://localhost:8000/movies/import/popular?page=1"
```

## Listar películas con filtros

```bash
curl -X GET "http://localhost:8000/movies/?title=fight&min_rating=7&skip=0&limit=10"
```

---
