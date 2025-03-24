from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import base64
import os
import datetime
import json
from pcap_processing.pcap_parser import analyze_pcap
from database.mongo_operations import save_analysis
from utils.user_context import *

upload_path = "assets/uploads"
tmp_path = "tmp"

layout = html.Div([
    dbc.Row([
        dbc.Col(
            dcc.Upload(
                id="upload-pcap",
                children=html.Button("PCAP Dosyası Seç", className="btn btn-success"),
                multiple=False
            ),
            width={"size": 2, "offset": 0},  
        )
    ], style={"width": "100%", "justifyContent": "start"}),

    html.Div(id="upload-message", style={"margin-top": "10px"}),

    html.Div([
        html.H2("PCAP Analiz Arayüzüne Hoş Geldiniz", style={
            "text-align": "center",
            "color": "#00FF00",
            "margin-top": "auto",
            "margin-bottom": "20px"
        }),

        html.P("Lütfen analiz etmek istediğiniz PCAP dosyanızı yükleyin.",
               style={"text-align": "center"}),
    ], style={"width": "100%", "padding": "80px"}),

    dbc.Row([
        dbc.Col(html.Img(src="/assets/img/ip_sutun.png", 
                         style={"width": "500px", "height": "300px", "margin": "10px"}), width=4, style={"text-align": "left"}),
        dbc.Col(html.Img(src="/assets/img/pasta.png", 
                         style={"width": "400px", "height": "300px", "margin": "10px"}), width=4, style={"text-align": "center"}),
        dbc.Col(html.Img(src="/assets/img/zaman.png", 
                         style={"width": "500px", "height": "300px", "margin": "10px"}), width=4, style={"text-align": "right"})
    ], style={"margin-top": "125px"})
], style={"backgroundColor": "#000000", "color": "#00FF00", "padding": "20px", "font-family": "Arial, sans-serif"})


@callback(
    Output("upload-message", "children"),
    Input("upload-pcap", "contents"),
    State("upload-pcap", "filename")
)
def handle_upload(content, filename):
    if content is None:
        return ""

    try:
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(upload_path, new_filename)

        # Dosyayı kaydet
        with open(filepath, "wb") as f:
            f.write(decoded)

        # Analiz et
        result = analyze_pcap(filepath)

        # JSON olarak tmp klasörüne yaz
        json_name = f"{new_filename}.json"
        json_path = os.path.join(tmp_path, json_name)
        with open(json_path, "w") as jf:
            json.dump(result, jf, indent=4)

        username = get_current_user()

        timestamp_iso = datetime.datetime.now().isoformat()

        # Mongo'ya kaydet
        save_analysis(username, new_filename, timestamp_iso, result)

        # PCAP dosyasını sil
        os.remove(filepath)

        return html.Div(f"✅ Dosya analiz edildi ve kayıt edildi: {json_name}")

    except Exception as e:
        return html.Div(f"❌ Hata: {str(e)}")
