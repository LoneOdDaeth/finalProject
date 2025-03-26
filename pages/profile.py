from dash import html, dcc, Input, Output, callback, MATCH
from utils.user_context import get_current_user
from database.mongo_operations import *
import urllib.parse as urlparse
from urllib.parse import parse_qs

username = get_current_user()

layout = html.Div([
    dcc.Location(id="page-url", refresh=False),

    html.H2("Kullanıcı Profili", style={"text-align": "center", "color": "#00FF00"}),

    html.Div(id="user-info", style={"margin-bottom": "20px"}),

    html.Div(id="user-analyses"),

    html.Div(id="user-list-section", style={"margin-top": "40px"}),

    html.Div(id="pdf-history-section", style={"margin-top": "40px"}),

    html.Div(id="pdf-open-feedback", style={"margin-top": "20px", "color": "red"})
], style={
    "backgroundColor": "#000000",
    "color": "#00FF00",
    "padding": "20px",
    "font-family": "Arial, sans-serif"
})


@callback(
    Output("user-info", "children"),
    Output("user-analyses", "children"),
    Output("user-list-section", "children"),
    Output("pdf-history-section", "children"),
    Input("page-url", "search"),
    prevent_initial_call=False
)
def render_profile(search):
    if not username:
        return html.Div("🔒 Giriş yapılmamış.", style={"color": "red"}), "", "", ""

    selected_user = username
    if search:
        parsed = urlparse.urlparse(search)
        params = parse_qs(parsed.query)
        if "user" in params:
            selected_user = params["user"][0]

    user_analyses = get_user_analyses(selected_user)

    user_info = html.Div([
        html.P(f"👤 User: {selected_user}", style={"font-size": "18px"}),
        html.P("🔰 Yetki: Yönetici (şimdilik tüm kullanıcılar eşit)")
    ])

    analysis_list = html.Ul([
        html.Li(
            dcc.Link(
                f"{a['filename']} – {a['timestamp']}",
                href=f"/analysis?id={a['filename']}"
            )
        ) for a in user_analyses
    ]) if user_analyses else html.P("Bu kullanıcı için analiz bulunamadı.")

    all_users = get_all_users()
    user_links = html.Ul([
        html.Li(dcc.Link(user["_id"], href=f"/profile?user={user['_id']}"))
        for user in all_users if user["_id"] != username
    ])

    user_list_section = html.Div([
        html.H4("👥 Kullanıcı Listesi:"),
        user_links
    ])

    user_pdfs = get_user_pdfs(selected_user)

    pdf_list = html.Ul([
        html.Li(
            html.A(
                f"{pdf['pdf_filename']} – {pdf['timestamp']}",
                href=f"file://{pdf['path']}",
                target="_blank"
            )
        ) for pdf in user_pdfs
    ]) if user_pdfs else html.P("Bu kullanıcıya ait PDF raporu bulunamadı.")

    pdf_list_section = html.Div([
        html.H4("📄 PDF Rapor Geçmişi:"),
        pdf_list
    ], style={"margin-top": "40px"})

    return user_info, analysis_list, user_list_section, pdf_list_section
