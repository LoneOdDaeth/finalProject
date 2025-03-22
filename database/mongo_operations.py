from crypto.cryptoSaveMaterials import *
from pymongo import MongoClient
import os

client = MongoClient("mongodb://localhost:27017/")
db = client["Erlik"]
users_collection = db["users"]

def saveUser(username, password):
    encryptedPassword, key = aes_encrypt(password)

    data = {
        "_id": username,
        "password": encryptedPassword,
        "key": key
    }

    users_collection.insert_one(data)

def getUserName():
    users = users_collection.find({}, {"_id": 1})
    return [user["_id"] for user in users]

def getUserPass(username):
    user_doc = users_collection.find_one({"_id": username})
    
    if user_doc:
        password = user_doc["password"]
        key = user_doc["key"]
        decrypted = aes_dcrypted(password, key)
        return decrypted
    else:
        return 0  # Kullanıcı bulunamadı
