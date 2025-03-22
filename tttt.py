import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Dash Uygulamasını Başlat
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])  # Dark Tema Kullanıyoruz

# Navbar (Üst Menü) - Yeşil Vurgulu
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Ana Sayfa", href="/")),
        dbc.NavItem(dbc.NavLink("Analiz", href="/analysis")),
        dbc.NavItem(dbc.NavLink("Profil", href="/profile")),
        dbc.NavItem(dbc.NavLink("Dışa Aktarma & Mail", href="/export"))
    ],
    brand="PCAP Analiz Arayüzü",
    brand_href="/",
    color="#222222",
    dark=True,
)

# Genel Sayfa Stili - Arka Plan Siyah ve Tam Ekran
page_style = {
    "backgroundColor": "#000000",  # ✅ Tamamen Siyah Arka Plan
    "color": "#00FF00",
    "display": "flex",
    "flexDirection": "column",
    "alignItems": "center",  # İçeriği yatayda ortala
    "justifyContent": "center",  # İçeriği dikeyde ortala
    "padding": "100px",
    "font-family": "Arial, sans-serif"
}

# Ana Sayfa (PCAP Yükleme ve Resim Ekleme)
home_layout = html.Div([
    dbc.Row([
        dbc.Col(
            dcc.Upload(
                id="upload-pcap",
                children=html.Button("PCAP Dosyası Seç", className="btn btn-success"),
                multiple=False
            ),
            width={"size": 2, "offset": 0},  # ✅ Buton Sol Üstte Navbarın Altında
        )
    ], style={"width": "100%", "justifyContent": "start"}),  # ✅ Butonu sola yasla

    html.Div([
        html.H2("PCAP Analiz Arayüzüne Hoş Geldiniz", style={
            "text-align": "center",
            "color": "#00FF00",
            "margin-top": "auto",
            "margin-bottom": "20px"
        }),

        html.P("Lütfen analiz etmek istediğiniz PCAP dosyanızı yükleyin.",
               style={"text-align": "center"}),
    ], style={"width": "100%"}),

    # Resimleri Daha Aşağı ve Esnek Yerleştirme
    dbc.Row([
        dbc.Col(html.Img(src="/assets/img/ip_sutun.png", 
                         style={"width": "500px", "height": "300px", "margin": "10px"}), 
                width=4, style={"text-align": "left"}),  # ✅ Sol Tarafa Yasla
        
        dbc.Col(html.Img(src="/assets/img/pasta.png", 
                         style={"width": "400px", "height": "300px", "margin": "10px"}), 
                width=4, style={"text-align": "center"}),  # ✅ Ortada
        
        dbc.Col(html.Img(src="/assets/img/zaman.png", 
                         style={"width": "500px", "height": "300px", "margin": "10px"}), 
                width=4, style={"text-align": "right"})  # ✅ Sağa Yasla
    ], style={"margin-top": "125px"})  # ✅ Resimleri Daha Aşağı İndir

], style=page_style)

# Analiz Sayfası
analysis_layout = html.Div([
    html.H2("Analiz Sayfası", style={"text-align": "center", "color": "#00FF00"}),
    html.P("Yüklenen PCAP dosyası burada analiz edilecektir."),
    html.Div(id="analysis-output")
], style=page_style)

# Profil Sayfası
profile_layout = html.Div([
    html.H2("Kullanıcı Profili", style={"text-align": "center", "color": "#00FF00"}),
    html.P("Burada kullanıcı bilgilerini ve kayıtlı analizleri görebileceksiniz."),
    html.Div(id="profile-output")
], style=page_style)

# Dışa Aktarma & Mail Sayfası
export_layout = html.Div([
    html.H2("Dışa Aktarma ve Mail Gönderme", style={"text-align": "center", "color": "#00FF00"}),
    html.P("Seçtiğiniz analizleri PDF olarak dışa aktarabilir ve yöneticinize e-posta ile gönderebilirsiniz."),
    dbc.Button("📄 PDF Oluştur", id="generate-pdf", color="success"),
    dbc.Button("📩 Mail Gönder", id="send-mail", color="info"),
    html.Div(id="export-output")
], style=page_style)

# Sayfa İçeriği Güncelleme
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    navbar,
    html.Div(id="page-content")
])

# Sayfa Yönlendirme
@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/analysis":
        return analysis_layout
    elif pathname == "/profile":
        return profile_layout
    elif pathname == "/export":
        return export_layout
    else:
        return home_layout

# Uygulamayı Çalıştır
if __name__ == "__main__":
    app.run(debug=True)
