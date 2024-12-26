import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

def aes_encrypt(data):

    key = os.urandom(16) # Rastgele bir 128-bit anahtar
    iv = os.urandom(16) # Rastgele bir 16 baytlık IV oluştur
    
    # Şifreleme algoritmasını ve modunu ayarla
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Veriyi AES blok boyutuna uygun şekilde doldur
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data.encode()) + padder.finalize()
    
    # Veriyi şifrele
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    passData = base64.b64encode(iv + encrypted_data).decode()
    keyData = base64.b64encode(key).decode()
    # IV ve şifrelenmiş veriyi Base64 formatında birleştirip döndür
    return passData, keyData

def aes_dcrypted(passData, keyData):
    
    key = base64.b64decode(keyData)  # Şifreleme sırasında kullanılan anahtar
    combined_data = base64.b64decode(passData)  # IV ve şifrelenmiş veri birleşimi

    # IV (ilk 16 bayt) ve şifrelenmiş veriyi ayır
    iv = combined_data[:16]
    encrypted_data = combined_data[16:]

    # Şifreleme algoritmasını ve modunu ayarla
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Şifrelenmiş veriyi çöz
    padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Veriyi AES blok boyutuna uygun olarak doldurma işlemini geri al
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    # Veriyi string olarak döndür
    return data.decode()
