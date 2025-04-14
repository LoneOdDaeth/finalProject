import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pages import profile, analysis, export, settings, admin
from utils.user_context import remove_current_user
import threading
import webbrowser
import os
import time

def open_browser():
    webbrowser.open_new("http://127.0.0.1:8050")

# Dash Uygulamasını Başlat
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.DARKLY],
    suppress_callback_exceptions=True
)
server = app.server

# Sidebar (Yana alınmış menü)
sidebar = dbc.NavbarSimple([
    html.Div([
        html.H2("🧠 Erlik", style={"color": "#2ecc71", "marginBottom": "40px"}),

        dcc.Link("👤 Profil", href="/profile", className="custom-link", id="link-profile"),
        dcc.Link("📊 Analiz", href="/analysis", className="custom-link", id="link-analysis"),
        dcc.Link("📄 PDF & Rapor", href="/export", className="custom-link", id="link-export"),
        dcc.Link("⚙️ Ayarlar", href="/settings", className="custom-link", id="link-settings"),
        dcc.Link("🛠️ Admin Paneli", href="/admin", className="custom-link", id="link-admin"),

        html.Div([
            dcc.Link("📜 Çıkış", href="/logout", className="custom-link logout-link")
        ], style={"marginTop": "auto"})
    ], className="sidebar-container")
], color="dark", dark=True)

# Header bileşeni
header_bar = html.Div([
    html.Div(id="current-page-title", style={
        "color": "#FFFFFF",
        "fontSize": "30px",
        "fontWeight": "bold",
        "marginRight": "auto"
    }),
    html.A("🧠 Erlik", style={
        "color": "#00FF00",
        "textDecoration": "none",
        "fontWeight": "bold",
        "fontSize": "20px",
        "marginLeft": "20px"
    })
], style={
    "width": "100%",
    "height": "100px",
    "backgroundColor": "#1c1c24",
    "padding": "10px 20px",
    "fontSize": "18px",
    "borderBottom": "2px solid #2ecc71",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "space-between"
})


app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div([sidebar], style={"width": "250px"}),
    html.Div([
        header_bar,  # Her sayfanın üstünde sabit header
        html.Div(id="page-content", style={"flex": 1, "padding": "20px"})
    ], style={
        "flex": 1,
        "display": "flex",
        "flexDirection": "column"
    })
], style={
    "display": "flex",
    "minHeight": "100vh",
    "backgroundColor": "#1E2124",
})

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
    elif pathname == "/logout":
        remove_current_user()

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
            "backgroundColor": "#1E2124",
            "height": "100vh",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "alignItems": "center",
            "font-family": "Arial, sans-serif"
        })
    else:
        return profile.layout
    
@app.callback(
    Output("current-page-title", "children"),
    Input("url", "pathname")
)
def update_header(pathname):
    page_names = {
        "/profile": "Profil Sayfası",
        "/analysis": "Analiz Sayfası",
        "/export": "PDF & Rapor Sayfası",
        "/settings": "Ayarlar",
        "/admin": "Admin Paneli",
    }
    return f"{page_names.get(pathname, 'Profil Sayfası')}"

# Uygulamayı Başlat
if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    app.run(debug=False, port=8050)