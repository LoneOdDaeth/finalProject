import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pages import home, profile, analysis, export  # Modüler sayfaları içe aktarıyoruz
import threading
import webbrowser

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
        dbc.NavItem(dbc.NavLink("Dışa Aktarma & Mail", href="/export"))
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
    else:
        return home.layout

# Uygulamayı Çalıştır
if __name__ == "__main__":
    threading.Timer(1.5, open_browser).start()
    app.run(debug=False, port=8050)
