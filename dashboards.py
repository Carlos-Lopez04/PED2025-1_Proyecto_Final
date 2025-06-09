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
        #* Cambia los datos de usuario, contraseña y base según corresponda
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
    # Crear datos de ejemplo para realizar pruebas
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

# Obtener los datos
df_combined, df_movies, df_tv = get_data_from_db()

# Estilos CSS
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

# Función para crear los KPI Cards
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

# Página de inicio
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
                        ])
                    ])
                ], style=CARD_STYLE)
            ], width=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🎯 Top 5 Más Populares"),
                    dbc.CardBody([
                        html.Div([
                            html.P(f"{i + 1}. {row['title'][:30]}{'...' if len(row['title']) > 30 else ''}",
                                className="mb-1 small")
                            for i, (_, row) in enumerate(df_combined.head(5).iterrows())
                        ])
                    ])
                ], style=CARD_STYLE)
            ], width=4)
        ])
    ])

#Crear dashboard #1
def create_dashboard1():
    
    # Gráfico de dispersión popularidad vs rating
    scatter_fig = px.scatter(
        df_combined, x='vote_average', y='popularity',
        color='type', size='popularity',
        title="Popularidad vs Rating",
        labels={'vote_average': 'Rating Promedio', 'popularity': 'Popularidad'},
        color_discrete_map={'movie': '#6366f1', 'tv': '#10b981'}
    )
    scatter_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#1f2937'
    )

    # Gráfico de barras con el top 10 de pelis
    top_10 = df_combined.head(10)
    bar_fig = px.bar(
        top_10, x='popularity', y='title', orientation='h',
        color='type', title="Top 10 Más Populares",
        color_discrete_map={'movie': '#6366f1', 'tv': '#10b981'}
    )
    bar_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#1f2937',
        yaxis={'categoryorder': 'total ascending'}
    )

    return html.Div([
        html.H1("📊 Dashboard 1 - Análisis de Popularidad", className="mb-4"),
        dbc.Row([
            dbc.Col([
                create_kpi_card("Movies", f"{len(df_movies)}", "Total películas", "#6366f1", "🎬")
            ], width=4),
            dbc.Col([
                create_kpi_card("TV Shows", f"{len(df_tv)}", "Total series", "#10b981", "📺")
            ], width=4),
            dbc.Col([
                create_kpi_card("Avg Rating", f"{df_combined['vote_average'].mean():.1f}", "Rating promedio", "#f59e0b",
                                "⭐")
            ], width=4),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(figure=scatter_fig)
                    ])
                ], style=CARD_STYLE)
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(figure=bar_fig)
                    ])
                ], style=CARD_STYLE)
            ], width=6)
        ])
    ])

#Crear el dashboard #2
def create_dashboard2():
    
    # Gráfico circular de distribución
    type_counts = df_combined['type'].value_counts()
    pie_fig = px.pie(
        values=type_counts.values, names=type_counts.index,
        title="Distribución Movies vs TV Shows",
        color_discrete_map={'movie': '#6366f1', 'tv': '#10b981'}
    )
    pie_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#1f2937'
    )

    # Box plot de ratings por tipo
    box_fig = px.box(
        df_combined, x='type', y='vote_average',
        color='type', title="Distribución de Ratings por Tipo",
        color_discrete_map={'movie': '#6366f1', 'tv': '#10b981'}
    )
    box_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#1f2937'
        
    )

    #Estadisticas
    movie_stats = df_movies['vote_average'].describe()
    tv_stats = df_tv['vote_average'].describe()

    return html.Div([
        html.H1("📈 Dashboard 2 - Comparativa Movies vs TV", className="mb-4"),
        dbc.Row([
            dbc.Col([
                create_kpi_card("Movies Avg", f"{movie_stats['mean']:.1f}", "Rating promedio movies", "#6366f1", "🎬")
            ], width=4),
            dbc.Col([
                create_kpi_card("TV Avg", f"{tv_stats['mean']:.1f}", "Rating promedio TV", "#10b981", "📺")
            ], width=4),
            dbc.Col([
                create_kpi_card("Diferencia", f"{abs(movie_stats['mean'] - tv_stats['mean']):.1f}",
                                "Diferencia promedio", "#f59e0b", "📊")
            ], width=4),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(figure=pie_fig)
                    ])
                ], style=CARD_STYLE)
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(figure=box_fig)
                    ])
                ], style=CARD_STYLE)
            ], width=6)
        ])
    ])

