from dash import html, dcc, callback, Output, Input, State
import dash
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
    # Header section with file upload and controls
    html.Div([
        html.Div([
            html.H3("Network Traffic Analysis", style={
                "color": "white", 
                "fontWeight": "bold",
                "marginBottom": "20px"
            }),
            html.Div([
                dcc.Upload(
                    id="upload-pcap",
                    children=html.Button("PCAP Dosyası Seç", 
                                       className="admin-btn-success",
                                       style={"marginRight": "10px"}),
                    multiple=False,
                ),
                html.Button("Analizi Göster", 
                           id="start-analysis", 
                           className="admin-btn-success"),
            ], style={"display": "flex", "alignItems": "center"}),
            html.Div(id="upload-message", style={"margin": "10px 0", "color": "var(--text-green)"}),
        ], style={"width": "100%", "marginBottom": "20px"}),
        
        html.Div([
            html.P("🔽 Görüntülemek istediğiniz analiz dosyasını seçin:", 
                  style={"marginBottom": "10px", "color": "var(--text-main)"}),
            dcc.Dropdown(
                id="analysis-dropdown", 
                style={
                    "width": "100%", 
                    "color": "#000", 
                    "backgroundColor": "#1a1a1a",
                    "borderColor": "var(--text-green)"
                }
            ),
        ], style={"width": "50%", "marginBottom": "30px"}),
    ], style={"padding": "20px 0"}),
    
    # Top row - KPI cards
    html.Div([
        # Analiz özeti kartı
        dbc.Card([
            html.Div([
                html.H5("📊 Analiz Özeti", 
                       className="card-title", 
                       style={"color": "white", "fontWeight": "bold", "marginBottom": "15px"}),
                html.Div(id="analysis-summary-content", className="card-content-scroll")
            ], style={"padding": "15px"})
        ], id="info-card", className="dashboard-card", 
           style={"backgroundColor": "var(--card-bg-dark)", "flex": "1", "minWidth": "300px"}),
        
        # Toplam Paket kartı
        dbc.Card([
            html.Div([
                html.H5("📦 Toplam Paket", 
                       className="card-title", 
                       style={"color": "white", "fontWeight": "bold", "marginBottom": "15px"}),
                html.Div(id="total-packets", 
                        style={"fontSize": "36px", "fontWeight": "bold", "color": "var(--text-green)", "textAlign": "center"})
            ], style={"padding": "15px"})
        ], className="dashboard-card", 
           style={"backgroundColor": "var(--card-bg-dark)", "flex": "1", "minWidth": "200px"}),
        
        # Unique IP'ler kartı
        dbc.Card([
            html.Div([
                html.H5("🌐 Benzersiz IP'ler", 
                       className="card-title", 
                       style={"color": "white", "fontWeight": "bold", "marginBottom": "15px"}),
                html.Div([
                    html.Div([
                        html.Span("Kaynak: ", style={"color": "var(--text-gray)"}),
                        html.Span(id="unique-src-count", style={"color": "var(--text-green)", "fontWeight": "bold"})
                    ], style={"marginBottom": "10px", "fontSize": "18px"}),
                    html.Div([  # Burada `html.div` yerine `html.Div` olarak düzeltildi
                        html.Span("Hedef: ", style={"color": "var(--text-gray)"}),
                        html.Span(id="unique-dst-count", style={"color": "var(--text-green)", "fontWeight": "bold"})
                    ], style={"fontSize": "18px"})
                ], style={"textAlign": "center"})
            ], style={"padding": "15px"})
        ], className="dashboard-card", 
           style={"backgroundColor": "var(--card-bg-dark)", "flex": "1", "minWidth": "200px"}),
    ], style={"display": "flex", "gap": "20px", "marginBottom": "20px", "flexWrap": "wrap"}),
    
    # Middle row - Main charts
    html.Div([
        # Sol sütun - Protocol Pie Chart
        dbc.Card([
            html.Div([
                html.H5("🥧 Protokol Dağılımı", 
                       className="card-title", 
                       style={"color": "white", "fontWeight": "bold", "marginBottom": "15px"}),
                html.Div(id="protocol-pie-chart")
            ], style={"padding": "15px"})
        ], className="dashboard-card", 
           style={"backgroundColor": "var(--card-bg-dark)", "flex": "1", "minWidth": "300px"}),
        
        # Orta sütun - Top talkers
        dbc.Card([
            html.Div([
                html.H5("🔝 En Yoğun Trafik Üreten IP'ler", 
                       className="card-title", 
                       style={"color": "white", "fontWeight": "bold", "marginBottom": "15px"}),
                html.Div(id="top-talkers-chart")
            ], style={"padding": "15px"})
        ], className="dashboard-card", 
           style={"backgroundColor": "var(--card-bg-dark)", "flex": "1", "minWidth": "400px"}),
        
        # Sağ sütun - Protocol bar chart
        dbc.Card([
            html.Div([
                html.H5("📊 Protokol Paket Dağılımı", 
                       className="card-title", 
                       style={"color": "white", "fontWeight": "bold", "marginBottom": "15px"}),
                html.Div(id="protocol-bar-chart")
            ], style={"padding": "15px"})
        ], className="dashboard-card", 
           style={"backgroundColor": "var(--card-bg-dark)", "flex": "1", "minWidth": "300px"}),
    ], style={"display": "flex", "gap": "20px", "marginBottom": "20px", "flexWrap": "wrap"}),
    
    # Bottom row - IP distributions and time series
    html.Div([
        # IP dağılımları yan yana
        html.Div([
            # Source IP Card
            dbc.Card([
                html.Div([
                    html.H5("📤 Kaynak IP Dağılımı", 
                           className="card-title", 
                           style={"color": "white", "fontWeight": "bold", "marginBottom": "15px"}),
                    html.Div(id="source-ip-chart")
                ], style={"padding": "15px"})
            ], className="dashboard-card", 
               style={"backgroundColor": "var(--card-bg-dark)", "flex": "1", "minWidth": "300px"}),
            
            # Destination IP Card
            dbc.Card([
                html.Div([
                    html.H5("📥 Hedef IP Dağılımı", 
                           className="card-title", 
                           style={"color": "white", "fontWeight": "bold", "marginBottom": "15px"}),
                    html.Div(id="dest-ip-chart")
                ], style={"padding": "15px"})
            ], className="dashboard-card", 
               style={"backgroundColor": "var(--card-bg-dark)", "flex": "1", "minWidth": "300px"}),
        ], style={"display": "flex", "gap": "20px", "marginBottom": "20px", "flexWrap": "wrap", "flex": "2"}),
        
        # Zaman serisi kartı
        dbc.Card([
            html.Div([
                html.H5("⏱️ Zamana Göre Paket Yoğunluğu", 
                       className="card-title", 
                       style={"color": "white", "fontWeight": "bold", "marginBottom": "15px"}),
                html.Div(id="time-series-chart")
            ], style={"padding": "15px"})
        ], className="dashboard-card", 
           style={"backgroundColor": "var(--card-bg-dark)", "flex": "1", "minWidth": "300px"}),
    ], style={"display": "flex", "gap": "20px", "flexWrap": "wrap"}),
    
    # Hidden storage for processed data
    dcc.Store(id="analysis-data-store"),
    
], style={
    "backgroundColor": "#1E2124",
    "color": "#E0E0E0",
    "padding": "20px",
    "font-family": "Arial, sans-serif",
    "minHeight": "95vh"  
})


