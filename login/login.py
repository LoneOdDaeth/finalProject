import tkinter as tk
from tkinter import messagebox
from firebaseOp import *
from PIL import Image, ImageTk  # Pillow kütüphanesi

# Ortak tasarım özellikleri
COLORS = {
    "bg": "#2C2F33",
    "fg": "#00ff00",
    "entry_bg": "#1E1F22",
    "button_bg": "#2C2F33",
    "button_active_bg": {"login": "#00ff00", "signup": "#00ff00"},
    "button_active_fg": "#2C2F33"
}
FONTS = {
    "label": ('Arial', 12, 'bold'),
    "entry": ('Arial', 12),
    "button": ('Arial', 12, 'bold'),
    "kendiButon": ('Arial', 12)
}

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
        switch_to_new_page()
    elif passData == 0:
        messagebox.showerror("HATA", "Kullanıcı ismi bulunamadı!")
    elif passData != password:
        messagebox.showerror("HATA", "Parola hatalı girildi")

def switch_to_new_page():
    # Mevcut pencerenin tüm widget'larını kaldır
    for widget in root.winfo_children():
        widget.destroy()

    # Arka plan resmini yeniden ekle
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)  # Tam ekran kaplama

    # Üst çubuğu yeniden oluştur
    title_bar = tk.Frame(root, bg=COLORS["bg"], relief="raised", bd=2)
    title_bar.pack(side="top", fill="x")

    # Üst çubuğa başlık ekle
    title_label = tk.Label(
        title_bar, text="Yeni Sayfa", bg=COLORS["bg"], fg=COLORS["fg"], font=FONTS["label"]
    )
    title_label.pack(side="left", padx=10)

    # Üst çubuğa kapatma butonu ekle
    close_button = tk.Button(
        title_bar, text="X", bg=COLORS["button_bg"], fg=COLORS["fg"],
        command=root.destroy, font=FONTS["kendiButon"], width=3
    )
    close_button.pack(side="right")

    # Sol çerçeve
    frame1 = tk.Frame(root, width=300, height=200, bg="white", relief="solid", bd=1)
    frame1.place(relx=0.2, rely=0.5, anchor="center")

    # Buton 1
    button1 = tk.Button(
        root, text="Buton 1", bg=COLORS["button_bg"], fg=COLORS["fg"],
        font=FONTS["button"], command=lambda: print("Buton 1'e tıklandı!")
    )
    button1.place(relx=0.2, rely=0.75, anchor="center")

    # Sağ çerçeve
    frame2 = tk.Frame(root, width=300, height=200, bg="white", relief="solid", bd=1)
    frame2.place(relx=0.8, rely=0.5, anchor="center")

    # Buton 2
    button2 = tk.Button(
        root, text="Buton 2", bg=COLORS["button_bg"], fg=COLORS["fg"],
        font=FONTS["button"], command=lambda: print("Buton 2'ye tıklandı!")
    )
    button2.place(relx=0.8, rely=0.75, anchor="center")



root = tk.Tk()
root.title("Giriş Ekranı")
root.geometry("1920x1080")  # Sabit pencere boyutu
root.configure(bg=COLORS["bg"])  # Arkaplan rengi
root.overrideredirect(True)  # Başlık çubuğunu kaldır

# Resmi arka plan olarak eklemek
bg_image = Image.open("../img/main.png")
bg_image = bg_image.resize((1920, 1080), Image.LANCZOS)  # Pencere boyutuna göre yeniden boyutlandır
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Tam ekran kaplama

# Ana çerçeve (arka plan resmi üzerinde konumlandırılmış)
main_frame = tk.Frame(root, bg=COLORS["bg"], bd=2, relief="ridge", width=400, height=250)
main_frame.place(x=760, y=440)  # Sabit konum
main_frame.pack_propagate(False)  # Çerçevenin boyutunun içeriğe göre değişmesini engelle

# Kullanıcı Adı için düzenleme
username_label = tk.Label(main_frame, text="Kullanıcı Adı", bg=COLORS["bg"], fg=COLORS["fg"], font=FONTS["label"])
username_label.grid(row=0, column=0, padx=(20, 10), pady=10, sticky="w")

username_entry = tk.Entry(main_frame, bg=COLORS["entry_bg"], fg=COLORS["fg"], font=FONTS["entry"], insertbackground='white', width=25)
username_entry.grid(row=0, column=1, ipady=5, pady=10, sticky="w")

# Parola için düzenleme
password_label = tk.Label(main_frame, text="Parola", bg=COLORS["bg"], fg=COLORS["fg"], font=FONTS["label"])
password_label.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")

password_entry = tk.Entry(main_frame, show="*", bg=COLORS["entry_bg"], fg=COLORS["fg"], font=FONTS["entry"], insertbackground='white', width=25)
password_entry.grid(row=1, column=1, ipady=5, pady=10, sticky="w")

# Giriş ve Kaydol Butonları
button_frame = tk.Frame(main_frame, bg=COLORS["bg"])
button_frame.grid(row=2, column=0, columnspan=2, pady=20)

login_button = tk.Button(
    button_frame, text="Giriş Yap", command=login, bg=COLORS["button_bg"], fg=COLORS["fg"],
    activebackground=COLORS["button_active_bg"]["login"], activeforeground=COLORS["button_active_fg"],
    font=FONTS["button"], width=12
)
login_button.grid(row=0, column=0, padx=10)

signup_button = tk.Button(
    button_frame, text="Kaydol", command=signup, bg=COLORS["button_bg"], fg=COLORS["fg"],
    activebackground=COLORS["button_active_bg"]["signup"], activeforeground=COLORS["button_active_fg"],
    font=FONTS["button"], width=12
)
signup_button.grid(row=0, column=1, padx=10)

# Başlık çubuğunu tasarlama
title_bar = tk.Frame(root, bg=COLORS["bg"], relief="raised", bd=2)
title_bar.pack(side="top", fill="x")

# Pencere başlığı
title_label = tk.Label(title_bar, text="Giriş Ekranı", bg=COLORS["bg"], fg=COLORS["fg"], font=FONTS["label"])
title_label.pack(side="left", padx=10)

# Kapatma butonu
close_button = tk.Button(title_bar, text="X", bg=COLORS["button_bg"], fg=COLORS["fg"],
                         command=root.destroy, font=FONTS["kendiButon"], width=3)
close_button.pack(side="right")

root.mainloop()
