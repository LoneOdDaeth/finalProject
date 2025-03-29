from dash import html, dcc, Input, Output, State, callback
from database.mongo_operations import get_user_analyses, get_analysis_by_filename, save_pdf_record
from utils.user_context import get_current_user
from utils.pdf_generator import generate_pdf_from_figures
import plotly.express as px
import datetime
import os

layout = html.Div([
    html.H2("Dışa Aktarma ve PDF Oluşturma", style={"text-align": "center", "color": "#00FF00"}),

    html.P("Lütfen bir analiz dosyası seçin ve PDF raporu oluşturun:", style={"margin-top": "20px"}),

    dcc.Dropdown(id="analysis-selector", style={"color": "#000000"}),

    html.Button("📄 PDF Oluştur", id="generate-pdf-btn", className="btn btn-success", style={"margin-top": "10px"}),

    html.Div(id="export-output", style={"margin-top": "30px"})
], style={"backgroundColor": "#000000", "color": "#00FF00", "padding": "20px", "font-family": "Arial, sans-serif"})


@callback(
    Output("analysis-selector", "options"),
    Input("generate-pdf-btn", "n_clicks"),
    prevent_initial_call=False
)
def populate_dropdown(n):
    username = get_current_user()
    analyses = get_user_analyses(username)
    return [{"label": f"{a['filename']} – {a['timestamp']}", "value": a["filename"]} for a in analyses]


@callback(
    Output("export-output", "children"),
    Input("generate-pdf-btn", "n_clicks"),
    State("analysis-selector", "value"),
    prevent_initial_call=True
)
def generate_selected_pdf(n_clicks, selected_filename):
    if not selected_filename:
        return "❌ Lütfen önce bir analiz dosyası seçin."

    try:
        data = get_analysis_by_filename(selected_filename)
        result = data["analysis"]
        username = data["username"]

        # Grafikler
        protocol_data = result["protocols"]
        pie_fig = px.pie(names=list(protocol_data.keys()), values=list(protocol_data.values()), title="Protokol Dağılımı")
        bar_fig_protocols = px.bar(x=list(protocol_data.keys()), y=list(protocol_data.values()), title="Protokollere Göre Paket Sayısı")
        src_fig = px.bar(x=result["unique_src_ips"], y=[1]*len(result["unique_src_ips"]), title="Kaynak IP Dağılımı")
        dst_fig = px.bar(x=result["unique_dst_ips"], y=[1]*len(result["unique_dst_ips"]), title="Hedef IP Dağılımı")
        top_talkers = sorted(result["src_ip_counts"].items(), key=lambda x: x[1], reverse=True)[:10]
        talker_fig = px.bar(x=[ip for ip, _ in top_talkers], y=[count for _, count in top_talkers], title="En Yoğun Trafik Üreten IP'ler")

        time_series_fig = None
        if result["timestamps"]:
            time_series_fig = px.line(
                x=[datetime.datetime.fromtimestamp(ts) for ts in result["timestamps"]],
                y=list(range(len(result["timestamps"]))),
                title="Zamana Göre Paket Yoğunluğu"
            )

        figures = {
            "protocol_pie": pie_fig,
            "protocol_bar": bar_fig_protocols,
            "src_ips": src_fig,
            "dst_ips": dst_fig,
            "top_talkers": talker_fig
        }
        if time_series_fig:
            figures["time_series"] = time_series_fig

        # PDF oluştur
        pdf_path = generate_pdf_from_figures(
            figures_dict=figures,
            meta_info={
                "Dosya": selected_filename,
                "Kullanıcı": username,
                "Tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            username=username
        )

        # MongoDB’ye kaydet
        save_pdf_record(
            username=username,
            pdf_filename=os.path.basename(pdf_path),
            timestamp=datetime.datetime.now().isoformat(),
            related_analysis=selected_filename,
            path=pdf_path
        )

        return f"✅ PDF başarıyla oluşturuldu: {selected_filename}.pdf"

    except Exception as e:
        return f"❌ Hata: {str(e)}"