from dash import dcc, html
import dash_bootstrap_components as dbc

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

    # Resimler
    dbc.Row([
        dbc.Col(html.Img(src="/assets/img/ip_sutun.png", 
                         style={"width": "500px", "height": "300px", "margin": "10px"}), width=4, style={"text-align": "left"}),
        dbc.Col(html.Img(src="/assets/img/pasta.png", 
                         style={"width": "400px", "height": "300px", "margin": "10px"}), width=4, style={"text-align": "center"}),
        dbc.Col(html.Img(src="/assets/img/zaman.png", 
                         style={"width": "500px", "height": "300px", "margin": "10px"}), width=4, style={"text-align": "right"})
    ], style={"margin-top": "125px"})
], style={"backgroundColor": "#000000", "color": "#00FF00", "padding": "20px", "font-family": "Arial, sans-serif"})