#Dashboard #3
def create_dashboard3():
    # Convertir fechas
    df_combined['release_date'] = pd.to_datetime(df_combined['release_date'])
    df_combined['year'] = df_combined['release_date'].dt.year

 # Tendencia por año
    yearly_data = df_combined.groupby(['year', 'type']).agg({
        'vote_average': 'mean',
        'popularity': 'mean'
    }).reset_index()

    line_fig = px.line(
        yearly_data, x='year', y='vote_average', color='type',
        title="Evolución del Rating Promedio por Año",
        color_discrete_map={'movie': '#6366f1', 'tv': '#10b981'}
    )
    line_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#1f2937'
    )

    # Histograma de ratings
    hist_fig = px.histogram(
        df_combined, x='vote_average', color='type',
        title="Distribución de Ratings",
        color_discrete_map={'movie': '#6366f1', 'tv': '#10b981'},
        opacity=0.7
    )
    hist_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#1f2937'
    )

    return html.Div([
        html.H1("🎭 Dashboard 3 - Tendencias Temporales", className="mb-4"),
        dbc.Row([
            dbc.Col([
                create_kpi_card("Años", f"{df_combined['year'].nunique()}", "Años cubiertos", "#6366f1", "📅")
            ], width=4),
            dbc.Col([
                create_kpi_card("Mejor Año", f"{yearly_data.loc[yearly_data['vote_average'].idxmax(), 'year']:.0f}",
                                "Año con mejor rating", "#10b981", "🏆")
            ], width=4),
            dbc.Col([
                create_kpi_card("Rating Max", f"{df_combined['vote_average'].max():.1f}", "Rating más alto", "#f59e0b",
                                "⭐")
            ], width=4),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(figure=line_fig)
                    ])
                ], style=CARD_STYLE)
            ], width=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Graph(figure=hist_fig)
                    ])
                ], style=CARD_STYLE)
            ], width=4)
        ])
    ])

# Página de Contacto
def create_contact_page():
    return html.Div([
        html.H1("📧 Contáctanos", className="mb-4"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📬 Información de Contacto"),
                    dbc.CardBody([
                        html.H5("¿Tienes preguntas sobre este dashboard?", className="mb-3"),
                        html.P("Este dashboard fue creado usando datos de TMDB API.", className="mb-3"),
                        html.Hr(),
                        html.H6("🔧 Tecnologías utilizadas:"),
                        html.Ul([
                            html.Li("Python + Dash"),
                            html.Li("Plotly para visualizaciones"),
                            html.Li("MySQL para base de datos"),
                            html.Li("Bootstrap para estilos")
                        ]),
                        html.Hr(),
                        html.P("📊 Dashboard creado para análisis de datos de entretenimiento", className="text-muted")
                    ])
                ], style=CARD_STYLE)
            ], width=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📈 Estadísticas del Sistema"),
                    dbc.CardBody([
                        html.P(f"🎬 Movies: {len(df_movies)}", className="mb-2"),
                        html.P(f"📺 TV Shows: {len(df_tv)}", className="mb-2"),
                        html.P(f"📊 Total registros: {len(df_combined)}", className="mb-2"),
                        html.P(f"📅 Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}", className="mb-2")
                    ])
                ], style=CARD_STYLE)
            ], width=4)
        ])
    ])

# Layout principal
app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    html.Div(id="page-content", style=CONTENT_STYLE)
])

# Callback para navegación
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return create_home_page()
    elif pathname == "/dashboard1":
        return create_dashboard1()
    elif pathname == "/dashboard2":
        return create_dashboard2()
    elif pathname == "/dashboard3":
        return create_dashboard3()
    elif pathname == "/contacto":
        return create_contact_page()
    return html.Div([
        html.H1("404: Página no encontrada", className="text-danger"),
        html.P("La página que buscas no existe.")
    ])

# CSS adicional
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .nav-link:hover {
                background-color: rgba(255,255,255,0.1) !important;
                transform: translateX(5px);
                transition: all 0.3s ease;
            }
            .nav-link.active {
                background-color: rgba(255,255,255,0.2) !important;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8050)
