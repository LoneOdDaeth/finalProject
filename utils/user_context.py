# Basit bir oturum yönetimi

current_user = {
    "username": None
}

def set_current_user(username):
    current_user["username"] = username

def get_current_user():
    return current_user["username"]
