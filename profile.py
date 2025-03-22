import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Dash Uygulamasını Başlat
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Dummy Kullanıcı Verileri
dummy_user = {
    "name": "Selim Oğuz Şahin",
    "email": "selim@example.com",
    "role": "Yönetici",  # "Analist", "Uzman" veya "Yönetici" olabilir
    "analyses": [
        {"id": 1, "name": "Analiz 1", "date": "2025-03-10"},
        {"id": 2, "name": "Analiz 2", "date": "2025-03-12"},
        {"id": 3, "name": "Analiz 3", "date": "2025-03-15"}
    ],
    "team": [
        {"name": "Ali Can", "email": "ali@example.com", "role": "Analist"},
        {"name": "Zeynep Yılmaz", "email": "zeynep@example.com", "role": "Uzman"}
    ]
}

# Navbar
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

# Sayfa Stili
page_style = {
    "backgroundColor": "#000000",
    "color": "#00FF00",
    "padding": "20px",
    "font-family": "Arial, sans-serif"
}

# Kullanıcı Profili Sekmesi
profile_layout = html.Div([
    html.H2("Kullanıcı Profili", style={"text-align": "center", "color": "#00FF00"}),
    
    # Kullanıcı Bilgileri
    html.Div([
        html.P(f"👤 Ad: {dummy_user['name']}", style={"font-size": "18px"}),
        html.P(f"📧 E-posta: {dummy_user['email']}", style={"font-size": "18px"}),
        html.P(f"🔰 Yetki: {dummy_user['role']}", style={"font-size": "18px", "font-weight": "bold"})
    ], style={"margin-bottom": "20px"}),

    html.H4("📊 Kayıtlı Analizler:", style={"margin-top": "20px", "color": "#00FF00"}),
    html.Ul([
        html.Li(f"{analysis['name']} - {analysis['date']}")
        for analysis in dummy_user["analyses"]
    ], style={"font-size": "16px"}),

    # Eğer kullanıcı "Yönetici" ise ekibi göster
    html.Div([
        html.H4("👥 Ekip Üyeleri:", style={"margin-top": "20px", "color": "#00FF00"}),
        html.Ul([
            html.Li(f"{member['name']} - {member['email']} ({member['role']})")
            for member in dummy_user["team"]
        ], style={"font-size": "16px"})
    ]) if dummy_user["role"] == "Yönetici" else None
], style=page_style)

# Sayfa Yönlendirme
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    navbar,
    html.Div(id="page-content")
])

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    if pathname == "/profile":
        return profile_layout
    else:
        return html.Div(html.H2("Diğer Sayfalar İçin Menüden Seçim Yapın", style={"text-align": "center", "color": "#00FF00"}))

# Uygulamayı Çalıştır
if __name__ == "__main__":
    app.run(debug=True)
