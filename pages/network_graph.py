from dash import html, dcc, Input, Output, State, callback, ctx
import plotly.graph_objects as go
import dash
import os
from utils.user_context import get_current_user
from database.mongo_operations import get_user_analyses, get_analysis_by_filename, save_pdf_record
from utils.pdf_generator import generate_pdf_from_figures
import datetime
import networkx as nx
from collections import defaultdict, Counter

layout = html.Div([
    # Üst başlık + PDF oluştur butonu
    html.Div([
        html.H3("🌐 IP Trafik Ağı Haritası", style={"color": "var(--text-green)", "margin": 0}),
        html.Div([
            html.Button("📄 PDF Oluştur", id="generate-pdf-btn", n_clicks=0, className="admin-btn-success", style={
                "padding": "8px 16px",
                "fontWeight": "bold"
            }),
            html.Div(id="pdf-export-feedback", style={"color": "var(--text-green)", "marginTop": "6px"})
        ], style={"display": "flex", "flexDirection": "column", "alignItems": "flex-end"})
    ], style={
        "display": "flex",
        "justifyContent": "space-between",
        "alignItems": "center",
        "marginBottom": "20px"
    }),

    # Üst satır: dropdown + filtre
    html.Div([
        html.Div([
            html.Label("Analiz Dosyası Seçin:", style={"color": "white"}),
            dcc.Dropdown(id="network-analysis-dropdown", style={"color": "#000"})
        ], style={"flex": 1, "marginRight": "20px"}),

        html.Div([
            html.Label("IP Filtresi:", style={"color": "white"}),
            dcc.Dropdown(id="node-filter-dropdown", style={"color": "#000"}, placeholder="Tümünü göster")
        ], style={"flex": 1})
    ], style={"display": "flex", "gap": "10px", "marginBottom": "30px", "flexWrap": "wrap"}),

    # Orta satır: büyük network graph kartı (yükseklik net tanımlandı)
    html.Div([
        html.Div([
            html.H5("IP Trafik Ağı Haritası", className="card-title"),
            dcc.Loading(dcc.Graph(id="network-graph", style={"height": "600px"}))
        ], className="network-graph-card", style={
            "width": "100%",
            "height": "650px",
            "minHeight": "650px",
            "maxHeight": "650px",
            "display": "flex",
            "flexDirection": "column",
            "justifyContent": "stretch"
        })
    ], style={"marginBottom": "30px"}),

    # Alt satır: 2 küçük kart yan yana (yükseklik sabitlendi)
    html.Div([
        html.Div([
            html.H5("En Yoğun Trafik Üreten Düğümler", className="card-title"),
            dcc.Graph(id="top-talkers-bar", style={"height": "300px"})
        ], className="dashboard-card", style={
            "flex": 1,
            "minWidth": "400px",
            "height": "300px",
            "minHeight": "300px",
            "maxHeight": "300px"
        }),

        html.Div([
            html.H5("En Fazla Bağlantıya Sahip IP'ler", className="card-title"),
            dcc.Graph(id="most-connected-bar", style={"height": "300px"})
        ], className="dashboard-card", style={
            "flex": 1,
            "minWidth": "400px",
            "height": "300px",
            "minHeight": "300px",
            "maxHeight": "300px"
        })
    ], style={"display": "flex", "gap": "20px", "flexWrap": "wrap", "marginBottom": "20px"})
], style={"backgroundColor": "#1E2124", "color": "#E0E0E0", "padding": "20px", "minHeight": "95vh"})


@callback(
    Output("network-analysis-dropdown", "options"),
    Input("network-analysis-dropdown", "id")
)
def load_analysis_files(_):
    username = get_current_user()
    analyses = get_user_analyses(username)
    return [{"label": a["filename"], "value": a["filename"]} for a in analyses]


