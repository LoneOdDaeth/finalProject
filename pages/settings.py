from dash import html, dcc, Input, Output, State, callback
from utils.user_context import get_current_user
from database.mongo_operations import is_admin
import json
import os

SETTINGS_FILE = "config/smtp_settings.json"

layout = html.Div([
    html.H2("⚙️ Sistem Ayarları", style={"text-align": "center", "color": "#00FF00"}),

    html.Div(id="settings-content")
], style={"backgroundColor": "#000000", "color": "#00FF00", "padding": "20px", "font-family": "Arial, sans-serif"})


@callback(
    Output("settings-content", "children"),
    Input("settings-content", "id"),
    prevent_initial_call=False
)
def load_settings_content(_):
    current_user = get_current_user()
    if not is_admin(current_user):
        return html.Div("❌ Bu sayfaya erişim izniniz yok.", style={"color": "red"})

    return html.Div([
        html.H3("📧 SMTP Ayarları", style={"margin-top": "30px"}),

        html.Div([
            html.Label("Gönderen Mail Adresi:"),
            dcc.Input(id="sender-email", type="email", style={"width": "100%"}, value=current_user, disabled=True),

            html.Label("SMTP Host:"),
            dcc.Input(id="smtp-host", type="text", style={"width": "100%"}),

            html.Label("SMTP Port:"),
            dcc.Input(id="smtp-port", type="number", style={"width": "100%"}),

            html.Label("TLS Kullanılsın mı?"),
            dcc.Dropdown(
                options=[
                    {"label": "Evet", "value": True},
                    {"label": "Hayır", "value": False}
                ],
                id="smtp-tls",
                style={"width": "100%"}
            ),

            html.Button("💾 Ayarları Kaydet", id="save-settings-btn", className="btn btn-success", style={"margin-top": "10px"}),

            html.Div(id="settings-feedback", style={"margin-top": "20px", "color": "lime"})
        ], style={"margin-top": "30px"})
    ])


@callback(
    Output("settings-feedback", "children"),
    Input("save-settings-btn", "n_clicks"),
    State("smtp-host", "value"),
    State("smtp-port", "value"),
    State("smtp-tls", "value"),
    prevent_initial_call=True
)
def save_settings(n_clicks, host, port, tls):
    if not all([host, port, tls is not None]):
        return "❌ Lütfen tüm alanları doldurun."

    settings = {
        "host": host,
        "port": port,
        "tls": tls
    }

    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)

    return "✅ SMTP ayarları kaydedildi."
