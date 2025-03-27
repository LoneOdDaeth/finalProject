import tkinter as tk
import subprocess
from tkinter import messagebox
from database.mongo_operations import *
from PIL import Image, ImageTk
from utils.user_context import *

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

def run_dash():
    root.destroy()
    subprocess.run(["python", "app.py"])

def signup():
    name = name_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

    if not email.endswith("@gmail.com"):
        messagebox.showerror("HATA", "Sadece Gmail adresleri ile kayıt yapılabilir!")
        return

    username_list = getUserName()
    if email in username_list:
        messagebox.showerror("HATA", "Bu e-posta adresi zaten kayıtlı!")
    else:
        saveUser(name, email, password)
        messagebox.showinfo("Kayıt Başarılı", f"Hoş geldiniz {name}!")

def login():
    name = name_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    name_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

    if not email.endswith("@gmail.com"):
        messagebox.showerror("HATA", "Sadece Gmail adresleri ile giriş yapılabilir!")
        return

    passData = getUserPass(email)
    if passData == password:
        set_current_user(name)
        messagebox.showinfo("Giriş Başarılı", "Hoş geldiniz!")
        switch_to_new_page()
    elif passData == 0:
        messagebox.showerror("HATA", "Kullanıcı bulunamadı!")
    else:
        messagebox.showerror("HATA", "Parola hatalı!")

def switch_to_new_page():
    email = get_current_user()

    for widget in root.winfo_children():
        widget.destroy()

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(relwidth=1, relheight=1)

    title_bar = tk.Frame(root, bg=COLORS["bg"], relief="raised", bd=2)
    title_bar.pack(side="top", fill="x")

    name = get_user_name_by_email(email)
    title_label = tk.Label(title_bar, text=email, bg=COLORS["bg"], fg=COLORS["fg"], font=FONTS["label"])
    title_label.pack(side="left", padx=10)

    close_button = tk.Button(title_bar, text="X", bg=COLORS["button_bg"], fg=COLORS["fg"],
                             command=root.destroy, font=FONTS["kendiButon"], width=3)
    close_button.pack(side="right")

    frame1 = tk.Frame(root, width=300, height=200, bg="white", relief="solid", bd=1)
    frame1.place(relx=0.2, rely=0.5, anchor="center")

    image_path1 = "assets/img/analysis.png"
    img1 = Image.open(image_path1).resize((300, 200), Image.LANCZOS)
    photo1 = ImageTk.PhotoImage(img1)

    left_label = tk.Label(frame1, image=photo1)
    left_label.image = photo1
    left_label.pack()

    tk.Button(root, text="Dash'i Aç", bg="gray", fg="black",
              font=("Arial", 12), command=run_dash).place(relx=0.2, rely=0.75, anchor="center")

    frame2 = tk.Frame(root, width=300, height=200, bg="white", relief="solid", bd=1)
    frame2.place(relx=0.8, rely=0.5, anchor="center")

    image_path2 = "assets/img/monitoring.png"
    img2 = Image.open(image_path2).resize((300, 200), Image.LANCZOS)
    photo2 = ImageTk.PhotoImage(img2)

    right_label = tk.Label(frame2, image=photo2)
    right_label.image = photo2
    right_label.pack()

    tk.Button(root, text="Buton 2", bg="gray", fg="black",
              font=("Arial", 12), command=lambda: print("Buton 2'ye tıklandı!")).place(relx=0.8, rely=0.75, anchor="center")


# Arayüz
root = tk.Tk()
root.title("Login | Signin")
root.geometry("1920x1080")
root.configure(bg=COLORS["bg"])
root.overrideredirect(True)

bg_image = Image.open("assets/img/main.png").resize((1920, 1080), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

tk.Label(root, image=bg_photo).place(relwidth=1, relheight=1)

main_frame = tk.Frame(root, bg=COLORS["bg"], bd=2, relief="ridge", width=400, height=300)
main_frame.place(x=760, y=420)
main_frame.pack_propagate(False)

# İsim Soyisim
tk.Label(main_frame, text="İsim Soyisim", bg=COLORS["bg"], fg=COLORS["fg"], font=FONTS["label"]).grid(row=0, column=0, padx=(20, 10), pady=10, sticky="w")
name_entry = tk.Entry(main_frame, bg=COLORS["entry_bg"], fg=COLORS["fg"], font=FONTS["entry"], insertbackground='white', width=25)
name_entry.grid(row=0, column=1, ipady=5, pady=10, sticky="w")

# E-posta
tk.Label(main_frame, text="Gmail Adresi", bg=COLORS["bg"], fg=COLORS["fg"], font=FONTS["label"]).grid(row=1, column=0, padx=(20, 10), pady=10, sticky="w")
email_entry = tk.Entry(main_frame, bg=COLORS["entry_bg"], fg=COLORS["fg"], font=FONTS["entry"], insertbackground='white', width=25)
email_entry.grid(row=1, column=1, ipady=5, pady=10, sticky="w")

# Şifre
tk.Label(main_frame, text="Parola", bg=COLORS["bg"], fg=COLORS["fg"], font=FONTS["label"]).grid(row=2, column=0, padx=(20, 10), pady=10, sticky="w")
password_entry = tk.Entry(main_frame, show="*", bg=COLORS["entry_bg"], fg=COLORS["fg"], font=FONTS["entry"], insertbackground='white', width=25)
password_entry.grid(row=2, column=1, ipady=5, pady=10, sticky="w")

# Butonlar
button_frame = tk.Frame(main_frame, bg=COLORS["bg"])
button_frame.grid(row=3, column=0, columnspan=2, pady=20)

tk.Button(button_frame, text="Giriş Yap", command=login, bg=COLORS["button_bg"], fg=COLORS["fg"],
          activebackground=COLORS["button_active_bg"]["login"], activeforeground=COLORS["button_active_fg"],
          font=FONTS["button"], width=12).grid(row=0, column=0, padx=10)

tk.Button(button_frame, text="Kaydol", command=signup, bg=COLORS["button_bg"], fg=COLORS["fg"],
          activebackground=COLORS["button_active_bg"]["signup"], activeforeground=COLORS["button_active_fg"],
          font=FONTS["button"], width=12).grid(row=0, column=1, padx=10)

# Üst başlık çubuğu
title_bar = tk.Frame(root, bg=COLORS["bg"], relief="raised", bd=2)
title_bar.pack(side="top", fill="x")

tk.Label(title_bar, text="Giriş Ekranı", bg=COLORS["bg"], fg=COLORS["fg"], font=FONTS["label"]).pack(side="left", padx=10)
tk.Button(title_bar, text="X", bg=COLORS["button_bg"], fg=COLORS["fg"],
          command=root.destroy, font=FONTS["kendiButon"], width=3).pack(side="right")

root.mainloop()
