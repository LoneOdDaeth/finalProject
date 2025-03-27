import os
import datetime
import plotly.graph_objects as go
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import webbrowser
import threading

img_dir = "tmp/images"
pdf_dir = "tmp/pdf"

# Klasörleri oluştur (varsa hata vermez)
os.makedirs(img_dir, exist_ok=True)
os.makedirs(pdf_dir, exist_ok=True)

GRAPH_DESCRIPTIONS = {
    "protocol_pie": "Ağ trafiğinde kullanılan protokollerin yüzdelik dağılımı.",
    "protocol_bar": "Her protokolün toplam kaç paket taşıdığını gösterir.",
    "src_ips": "Veri gönderen eşsiz IP adreslerinin dağılımı.",
    "dst_ips": "Veri alan hedef IP adreslerinin çeşitliliği.",
    "top_talkers": "En çok paket gönderen IP adresleri.",
    "time_series": "Paketlerin zaman içerisindeki sıklığını gösterir."
}

def save_plotly_figure(fig: go.Figure, filename: str):
    path = os.path.join(img_dir, filename)
    fig.write_image(path, format="png")
    return path

def generate_pdf_from_figures(figures_dict: dict, meta_info: dict, username: str):
    user_pdf_dir = os.path.join(pdf_dir, username)
    os.makedirs(user_pdf_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_path = os.path.join(user_pdf_dir, f"analysis_report_{timestamp}.pdf")

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    y_position = height - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y_position, "PCAP Analiz Raporu")
    y_position -= 30

    c.setFont("Helvetica", 10)
    for key, value in meta_info.items():
        c.drawString(50, y_position, f"{key}: {value}")
        y_position -= 15

    y_position -= 20

    for key, fig in figures_dict.items():
        img_filename = f"{key}.png"
        img_path = save_plotly_figure(fig, img_filename)

        if y_position < 250:
            c.showPage()
            y_position = height - 50

        img = ImageReader(img_path)
        c.drawImage(img, 50, y_position - 200, width=500, height=200)

        y_position -= 210
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(50, y_position, GRAPH_DESCRIPTIONS.get(key, ""))
        y_position -= 40

    c.save()

    def open_pdf(path):
        try:
            abs_path = os.path.abspath(path)
            webbrowser.open_new_tab(f"file://{abs_path}")
        except:
            pass

    threading.Thread(target=open_pdf, args=(pdf_path,), daemon=True).start()

    return pdf_path