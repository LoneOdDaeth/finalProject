from dash import html, dcc, Input, Output, State, callback
from utils.user_context import get_current_user
from database.mongo_operations import (
    is_admin, get_admin_list, add_admin, get_all_users, remove_admin, get_user_name_by_email
)

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

    ], style={"display": "flex", "gap": "20px", "margin-top": "30px", "flex-wrap": "wrap"})

], style={
    "backgroundColor": "#000000",
    "color": "#00FF00",
    "padding": "20px",
    "font-family": "Arial, sans-serif"
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
    return [{"label": get_user_name_by_email(admin["_id"]), "value": admin["_id"]} for admin in admin_list]


@callback(
    Output("new-admin-dropdown", "options"),
    Input("add-admin-btn", "n_clicks"),
    prevent_initial_call=False
)
def populate_user_dropdown(n):
    users = get_all_users()
    return [{"label": get_user_name_by_email(user["_id"]), "value": user["_id"]} for user in users]


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
    return [html.Li(get_user_name_by_email(admin["_id"])) for admin in admin_list]