@callback(
    Output("analysis-dropdown", "options"),
    [Input("start-analysis", "n_clicks"),
     Input("upload-message", "children")],
    prevent_initial_call=False
)
def populate_dropdown(n_clicks, upload_message):
    username = get_current_user()
    analyses = get_user_analyses(username)
    
    if not analyses:
        return []
        
    # Ensure we're returning a properly formatted list of options
    return [{"label": f"{a['filename']} – {a.get('timestamp', 'No timestamp')}", 
             "value": a["filename"]} 
            for a in analyses if "filename" in a]


@callback(
    Output("analysis-data-store", "data"),
    [Input("start-analysis", "n_clicks"),
     Input("analysis-dropdown", "value")],
    prevent_initial_call=True
)
def process_analysis_data(n_clicks, selected_filename):
    # Check if the callback was triggered by the dropdown change
    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    # If trigger is start-analysis but no clicks or no file selected, return None
    if trigger_id == "start-analysis" and (not n_clicks or not selected_filename):
        return None
    
    # If a file is selected, proceed
    if selected_filename:
        # Orijinal fonksiyon çağrısına uygun şekilde, sadece filename ile çağırıyoruz
        data = get_analysis_by_filename(selected_filename)
        if not data:
            return None
        
        # Ensure the data is JSON serializable
        try:
            import json
            # Test if data is JSON serializable
            json.dumps(data)
            return data
        except TypeError:
            # If not serializable, convert to a safe format
            if isinstance(data, dict):
                safe_data = {}
                for k, v in data.items():
                    if k == '_id' and not isinstance(v, str):
                        safe_data[k] = str(v)
                    else:
                        safe_data[k] = v
                return safe_data
            return None
    
    return None

