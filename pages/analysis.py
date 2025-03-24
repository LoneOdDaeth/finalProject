from dash import html, dcc, callback, Output, Input
import os
import json
import datetime
import plotly.express as px

tmp_dir = "tmp"

layout = html.Div([
    html.H2("Analiz Sayfası", style={"text-align": "center", "color": "#00FF00"}),
    html.Button("📊 Analizi Başlat", id="start-analysis", className="btn btn-success"),
    html.Div(id="analysis-output")
], style={"backgroundColor": "#000000", "color": "#00FF00", "padding": "20px", "font-family": "Arial, sans-serif"})


@callback(
    Output("analysis-output", "children"),
    Input("start-analysis", "n_clicks")
)
def show_analysis(n):
    if not n:
        return ""

    try:
        # tmp klasöründeki en son json dosyasını bul
        files = [f for f in os.listdir(tmp_dir) if f.endswith(".json")]
        if not files:
            return html.Div("❌ Analiz verisi bulunamadı.")

        latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(tmp_dir, f)))
        json_path = os.path.join(tmp_dir, latest_file)

        # JSON dosyasını oku
        with open(json_path, "r") as f:
            result = json.load(f)

        # Zaman aralığını formatla
        start_time = result["time_range"][0]
        end_time = result["time_range"][1]
        if start_time and end_time:
            start_str = datetime.datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S")
            end_str = datetime.datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S")
            time_range_str = f"{start_str} - {end_str}"
        else:
            time_range_str = "Zaman bilgisi bulunamadı"

        ### GRAFİKLER ###

        # 1. Pie Chart – Protokol Dağılımı
        protocol_data = result["protocols"]
        pie_fig = px.pie(
            names=list(protocol_data.keys()),
            values=list(protocol_data.values()),
            title="Protokol Dağılımı",
            color_discrete_sequence=px.colors.sequential.Viridis
        )

        # 2. Bar Chart – Protokol Dağılımı
        bar_fig_protocols = px.bar(
            x=list(protocol_data.keys()),
            y=list(protocol_data.values()),
            title="Protokollere Göre Paket Sayısı",
            labels={"x": "Protokol", "y": "Paket Sayısı"},
            color=list(protocol_data.keys()),
            color_discrete_sequence=px.colors.qualitative.Set3
        )

        # 3. Bar Chart – Kaynak IP Dağılımı
        src_ips = result["unique_src_ips"]
        src_fig = px.bar(
            x=src_ips,
            y=[1]*len(src_ips),
            title="Kaynak IP Dağılımı",
            labels={"x": "Kaynak IP", "y": "Trafik (temsilî)"},
            color=src_ips,
            color_discrete_sequence=px.colors.qualitative.Dark24
        )

        # 4. Bar Chart – Hedef IP Dağılımı
        dst_ips = result["unique_dst_ips"]
        dst_fig = px.bar(
            x=dst_ips,
            y=[1]*len(dst_ips),
            title="Hedef IP Dağılımı",
            labels={"x": "Hedef IP", "y": "Trafik (temsilî)"},
            color=dst_ips,
            color_discrete_sequence=px.colors.qualitative.Prism
        )

        # 5. Line Chart – Zaman Serisi
        timestamps = result["timestamps"]
        if timestamps:
            time_series_fig = px.line(
                x=[datetime.datetime.fromtimestamp(ts) for ts in timestamps],
                y=list(range(len(timestamps))),
                title="Zamana Göre Paket Yoğunluğu",
                labels={"x": "Zaman", "y": "Paket No"},
            )
        else:
            time_series_fig = None

        # 6. Bar Chart – En Yoğun Trafik Üreten IP'ler
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

        # Sayfaya ekle
        components = [
            html.P(f"📄 Analiz Dosyası: {latest_file}"),
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
        return html.Div(f"❌ Hata: {str(e)}")
