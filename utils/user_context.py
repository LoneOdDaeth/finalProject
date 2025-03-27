
def set_current_user(username):
    with open("tmp/user", "w") as file:
        file.write(username)

def get_current_user():
    with open("tmp/user", "r") as file:
        return file.read()  # <-- eksik olan return eklendi

def remove_current_user():
    import os
    try:
        os.remove("tmp/user")
    except FileNotFoundError:
        pass
