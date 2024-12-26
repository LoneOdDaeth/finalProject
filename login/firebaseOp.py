import firebase_admin
from firebase_admin import credentials, firestore
from cryptoSaveMaterials import *

# Firebase Admin SDK ile bağlantı kur
cred = credentials.Certificate("erlik-12fd1-firebase-adminsdk-giyoo-a4ab91258c.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
collectionName = "Erlik"

def saveUser(username, password):
    encryptedPassword, key = aes_encrypt(password)

    data = {
        'key': f'{key}',
        'password': f'{encryptedPassword}'
    }

    doc_ref = db.collection(collectionName).document(username)
    doc_ref.set(data)

def getUserName():
    docs = db.collection(collectionName).stream()
    documentNames = [doc.id for doc in docs]
    return documentNames

def getUserPass(username):
    check = getUserName()

    if username in check:

        data = []

        doc_ref = db.collection(collectionName).document(username)
        doc = doc_ref.get()
        doc = doc.to_dict()
        
        for item in doc.values():
            data.append(item)

        password = data[0]
        key = data[1]
        passTocheck = aes_dcrypted(password, key)

        return passTocheck
    else:
        return 0