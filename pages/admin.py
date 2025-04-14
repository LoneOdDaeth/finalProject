from dash import html, dcc, Input, Output, State, callback, callback_context
from utils.user_context import get_current_user
import datetime
from database.mongo_operations import (
    is_admin, get_admin_list, add_admin, get_all_users, remove_admin, get_all_mail_logs
)

current_user = get_current_user()

if not is_admin(current_user):
    layout = html.Div([
        html.H2("❌ Yetkisiz Erişim", style={"color": "red", "text-align": "center"}),
        html.P("Bu sayfayı görüntülemek için admin olmalısınız.", style={"text-align": "center"})
    ], style={"backgroundColor": "#1E2124", "color": "#FFF", "padding": "50px", "minHeight": "95vh"})
else:
    layout = html.Div([
        dcc.Location(id="admin-url", refresh=False),
        
        # Özel İşlem butonu sağ üstte
        html.Div([
            html.Button("🛠️ Özel İşlem Başlat", 
                    id="custom-admin-btn", 
                    n_clicks=0,
                    className="admin-btn-success",
                    style={"padding": "8px 20px"})
        ], style={"display": "flex", "justify-content": "flex-end", "margin-bottom": "25px"}),

        # Admin ve Kullanıcı Yönetimi Satırı
        html.Div([
            # Sol Sütun
            html.Div([
                # Admin Listesi Kartı
                html.Div([
                    html.Div([
                        html.H5("👑 Yetkili Adminler", className="admin-title"),
                        html.Div([
                            html.Ul(
                                id="admin-list-display",
                                className="admin-list"
                            )
                        ], className="card-content-scroll")
                    ], style={"padding": "15px"})
                ], className="admin-card fixed-height-card"),
                
                # Kullanıcı Listesi Kartı
                html.Div([
                    html.Div([
                        html.H5("👥 Kayıtlı Kullanıcılar", className="admin-title"),
                        html.Div([
                            html.Ul(id="user-list-display", className="admin-list")
                        ], className="card-content-scroll")
                    ], style={"padding": "15px"})
                ], className="admin-card fixed-height-card")
            ], className="admin-column"),
            
            # Sağ Sütun
            html.Div([
                # Yeni Admin Ekleme Kartı
                html.Div([
                    html.Div([
                        html.H5("➕ Yeni Admin Ekle", className="admin-title"),
                        html.Div([
                            dcc.Dropdown(
                                id="new-admin-dropdown",
                                placeholder="Bir kullanıcı seçin...",
                                style={"color": "#000000", "margin-bottom": "15px"}
                            ),
                            html.Button("Admin Olarak Ekle", 
                                        id="add-admin-btn", 
                                        n_clicks=0,
                                        className="admin-btn-success")
                        ], className="admin-form-group"),
                        html.Div(id="add-admin-feedback", 
                                 style={"margin-top": "15px", "color": "#00FF00"})
                    ], style={"padding": "15px"})
                ], className="admin-card fixed-height-card"),
                
                # Admin Silme Kartı
                html.Div([
                    html.Div([
                        html.H5("❌ Admin Sil", className="admin-title"),
                        html.Div([
                            dcc.Dropdown(
                                id="admin-remove-dropdown",
                                placeholder="Admin seçin...",
                                style={"color": "#000000", "margin-bottom": "15px"}
                            ),
                            html.Button("Adminliği Kaldır", 
                                        id="remove-admin-btn", 
                                        n_clicks=0,
                                        className="admin-btn-danger")
                        ], className="admin-form-group"),
                        html.Div(id="remove-admin-feedback", 
                                 style={"margin-top": "15px", "color": "#FF4444"})
                    ], style={"padding": "15px"})
                ], className="admin-card fixed-height-card")
            ], className="admin-column")
        ], className="admin-section"),

        # Mail Log Kartı
        html.Div([
            html.Div([
                html.H5("📬 Gönderilen Mail Kayıtları", className="admin-title"),
                html.Div(id="mail-log-section", className="admin-scrollable", 
                         style={"maxHeight": "400px"})
            ], style={"padding": "15px"})
        ], className="admin-card")

    ], style={
        "backgroundColor": "#1E2124",
        "color": "#FFF",
        "padding": "20px",
        "font-family": "Arial, sans-serif",
        "minHeight": "95vh"
    })

@callback(
    Output("admin-remove-dropdown", "options"),
    Input("admin-url", "pathname"),
    Input("add-admin-feedback", "children"),
    Input("remove-admin-feedback", "children"),
    prevent_initial_call=False
)
def update_admin_dropdown(_, add_feedback, remove_feedback):
    admin_list = get_admin_list()
    return [{"label": admin["_id"], "value": admin["_id"]} for admin in admin_list]


@callback(
    Output("new-admin-dropdown", "options"),
    Input("add-admin-btn", "n_clicks"),
    prevent_initial_call=False
)
def populate_user_dropdown(n):
    users = get_all_users()
    return [{"label": user["_id"], "value": user["_id"]} for user in users]


@callback(
    Output("add-admin-feedback", "children"),
    Input("add-admin-btn", "n_clicks"),
    State("new-admin-dropdown", "value"),
    prevent_initial_call=True
)
def handle_add_admin(n_clicks, selected_email):
    if not selected_email:
        return "❌ Lütfen bir kullanıcı seçin."

    current_user = get_current_user()
    success, message = add_admin(selected_email, current_user)
    return message


@callback(
    Output("remove-admin-feedback", "children"),
    Input("remove-admin-btn", "n_clicks"),
    State("admin-remove-dropdown", "value"),
    prevent_initial_call=True
)
def handle_remove_admin(n_clicks, selected_admin_email):
    if not selected_admin_email:
        return "❌ Lütfen silmek için bir admin seçin."

    current_user = get_current_user()
    success, message = remove_admin(selected_admin_email, current_user)
    return message


@callback(
    Output("admin-list-display", "children"),
    Input("add-admin-feedback", "children"),
    Input("remove-admin-feedback", "children"),
    Input("admin-url", "pathname"),
    prevent_initial_call=False
)
def update_admin_display(_, __, ___):
    admin_list = get_admin_list()
    return [html.Li(admin["_id"]) for admin in admin_list]

@callback(
    Output("mail-log-section", "children"),
    Input("admin-url", "pathname"),
    prevent_initial_call=False
)
def render_mail_logs(_):
    logs = get_all_mail_logs()
    if not logs:
        return html.P("📭 Henüz gönderilen mail kaydı yok.", style={"color": "gray"})

    headers = ["Tarih", "Gönderen", "Alıcı", "Konu", "Dosya Adı"]
    table_head = html.Tr([html.Th(h) for h in headers])

    table_rows = []
    for log in logs:
        time = datetime.datetime.fromisoformat(log["timestamp"]).strftime("%d.%m.%Y %H:%M")
        table_rows.append(html.Tr([
            html.Td(time),
            html.Td(log["sender"]),
            html.Td(log["recipient"]),
            html.Td(log["subject"]),
            html.Td(log.get("attachment_name", "—"))
        ]))

    return html.Table([html.Thead(table_head), html.Tbody(table_rows)], 
                     className="admin-mail-table")

@callback(
    Output("user-list-display", "children"),
    Input("admin-url", "pathname"),
    prevent_initial_call=False
)
def render_user_list(_):
    users = get_all_users()
    return [
        html.Li(
            dcc.Link(user["_id"], href=f"/profile?user={user['_id']}", 
                    style={"color": "var(--text-green)"})
        )
        for user in users
    ]