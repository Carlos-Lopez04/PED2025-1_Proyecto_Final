import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from datetime import datetime
import numpy as np
from sqlalchemy import create_engine

# Configuración de la app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "TMDB Dashboard"

# Función para conectar a la base de datos
def get_data_from_db():
    try:
        # Cambia los datos de usuario, contraseña y base según corresponda
        engine = create_engine("mysql+mysqlconnector://root:12345678@localhost/tmdb_db")
        df_combined = pd.read_sql("SELECT * FROM combined_popular ORDER BY popularity DESC", engine)
        df_movies = pd.read_sql("SELECT * FROM movies_popular ORDER BY popularity DESC", engine)
        df_tv = pd.read_sql("SELECT * FROM tv_popular ORDER BY popularity DESC", engine)
        return df_combined, df_movies, df_tv
    except Exception as e:
        print(f"Error: {e}")
        # Datos de ejemplo si no hay conexión a BD
        return create_sample_data()

def create_sample_data():
    """Crear datos de ejemplo para pruebas"""
    np.random.seed(42)

    movies_data = {
        'id': range(1, 51),
        'title': [f'Movie {i}' for i in range(1, 51)],
        'vote_average': np.random.uniform(6.0, 9.0, 50),
        'popularity': np.random.uniform(100, 1000, 50),
        'release_date': pd.date_range('2020-01-01', periods=50, freq='W'),
        'type': ['movie'] * 50
    }

    tv_data = {
        'id': range(51, 101),
        'title': [f'TV Show {i}' for i in range(1, 51)],
        'vote_average': np.random.uniform(6.0, 9.0, 50),
        'popularity': np.random.uniform(100, 1000, 50),
        'release_date': pd.date_range('2020-01-01', periods=50, freq='W'),
        'type': ['tv'] * 50
    }

    df_movies = pd.DataFrame(movies_data)
    df_tv = pd.DataFrame(tv_data)
    df_combined = pd.concat([df_movies, df_tv], ignore_index=True)

    return df_combined, df_movies, df_tv

# Obtener datos
df_combined, df_movies, df_tv = get_data_from_db()

# Estilos CSS personalizados
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "color": "white",
    "box-shadow": "2px 0 10px rgba(0,0,0,0.1)"
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa"
}

CARD_STYLE = {
    "background": "white",
    "border-radius": "15px",
    "box-shadow": "0 8px 25px rgba(0,0,0,0.1)",
    "margin-bottom": "20px",
    "border": "none"
}

# Componente del Sidebar
sidebar = html.Div([
    html.H2("🎬 TMDB", className="display-6 text-center mb-4"),
    html.Hr(style={"border-color": "rgba(255,255,255,0.3)"}),
    dbc.Nav([
        dbc.NavLink("🏠 Inicio", href="/", active="exact", className="text-white mb-2",
                    style={"border-radius": "10px", "padding": "10px 15px"}),
        dbc.NavLink("📊 Dashboard 1", href="/dashboard1", active="exact", className="text-white mb-2",
                    style={"border-radius": "10px", "padding": "10px 15px"}),
        dbc.NavLink("📈 Dashboard 2", href="/dashboard2", active="exact", className="text-white mb-2",
                    style={"border-radius": "10px", "padding": "10px 15px"}),
        dbc.NavLink("🎭 Dashboard 3", href="/dashboard3", active="exact", className="text-white mb-2",
                    style={"border-radius": "10px", "padding": "10px 15px"}),
        dbc.NavLink("📧 Contáctanos", href="/contacto", active="exact", className="text-white mb-2",
                    style={"border-radius": "10px", "padding": "10px 15px"}),
    ], vertical=True, pills=True),
    html.Hr(style={"border-color": "rgba(255,255,255,0.3)"}),
    html.Div([
        html.P("💡 Dashboard Mejorado", className="text-center text-white-50 small"),
        html.P(f"Última actualización: {datetime.now().strftime('%d/%m/%Y')}",
               className="text-center text-white-50 small")
    ])
], style=SIDEBAR_STYLE)

# Función para crear KPI Cards
def create_kpi_card(title, value, subtitle, color, icon, percentage=None):
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.Div([
                    html.H4(icon, className="mb-0", style={"color": color}),
                    html.H3(value, className="mb-0 fw-bold"),
                    html.P(title, className="text-muted mb-0"),
                    html.Small(subtitle, className="text-muted")
                ], className="d-flex flex-column"),
                html.Div([
                    html.H5(f"{percentage}%" if percentage else "",
                            className="mb-0",
                            style={"color": "#10b981" if percentage and percentage > 0 else "#ef4444"})
                ], className="text-end") if percentage else html.Div()
            ], className="d-flex justify-content-between align-items-start")
        ])
    ], style=CARD_STYLE)

# Página de Inicio
def create_home_page():
    return html.Div([
        html.H1("🎬 TMDB Analytics Dashboard", className="mb-4"),
        dbc.Row([
            dbc.Col([
                create_kpi_card("Total Movies", f"{len(df_movies):,}", "Películas populares", "#6366f1", "🎬", 12.4)
            ], width=3),
            dbc.Col([
                create_kpi_card("Total TV Shows", f"{len(df_tv):,}", "Series populares", "#10b981", "📺", 8.7)
            ], width=3),
            dbc.Col([
                create_kpi_card("Avg Rating", f"{df_combined['vote_average'].mean():.1f}", "Promedio general",
                                "#f59e0b", "⭐", 5.2)
            ], width=3),
            dbc.Col([
                create_kpi_card("Top Popularity", f"{df_combined['popularity'].max():.0f}", "Máxima popularidad",
                                "#ef4444", "🔥", 15.3)
            ], width=3),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📊 Resumen General"),
                    dbc.CardBody([
                        html.P("Este dashboard te permite analizar datos de películas y series de TMDB.",
                               className="mb-3"),
                        html.Ul([
                            html.Li("Dashboard 1: Análisis de popularidad y ratings"),
                            html.Li("Dashboard 2: Comparativa entre películas y series"),
                            html.Li("Dashboard 3: Tendencias temporales y evolución")
