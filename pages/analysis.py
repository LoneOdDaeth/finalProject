from dash import html, dcc, callback, Output, Input, State
import os
import json
import datetime
import base64
import plotly.express as px
from utils.user_context import get_current_user
from database.mongo_operations import get_user_analyses, get_analysis_by_filename, save_analysis
from pathlib import Path
from pcap_processing.pcap_parser import analyze_pcap
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H2("Analiz Sayfası", style={"text-align": "center", "color": "#00FF00"}),

    dbc.Row([
        dbc.Col(
            dcc.Upload(
                id="upload-pcap",
                children=html.Button("PCAP Dosyası Seç", className="btn btn-success"),
                multiple=False
            ),
            width={"size": 3, "offset": 0}
        )
    ], style={"width": "100%", "justifyContent": "start", "margin-top": "20px"}),

    html.Div(id="upload-message", style={"margin-top": "10px"}),

    html.P("🔽 Lütfen görüntülemek istediğiniz analiz dosyasını seçin:", style={"text-align": "center"}),
    dcc.Dropdown(id="analysis-dropdown", style={"width": "50%", "margin": "auto", "color": "#000"}),

    html.Button("📊 Analizi Göster", id="start-analysis", className="btn btn-success", style={"margin-top": "20px"}),

    html.Div(id="analysis-output", style={"margin-top": "30px"})
], style={
    "backgroundColor": "#1E2124",
    "color": "#00FF00",
    "padding": "20px",
    "font-family": "Arial, sans-serif",
    "minHeight": "95vh"  
})


@callback(
    Output("analysis-dropdown", "options"),
    Input("start-analysis", "n_clicks"),
    prevent_initial_call=False
)
def populate_dropdown(_):
    username = get_current_user()
    analyses = get_user_analyses(username)
    return [{"label": f"{a['filename']} – {a['timestamp']}", "value": a["filename"]} for a in analyses]


@callback(
    Output("analysis-output", "children"),
    Input("start-analysis", "n_clicks"),
    State("analysis-dropdown", "value"),
    prevent_initial_call=True
)
def show_analysis(n_clicks, selected_filename):
    if not selected_filename:
        return html.Div("❌ Lütfen bir analiz seçin.")

    data = get_analysis_by_filename(selected_filename)
    if not data:
        return html.Div("❌ Seçilen analiz verisi bulunamadı.")

    result = data["analysis"]
    filename = data["filename"]
    owner_email = data["username"]

    try:
        start_time, end_time = result.get("time_range", (None, None))
        if start_time and end_time:
            start_str = datetime.datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S")
            end_str = datetime.datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S")
            time_range_str = f"{start_str} - {end_str}"
        else:
            time_range_str = "Zaman bilgisi bulunamadı"

        protocol_data = result["protocols"]

        pie_fig = px.pie(
            names=list(protocol_data.keys()),
            values=list(protocol_data.values()),
            title="Protokol Dağılımı",
            color_discrete_sequence=px.colors.sequential.Viridis
        )

        bar_fig_protocols = px.bar(
            x=list(protocol_data.keys()),
            y=list(protocol_data.values()),
            title="Protokollere Göre Paket Sayısı",
            labels={"x": "Protokol", "y": "Paket Sayısı"},
            color=list(protocol_data.keys()),
            color_discrete_sequence=px.colors.qualitative.Set3
        )

        src_ips = result["unique_src_ips"]
        src_fig = px.bar(
            x=src_ips,
            y=[1]*len(src_ips),
            title="Kaynak IP Dağılımı",
            labels={"x": "Kaynak IP", "y": "Trafik (temsilî)"},
            color=src_ips,
            color_discrete_sequence=px.colors.qualitative.Dark24
        )

        dst_ips = result["unique_dst_ips"]
        dst_fig = px.bar(
            x=dst_ips,
            y=[1]*len(dst_ips),
            title="Hedef IP Dağılımı",
            labels={"x": "Hedef IP", "y": "Trafik (temsilî)"},
            color=dst_ips,
            color_discrete_sequence=px.colors.qualitative.Prism
        )

        timestamps = result["timestamps"]
        time_series_fig = None
        if timestamps:
            time_series_fig = px.line(
                x=[datetime.datetime.fromtimestamp(ts) for ts in timestamps],
                y=list(range(len(timestamps))),
                title="Zamana Göre Paket Yoğunluğu",
                labels={"x": "Zaman", "y": "Paket No"},
            )

        src_ip_counts = result["src_ip_counts"]
        top_talkers = sorted(src_ip_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        talker_ips = [ip for ip, _ in top_talkers]
        talker_counts = [count for _, count in top_talkers]
        talker_fig = px.bar(
            x=talker_ips,
            y=talker_counts,
            title="En Yoğun Trafik Üreten IP'ler",
            labels={"x": "Kaynak IP", "y": "Paket Sayısı"},
            color=talker_ips,
            color_discrete_sequence=px.colors.sequential.Magma
        )

        components = [
            html.P(f"👤 Analizi Yapan: {owner_email}"),
            html.P(f"📄 Dosya: {filename}"),
            html.P(f"📦 Toplam Paket: {result['total_packets']}"),
            html.P(f"📤 Kaynak IP Sayısı: {len(result['unique_src_ips'])}"),
            html.P(f"📥 Hedef IP Sayısı: {len(result['unique_dst_ips'])}"),
            html.P(f"🕒 Zaman Aralığı: {time_range_str}"),
            dcc.Graph(figure=pie_fig),
            dcc.Graph(figure=bar_fig_protocols),
            dcc.Graph(figure=src_fig),
            dcc.Graph(figure=dst_fig),
            dcc.Graph(figure=talker_fig),
        ]

        if time_series_fig:
            components.append(dcc.Graph(figure=time_series_fig))

        return html.Div(components)

    except Exception as e:
        return html.Div(f"❌ Gösterim hatası: {str(e)}")


@callback(
    Output("upload-message", "children"),
    Input("upload-pcap", "contents"),
    State("upload-pcap", "filename")
)
def handle_upload(content, filename):
    if content is None:
        return ""

    try:
        content_type, content_string = content.split(',')
        decoded = base64.b64decode(content_string)

        if filename.endswith(".pcapng"):
            filename = filename.replace(".pcapng", ".pcap")

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"{timestamp}_{filename}"
        upload_path = "assets/uploads"
        tmp_path = "tmp/json"
        filepath = os.path.join(upload_path, new_filename)

        with open(filepath, "wb") as f:
            f.write(decoded)

        try:
            result = analyze_pcap(filepath)
        except Exception:
            return html.Div("❌ Dosya analiz edilemedi. Lütfen geçerli bir .pcap dosyası yükleyin.")

        username = get_current_user()
        user_json_dir = Path(tmp_path) / username
        user_json_dir.mkdir(parents=True, exist_ok=True)

        json_name = f"{new_filename}.json"
        json_path = user_json_dir / json_name

        with open(json_path, "w") as jf:
            json.dump(result, jf, indent=4)

        timestamp_iso = datetime.datetime.now().isoformat()
        save_analysis(username, new_filename, timestamp_iso, result)

        if os.path.exists(filepath):
            os.remove(filepath)

        return html.Div(f"✅ Dosya analiz edildi ve kayıt edildi: {json_name}")

    except Exception as e:
        return html.Div(f"❌ Hata: {str(e)}")
