from dash import html

layout = html.Div([
    html.H2("Dışa Aktarma ve Mail Gönderme", style={"text-align": "center", "color": "#00FF00"}),
    html.P("Seçtiğiniz analizleri PDF olarak dışa aktarabilir ve yöneticinize e-posta ile gönderebilirsiniz."),
    html.Div(id="export-output")
], style={"backgroundColor": "#000000", "color": "#00FF00", "padding": "20px", "font-family": "Arial, sans-serif"})
