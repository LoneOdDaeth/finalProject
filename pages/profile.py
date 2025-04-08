from dash import html, dcc, Input, Output, State, callback, MATCH, ALL, ctx
import os
from dash.exceptions import PreventUpdate
from utils.user_context import get_current_user
from database.mongo_operations import *
from utils.mail_sender import send_mail
import urllib.parse as urlparse
from urllib.parse import parse_qs
import dash_bootstrap_components as dbc

username = get_current_user()
json_dir = "tmp/json"

layout = html.Div([
    dcc.Location(id="page-url", refresh=False),

    html.H2("Kullanıcı Profili", style={"text-align": "center", "color": "#00FF00"}),

    html.Div(id="user-info", style={"margin-bottom": "20px"}),

    html.Div(id="user-analyses"),

    html.Div(id="user-list-section", style={"margin-top": "40px"}),

    html.Div(id="pdf-history-section", style={"margin-top": "40px"}),

    html.Div(id="pdf-open-feedback", style={"margin-top": "20px", "color": "red"}),

    html.Div(id="delete-feedback", style={"margin-top": "20px", "color": "red"}),

    dbc.Modal([
        dbc.ModalHeader("📧 Mail Gönder", close_button=True),
        dbc.ModalBody([
            html.P(id="selected-filename", style={"font-weight": "bold"}),
            html.Label("Alıcı Seçin:"),
            dcc.Dropdown(id="mail-recipient", style={"color": "#000000"}),
            html.Label("Mesaj (isteğe bağlı):"),
            dcc.Textarea(id="quick-mail-body", style={"width": "100%", "height": "100px"}),
            html.Div(id="quick-mail-feedback", style={"margin-top": "10px"})
        ]),
        dbc.ModalFooter([
            html.Button("📤 Gönder", id="confirm-quick-mail", className="btn btn-success"),
            html.Button("İptal", id="cancel-quick-mail", className="btn btn-secondary")
        ])
    ], id="quick-mail-modal", is_open=False)
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
    current_user = get_current_user()

    if not current_user:
        return html.Div("🔐 Giriş yapılmamış.", style={"color": "red"}), "", "", ""

    selected_user = current_user
    if search:
        parsed = urlparse.urlparse(search)
        params = parse_qs(parsed.query)
        if "user" in params:
            selected_user = params["user"][0]

    if selected_user != current_user and not is_admin(current_user):
        return html.Div("❌ Bu sayfaya erişim izniniz yok.", style={"color": "red"}), "", "", ""

    user_analyses = get_user_analyses(selected_user)

    yetki = "Yönetici" if is_admin(selected_user) else "Kullanıcı"
    user_info = html.Div([
        html.P(f"👤 Kullanıcı (E-posta): {selected_user}", style={"font-size": "18px"}),
        html.P(f"🔰 Yetki: {yetki}")
    ])

    analysis_list = html.Ul([
        html.Li([
            html.Span(f"{a['filename']} – {a['timestamp']}"),
            html.Button("❌ Sil", id={"type": "delete-btn", "index": a['filename']}, n_clicks=0,
                        style={"margin-left": "10px", "color": "white", "background-color": "#ff4444"})
        ]) if selected_user == current_user or is_admin(current_user) else
        html.Li([
            html.Span(f"{a['filename']} – {a['timestamp']}")
        ])
        for a in user_analyses
    ]) if user_analyses else html.P("Bu kullanıcı için analiz bulunamadı.")


    all_users = get_all_users()
    user_links = html.Ul([
        html.Li(dcc.Link(
            user["_id"],
            href=f"/profile?user={user['_id']}"
        )) for user in all_users if user["_id"] != current_user
    ])

    user_list_section = html.Div([
        html.H4("👥 Kullanıcı Listesi:"),
        user_links
    ]) if is_admin(current_user) else html.Div()

    user_pdfs = get_user_pdfs(selected_user)

    pdf_list = html.Ul([
        html.Li([
            html.A(
                f"{pdf['pdf_filename']} – {pdf['timestamp']}",
                href=f"file://{pdf['path']}",
                target="_blank"
            ),
            html.Button("❌ Sil", id={"type": "delete-pdf-btn", "index": pdf["pdf_filename"]}, n_clicks=0,
                        style={"margin-left": "10px", "color": "white", "background-color": "#ff4444"}),
            html.Button("📧 Mail At", id={"type": "open-mail-modal", "filename": pdf['pdf_filename'], "filetype": "pdf"},
                        n_clicks=0, style={"margin-left": "10px"})
        ]) if selected_user == current_user or is_admin(current_user) else
        html.Li([
            html.A(
                f"{pdf['pdf_filename']} – {pdf['timestamp']}",
                href=f"file://{pdf['path']}",
                target="_blank"
            )
        ])
        for pdf in user_pdfs
    ]) if user_pdfs else html.P("Bu kullanıcıya ait PDF raporu bulunamadı.")

    pdf_list_section = html.Div([
        html.H4("📄 PDF Rapor Geçmişi:"),
        pdf_list
    ], style={"margin-top": "40px"})

    admin_link = html.Div(
        dcc.Link("🚰 Yönetim Paneline Git", href="/admin"),
        style={"margin-top": "40px", "text-align": "center"}
    ) if is_admin(selected_user) else html.Div()

    return user_info, analysis_list, user_list_section, html.Div([pdf_list_section, admin_link])


@callback(
    Output("delete-feedback", "children"),
    Input({"type": "delete-btn", "index": ALL}, "n_clicks"),
    State({"type": "delete-btn", "index": ALL}, "id")
)
def delete_analysis(n_clicks_list, ids):
    triggered = [i for i, n in enumerate(n_clicks_list) if n > 0]
    if not triggered:
        return ""

    index = triggered[0]
    filename = ids[index]["index"]

    delete_analysis_by_filename(filename)

    username = get_current_user()
    json_path = os.path.join(json_dir, username, f"{filename}.json")

    if os.path.exists(json_path):
        os.remove(json_path)

    return f"🗑️ '{filename}' adlı analiz başarıyla silindi. Sayfayı yenileyin."


@callback(
    Output("pdf-open-feedback", "children"),
    Input({"type": "delete-pdf-btn", "index": ALL}, "n_clicks"),
    State({"type": "delete-pdf-btn", "index": ALL}, "id")
)
def delete_pdf(n_clicks_list, ids):
    triggered = [i for i, n in enumerate(n_clicks_list) if n > 0]
    if not triggered:
        return ""

    index = triggered[0]
    pdf_filename = ids[index]["index"]

    delete_pdf_by_filename(pdf_filename)

    username = get_current_user()
    pdf_path = os.path.join("tmp/pdf", username, pdf_filename)

    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    return f"🗑️ '{pdf_filename}' adlı PDF başarıyla silindi. Sayfayı yenileyin."

@callback(
    Output("quick-mail-modal", "is_open"),
    Output("selected-filename", "children"),
    Output("mail-recipient", "options"),
    Output("quick-mail-body", "value"),
    Input({"type": "open-mail-modal", "filename": ALL, "filetype": ALL}, "n_clicks"),
    prevent_initial_call=True
)
def open_quick_mail_modal(n_clicks_list):
    triggered = ctx.triggered_id
    if not triggered:
        raise PreventUpdate

    # Sadece bir buton tıklandığında aç
    if all(n == 0 or n is None for n in n_clicks_list):
        raise PreventUpdate

    current_user = get_current_user()
    users = get_all_users()
    recipients = [{"label": user["_id"], "value": user["_id"]} for user in users if user["_id"] != current_user]

    smtp = get_smtp_settings(current_user)
    default_msg = smtp.get("default_message", "") if smtp else ""

    file_label = triggered["filename"]
    file_type = triggered["filetype"]

    return True, f"{file_label} ({file_type.upper()})", recipients, default_msg

@callback(
    Output("quick-mail-feedback", "children"),
    Input("confirm-quick-mail", "n_clicks"),
    State("selected-filename", "children"),
    State("mail-recipient", "value"),
    State("quick-mail-body", "value"),
    prevent_initial_call=True
)
def send_quick_mail(_, file_info, recipient, body):
    if not file_info or not recipient:
        return "❌ Alıcı veya dosya bilgisi eksik."

    filename, filetype = file_info.split(" (")[0], file_info.split("(")[1].strip(")")

    sender = get_current_user()
    subject = "PCAP JSON Paylaşımı" if filetype.lower() == "json" else "PDF Analiz Raporu"
    filepath = os.path.join("tmp/json" if filetype == "json" else "tmp/pdf", sender, filename)

    if not os.path.exists(filepath):
        return "❌ Dosya bulunamadı."

    success, msg = send_mail(sender, recipient, subject, body, attachments=[filepath])
    return msg


@callback(
    Output("quick-mail-modal", "is_open", allow_duplicate=True),
    Input("cancel-quick-mail", "n_clicks"),
    prevent_initial_call=True
)
def close_modal(n):
    return False
