import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pages import home, profile, analysis, export  # Modüler sayfaları içe aktarıyoruz
import threading
import webbrowser
from utils.user_context import remove_current_user
import os
import time
from pages import admin

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050")

# Dash Uygulamasını Başlat
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Navbar (Menü)
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Ana Sayfa", href="/")),
        dbc.NavItem(dbc.NavLink("Analiz", href="/analysis")),
        dbc.NavItem(dbc.NavLink("Profil", href="/profile")),
        dbc.NavItem(dbc.NavLink("Dışa Aktarma & Mail", href="/export")),
        dbc.NavItem(dbc.NavLink("Çıkış Yap", href="/logout", style={"color": "red"}))
    ],
    brand="PCAP Analiz Arayüzü",
    brand_href="/",
    color="gray",
    dark=True,
)

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
        return analysis.layout
    elif pathname == "/profile":
        return profile.layout
    elif pathname == "/export":
        return export.layout
    elif pathname == "/admin":
        return admin.layout
    elif pathname == "/logout":
        remove_current_user()

        # Kullanıcıya sade bir mesaj göster
        def delayed_exit():
            time.sleep(1)  # 2 saniye bekle, sonra kapat
            os._exit(0)

        threading.Thread(target=delayed_exit, daemon=True).start()

        # Kullanıcıya sade ve izole bir mesaj göster
        return html.Div([
            html.H2("🔒 Oturum Sonlandırıldı", style={
                "text-align": "center",
                "color": "#FF4444",
                "margin-top": "200px"
            }),
            html.P("Uygulama kapatılıyor...", style={"text-align": "center", "color": "#FFFFFF"})
        ], style={
            "backgroundColor": "#000000",
            "height": "100vh",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "alignItems": "center",
            "font-family": "Arial, sans-serif"
        })

    else:
        return home.layout

# Uygulamayı Çalıştır
if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    app.run(debug=False, port=8050)
