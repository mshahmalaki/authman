# -----------------------------------[Define]-------------------------------- #
user = {
    "username": "test",
    "password": "test"
}
id = 1

# -----------------------------------[Create]-------------------------------- #
def test_create_user(client):
    # Send a POST request with true parameters.
    # Happy path so should success with 201 code.
    global id
    response = client.post("/users",
        json=user, headers={"Content-Type": "application/json"})

    assert response.content_type == "application/json"
    assert response.status_code == 200

    res_obj = response.json["user"]
    assert "username" in res_obj
    assert res_obj["username"] == user["username"]
    assert "id" in res_obj
    assert "created_at" in res_obj
    assert "is_enabled" in res_obj
    assert "password" not in res_obj

    id = res_obj["id"]

def test_create_user_duplicated(client):
    # Send a POST request with true parameters.
    # Happy path so should success with 201 code.
    response = client.post("/users",
        json=user, headers={"Content-Type": "application/json"})
    assert response.status_code == 409

def test_create_user_without_password(client):
    # Send a POST request without password.
    # should fail with 415 error code.
    response = client.post("/users",
        json={"username": "foo"}, headers={"Content-Type": "application/json"})
    assert response.status_code == 400

def test_create_user_without_username(client):
    # Send a POST request without username.
    # should fail with 415 error code.
    response = client.post("/users",
        json={"password": "bar"}, headers={"Content-Type": "application/json"})
    assert response.status_code == 400

def test_create_invalid_user(client):
    # Send a POST request without json or headers.
    # Wrong content type so should fail with 415 error code.
    response = client.post("/users")
    assert response.status_code == 415

# -----------------------------------[Index]--------------------------------- #
def test_get_user(client):
    # Send a GET request for a created user.
    # Happy path so should success with 200 code.
    response = client.get(f"/users/{id}")
    assert response.content_type == "application/json"
    assert response.json["user"]["username"] == user["username"]
    assert response.status_code == 200

def test_get_user_0(client):
    # Send a GET request for an invalid user.
    # Will not found so should fail with 404 code.
    response = client.get("/users/0")
    assert response.status_code == 404

# -----------------------------------[List]---------------------------------- #
def test_get_users(client):
    # Send a GET request for created users.
    # Happy path so should success with 200 code.
    response = client.get("/users")
    assert response.content_type == "application/json"
    assert response.status_code == 200

# -----------------------------------[Delete]-------------------------------- #
def test_delete_user(client):
    # Send a DELTE request for a created users.
    # Happy path so should success with 200 code.
    response = client.delete(f"/users/{id}")
    assert response.status_code == 204

def test_delete_invalid_user(client):
    # Send a DELTE request for an invalid users.
    # Will not found so should fail with 404 code.
    response = client.delete("/users/0")
    assert response.status_code == 404

def test_delete_without_user_id(client):
    # Send a DELTE request to /users.
    # Invalid operatin so should fail with 405.
    response = client.delete("/users")
    assert response.status_code == 405

# -----------------------------------[Other]--------------------------------- #
def test_post_to_user_id(client):
    # Send a POST request to /users/<id>.
    # Invalid operatin so should fail with 405.
    response = client.post("/users/1")
    assert response.status_code == 405
