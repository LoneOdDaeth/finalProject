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
from database.mongo_operations import get_user_pdfs, save_pdf_record, get_analysis_by_filename
from utils.pdf_generator import generate_pdf_from_figures

# Layout değişikliği (mevcut layout'unuzun yerine aşağıdaki düzeni kullanabilirsiniz)
layout = html.Div([
    # Header section with file upload and controls
    html.Div([

        # Butonlar aynı hizada - sağda 'Yeni Test' olacak şekilde hizalandı
        html.Div([
            # Sol taraftaki PCAP butonları
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

            # Sağ taraftaki "Yeni Test" butonu
            html.Div([
                html.Button("PDF Oluştur", id="special-analysis-btn", className="admin-btn-success"),
                html.Div(id="special-pdf-feedback", style={"color": "var(--text-green)", "marginTop": "6px"})
            ], style={"display": "flex", "flexDirection": "column", "alignItems": "flex-end", "justifyContent": "center"})

        ], style={
            "display": "flex",
            "justifyContent": "space-between",
            "alignItems": "center",
            "marginBottom": "20px",
            "paddingRight": "20px"
        }),

        html.Div(id="upload-message", style={"margin": "10px 0", "color": "var(--text-green)"}),

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

    
    # Yeni yerleşim planı
    # İlk satır - Analiz Özeti ve En Yoğun Trafik Üreten IP'ler
    html.Div([
        # Sol taraf - Analiz Özeti Kartı
        dbc.Card([
            html.Div([
                html.H5("Analiz Özeti", 
                       className="card-title", 
                       style={"color": "white", "fontWeight": "bold", "marginBottom": "15px"}),
                html.Div(id="analysis-summary-content", className="card-content-scroll")
            ], style={"padding": "15px"})
        ], className="dashboard-card", 
           style={"backgroundColor": "var(--card-bg-dark)", "flex": "1", "minWidth": "300px"}),
        
        # Sağ taraf - En Yoğun Trafik Üreten IP'ler
        dbc.Card([
            html.Div([
                html.H5("En Yoğun Trafik Üreten IP'ler", 
                       className="card-title", 
                       style={"color": "white", "fontWeight": "bold", "marginBottom": "15px"}),
                html.Div(id="top-talkers-chart")
            ], style={"padding": "15px"})
        ], className="dashboard-card", 
           style={"backgroundColor": "var(--card-bg-dark)", "flex": "3", "minWidth": "400px"}),
    ], style={"display": "flex", "gap": "20px", "marginBottom": "20px", "flexWrap": "wrap"}),
    
    # İkinci satır - Protokol Dağılımı kartları
    html.Div([
        # Sol taraf - Protokol Dağılımı (pie chart)
        dbc.Card([
            html.Div([
                html.H5("Protokol Dağılımı", 
                       className="card-title", 
                       style={"color": "white", "fontWeight": "bold", "marginBottom": "15px"}),
                html.Div(id="protocol-pie-chart")
            ], style={"padding": "15px"})
        ], className="dashboard-card", 
           style={"backgroundColor": "var(--card-bg-dark)", "flex": "1", "minWidth": "300px"}),
        
        # Sağ taraf - Protokol Paket Dağılımı (bar chart)
        dbc.Card([
            html.Div([
                html.H5("Protokol Paket Dağılımı", 
                       className="card-title", 
                       style={"color": "white", "fontWeight": "bold", "marginBottom": "15px"}),
                html.Div(id="protocol-bar-chart")
            ], style={"padding": "15px"})
        ], className="dashboard-card", 
           style={"backgroundColor": "var(--card-bg-dark)", "flex": "1", "minWidth": "300px"}),
    ], style={"display": "flex", "gap": "20px", "marginBottom": "20px", "flexWrap": "wrap"}),
    
    # Üçüncü satır - IP dağılımları
    html.Div([
        # Sol taraf - Kaynak IP Dağılımı
        dbc.Card([
            html.Div([
                html.H5("Kaynak IP Dağılımı", 
                       className="card-title", 
                       style={"color": "white", "fontWeight": "bold", "marginBottom": "15px"}),
                html.Div(id="source-ip-chart")
            ], style={"padding": "15px"})
        ], className="dashboard-card", 
           style={"backgroundColor": "var(--card-bg-dark)", "flex": "1", "minWidth": "300px"}),
        
        # Sağ taraf - Hedef IP Dağılımı
        dbc.Card([
            html.Div([
                html.H5("Hedef IP Dağılımı", 
                       className="card-title", 
                       style={"color": "white", "fontWeight": "bold", "marginBottom": "15px"}),
                html.Div(id="dest-ip-chart")
            ], style={"padding": "15px"})
        ], className="dashboard-card", 
           style={"backgroundColor": "var(--card-bg-dark)", "flex": "1", "minWidth": "300px"}),
    ], style={"display": "flex", "gap": "20px", "marginBottom": "20px", "flexWrap": "wrap"}),
    
    # Dördüncü satır - Zamana Göre Paket Yoğunluğu
    html.Div([
        dbc.Card([
            html.Div([
                html.H5("Zamana Göre Paket Yoğunluğu", 
                       className="card-title", 
                       style={"color": "white", "fontWeight": "bold", "marginBottom": "15px"}),
                html.Div(id="time-series-chart")
            ], style={"padding": "15px"})
        ], className="dashboard-card", 
           style={"backgroundColor": "var(--card-bg-dark)", "width": "100%"}),
    ], style={"marginBottom": "20px"}),
    
    # Gizli veri depolama
    dcc.Store(id="analysis-data-store"),
    
    # Toplam paket ve benzersiz IP sayılarını saklamak için gizli div'ler
    html.Div(id="total-packets", style={"display": "none"}),
    html.Div(id="unique-src-count", style={"display": "none"}),
    html.Div(id="unique-dst-count", style={"display": "none"}),
    
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
            
        summary_content = html.Div([
            # Üst Kısım - Analiz özeti bilgileri (daha kompakt)
            html.Div([
                # User info line
                html.Div([
                    html.Span("👤 ", style={"marginRight": "5px"}),
                    html.Span("Analizi Yapan: ", style={"fontSize": "13px", "opacity": "0.9"}),
                    html.Span(f"{owner_email}", style={"fontSize": "15px", "fontWeight": "bold"})
                ], style={"marginBottom": "8px"}),
                
                # File info line
                html.Div([
                    html.Span("📄 ", style={"marginRight": "5px"}),
                    html.Span("Dosya: ", style={"fontSize": "13px", "opacity": "0.9"}),
                    html.Span(f"{filename}", style={"fontSize": "15px", "fontWeight": "bold"})
                ], style={"marginBottom": "8px"}),
                
                # Time range info line
                html.Div([
                    html.Span("🕒 ", style={"marginRight": "5px"}),
                    html.Span("Zaman Aralığı: ", style={"fontSize": "13px", "opacity": "0.9"}),
                    html.Span(f"{time_range_str}", style={"fontSize": "15px", "fontWeight": "bold"})
                ])
            ], style={"marginBottom": "25px", "paddingBottom": "10px", "borderBottom": "1px solid #333"}),
            
            # Alt Kısım - Yalın KPI Kutuları
            html.Div([
                # Toplam Paket
                html.Div([
                    html.Div("Toplam Paket", style={"color": "#CCCCCC", "fontSize": "13px", "fontWeight": "bold"}),
                    html.Div(f"{result['total_packets']}", style={"color": "#2ecc71", "fontSize": "18px", "fontWeight": "bold"})
                ], style={
                    "backgroundColor": "#1a1a1a",
                    "border": "1px solid #333",
                    "borderRadius": "5px",
                    "padding": "10px",
                    "textAlign": "center",
                    "width": "32%"
                }),
                
                # Kaynak IP
                html.Div([
                    html.Div("Kaynak IP", style={"color": "#CCCCCC", "fontSize": "13px", "fontWeight": "bold"}),
                    html.Div(f"{len(result['unique_src_ips'])}", style={"color": "#2ecc71", "fontSize": "18px", "fontWeight": "bold"})
                ], style={
                    "backgroundColor": "#1a1a1a",
                    "border": "1px solid #333",
                    "borderRadius": "5px",
                    "padding": "10px",
                    "textAlign": "center",
                    "width": "32%"
                }),
                
                # Hedef IP
                html.Div([
                    html.Div("Hedef IP", style={"color": "#CCCCCC", "fontSize": "13px", "fontWeight": "bold"}),
                    html.Div(f"{len(result['unique_dst_ips'])}", style={"color": "#2ecc71", "fontSize": "18px", "fontWeight": "bold"})
                ], style={
                    "backgroundColor": "#1a1a1a",
                    "border": "1px solid #333",
                    "borderRadius": "5px",
                    "padding": "10px",
                    "textAlign": "center",
                    "width": "32%"
                })
            ], style={
                "display": "flex",
                "justifyContent": "space-between",
                "width": "100%"
            })
        ], style={
            "padding": "5px",
            "height": "auto",  # Otomatik yükseklik
            "overflowY": "visible",  # Kaydırma çubuğunu kaldırma
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "space-between"
        })
        
        # KPI values
        total_packets = result['total_packets']
        unique_src = len(result['unique_src_ips'])
        unique_dst = len(result['unique_dst_ips'])
        
        # Protocol pie chart - Saydam arkaplan
        protocol_data = result["protocols"]
        protocol_pie = dcc.Graph(
            figure=px.pie(
                names=list(protocol_data.keys()),
                values=list(protocol_data.values()),
                title="",
                color_discrete_sequence=px.colors.sequential.Viridis
            ).update_layout(
                paper_bgcolor='rgba(0,0,0,0)',  # Saydam arkaplan
                plot_bgcolor='rgba(0,0,0,0)',   # Saydam arkaplan
                font=dict(color='white'),
                margin=dict(t=10, b=10, l=10, r=10),
                height=300
            )
        )
        
        # Protocol bar chart - Saydam arkaplan
        protocol_bar = dcc.Graph(
            figure=px.bar(
                x=list(protocol_data.keys()),
                y=list(protocol_data.values()),
                title="",
                labels={"x": "Protokol", "y": "Paket Sayısı"},
                color=list(protocol_data.keys()),
                color_discrete_sequence=px.colors.qualitative.Set3
            ).update_layout(
                paper_bgcolor='rgba(0,0,0,0)',  # Saydam arkaplan
                plot_bgcolor='rgba(0,0,0,0)',   # Saydam arkaplan
                font=dict(color='white'),
                margin=dict(t=10, b=10, l=10, r=10),
                height=300
            )
        )
        
        # Top talkers chart - Saydam arkaplan
        top_talkers = dcc.Graph(
            figure=px.bar(
                x=list(result["src_ip_counts"].keys())[:10],
                y=list(result["src_ip_counts"].values())[:10],
                title="",
                labels={"x": "Kaynak IP", "y": "Paket Sayısı"},
                color=list(result["src_ip_counts"].keys())[:10],
                color_discrete_sequence=px.colors.sequential.Magma
            ).update_layout(
                paper_bgcolor='rgba(0,0,0,0)',  # Saydam arkaplan
                plot_bgcolor='rgba(0,0,0,0)',   # Saydam arkaplan
                font=dict(color='white'),
                margin=dict(t=10, b=10, l=10, r=10),
                height=300
            )
        )
        
        # Source IP chart - Saydam arkaplan
        source_ip = dcc.Graph(
            figure=px.bar(
                x=result["unique_src_ips"][:15],
                y=[1]*min(15, len(result["unique_src_ips"])),
                title="",
                labels={"x": "Kaynak IP", "y": "Trafik (temsilî)"},
                color=result["unique_src_ips"][:15],
                color_discrete_sequence=px.colors.qualitative.Dark24
            ).update_layout(
                paper_bgcolor='rgba(0,0,0,0)',  # Saydam arkaplan
                plot_bgcolor='rgba(0,0,0,0)',   # Saydam arkaplan
                font=dict(color='white'),
                margin=dict(t=10, b=10, l=10, r=10),
                height=250
            )
        )
        
        # Destination IP chart - Saydam arkaplan
        dest_ip = dcc.Graph(
            figure=px.bar(
                x=result["unique_dst_ips"][:15],
                y=[1]*min(15, len(result["unique_dst_ips"])),
                title="",
                labels={"x": "Hedef IP", "y": "Trafik (temsilî)"},
                color=result["unique_dst_ips"][:15],
                color_discrete_sequence=px.colors.qualitative.Prism
            ).update_layout(
                paper_bgcolor='rgba(0,0,0,0)',  # Saydam arkaplan
                plot_bgcolor='rgba(0,0,0,0)',   # Saydam arkaplan
                font=dict(color='white'),
                margin=dict(t=10, b=10, l=10, r=10),
                height=250
            )
        )
        
        # Time series chart - Saydam arkaplan
        timestamps = result.get("timestamps", [])
        if timestamps:
            time_series = dcc.Graph(
                figure=px.line(
                    x=[datetime.datetime.fromtimestamp(ts) for ts in timestamps],
                    y=list(range(len(timestamps))),
                    title="",
                    labels={"x": "Zaman", "y": "Paket No"},
                ).update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',  # Saydam arkaplan
                    plot_bgcolor='rgba(0,0,0,0)',   # Saydam arkaplan
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
    
@callback(
    Output("special-pdf-feedback", "children"),
    Input("special-analysis-btn", "n_clicks"),
    State("analysis-dropdown", "value"),
    prevent_initial_call=True
)
def generate_pdf_from_selected_analysis(n_clicks, selected_filename):
    if not selected_filename:
        return "❌ Lütfen önce bir analiz dosyası seçin."

    username = get_current_user()

    # 1. Aynı dosya için PDF oluşturulmuş mu?
    existing_pdfs = get_user_pdfs(username)
    for pdf in existing_pdfs:
        if pdf["related_analysis"] == selected_filename:
            return f"⚠️ '{selected_filename}' dosyası için PDF zaten oluşturulmuş."

    # 2. JSON analiz verisini getir
    data = get_analysis_by_filename(selected_filename)
    if not data:
        return f"❌ '{selected_filename}' adlı analiz bulunamadı."

    result = data["analysis"]

    try:
        import plotly.express as px
        import datetime
        import os

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

        pdf_path = generate_pdf_from_figures(
            figures_dict=figures,
            meta_info={
                "Dosya": selected_filename,
                "Kullanıcı": username,
                "Tarih": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            },
            username=username
        )

        save_pdf_record(
            username=username,
            pdf_filename=os.path.basename(pdf_path),
            timestamp=datetime.datetime.now().isoformat(),
            related_analysis=selected_filename,
            path=pdf_path
        )

        return f"✅ PDF başarıyla oluşturuldu: {os.path.basename(pdf_path)}"

    except Exception as e:
        return f"❌ PDF oluşturulurken hata oluştu: {str(e)}"
