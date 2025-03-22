from dash import html

layout = html.Div([
    html.H2("Analiz Sayfası", style={"text-align": "center", "color": "#00FF00"}),
    html.P("Yüklenen PCAP dosyası burada analiz edilecektir."),
    html.Div(id="analysis-output")
], style={"backgroundColor": "#000000", "color": "#00FF00", "padding": "20px", "font-family": "Arial, sans-serif"})
