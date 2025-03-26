from crypto.cryptoSaveMaterials import *
from pymongo import MongoClient
from bson import ObjectId

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

analyses_collection = db["analyses"]

def save_analysis(username, filename, timestamp, analysis_data):
    analysis_doc = {
        "username": username,
        "filename": filename,
        "timestamp": timestamp,
        "analysis": analysis_data
    }
    analyses_collection.insert_one(analysis_doc)

def get_user_analyses(username):
    return list(db["analyses"].find({"username": username}).sort("timestamp", -1))

def get_all_users():
    return list(db["users"].find({}, {"_id": 1}))

def get_analysis_by_filename(filename):
    return db["analyses"].find_one({"filename": filename})

def save_pdf_record(username, pdf_filename, timestamp, related_analysis, path):
    db["pdf_reports"].insert_one({
        "username": username,
        "pdf_filename": pdf_filename,
        "timestamp": timestamp,
        "related_analysis": related_analysis,
        "path": path
    })

def get_user_pdfs(username):
    return list(db["pdf_reports"].find({"username": username}).sort("timestamp", -1))

