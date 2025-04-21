from pymongo import MongoClient
from datetime import datetime

# MongoDB bağlantısı
client = MongoClient("mongodb://localhost:27017/")
db = client["Erlik"]
admin_collection = db["admins"]

# Eklenecek admin bilgisi
email = "9selim.oguz.sahin9@gmail.com"
created_by = "system"  # sistem tarafından eklendi

# Kontrol et, varsa ekleme
if admin_collection.find_one({"_id": email}):
    print(f"⚠️ '{email}' zaten admin.")
else:
    admin_collection.insert_one({
        "_id": email,
        "created_by": created_by,
        "created_at": datetime.utcnow().isoformat()
    })
    print(f"✅ '{email}' admin olarak eklendi.")
