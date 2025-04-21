from crypto.cryptoSaveMaterials import *
from pymongo import MongoClient
from datetime import datetime
import os
import os
from datetime import datetime
import json

client = MongoClient("mongodb://localhost:27017/")
db = client["Erlik"]
users_collection = db["users"]
admin_collection = db["admins"]
analyses_collection = db["analyses"]
pdf_reports_collection = db["pdf_reports"]
smtp_settings_collection = db["smtp_settings"]
mail_logs_collection = db["mail_logs"]

def json_dump_to_folder(folder_path):
    os.makedirs(folder_path, exist_ok=True)
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Erlik"]

    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        data = list(collection.find({}))
        for d in data:
            d["_id"] = str(d["_id"])  # ObjectId string'e dönüştürülür
        file_path = os.path.join(folder_path, f"{collection_name}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    return True, f"✅ Tüm veriler {folder_path} klasörüne yedeklendi."


def json_restore_from_folder(folder_path):
    client = MongoClient("mongodb://localhost:27017/")
    db = client["Erlik"]

    for file_name in os.listdir(folder_path):
        if not file_name.endswith(".json"):
            continue
        collection_name = file_name.replace(".json", "")
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)

        # BURADA _id'leri ellemiyoruz!
        db[collection_name].drop()
        if data:
            db[collection_name].insert_many(data)

    return True, f"✅ Veritabanı {folder_path} klasöründen geri yüklendi."



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

# 💾 SMTP Ayarlarını Kaydet/Güncelle
def save_smtp_settings(email, host, port, tls, username, password, default_message=""):
    encrypted_password, key = aes_encrypt(password)

    smtp_doc = {
        "_id": email,  # kullanıcı maili (tekil tutar)
        "host": host,
        "port": port,
        "tls": tls,
        "username": username,
        "password": encrypted_password,
        "key": key,
        "updated_at": datetime.utcnow().isoformat(),
        "default_message": default_message
    }

    smtp_settings_collection.replace_one({"_id": email}, smtp_doc, upsert=True)


# 📥 SMTP Ayarlarını Getir
def get_smtp_settings(email):
    doc = smtp_settings_collection.find_one({"_id": email})
    if not doc:
        return None

    try:
        decrypted_password = aes_dcrypted(doc["password"], doc["key"])
    except:
        decrypted_password = ""

    return {
        "host": doc.get("host", ""),
        "port": doc.get("port", ""),
        "tls": doc.get("tls", None),
        "username": doc.get("username", ""),
        "password": decrypted_password,
        "default_message": doc.get("default_message", "")
    }

def save_mail_log(sender, recipient, subject, attachment_name=None):
    mail_logs_collection.insert_one({
        "timestamp": datetime.utcnow().isoformat(),
        "sender": sender,
        "recipient": recipient,
        "subject": subject,
        "attachment_name": attachment_name or ""
    })

def get_all_mail_logs():
    return list(mail_logs_collection.find().sort("timestamp", -1))
