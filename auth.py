users = {
    "customer1": {"password": "password1", "role": "customer", "email": "customer1@example.com"},
    "laundryman1": {"password": "password2", "role": "laundryman"},
    "admin": {"password": "admin123", "role": "admin"}
}

def authenticate(username, password):
    user = users.get(username)
    if user and user["password"] == password:
        return user["role"]
    return None
