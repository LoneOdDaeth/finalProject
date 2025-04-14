from dash import html, dcc, Input, Output, State, callback, MATCH, ALL, ctx
import os
from dash.exceptions import PreventUpdate
from utils.user_context import get_current_user
from database.mongo_operations import *
from utils.mail_sender import send_mail
import urllib.parse as urlparse
from urllib.parse import parse_qs
import dash_bootstrap_components as dbc
from datetime import datetime

username = get_current_user()
json_dir = "tmp/json"

layout = html.Div([
    dcc.Location(id="page-url", refresh=False),

    html.Div([
        html.Div([  # Sol Sütun (daha dar)
            html.Div(id="user-info", className="profile-card user-info", style={"margin-bottom": "20px"}),
            html.Div(id="user-analyses", className="profile-card")
        ], style={"flex": "0.6", "minWidth": "280px"}),

        html.Div([  # Sağ Sütun (biraz daha geniş)
            html.Div(id="user-mail-log-section", className="profile-card", style={"margin-bottom": "20px", "overflowY": "auto", "maxHeight": "300px", "minHeight": "327px"}),
            html.Div(id="pdf-history-section", className="profile-card")
        ], style={"flex": "1.4", "minWidth": "380px"})
    ], className="profile-columns", style={"display": "flex", "gap": "20px"}),

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
    "backgroundColor": "#1E2124",
    "color": "#00FF00",
    "padding": "20px",
    "font-family": "Arial, sans-serif",
    "minHeight": "95vh"  
})

