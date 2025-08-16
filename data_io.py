import json

def load_json(file_path):
    with open("data/anime.json", "r") as f:
        data = json.load(f)
    return data

def write_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent = 4)

def create_user(email, password, name, birthday = "", gender = ""):
    users = load_json("data/users.json")
    users.append({
        "id": len(users) + 1,
        "email": email,
        "password": password,
        "name": name,
        "birthday": birthday,
        "gender": gender
    })
    write_json("data/users.json", users)

def get_user_by_id(id):
    users = load_json("data/users.json")
    for user in users:
        if user["id"] == id:
            return user
    return None

def get_user_by_email(email):
    users = load_json("data/users.json")
    for user in users:
        if user["email"] == email:
            return user
    return None

def get_user_by_email_and_password(email, password):
    users = load_json("data/users.json")
    for user in users:
        if user["email"] == email and user["password"] == password:
            return user
        return None

def update_user(email, password, name, birthday = "", gender = ""):
    users = load_json("data/users.json")
    for user in users:
        if user["id"] == id:
            user["id"] = id
            user["name"] = name
            user["birthday"] = birthday
            user["gender"] = gender
            break
    write_json("data/users.json", users)

def update_user_avatar(id, avatar):
    users = load_json("data/users.json")
    for user in users:
        if user["id"] == id:
            user["avatar"] = avatar
            break
    write_json("data/users.json", users)