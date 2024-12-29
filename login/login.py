# import tkinter as tk
# from tkinter import messagebox
# from firebaseOp import *

# def signup():
#     username = username_entry.get()
#     password = password_entry.get()
#     username_entry.delete(0, tk.END)
#     password_entry.delete(0, tk.END)   

#     usernameList = getUserName()

#     if username in usernameList:
#         messagebox.showerror("HATA", "Bu kullanıcı adı alınmış!")
#     else:
#         saveUser(username, password)
#         messagebox.showinfo("Kayıt Başarılı", "Hoş Geldiniz!")

# def login():
#     username = username_entry.get()
#     password = password_entry.get()
#     username_entry.delete(0, tk.END)
#     password_entry.delete(0, tk.END)
    
#     passData = getUserPass(username)

#     if passData == password:
#         messagebox.showinfo("Giriş Başarılı", "Hoş geldiniz!")
#     elif passData == 0:
#         messagebox.showerror("HATA", "Kullanıcı ismi bulunamadı!")
#     elif passData != password:
#         messagebox.showerror("HATA", "Parola hatalı girildi")

#     # if username == "admin" and password == "1234":
#     #     messagebox.showinfo("Giriş Başarılı", "Hoş geldiniz!")
#     # else:
#     #     messagebox.showerror("HATA", "Kullanıcı adı veya parola hatalı!")

# root = tk.Tk()
# root.title("Giriş Ekranı")
# root.state('zoomed')
# root.configure(bg="#2C2F33")  # Arkaplan rengi

# # Ana çerçeve
# main_frame = tk.Frame(root, bg="#2C2F33")
# main_frame.place(relx=0.5, rely=0.5, anchor="center")

# # Kullanıcı Adı Etiketi ve Girişi
# username_label = tk.Label(main_frame, text="Kullanıcı Adı", bg="#2C2F33", fg="white", font=('Arial', 12))
# username_label.pack(pady=(10, 5))

# username_entry = tk.Entry(main_frame, bg="#1E1F22", fg="white", font=('Arial', 12), insertbackground='white')
# username_entry.pack(pady=5, ipady=5, ipadx=5)

# # Parola Etiketi ve Girişi
# password_label = tk.Label(main_frame, text="Parola", bg="#2C2F33", fg="white", font=('Arial', 12))
# password_label.pack(pady=(10, 5))

# password_entry = tk.Entry(main_frame, show="*", bg="#1E1F22", fg="white", font=('Arial', 12), insertbackground='white')
# password_entry.pack(pady=5, ipady=5, ipadx=5)

# # Giriş ve Kaydol Butonları
# button_frame = tk.Frame(main_frame, bg="#2C2F33")
# button_frame.pack(pady=20)

# login_button = tk.Button(button_frame, text="Giriş Yap", command=login, bg="#7289DA", fg="white",
#                          activebackground="#5A78B8", activeforeground="white", font=('Arial', 12, 'bold'))
# login_button.pack(side=tk.LEFT, padx=10)

# signup_button = tk.Button(button_frame, text="Kaydol", command=signup, bg="#43B581", fg="white",
#                           activebackground="#358965", activeforeground="white", font=('Arial', 12, 'bold')) # yeşil buton
# signup_button.pack(side=tk.LEFT, padx=10)

# root.mainloop()


# import tkinter as tk
# from tkinter import messagebox
# from firebaseOp import *
# from PIL import Image, ImageTk  # Pillow kütüphanesi

# def signup():
#     username = username_entry.get()
#     password = password_entry.get()
#     username_entry.delete(0, tk.END)
#     password_entry.delete(0, tk.END)   

#     usernameList = getUserName()

#     if username in usernameList:
#         messagebox.showerror("HATA", "Bu kullanıcı adı alınmış!")
#     else:
#         saveUser(username, password)
#         messagebox.showinfo("Kayıt Başarılı", "Hoş Geldiniz!")

# def login():
#     username = username_entry.get()
#     password = password_entry.get()
#     username_entry.delete(0, tk.END)
#     password_entry.delete(0, tk.END)
    
#     passData = getUserPass(username)

#     if passData == password:
#         messagebox.showinfo("Giriş Başarılı", "Hoş geldiniz!")
#     elif passData == 0:
#         messagebox.showerror("HATA", "Kullanıcı ismi bulunamadı!")
#     elif passData != password:
#         messagebox.showerror("HATA", "Parola hatalı girildi")

# root = tk.Tk()
# root.title("Giriş Ekranı")
# root.geometry("1920x1080")  # Sabit pencere boyutu
# root.configure(bg="#2C2F33")  # Arkaplan rengi

# # Resmi arka plan olarak eklemek
# bg_image = Image.open("loginArkaplan.png")
# bg_image = bg_image.resize((1920, 1080), Image.LANCZOS)  # Pencere boyutuna göre yeniden boyutlandır
# bg_photo = ImageTk.PhotoImage(bg_image)

# bg_label = tk.Label(root, image=bg_photo)
# bg_label.place(relwidth=1, relheight=1)  # Tam ekran kaplama

# # Ana çerçeve (arka plan resmi üzerinde konumlandırılmış)
# main_frame = tk.Frame(root, bg="#2C2F33", bd=2, relief="ridge")
# main_frame.place(relx=0.5, rely=0.5, anchor="center")

# # Kullanıcı Adı Etiketi ve Girişi
# username_label = tk.Label(main_frame, text="Kullanıcı Adı", bg="#2C2F33", fg="white", font=('Arial', 12))
# username_label.pack(pady=(10, 5))

