import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import random
from datetime import datetime

app = dash.Dash(__name__)

# Couleurs personnalisées
COLORS = {
    'background': '#1e2130',
    'card': '#2b2f4b',
    'text': '#ffffff',
    'temp': '#ff4d4d',
    'hum': '#33ccff',
    'co2': '#00ffcc',
    'h2': '#ffcc00'
}

app.layout = html.Div(style={'backgroundColor': COLORS['background'], 'color': COLORS['text'], 'fontFamily': 'sans-serif', 'padding': '20px'}, children=[
    
    html.H1("🚀 MONITORING CAPTEURS TEMPS RÉEL", style={'textAlign': 'center', 'marginBottom': '30px', 'fontWeight': 'bold', 'letterSpacing': '2px'}),
    
    dcc.Interval(id='interval-component', interval=2000, n_intervals=0),

    # Grille des indicateurs (Cartes colorées)
    html.Div(style={'display': 'grid', 'gridTemplateColumns': 'repeat(4, 1fr)', 'gap': '20px', 'marginBottom': '30px'}, children=[
        html.Div(id='card-temp', style={'backgroundColor': COLORS['card'], 'padding': '20px', 'borderRadius': '15px', 'borderLeft': f'10px solid {COLORS["temp"]}', 'textAlign': 'center'}),
        html.Div(id='card-hum', style={'backgroundColor': COLORS['card'], 'padding': '20px', 'borderRadius': '15px', 'borderLeft': f'10px solid {COLORS["hum"]}', 'textAlign': 'center'}),
        html.Div(id='card-co2', style={'backgroundColor': COLORS['card'], 'padding': '20px', 'borderRadius': '15px', 'borderLeft': f'10px solid {COLORS["co2"]}', 'textAlign': 'center'}),
        html.Div(id='card-h2', style={'backgroundColor': COLORS['card'], 'padding': '20px', 'borderRadius': '15px', 'borderLeft': f'10px solid {COLORS["h2"]}', 'textAlign': 'center'}),
    ]),

    # Graphiques stylisés
    html.Div(style={'display': 'flex', 'gap': '20px'}, children=[
        dcc.Graph(id='graph-main', style={'width': '100%', 'borderRadius': '15px', 'overflow': 'hidden'})
    ])
])

data_store = {'time': [], 'temp': [], 'hum': [], 'co2': [], 'h2': []}

@app.callback(
    [Output('card-temp', 'children'), Output('card-hum', 'children'),
     Output('card-co2', 'children'), Output('card-h2', 'children'),
     Output('graph-main', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_dashboard(n):
    # Simulation des données
    now = datetime.now().strftime('%H:%M:%S')
    t, h, c, h2 = round(random.uniform(20, 26), 1), round(random.uniform(40, 55), 1), round(random.uniform(400, 900)), round(random.uniform(0, 5), 2)

    for key, val in zip(['time', 'temp', 'hum', 'co2', 'h2'], [now, t, h, c, h2]):
        data_store[key].append(val)
        data_store[key] = data_store[key][-15:]

    # Création des contenus de cartes
    def create_card(label, value, unit, color):
        return [html.H3(label, style={'fontSize': '16px', 'opacity': '0.7'}), 
                html.P(f"{value} {unit}", style={'fontSize': '28px', 'fontWeight': 'bold', 'color': color})]

    # Graphique avec design Dark
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data_store['time'], y=data_store['temp'], name="Temp °C", line=dict(color=COLORS['temp'], width=4), mode='lines+markers'))
    fig.add_trace(go.Scatter(x=data_store['time'], y=data_store['hum'], name="Hum %", line=dict(color=COLORS['hum'], width=4), yaxis="y2"))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(l=40, r=40, t=40, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(gridcolor='#3d405b'),
        yaxis=dict(title="Température (°C)", gridcolor='#3d405b'),
        yaxis2=dict(title="Humidité (%)", overlaying='y', side='right')
    )

    return (create_card("TEMPÉRATURE", t, "°C", COLORS['temp']),
            create_card("HUMIDITÉ", h, "%", COLORS['hum']),
            create_card("CO2", c, "ppm", COLORS['co2']),
            create_card("H2", h2, "ppm", COLORS['h2']),
            fig)

if __name__ == '__main__':
    app.run(debug=True)