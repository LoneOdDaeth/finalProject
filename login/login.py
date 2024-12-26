import tkinter as tk
from tkinter import messagebox
from firebaseOp import *

def signup():
    username = username_entry.get()
    password = password_entry.get()
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)   

    usernameList = getUserName()

    if username in usernameList:
        messagebox.showerror("HATA", "Bu kullanıcı adı alınmış!")
    else:
        saveUser(username, password)
        messagebox.showinfo("Kayıt Başarılı", "Hoş Geldiniz!")

def login():
    username = username_entry.get()
    password = password_entry.get()
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    
    passData = getUserPass(username)

    if passData == password:
        messagebox.showinfo("Giriş Başarılı", "Hoş geldiniz!")
    elif passData == 0:
        messagebox.showerror("HATA", "Kullanıcı ismi bulunamadı!")
    elif passData != password:
        messagebox.showerror("HATA", "Parola hatalı girildi")

    # if username == "admin" and password == "1234":
    #     messagebox.showinfo("Giriş Başarılı", "Hoş geldiniz!")
    # else:
    #     messagebox.showerror("HATA", "Kullanıcı adı veya parola hatalı!")

root = tk.Tk()
root.title("Giriş Ekranı")
root.state('zoomed')
root.configure(bg="#2C2F33")  # Arkaplan rengi

# Ana çerçeve
main_frame = tk.Frame(root, bg="#2C2F33")
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Kullanıcı Adı Etiketi ve Girişi
username_label = tk.Label(main_frame, text="Kullanıcı Adı", bg="#2C2F33", fg="white", font=('Arial', 12))
username_label.pack(pady=(10, 5))

username_entry = tk.Entry(main_frame, bg="#1E1F22", fg="white", font=('Arial', 12), insertbackground='white')
username_entry.pack(pady=5, ipady=5, ipadx=5)

# Parola Etiketi ve Girişi
password_label = tk.Label(main_frame, text="Parola", bg="#2C2F33", fg="white", font=('Arial', 12))
password_label.pack(pady=(10, 5))

password_entry = tk.Entry(main_frame, show="*", bg="#1E1F22", fg="white", font=('Arial', 12), insertbackground='white')
password_entry.pack(pady=5, ipady=5, ipadx=5)

# Giriş ve Kaydol Butonları
button_frame = tk.Frame(main_frame, bg="#2C2F33")
button_frame.pack(pady=20)

login_button = tk.Button(button_frame, text="Giriş Yap", command=login, bg="#7289DA", fg="white",
                         activebackground="#5A78B8", activeforeground="white", font=('Arial', 12, 'bold'))
login_button.pack(side=tk.LEFT, padx=10)

signup_button = tk.Button(button_frame, text="Kaydol", command=signup, bg="#43B581", fg="white",
                          activebackground="#358965", activeforeground="white", font=('Arial', 12, 'bold')) # yeşil buton
signup_button.pack(side=tk.LEFT, padx=10)

root.mainloop()