# username_entry = tk.Entry(main_frame, bg="#1E1F22", fg="white", font=('Arial', 12), insertbackground='white')
# username_entry.pack(pady=5, ipady=5, ipadx=5)

# # Parola Etiketi ve Girişi
# password_label = tk.Label(main_frame, text="Parola", bg="#2C2F33", fg="white", font=('Arial', 12))
# password_label.pack(pady=(10, 5))

# password_entry = tk.Entry(main_frame, show="*", bg="#1E1F22", fg="white", font=('Arial', 12), insertbackground='white')
# password_entry.pack(pady=5, ipady=5, ipadx=5)

# # Giriş ve Kaydol Butonları
# button_frame = tk.Frame(main_frame, bg="#2C2F33")
# button_frame.pack(pady=20)

# login_button = tk.Button(button_frame, text="Giriş Yap", command=login, bg="#7289DA", fg="white",
#                          activebackground="#5A78B8", activeforeground="white", font=('Arial', 12, 'bold'))
# login_button.pack(side=tk.LEFT, padx=10)

# signup_button = tk.Button(button_frame, text="Kaydol", command=signup, bg="#43B581", fg="white",
#                           activebackground="#358965", activeforeground="white", font=('Arial', 12, 'bold'))
# signup_button.pack(side=tk.LEFT, padx=10)

# root.mainloop()

from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QMainWindow, QWidget)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from firebaseOp import *
import sys

def signup(username_entry, password_entry):
    username = username_entry.text()
    password = password_entry.text()
    username_entry.clear()
    password_entry.clear()

    usernameList = getUserName()

    if username in usernameList:
        QMessageBox.critical(None, "HATA", "Bu kullanıcı adı alınmış!")
    else:
        saveUser(username, password)
        QMessageBox.information(None, "Kayıt Başarılı", "Hoş Geldiniz!")

def login(username_entry, password_entry):
    username = username_entry.text()
    password = password_entry.text()
    username_entry.clear()
    password_entry.clear()

    passData = getUserPass(username)

    if passData == password:
        QMessageBox.information(None, "Giriş Başarılı", "Hoş geldiniz!")
    elif passData == 0:
        QMessageBox.critical(None, "HATA", "Kullanıcı ismi bulunamadı!")
    elif passData != password:
        QMessageBox.critical(None, "HATA", "Parola hatalı girildi")

def main():
    app = QApplication(sys.argv)

    # Ana pencere
    window = QMainWindow()
    window.setWindowTitle("Giriş Ekranı")
    window.setGeometry(0, 0, 1920, 1080)

    # Ana widget ve layout
    main_widget = QWidget()
    window.setCentralWidget(main_widget)

    # Arkaplan resmi
    bg_label = QLabel(main_widget)
    bg_pixmap = QPixmap("main.png").scaled(1920, 1080, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
    bg_label.setPixmap(bg_pixmap)
    bg_label.setGeometry(0, 0, 1920, 1080)

    # Ana çerçeve
    main_frame = QWidget(main_widget)
    main_frame.setStyleSheet("background-color:rgb(25, 25, 25); border: 2px #00ff00;")
    main_frame.setFixedSize(300, 200)
    main_frame.move(760, 390)  # Ekranın ortasında konumlandırma

    # Kullanıcı Adı
    username_label = QLabel("Kullanıcı Adı", main_frame)
    username_label.setStyleSheet("color: #00ff00; font-size: 14px;")
    username_label.setFixedHeight(30)
    username_entry = QLineEdit(main_frame)
    username_entry.setStyleSheet("background-color:rgb(10, 10, 10); color: #00ff00; font-size: 14px; padding: 5px;") 

    # Parola
    password_label = QLabel("Parola", main_frame)
    password_label.setStyleSheet("color: #00ff00; font-size: 14px;")
    password_label.setFixedHeight(30)
    password_entry = QLineEdit(main_frame)
    password_entry.setEchoMode(QLineEdit.Password)
    password_entry.setStyleSheet("background-color:rgb(10, 10, 10); color: #00ff00; font-size: 14px; padding: 5px;")

    username_layout = QHBoxLayout()
    username_layout.addWidget(username_label)
    username_layout.addWidget(username_entry)

    password_layout = QHBoxLayout()
    password_layout.addWidget(password_label)
    password_layout.addWidget(password_entry)

    # Butonlar
    login_button = QPushButton("Giriş Yap", main_frame)
    login_button.setStyleSheet("background-color:rgb(0, 0, 0); color: #00ff00; font-size: 14px; font-weight: bold;")
    login_button.clicked.connect(lambda: login(username_entry, password_entry))

    signup_button = QPushButton("Kaydol", main_frame)
    signup_button.setStyleSheet("background-color:rgb(0, 0, 0); color: #00ff00; font-size: 14px; font-weight: bold;")
    signup_button.clicked.connect(lambda: signup(username_entry, password_entry))

    # Layout
    layout = QVBoxLayout()
    layout.addLayout(username_layout)  # Kullanıcı adı layout'u
    layout.addLayout(password_layout)  # Parola layout'u
    main_frame.setLayout(layout)

    login_button.setFixedSize(137, 40)  # Genişlik: 120px, Yükseklik: 40px
    signup_button.setFixedSize(137, 40)  # Genişlik: 140px, Yükseklik: 50px

    button_layout = QHBoxLayout()
    button_layout.addWidget(login_button)
    button_layout.addWidget(signup_button)

    layout.addLayout(button_layout)
    main_frame.setLayout(layout)

    window.showFullScreen()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
