from fastapi.testclient import TestClient
from main import app
import random

client = TestClient(app)

def random_suffix():
    return str(random.randint(1000, 9999))

def test_create_user():
    suffix = random_suffix()
    response = client.post("/api/users/", json={
        "username": f"testuser{suffix}",
        "email": f"test{suffix}@example.com",
        "full_name": "Test User"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == f"testuser{suffix}"
    assert "id" in data
    return data["id"]

def test_list_users():
    # Create one user first
    test_create_user()
    response = client.get("/api/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_user_by_id():
    user_id = test_create_user()
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id

def test_update_user():
    user_id = test_create_user()
    response = client.put(f"/api/users/{user_id}", json={
        "full_name": "Updated Name"
    })
    if response.status_code != 200:
        print(f"Update user failed: {response.status_code} {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"

def test_delete_user():
    user_id = test_create_user()
    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 204

def test_create_movie():
    suffix = random_suffix()
    response = client.post("/api/movies/", json={
        "title": f"Test Movie {suffix}",
        "overview": "A test movie",
        "release_date": "2023-01-01",
        "vote_average": 8.0,
        "tmdb_id": 12345 + int(suffix)
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == f"Test Movie {suffix}"
    return data["id"]

def test_list_movies():
    # Create one movie first
    test_create_movie()
    response = client.get("/api/movies/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_movie_by_id():
    movie_id = test_create_movie()
    response = client.get(f"/api/movies/{movie_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == movie_id

def test_update_movie():
    movie_id = test_create_movie()
    response = client.put(f"/api/movies/{movie_id}", json={
        "title": "Updated Movie"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Movie"

def test_delete_movie():
    movie_id = test_create_movie()
    response = client.delete(f"/api/movies/{movie_id}")
    assert response.status_code == 204

def test_import_movie_by_tmdb_id():
    # Assuming TMDB ID 550 is Fight Club
    response = client.post("/api/movies/import/550")
    assert response.status_code == 201
    data = response.json()
    assert "title" in data

def test_import_popular_movies():
    response = client.post("/api/movies/import/popular?page=1")
    assert response.status_code == 201
    data = response.json()
    assert isinstance(data, list)

def test_search_movies_tmdb():
    response = client.get("/api/movies/search/fight")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data

if __name__ == "__main__":
    # Run tests
    try:
        test_create_user()
        print("✓ User creation works")
        test_list_users()
        print("✓ List users works")
        test_get_user_by_id()
        print("✓ Get user by ID works")
        test_update_user()
        print("✓ Update user works")
        test_delete_user()
        print("✓ Delete user works")
        test_create_movie()
        print("✓ Create movie works")
        test_list_movies()
        print("✓ List movies works")
        test_get_movie_by_id()
        print("✓ Get movie by ID works")
        test_update_movie()
        print("✓ Update movie works")
        test_delete_movie()
        print("✓ Delete movie works")
        test_import_movie_by_tmdb_id()
        print("✓ Import movie by TMDB ID works")
        test_import_popular_movies()
        print("✓ Import popular movies works")
        test_search_movies_tmdb()
        print("✓ Search movies in TMDB works")
        print("\nAll endpoints are functional!")
    except Exception as e:
        print(f"Error: {e}")