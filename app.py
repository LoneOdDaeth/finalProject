import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pages import home, profile, analysis, export, settings, mail_interface, admin
from utils.user_context import remove_current_user
import threading
import webbrowser
import os
import time

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050")

# Dash Uygulamasını Başlat (GÜNCELLEME BURADA ⬇)
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True  # 🛡️ Bu kritik satır!
)
server = app.server  # Eğer dışarıdan deploy yapılacaksa

# Navbar (Menü)
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Ana Sayfa", href="/")),
        dbc.NavItem(dbc.NavLink("Ayarlar", href="/settings")),
        dbc.NavItem(dbc.NavLink("Analiz", href="/analysis")),
        dbc.NavItem(dbc.NavLink("Profil", href="/profile")),
        dbc.NavItem(dbc.NavLink("Dışa Aktarma", href="/export")),
        dbc.NavItem(dbc.NavLink("Mail", href="/mail-interface")),
        dbc.NavItem(dbc.NavLink("Çıkış Yap", href="/logout", style={"color": "red"}))
    ],
    brand="PCAP Analiz Arayüzü",
    brand_href="/",
    color="gray",
    dark=True,
)

# Sayfa İçeriği
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    navbar,
    html.Div(id="page-content")
])

# Sayfa Yönlendirme Callback
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
    elif pathname == "/settings":
        return settings.layout
    elif pathname == "/mail-interface":
        return mail_interface.layout
    elif pathname == "/logout":
        remove_current_user()

        # Uygulamayı kapatmadan önce kullanıcıya mesaj göster
        def delayed_exit():
            time.sleep(1)
            os._exit(0)

        threading.Thread(target=delayed_exit, daemon=True).start()

        return html.Div([
            html.H2("🔒 Oturum Sonlandırıldı", style={
                "text-align": "center",
                "color": "#FF4444",
                "margin-top": "200px"
            }),
            html.P("Uygulama kapatılıyor...", style={
                "text-align": "center",
                "color": "#FFFFFF"
            })
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

# Uygulamayı Başlat
if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    app.run(debug=False, port=8050)
