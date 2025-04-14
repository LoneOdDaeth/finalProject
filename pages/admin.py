from dash import html, dcc, Input, Output, State, callback
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

        html.H2("🛠️ Yönetim Paneli", style={
            "text-align": "center",
            "margin-bottom": "30px",
            "color": "#FFD700"
        }),

        html.H4("👑 Yetkili Adminler:", style={"margin-bottom": "10px"}),

        html.Ul(
            id="admin-list-display",
            style={"list-style-type": "circle", "margin-left": "20px"}
        ),

        html.Hr(style={"margin": "30px 0"}),

        html.Div([

            html.Div([
                html.H4("➕ Yeni Admin Ekle", style={"margin-bottom": "10px"}),

                dcc.Dropdown(
                    id="new-admin-dropdown",
                    placeholder="Bir kullanıcı seçin...",
                    style={"width": "100%", "color": "#000000"}
                ),

                html.Button("Admin Olarak Ekle", id="add-admin-btn", n_clicks=0,
                            className="btn btn-success", style={"margin-top": "10px"}),

                html.Div(id="add-admin-feedback", style={"margin-top": "15px", "color": "#00FF00"})
            ], style={"flex": "1", "margin-right": "30px"}),

            html.Div([
                html.H4("❌ Admin Sil", style={"margin-bottom": "10px"}),

                dcc.Dropdown(
                    id="admin-remove-dropdown",
                    placeholder="Admin seçin...",
                    style={"width": "100%", "color": "#000000", "margin-bottom": "10px"}
                ),

                html.Button("Adminliği Kaldır", id="remove-admin-btn", n_clicks=0,
                            className="btn btn-danger"),

                html.Div(id="remove-admin-feedback", style={"margin-top": "15px", "color": "#FF4444"})
            ], style={"flex": "1"})

        ], style={"display": "flex", "gap": "20px", "margin-top": "30px", "flex-wrap": "wrap"}),

        # 🔽 Yeni eklenen mail log alanı
        html.Hr(style={"margin": "40px 0"}),
        html.Div(id="mail-log-section", style={"margin-top": "30px"}),

        html.Hr(style={"margin": "40px 0"}),

        html.Div([
            html.H4("👥 Kayıtlı Kullanıcılar", style={"margin-bottom": "10px"}),
            html.Ul(id="user-list-display", style={"margin-left": "20px"})
        ])


    ], style={
        "backgroundColor": "#1E2124",
        "color": "#00FF00",
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

    return html.Div([
        html.H4("📬 Gönderilen Mail Kayıtları", style={"margin-bottom": "20px"}),
        html.Table([table_head] + table_rows, style={
            "width": "100%",
            "border": "1px solid #00FF00",
            "borderCollapse": "collapse",
            "textAlign": "left"
        })
    ])

@callback(
    Output("user-list-display", "children"),
    Input("admin-url", "pathname"),
    prevent_initial_call=False
)
def render_user_list(_):
    users = get_all_users()
    return [
        html.Li(
            dcc.Link(user["_id"], href=f"/profile?user={user['_id']}", style={"color": "#00FF00"})
        )
        for user in users
    ]