@callback(
    Output("user-info", "children"),
    Output("user-analyses", "children"),
    Output("pdf-history-section", "children"),
    Output("user-mail-log-section", "children"),
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
    user_pdfs = get_user_pdfs(selected_user)
    mail_logs = get_all_mail_logs()
    mail_count = sum(1 for log in mail_logs if log["sender"] == selected_user)
    yetki = "Yönetici" if is_admin(selected_user) else "Kullanıcı"

    # Kullanıcı Bilgileri
    user_info = html.Div([
        dbc.Card([
            dbc.CardHeader("Kullanıcı Bilgileri", className="card-header-green"),
            dbc.CardBody(
                html.Div([

                    # Kullanıcı mail ve yetki bilgisi
                    html.Div([
                        html.P(f"Mail: {selected_user}", style={
                            "font-size": "16px", "margin": "0", "font-weight": "bold"
                        }),
                        html.P(f"Yetki: {yetki}", style={
                            "font-size": "16px", "margin": "0", "font-weight": "bold"
                        })
                    ], style={"marginBottom": "12px"}),

                    # İki istatistik kutusu
                    html.Div([

                        # PDF Sayısı Kutusu
                        html.Div([
                            html.P(f"{len(user_pdfs)}", style={
                                "margin": "0", "fontSize": "26px", "fontWeight": "bold",
                                "color": "#fff", "textAlign": "center"
                            }),
                            html.Div([
                                html.Span("📄", style={"fontSize": "18px", "marginRight": "6px"}),
                                html.Span("PDF Sayısı", style={
                                    "fontSize": "13px", "color": "#ccc", "fontWeight": "bold"
                                })
                            ], style={
                                "display": "flex",
                                "justifyContent": "center",
                                "alignItems": "center",
                                "marginTop": "8px"
                            })
                        ], style={
                            "display": "flex",
                            "flexDirection": "column",
                            "justifyContent": "center",
                            "alignItems": "center",
                            "padding": "12px 16px",
                            "border": "1px solid var(--text-green)",
                            "borderRadius": "6px",
                            "flex": "1",
                            "height": "140px",
                            "boxSizing": "border-box"
                        }),

                        # Mail Sayısı Kutusu
                        html.Div([
                            html.P(f"{mail_count}", style={
                                "margin": "0", "fontSize": "26px", "fontWeight": "bold",
                                "color": "#fff", "textAlign": "center"
                            }),
                            html.Div([
                                html.Span("📧", style={"fontSize": "18px", "marginRight": "6px"}),
                                html.Span("Mail Sayısı", style={
                                    "fontSize": "13px", "color": "#ccc", "fontWeight": "bold"
                                })
                            ], style={
                                "display": "flex",
                                "justifyContent": "center",
                                "alignItems": "center",
                                "marginTop": "8px"
                            })
                        ], style={
                            "display": "flex",
                            "flexDirection": "column",
                            "justifyContent": "center",
                            "alignItems": "center",
                            "padding": "12px 16px",
                            "border": "1px solid var(--text-green)",
                            "borderRadius": "6px",
                            "flex": "1",
                            "height": "140px",
                            "boxSizing": "border-box"
                        })

                    ], style={
                        "display": "flex",
                        "gap": "12px",
                        "marginTop": "10px"
                    })

                ], style={
                    "display": "flex",
                    "flexDirection": "column",
                    "justifyContent": "space-between",
                    "flexGrow": "1",
                    "height": "100%"
                }),
                style={
                    "height": "100%",
                    "display": "flex",
                    "flexDirection": "column"
                }
            )
        ], style={
            "height": "100%",
            "display": "flex",
            "flexDirection": "column"
        })
    ])

    # Analizler
    analysis_items = [
        html.Div([
            html.Div([
                html.P(f"📁 {a['filename']}", style={"margin": "0", "color": "white", "font-weight": "bold"}),
                html.P(f"🕒 {datetime.fromisoformat(a['timestamp']).strftime('%d.%m.%Y %H:%M')}",
                    style={"font-size": "12px", "color": "#AAAAAA"})
            ], style={"flex": "1"}),

            html.Div([
                html.Button("❌ Sil", id={"type": "delete-btn", "index": a["filename"]}, n_clicks=0,
                            style={"color": "white", "background-color": "#ff4444"})
            ], className="card-button-group")
        ], style={
            "display": "flex",
            "justifyContent": "space-between",
            "alignItems": "center",
            "padding": "12px 0",
            "borderBottom": "1px solid white"  # ← çizgi burada
        })
        for a in user_analyses
    ] if user_analyses else [html.P("Bu kullanıcı için analiz bulunamadı.", style={"color": "#AAAAAA"})]


    analysis_cards = dbc.Card([
        dbc.CardHeader("📊 Son Analizler", className="card-header-green"),
        dbc.CardBody(html.Div(analysis_items))
    ])
    user_analyses = html.Div(analysis_cards, className="scrollable-card fixed-card-height")

    # PDF Raporları
    pdf_items = [
        html.Div([
            html.Div([
                html.P(f"📄 {pdf['pdf_filename']}", style={
                    "margin": "0", "color": "white", "font-weight": "bold"
                }),
                html.P(f"🕒 {datetime.fromisoformat(pdf['timestamp']).strftime('%d.%m.%Y %H:%M')}",
                    style={"font-size": "12px", "color": "#AAAAAA"})
            ], style={"flex": "1"}),

            html.Div([
                html.Button("📧 Mail At", id={
                    "type": "open-mail-modal",
                    "filename": pdf['pdf_filename'],
                    "filetype": "pdf"
                }, n_clicks=0, className="btn btn-success", style={"margin-bottom": "5px"}),

                html.Button("❌ Sil", id={
                    "type": "delete-pdf-btn",
                    "index": pdf["pdf_filename"]
                }, n_clicks=0, style={"color": "white", "background-color": "#ff4444"})
            ], className="card-button-group")
        ], style={
            "display": "flex",
            "justifyContent": "space-between",
            "alignItems": "center",
            "padding": "12px 0",
            "borderBottom": "1px solid white"
        })
        for pdf in user_pdfs
    ] if user_pdfs else [html.P("Bu kullanıcıya ait PDF raporu bulunamadı.", style={"color": "#AAAAAA"})]


    pdf_cards = dbc.Card([
        dbc.CardHeader("📄 PDF Rapor Geçmişi", className="card-header-green"),
        dbc.CardBody(html.Div(pdf_items))
    ])
    pdf_list_section = html.Div(pdf_cards, className="scrollable-card fixed-card-height")

    # Mail Log
    if selected_user == current_user:
        user_mail_logs = [log for log in mail_logs if log["sender"] == current_user]

        mail_header = html.Div([
            html.Span("📎 Dosya", style={"font-weight": "bold"}),
            html.Span("👤 Alıcı", style={"font-weight": "bold"}),
            html.Span("🕒 Tarih", style={"font-weight": "bold"})
        ], className="mail-log-header")

        mail_rows = [
            html.Div([
                html.Span(f"📎 {log['attachment_name'] or 'Dosya yok'}", style={"color": "white", "font-weight": "bold"}),
                html.Span(f"👤 {log['recipient']}", style={"color": "white", "font-weight": "bold"}),
                html.Span(f"🕒 {datetime.fromisoformat(log['timestamp']).strftime('%d.%m.%Y %H:%M')}", style={"color": "white", "font-weight": "bold"})
            ], className="mail-log-row")
            for log in user_mail_logs
        ] if user_mail_logs else [
            html.Div([
                html.Span("Veri bulunamadı."),
                html.Span("-"),
                html.Span("-")
            ], className="mail-log-row")
        ]

        mail_log_cards = dbc.Card([
            dbc.CardHeader("📬 Gönderilen Mail Geçmişi", className="card-header-green"),
            dbc.CardBody(html.Div([mail_header] + mail_rows))
        ])
        mail_log_section = html.Div(mail_log_cards, className="scrollable-card fixed-card-height")
    else:
        mail_log_section = html.Div([
            dbc.Card([
                dbc.CardHeader("📬 Gönderilen Mail Geçmişi", className="card-header-green"),
                dbc.CardBody([
                    html.P("Bu alana sadece kendi profilinizden erişebilirsiniz.", style={"color": "#AAAAAA"})
                ])
            ])
        ], className="scrollable-card fixed-card-height")


    return user_info, user_analyses, pdf_list_section, mail_log_section

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


