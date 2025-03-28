from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["Erlik"]
admin_collection = db["admins"]

def add_admin_manually(email):
    if admin_collection.find_one({"_id": email}):
        print(f"⚠️ {email} zaten admin.")
        return

    admin_collection.insert_one({
        "_id": email,
        "created_by": "system",
        "created_at": datetime.utcnow().isoformat()
    })
    print(f"✅ {email} admin olarak eklendi.")

# ➤ BURAYA admin yapmak istediğin e-posta adresini yaz
add_admin_manually("9selim.oguz.sahin9@gmail.com")
