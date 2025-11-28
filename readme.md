# 🎬 API de Películas - Final Programación

Una API REST construida con **FastAPI** que permite gestionar usuarios y películas, con integración a **TMDB** (The Movie Database).

## 🚀 Características Principales

### Gestión de Usuarios

- ✅ Registrar nuevos usuarios
- ✅ Listar todos los usuarios
- ✅ Obtener usuario por ID
- ✅ Actualizar datos de usuario
- ✅ Eliminar usuarios (soft-delete)

### Gestión de Películas

- ✅ Crear películas manualmente
- ✅ Listar películas con filtros (título, calificación mínima)
- ✅ Obtener película por ID
- ✅ Actualizar información de película
- ✅ Eliminar películas
- ✅ Importar películas desde TMDB por ID
- ✅ Importar películas populares de TMDB
- ✅ Buscar películas en TMDB

## 📋 Requisitos Previos

- Python 3.10+
- pip (gestor de paquetes)
- Una clave API de TMDB (obtén una en [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api))

## ⚙️ Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd final-programacion
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Luego, edita el archivo `.env` con tus credenciales:

```env
PORT=8000
STRCNX=sqlite:///./app/database.sqlite
TMDB_BASE_URL=https://api.themoviedb.org/3
TMDB_ACCESS_TOKEN=tu_clave_api_tmdb
```

## 🏃 Iniciar el Proyecto

```bash
uvicorn app.main:app --reload
```

La API estará disponible en **<http://localhost:8000>**

Accede a la documentación interactiva en:

- **Swagger UI**: <http://localhost:8000/docs>
- **ReDoc**: <http://localhost:8000/redoc>

## 📡 Ejemplos de Uso

Consulta los endpoints utilizando - **Swagger UI**: <http://localhost:8000/docs>! (opcion recomendada)

Algunos ejemplos rápidos:

**Crear usuario:**

```bash
curl -X POST "http://localhost:8000/api/users/" \
     -H "Content-Type: application/json" \
     -d '{"username": "johndoe", "email": "john@example.com", "full_name": "John Doe"}'
```

**Importar película desde TMDB:**

```bash
curl -X POST "http://localhost:8000/api/movies/import/550"
```

**Listar películas con filtros:**

```bash
curl -X GET "http://localhost:8000/api/movies/?title=fight&min_rating=7"
```

## 🗄️ Estructura del Proyecto

```sh
app/
├── models/          # Modelos de base de datos (User, Movie)
├── schemas/         # Esquemas de validación (Pydantic)
├── routers/         # Endpoints de la API
├── services/        # Lógica de negocio
├── database.py      # Configuración de base de datos
└── main.py          # Punto de entrada de la aplicación
```

## 🛠️ Tecnologías Utilizadas

- **FastAPI** - Framework web moderno
- **SQLAlchemy** - ORM para base de datos
- **SQLite** - Base de datos
- **Pydantic** - Validación de datos
- **Requests** - Cliente HTTP para TMDB

## 📝 Notas

- Las películas se importan desde TMDB pero se almacenan localmente en SQLite
- Los usuarios se eliminan mediante soft-delete (se marca `is_active = False`)
- La API incluye manejo de errores y validación automática de datos