@callback(
    [Output("analysis-summary-content", "children"),
     Output("total-packets", "children"),
     Output("unique-src-count", "children"),
     Output("unique-dst-count", "children"),
     Output("protocol-pie-chart", "children"),
     Output("protocol-bar-chart", "children"),
     Output("top-talkers-chart", "children"),
     Output("source-ip-chart", "children"),
     Output("dest-ip-chart", "children"),
     Output("time-series-chart", "children")],
    Input("analysis-data-store", "data"),
    prevent_initial_call=True
)
def update_dashboard(data):
    if not data:
        return [html.P("Lütfen bir analiz dosyası seçin.")] + ["—"] * 3 + [html.P("Veri yok.")] * 6
    
    result = data["analysis"]
    filename = data["filename"]
    owner_email = data["username"]
    
    try:
        # Time range formatting
        start_time, end_time = result.get("time_range", (None, None))
        if start_time and end_time:
            start_str = datetime.datetime.fromtimestamp(start_time).strftime("%Y-%m-%d %H:%M:%S")
            end_str = datetime.datetime.fromtimestamp(end_time).strftime("%Y-%m-%d %H:%M:%S")
            time_range_str = f"{start_str} - {end_str}"
        else:
            time_range_str = "Zaman bilgisi bulunamadı"
            
        # Prepare summary content
        summary_content = html.Div([
            html.P(f"👤 Analizi Yapan: {owner_email}", className="mb-2"),
            html.P(f"📄 Dosya: {filename}", className="mb-2"),
            html.P(f"🕒 Zaman Aralığı: {time_range_str}", className="mb-2"),
        ])
        
        # KPI values
        total_packets = result['total_packets']
        unique_src = len(result['unique_src_ips'])
        unique_dst = len(result['unique_dst_ips'])
        
        # Protocol pie chart
        protocol_data = result["protocols"]
        protocol_pie = dcc.Graph(
            figure=px.pie(
                names=list(protocol_data.keys()),
                values=list(protocol_data.values()),
                title="",
                color_discrete_sequence=px.colors.sequential.Viridis
            ).update_layout(
                paper_bgcolor='#333030',
                plot_bgcolor='#333030',
                font=dict(color='white'),
                margin=dict(t=10, b=10, l=10, r=10),
                height=300
            )
        )
        
        # Protocol bar chart
        protocol_bar = dcc.Graph(
            figure=px.bar(
                x=list(protocol_data.keys()),
                y=list(protocol_data.values()),
                title="",
                labels={"x": "Protokol", "y": "Paket Sayısı"},
                color=list(protocol_data.keys()),
                color_discrete_sequence=px.colors.qualitative.Set3
            ).update_layout(
                paper_bgcolor='#333030',
                plot_bgcolor='#333030',
                font=dict(color='white'),
                margin=dict(t=10, b=10, l=10, r=10),
                height=300
            )
        )
        
        # Top talkers chart
        top_talkers = dcc.Graph(
            figure=px.bar(
                x=list(result["src_ip_counts"].keys())[:10],
                y=list(result["src_ip_counts"].values())[:10],
                title="",
                labels={"x": "Kaynak IP", "y": "Paket Sayısı"},
                color=list(result["src_ip_counts"].keys())[:10],
                color_discrete_sequence=px.colors.sequential.Magma
            ).update_layout(
                paper_bgcolor='#333030',
                plot_bgcolor='#333030',
                font=dict(color='white'),
                margin=dict(t=10, b=10, l=10, r=10),
                height=300
            )
        )
        
        # Source IP chart
        source_ip = dcc.Graph(
            figure=px.bar(
                x=result["unique_src_ips"][:15],
                y=[1]*min(15, len(result["unique_src_ips"])),
                title="",
                labels={"x": "Kaynak IP", "y": "Trafik (temsilî)"},
                color=result["unique_src_ips"][:15],
                color_discrete_sequence=px.colors.qualitative.Dark24
            ).update_layout(
                paper_bgcolor='#333030',
                plot_bgcolor='#333030',
                font=dict(color='white'),
                margin=dict(t=10, b=10, l=10, r=10),
                height=250
            )
        )
        
        # Destination IP chart
        dest_ip = dcc.Graph(
            figure=px.bar(
                x=result["unique_dst_ips"][:15],
                y=[1]*min(15, len(result["unique_dst_ips"])),
                title="",
                labels={"x": "Hedef IP", "y": "Trafik (temsilî)"},
                color=result["unique_dst_ips"][:15],
                color_discrete_sequence=px.colors.qualitative.Prism
            ).update_layout(
                paper_bgcolor='#333030',
                plot_bgcolor='#333030',
                font=dict(color='white'),
                margin=dict(t=10, b=10, l=10, r=10),
                height=250
            )
        )
        
        # Time series chart
        timestamps = result.get("timestamps", [])
        if timestamps:
            time_series = dcc.Graph(
                figure=px.line(
                    x=[datetime.datetime.fromtimestamp(ts) for ts in timestamps],
                    y=list(range(len(timestamps))),
                    title="",
                    labels={"x": "Zaman", "y": "Paket No"},
                ).update_layout(
                    paper_bgcolor='#333030',
                    plot_bgcolor='#333030',
                    font=dict(color='white'),
                    margin=dict(t=10, b=10, l=10, r=10),
                    height=250
                )
            )
        else:
            time_series = html.P("Zaman serisi verisi bulunamadı.", style={"color": "#AAAAAA"})
            
        return summary_content, total_packets, unique_src, unique_dst, protocol_pie, protocol_bar, top_talkers, source_ip, dest_ip, time_series
    
    except Exception as e:
        error_message = html.P(f"Hata: {str(e)}", style={"color": "#FF4444"})
        return [error_message] + ["—"] * 3 + [html.P(f"Gösterim hatası: {str(e)}", style={"color": "#FF4444"})] * 6


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

        # Dizin var mı kontrol et ve yoksa oluştur
        os.makedirs(upload_path, exist_ok=True)
        
        with open(filepath, "wb") as f:
            f.write(decoded)

        try:
            result = analyze_pcap(filepath)
        except Exception as e:
            return html.Div(f"❌ Dosya analiz edilemedi: {str(e)}", style={"color": "#FF4444"})

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

        return html.Div([
            html.Span("✅ ", style={"fontSize": "18px"}),
            html.Span(f"Dosya başarıyla analiz edildi: {json_name}")
        ], style={"color": "var(--text-green)"})

    except Exception as e:
        return html.Div(f"❌ Hata: {str(e)}", style={"color": "#FF4444"})