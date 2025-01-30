from dash import Dash, html

# Uygulamayı başlat
app = Dash(__name__)

# Layout tanımı
app.layout = html.Div(
    style={"display": "flex", "flexDirection": "column", "height": "100vh", "margin": "0", "padding": "0"},
    children=[
        # Başlık kısmı
        html.Div(
            style={"backgroundColor": "black", "height": "10%", "width": "100%", "border": "1px solid white"},
            children=[
                html.H1(
                    "Başlık",
                    style={"color": "white", "textAlign": "center", "margin": "0", "padding": "10px"}
                )
            ]
        ),
        # İçerik kısmı
        html.Div(
            style={"display": "flex", "flex": "1", "border": "1px solid white"},
            children=[
                # Sol sütun
                html.Div(
                    style={"width": "20%", "borderRight": "1px solid white", "backgroundColor": "black"},
                    children=[]
                ),
                # Sağ sütun
                html.Div(
                    style={"flex": "1", "backgroundColor": "black"},
                    children=[]
                ),
            ]
        ),
    ]
)

# Uygulamayı çalıştır
if __name__ == '__main__':
    app.run_server(debug=True)
