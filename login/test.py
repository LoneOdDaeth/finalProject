import tkinter as tk

# Ana pencere oluştur
root = tk.Tk()
root.geometry("800x450")  # 1920x1080 formatının küçültülmüş hali

# COLORS ve FONTS sabitleri (örnek)
COLORS = {"bg": "black", "fg": "green", "button_bg": "gray"}
FONTS = {"label": ("Arial", 14), "button": ("Arial", 12), "kendiButon": ("Arial", 10)}

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

# Çerçeve ve buton 1
frame1 = tk.Frame(root, width=200, height=100, bg="white", relief="solid", bd=1)
frame1.place(relx=0.2, rely=0.75, anchor="center")

button1 = tk.Button(
    frame1, text="Buton 1", bg=COLORS["button_bg"], fg=COLORS["fg"],
    font=FONTS["button"], command=lambda: print("Buton 1'e tıklandı!")
)
button1.pack(expand=True, fill="both")

# Çerçeve ve buton 2
frame2 = tk.Frame(root, width=200, height=100, bg="white", relief="solid", bd=1)
frame2.place(relx=0.8, rely=0.75, anchor="center")

button2 = tk.Button(
    frame2, text="Buton 2", bg=COLORS["button_bg"], fg=COLORS["fg"],
    font=FONTS["button"], command=lambda: print("Buton 2'ye tıklandı!")
)
button2.pack(expand=True, fill="both")

root.mainloop()
