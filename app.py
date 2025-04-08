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
sidebar = html.Div([
    html.H3("🧠 Erlik", style={"color": "#00FF00", "margin-bottom": "30px"}),

    html.Div([  # Menü kısmı
        dbc.Nav([
            dbc.NavLink("👤 Profil", href="/profile", active="exact", className="custom-link"),
            dbc.NavLink("📊 Analiz", href="/analysis", active="exact", className="custom-link"),
            dbc.NavLink("📄 PDF & Dışa Aktar", href="/export", active="exact", className="custom-link"),
            dbc.NavLink("⚙️ Ayarlar", href="/settings", active="exact", className="custom-link"),
            dbc.NavLink("🛠️ Admin Paneli", href="/admin", active="exact", className="custom-link"),
        ], vertical=True, pills=True)
    ]),

    html.Div([  # Çıkış kısmı
        dbc.NavLink("🚪 Çıkış", href="/logout", active="exact", className="custom-link logout-link"),
    ], style={"margin-top": "auto"})  # otomatik alta yasla
], style={
    "width": "250px",
    "backgroundColor": "#1c1c1c",
    "padding": "20px",
    "height": "100vh",
    "display": "flex",
    "flexDirection": "column",
    "justifyContent": "space-between"
})


# Sayfa İçeriği
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div([sidebar], style={"width": "250px"}),
    html.Div(id="page-content", style={"flex": 1, "padding": "20px"})
], style={
    "display": "flex",
    "height": "100vh",
    "backgroundColor": "#000000"
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
            "backgroundColor": "#000000",
            "height": "100vh",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "center",
            "alignItems": "center",
            "font-family": "Arial, sans-serif"
        })
    else:
        return profile.layout

# Uygulamayı Başlat
if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    app.run(debug=True, port=8050)