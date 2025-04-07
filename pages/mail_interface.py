from dash import html, dcc, Input, Output, State, callback
from utils.user_context import get_current_user
from utils.mail_sender import send_mail
import base64

layout = html.Div([
    html.H2("📬 Mail Gönderme", style={"text-align": "center", "color": "#00FF00"}),

    html.Label("📨 Alıcı E-Posta:"),
    dcc.Input(id="to-email", type="email", style={"width": "100%"}, placeholder="ornek@outlook.com"),

    html.Label("✏️ Konu:"),
    dcc.Input(id="mail-subject", type="text", style={"width": "100%"}, placeholder="Konu başlığı..."),

    html.Label("📝 Mail İçeriği (manuel giriş):"),
    dcc.Textarea(id="mail-body", style={"width": "100%", "height": "200px"}),

    html.Hr(),

    html.Label("📎 Alternatif olarak Markdown dosyası yükle:"),
    dcc.Upload(
        id="upload-markdown",
        children=html.Button("📁 Dosya Seç (örnek_mail.md)", className="btn btn-secondary"),
        multiple=False
    ),

    html.Div(id="file-preview-label", style={"margin-top": "20px", "font-weight": "bold"}),
    dcc.Markdown(id="file-preview", style={"whiteSpace": "pre-wrap", "backgroundColor": "#111", "padding": "10px"}),

    html.Button("📤 Gönder", id="send-mail-btn", className="btn btn-success", style={"margin-top": "30px"}),

    html.Div(id="send-feedback", style={"margin-top": "20px", "color": "lime"}),

    dcc.Store(id="uploaded-md-content")
], style={"backgroundColor": "#000000", "color": "#00FF00", "padding": "30px", "font-family": "Arial, sans-serif"})


@callback(
    Output("uploaded-md-content", "data"),
    Output("file-preview", "children"),
    Output("file-preview-label", "children"),
    Input("upload-markdown", "contents"),
    State("upload-markdown", "filename"),
    prevent_initial_call=True
)
def handle_markdown_upload(content, filename):
    if content is None:
        return "", "", ""

    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string).decode("utf-8")

    return decoded, decoded, f"📖 '{filename}' içeriği (önizleme):"


@callback(
    Output("send-feedback", "children"),
    Input("send-mail-btn", "n_clicks"),
    State("to-email", "value"),
    State("mail-subject", "value"),
    State("mail-body", "value"),
    State("uploaded-md-content", "data"),
    prevent_initial_call=True
)
def handle_send_mail(n_clicks, to_email, subject, body_textarea, uploaded_md):
    if not to_email or not subject:
        return "❌ Lütfen alıcı ve konu bilgilerini doldurun."

    body = uploaded_md if uploaded_md else body_textarea
    if not body.strip():
        return "❌ Mail içeriği boş olamaz."

    sender = get_current_user()
    success, msg = send_mail(sender, to_email, subject, body)

    return msg