from dash import html
from utils.user_context import *
from database.mongo_operations import *

username = get_current_user()

dummy_user = {
    "role": "Yönetici",
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

layout = html.Div([
    html.H2("Kullanıcı Profili", style={"text-align": "center", "color": "#00FF00"}),
    
    html.Div([
        html.P(f"👤 User: {username}", style={"font-size": "18px"}),
        html.P(f"🔰 Yetki: {dummy_user['role']}", style={"font-size": "18px", "font-weight": "bold"})
    ], style={"margin-bottom": "20px"}),

    html.H4("📊 Kayıtlı Analizler:", style={"margin-top": "20px", "color": "#00FF00"}),
    html.Ul([html.Li(f"{analysis['name']} - {analysis['date']}") for analysis in dummy_user["analyses"]]),

    html.Div([
        html.H4("👥 Ekip Üyeleri:", style={"margin-top": "20px", "color": "#00FF00"}),
        html.Ul([html.Li(f"{member['name']} - {member['email']} ({member['role']})") for member in dummy_user["team"]])
    ]) if dummy_user["role"] == "Yönetici" else None
], style={"backgroundColor": "#000000", "color": "#00FF00", "padding": "20px", "font-family": "Arial, sans-serif"})