@callback(
    Output("network-graph", "figure"),
    Output("top-talkers-bar", "figure"),
    Output("most-connected-bar", "figure"),
    Output("node-filter-dropdown", "options"),
    Input("network-analysis-dropdown", "value"),
    Input("node-filter-dropdown", "value"),
    prevent_initial_call=True
)
def generate_network_graph(selected_file, filter_node):
    if not selected_file:
        raise dash.exceptions.PreventUpdate

    data = get_analysis_by_filename(selected_file)
    if not data:
        return dash.no_update

    result = data["analysis"]
    edges = defaultdict(int)
    ip_set = set()
    connections = defaultdict(set)

    for src, dst in zip(result["unique_src_ips"], result["unique_dst_ips"]):
        if filter_node and filter_node not in [src, dst]:
            continue
        edges[(src, dst)] += 1
        ip_set.update([src, dst])
        connections[src].add(dst)
        connections[dst].add(src)

    G = nx.DiGraph()
    for ip in ip_set:
        G.add_node(ip)
    for (src, dst), weight in edges.items():
        G.add_edge(src, dst, weight=weight)

    pos = nx.spring_layout(G, seed=42)
    edge_trace = []
    for src, dst in G.edges():
        x0, y0 = pos[src]
        x1, y1 = pos[dst]
        weight = G.edges[src, dst]['weight']
        edge_trace.append(go.Scatter(
            x=[x0, x1, None], y=[y0, y1, None],
            line=dict(width=1 + weight / 50, color="#888"),
            hoverinfo='text',
            mode='lines',
            text=f"{src} → {dst} | {weight} paket"
        ))

    node_trace = go.Scatter(
        x=[pos[ip][0] for ip in G.nodes()],
        y=[pos[ip][1] for ip in G.nodes()],
        text=[ip for ip in G.nodes()],
        mode='markers+text',
        textposition='bottom center',
        hoverinfo='text',
        textfont=dict(color='white'),
        marker=dict(
            size=15,
            color="#2ecc71",
            line_width=2
        )
    )

    network_fig = go.Figure(data=edge_trace + [node_trace])
    network_fig.update_layout(
        height=600,
        showlegend=False,
        margin=dict(t=20, b=20, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )

    top_talkers = Counter(result["src_ip_counts"]).most_common(10)
    top_talkers_fig = go.Figure(data=[
        go.Bar(x=[ip for ip, _ in top_talkers], y=[count for _, count in top_talkers])
    ])
    top_talkers_fig.update_layout(
        title="",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )

    most_connected = sorted(connections.items(), key=lambda x: len(x[1]), reverse=True)[:10]
    most_connected_fig = go.Figure(data=[
        go.Bar(x=[ip for ip, _ in most_connected], y=[len(peers) for _, peers in most_connected])
    ])
    most_connected_fig.update_layout(
        title="",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )

    return network_fig, top_talkers_fig, most_connected_fig, [{"label": ip, "value": ip} for ip in ip_set]

@callback(
    Output("pdf-export-feedback", "children"),
    Input("generate-pdf-btn", "n_clicks"),
    State("network-analysis-dropdown", "value"),
    prevent_initial_call=True
)
def generate_pdf(n_clicks, selected_file):
    if not selected_file:
        return "❌ Lütfen önce bir analiz dosyası seçin."

    data = get_analysis_by_filename(selected_file)
    if not data:
        return "❌ Seçilen dosyaya ait analiz bulunamadı."

    username = get_current_user()

    # Daha önce bu analiz için PDF oluşturulmuş mu kontrol et
    from database.mongo_operations import get_user_pdfs
    existing_pdfs = get_user_pdfs(username)
    for pdf in existing_pdfs:
        if pdf.get("related_analysis") == selected_file:
            return f"⚠️ '{selected_file}' dosyası için PDF zaten oluşturulmuş."

    # Şekilleri tekrar üret
    from plotly.subplots import make_subplots
    import plotly.express as px

    fig1 = generate_network_graph(selected_file, None)[0]
    fig2 = generate_network_graph(selected_file, None)[1]
    fig3 = generate_network_graph(selected_file, None)[2]

    figures = {
        "IP Trafik Ağı Haritası": fig1,
        "En Yoğun Trafik Üreten Düğümler": fig2,
        "En Fazla Bağlantıya Sahip IP'ler": fig3
    }

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    pdf_path = generate_pdf_from_figures(figures_dict=figures, meta_info={
        "Kullanıcı": username,
        "Dosya": selected_file,
        "Tarih": timestamp
    }, username=username)

    save_pdf_record(
        username=username,
        pdf_filename=os.path.basename(pdf_path),
        timestamp=datetime.datetime.now().isoformat(),
        related_analysis=selected_file,
        path=pdf_path
    )

    return f"✅ PDF başarıyla oluşturuldu: {os.path.basename(pdf_path)}"

