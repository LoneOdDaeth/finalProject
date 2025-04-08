from dash import html, dcc, Input, Output, State, callback
from utils.user_context import get_current_user
from database.mongo_operations import is_admin, get_smtp_settings, save_smtp_settings
import os

layout = html.Div([
    html.H2("⚙️ Sistem Ayarları", style={"text-align": "center", "color": "#00FF00"}),

    dcc.Store(id="password-visible", data=False),  # 👁️ durumu sakla

    html.Div(id="settings-content")
], style={"backgroundColor": "#000000", "color": "#00FF00", "padding": "20px", "font-family": "Arial, sans-serif"})


@callback(
    Output("settings-content", "children"),
    Input("password-visible", "data"),
    prevent_initial_call=False
)
def load_settings_content(password_visible):
    current_user = get_current_user()
    if not is_admin(current_user):
        return html.Div("❌ Bu sayfaya erişim izniniz yok.", style={"color": "red"})

    smtp_data = get_smtp_settings(current_user) or {
        "host": "",
        "port": "",
        "tls": None,
        "username": "",
        "password": "",
        "default_message": ""
    }

    warning = html.Div()
    if smtp_data.get("password"):
        warning = html.Div("⚠️ Eğer şifrenizi değiştirmediyseniz yeni bir ayar oluşturmayın.",
                           style={"color": "orange", "margin-bottom": "20px"})

    return html.Div([
        warning,

        html.H3("📧 SMTP Ayarları", style={"margin-top": "30px"}),

        html.Label("Gönderen Mail Adresi:"),
        dcc.Input(id="sender-email", type="email", style={"width": "100%"}, value=current_user, disabled=True),

        html.Label("SMTP Host:"),
        dcc.Input(id="smtp-host", type="text", style={"width": "100%"}, value=smtp_data.get("host", "")),

        html.Label("SMTP Port:"),
        dcc.Input(id="smtp-port", type="number", style={"width": "100%"}, value=smtp_data.get("port", "")),

        html.Label("TLS Kullanılsın mı?"),
        dcc.Dropdown(
            options=[
                {"label": "Evet", "value": True},
                {"label": "Hayır", "value": False}
            ],
            id="smtp-tls",
            style={"width": "100%"},
            value=smtp_data.get("tls", None)
        ),

        html.Label("SMTP Kullanıcı Adı (genellikle e-posta):"),
        dcc.Input(id="smtp-username", type="text", style={"width": "100%"}, value=smtp_data.get("username", "")),

        html.Label("SMTP Şifresi (Uygulama Şifresi):"),
        dcc.Input(
            id="smtp-password",
            type="password",
            style={"width": "100%"},
            value=smtp_data.get("password", "")
        ),

        html.Label("✏️ Varsayılan Mail Mesajı (hızlı paylaşım için):"),
        dcc.Textarea(
            id="default-mail-message",
            style={"width": "100%", "height": "100px"},
            value=smtp_data.get("default_message", "")
        ),

        html.Button("💾 Ayarları Kaydet", id="save-settings-btn", className="btn btn-success", style={"margin-top": "20px"}),

        html.Div(id="settings-feedback", style={"margin-top": "20px", "color": "lime"})
    ])


@callback(
    Output("settings-feedback", "children"),
    Input("save-settings-btn", "n_clicks"),
    State("smtp-host", "value"),
    State("smtp-port", "value"),
    State("smtp-tls", "value"),
    State("smtp-username", "value"),
    State("smtp-password", "value"),
    State("sender-email", "value"),
    State("default-mail-message", "value"),
    prevent_initial_call=True
)
def save_settings(n_clicks, host, port, tls, username, password, sender_email, default_message):
    if not all([host, port, tls is not None, username, password]):
        return "❌ Lütfen tüm alanları doldurun."

    save_smtp_settings(
        email=sender_email,
        host=host,
        port=port,
        tls=tls,
        username=username,
        password=password,
        default_message=default_message
    )

    return html.Div([
        html.P("✅ SMTP ayarları kaydedildi."),
        html.P(f"✏️ Varsayılan mesaj: {default_message[:50]}...", style={"color": "orange"})
    ])
