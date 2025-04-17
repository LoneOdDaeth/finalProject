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
    html.H3("🧠 Erlik", style={
        "color": "var(--text-green)",
        "margin-bottom": "30px",
        "textAlign": "center"
    }),

    html.Div([
        dbc.Nav([
            dbc.NavLink("👤 Profil", href="/profile", active="exact", className="custom-link"),
            dbc.NavLink("📊 Analiz", href="/analysis", active="exact", className="custom-link"),
            dbc.NavLink("🛠️ Admin Paneli", href="/admin", active="exact", className="custom-link"),
        ], vertical=True, pills=True)
    ]),

    html.Div([
        dbc.NavLink("🚪 Çıkış", href="/logout", active="exact", className="custom-link logout-link"),
    ], style={"margin-top": "auto"})
], className="sidebar-container", style={
    "width": "250px",
    "backgroundColor": "#1c1c1c",
    "padding": "20px",
    "height": "100vh",
    "display": "flex",
    "flexDirection": "column",
    "justifyContent": "space-between",
    "border": "none"
})

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
    "backgroundColor": "#1c1c1c",
    "padding": "10px 20px",
    "fontSize": "18px",
    "borderBottom": "none",
    "borderLeft": "none",
    "display": "flex",
    "alignItems": "center",
    "justifyContent": "space-between",
    "border-bottom": "none"
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
        "/profile": "Profil",
        "/analysis": "Analiz",
        "/export": "PDF & Rapor",
        "/settings": "Ayarlar",
        "/admin": "Admin Paneli",
    }
    return f"{page_names.get(pathname, 'Profil')}"

# Uygulamayı Başlat
if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    app.run(debug=True, port=8050)