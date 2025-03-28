from crypto.cryptoSaveMaterials import *
from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")
db = client["Erlik"]
users_collection = db["users"]
admin_collection = db["admins"]
analyses_collection = db["analyses"]
pdf_reports_collection = db["pdf_reports"]

# 👤 Kullanıcı Kaydet
def saveUser(email, password):
    encryptedPassword, key = aes_encrypt(password)
    data = {
        "_id": email,  # e-posta adresi
        "password": encryptedPassword,
        "key": key
    }
    users_collection.insert_one(data)

# 📧 Tüm kullanıcı epostalarını getir
def getUserName():
    users = users_collection.find({}, {"_id": 1})
    return [user["_id"] for user in users]

# 🔐 Kullanıcı şifresini çöz
def getUserPass(email):
    user_doc = users_collection.find_one({"_id": email})
    if user_doc:
        password = user_doc["password"]
        key = user_doc["key"]
        decrypted = aes_dcrypted(password, key)
        return decrypted
    else:
        return 0  # Kullanıcı bulunamadı

# 📈 Analiz Kaydet
def save_analysis(username, filename, timestamp, analysis_data):
    analysis_doc = {
        "username": username,
        "filename": filename,
        "timestamp": timestamp,
        "analysis": analysis_data
    }
    analyses_collection.insert_one(analysis_doc)

# 🔍 Kullanıcının analizlerini getir
def get_user_analyses(username):
    return list(analyses_collection.find({"username": username}).sort("timestamp", -1))

# 👥 Tüm kullanıcıları getir
def get_all_users():
    return list(users_collection.find({}, {"_id": 1}))

# 🗂 Belirli analiz dosyasını getir
def get_analysis_by_filename(filename):
    return analyses_collection.find_one({"filename": filename})

# 📝 PDF rapor kaydet
def save_pdf_record(username, pdf_filename, timestamp, related_analysis, path):
    pdf_reports_collection.insert_one({
        "username": username,
        "pdf_filename": pdf_filename,
        "timestamp": timestamp,
        "related_analysis": related_analysis,
        "path": path
    })

# 📄 Kullanıcının PDF geçmişini getir
def get_user_pdfs(username):
    return list(pdf_reports_collection.find({"username": username}).sort("timestamp", -1))

# ❌ Analizi sil
def delete_analysis_by_filename(filename):
    analyses_collection.delete_one({"filename": filename})

# ❌ PDF raporu sil
def delete_pdf_by_filename(pdf_filename):
    pdf_reports_collection.delete_one({"pdf_filename": pdf_filename})

# 🛡 Admin kontrolü
def is_admin(username):
    return admin_collection.find_one({"_id": username}) is not None

# 👑 Admin listesini getir
def get_admin_list():
    return list(admin_collection.find({}))

# ➕ Admin ekle
def add_admin(target_email, created_by):
    if is_admin(target_email):
        return False, "⚠️ Bu kullanıcı zaten admin."

    admin_collection.insert_one({
        "_id": target_email,
        "created_by": created_by,
        "created_at": datetime.utcnow().isoformat()
    })
    return True, f"✅ {target_email} admin olarak eklendi."

# ➖ Admin sil
def remove_admin(target_email, requested_by):
    if target_email == requested_by:
        return False, "❌ Kendinizi admin listesinden silemezsiniz."

    if not is_admin(target_email):
        return False, "⚠️ Bu kullanıcı zaten admin değil."

    admin_collection.delete_one({"_id": target_email})
    return True, f"🗑️ {target_email} admin listesinden silindi."
