import dash
from dash import dcc, html, Input, Output, callback_context
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import numpy as np
from sqlalchemy import create_engine

# Configuración de la app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "TMDB Dashboard Completo"


# Función para conectar a la base de datos y obtener TODOS los datos
def get_all_data_from_db():
    try:
        engine = create_engine("mysql+mysqlconnector://root:12345678@localhost/tmdb_db")

        # Obtener todas las tablas
        df_combined = pd.read_sql("SELECT * FROM combined_popular ORDER BY popularity DESC", engine)
        df_movies_popular = pd.read_sql("SELECT * FROM movies_popular ORDER BY popularity DESC", engine)
        df_movies_top_rated = pd.read_sql("SELECT * FROM top_rated_movies ORDER BY vote_average DESC",
                                          engine) if table_exists(engine, 'top_rated_movies') else pd.DataFrame()
        df_tv = pd.read_sql("SELECT * FROM tv_popular ORDER BY popularity DESC", engine)
        df_genres = pd.read_sql("SELECT * FROM genres", engine) if table_exists(engine, 'genres') else pd.DataFrame()

        # Obtener datos con géneros (JOIN)
        df_with_genres = pd.read_sql("""
            SELECT c.*, GROUP_CONCAT(g.genre_name) as genres
            FROM combined_popular c
            LEFT JOIN content_genres cg ON c.id = cg.content_id AND c.type = cg.content_type
            LEFT JOIN genres g ON cg.genre_id = g.genre_id
            GROUP BY c.id, c.type
            ORDER BY c.popularity DESC
        """, engine) if table_exists(engine, 'content_genres') else df_combined

        return df_combined, df_movies_popular, df_movies_top_rated, df_tv, df_genres, df_with_genres

    except Exception as e:
        print(f"Error conectando a BD: {e}")
        return create_sample_data()


def table_exists(engine, table_name):
    try:
        result = engine.execute(f"SHOW TABLES LIKE '{table_name}'")
        return result.rowcount > 0
    except:
        return False


def create_sample_data():
    # Datos de ejemplo mejorados
    np.random.seed(42)

    # Movies populares
    movies_popular_data = {
        'id': range(1, 51),
        'title': [f'Popular Movie {i}' for i in range(1, 51)],
        'vote_average': np.random.uniform(6.0, 8.5, 50),
        'popularity': np.random.uniform(200, 1000, 50),
        'release_date': pd.date_range('2020-01-01', periods=50, freq='W'),
        'release_year': np.random.randint(2018, 2024, 50),
        'type': ['movie'] * 50
    }

    # Movies top rated
    movies_top_data = {
        'id': range(101, 151),
        'title': [f'Top Rated Movie {i}' for i in range(1, 51)],
        'vote_average': np.random.uniform(8.0, 9.5, 50),
        'popularity': np.random.uniform(100, 500, 50),
        'release_date': pd.date_range('2015-01-01', periods=50, freq='M'),
        'release_year': np.random.randint(2015, 2023, 50),
        'type': ['movie'] * 50
    }

    # TV Shows
    tv_data = {
        'id': range(201, 251),
        'title': [f'TV Show {i}' for i in range(1, 51)],
        'vote_average': np.random.uniform(6.5, 9.0, 50),
        'popularity': np.random.uniform(150, 800, 50),
        'release_date': pd.date_range('2019-01-01', periods=50, freq='2W'),
        'release_year': np.random.randint(2019, 2024, 50),
        'type': ['tv'] * 50
    }

    # Géneros
    genres_data = {
        'genre_id': [28, 12, 16, 35, 80, 18, 14, 27, 10749, 878],
        'genre_name': ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Drama', 'Fantasy', 'Horror', 'Romance',
                       'Sci-Fi']
    }

    df_movies_popular = pd.DataFrame(movies_popular_data)
    df_movies_top_rated = pd.DataFrame(movies_top_data)
    df_tv = pd.DataFrame(tv_data)
    df_genres = pd.DataFrame(genres_data)
    df_combined = pd.concat([df_movies_popular, df_tv], ignore_index=True)
    df_with_genres = df_combined.copy()
    df_with_genres['genres'] = np.random.choice(
        ['Action,Drama', 'Comedy,Romance', 'Horror,Thriller', 'Sci-Fi,Adventure'], len(df_combined))

    return df_combined, df_movies_popular, df_movies_top_rated, df_tv, df_genres, df_with_genres


# Obtener todos los datos
df_combined, df_movies_popular, df_movies_top_rated, df_tv, df_genres, df_with_genres = get_all_data_from_db()

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
        dbc.NavLink("📊 Dashboard Completo", href="/dashboard1", active="exact", className="text-white mb-2",
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
        html.P("💡 Dashboard Completo", className="text-center text-white-50 small"),
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
        html.H1("🎬 TMDB Analytics Dashboard Completo", className="mb-4"),
        dbc.Row([
            dbc.Col([
                create_kpi_card("Movies Populares", f"{len(df_movies_popular):,}", "Películas populares", "#6366f1",
                                "🎬", 12.4)
            ], width=3),
            dbc.Col([
                create_kpi_card("Movies Top Rated", f"{len(df_movies_top_rated):,}", "Películas mejor calificadas",
                                "#8b5cf6", "🏆", 8.7)
            ], width=3),
            dbc.Col([
                create_kpi_card("TV Shows", f"{len(df_tv):,}", "Series populares", "#10b981", "📺", 5.2)
            ], width=3),
            dbc.Col([
                create_kpi_card("Géneros", f"{len(df_genres):,}", "Géneros disponibles", "#f59e0b", "🎭", 15.3)
            ], width=3),
        ], className="mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📊 Resumen Completo del Sistema"),
                    dbc.CardBody([
                        html.P("Este dashboard incluye TODAS las tablas de la base de datos TMDB:", className="mb-3"),
                        html.Ul([
                            html.Li("📊 Dashboard Completo: Análisis interactivo de todas las tablas"),
                            html.Li("🎬 Movies Populares: Películas más populares"),
                            html.Li("🏆 Movies Top Rated: Películas mejor calificadas"),
                            html.Li("📺 TV Shows: Series más populares"),
                            html.Li("🎭 Análisis por géneros y años")
                        ]),
                        html.Hr(),
                        html.H6("🆕 Nuevas Características:"),
                        html.Ul([
                            html.Li("Filtros interactivos por tipo de contenido"),
                            html.Li("Filtros por año de lanzamiento"),
                            html.Li("Análisis de géneros más populares"),
                            html.Li("Comparativas entre tablas")
                        ])
                    ])
                ], style=CARD_STYLE)
            ], width=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📈 Estadísticas Generales"),
                    dbc.CardBody([
                        html.P(f"🎬 Movies Populares: {len(df_movies_popular)}", className="mb-2"),
                        html.P(f"🏆 Movies Top Rated: {len(df_movies_top_rated)}", className="mb-2"),
                        html.P(f"📺 TV Shows: {len(df_tv)}", className="mb-2"),
                        html.P(f"🎭 Géneros: {len(df_genres)}", className="mb-2"),
                        html.Hr(),
                        html.P(f"📊 Total registros: {len(df_combined)}", className="mb-2 fw-bold"),
                        html.P(f"⭐ Rating promedio: {df_combined['vote_average'].mean():.1f}", className="mb-2"),
                        html.P(f"🔥 Popularidad máxima: {df_combined['popularity'].max():.0f}", className="mb-2")
                    ])
                ], style=CARD_STYLE)
            ], width=4)
        ])
    ])


# Dashboard 1 Completo e Interactivo
def create_dashboard1():
    # Obtener años únicos para el filtro
    all_years = sorted(df_combined['release_year'].dropna().unique()) if 'release_year' in df_combined.columns else [
        2020, 2021, 2022, 2023]

    return html.Div([
        html.H1("📊 Dashboard Completo - Análisis Interactivo", className="mb-4"),

        # KPIs dinámicos
        dbc.Row([
            dbc.Col([
                create_kpi_card("Movies Populares", f"{len(df_movies_popular)}", "Películas populares", "#6366f1", "🎬")
            ], width=3),
            dbc.Col([
                create_kpi_card("Movies Top Rated", f"{len(df_movies_top_rated)}", "Mejor calificadas", "#8b5cf6", "🏆")
            ], width=3),
            dbc.Col([
                create_kpi_card("TV Shows", f"{len(df_tv)}", "Series populares", "#10b981", "📺")
            ], width=3),
            dbc.Col([
                create_kpi_card("Géneros", f"{len(df_genres)}", "Géneros disponibles", "#f59e0b", "🎭")
            ], width=3),
        ], className="mb-4"),

        # Controles interactivos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🎛️ Controles Interactivos"),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label("Tipo de Contenido:", className="fw-bold"),
                                dcc.Dropdown(
                                    id='content-type-filter',
                                    options=[
                                        {'label': 'Todos', 'value': 'all'},
                                        {'label': '🎬 Movies Populares', 'value': 'movie_popular'},
                                        {'label': '🏆 Movies Top Rated', 'value': 'movie_top_rated'},
                                        {'label': '📺 TV Shows', 'value': 'tv'}
                                    ],
                                    value='all',
                                    style={'marginBottom': '10px'}
                                )
                            ], width=6),
                            dbc.Col([
                                html.Label("Año de Lanzamiento:", className="fw-bold"),
                                dcc.Dropdown(
                                    id='year-filter',
                                    options=[{'label': 'Todos los años', 'value': 'all'}] +
                                            [{'label': str(year), 'value': year} for year in all_years],
                                    value='all',
                                    style={'marginBottom': '10px'}
                                )
                            ], width=6)
                        ])
                    ])
                ], style=CARD_STYLE)
            ], width=12)
        ], className="mb-4"),

        # Gráficos principales
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📊 Análisis de Popularidad vs Rating"),
                    dbc.CardBody([
                        dcc.Graph(id='interactive-scatter-plot')
                    ])
                ], style=CARD_STYLE)
            ], width=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🎭 Distribución por Géneros"),
                    dbc.CardBody([
                        dcc.Graph(id='genre-distribution')
                    ])
                ], style=CARD_STYLE)
            ], width=4)
        ]),

        # Segunda fila de gráficos
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("🏆 Top 15 Contenido Seleccionado"),
                    dbc.CardBody([
                        dcc.Graph(id='top-content-bar')
                    ])
                ], style=CARD_STYLE)
            ], width=8),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📈 Estadísticas por Año"),
                    dbc.CardBody([
                        dcc.Graph(id='yearly-stats')
                    ])
                ], style=CARD_STYLE)
            ], width=4)
        ]),

        # Tercera fila - Tabla interactiva
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("📋 Tabla Detallada del Contenido Filtrado"),
                    dbc.CardBody([
                        html.Div(id='detailed-table')
                    ])
                ], style=CARD_STYLE)
            ], width=12)
        ])
    ])


# Callbacks para interactividad
@app.callback(
    [Output('interactive-scatter-plot', 'figure'),
     Output('genre-distribution', 'figure'),
     Output('top-content-bar', 'figure'),
     Output('yearly-stats', 'figure'),
     Output('detailed-table', 'children')],
    [Input('content-type-filter', 'value'),
     Input('year-filter', 'value')]
)
def update_dashboard(content_type, year_filter):
    # Filtrar datos según selección
    if content_type == 'all':
        filtered_data = df_combined.copy()
        color_col = 'type'
        title_suffix = "Todo el Contenido"
    elif content_type == 'movie_popular':
        filtered_data = df_movies_popular.copy()
        color_col = None
        title_suffix = "Movies Populares"
    elif content_type == 'movie_top_rated' and not df_movies_top_rated.empty:
        filtered_data = df_movies_top_rated.copy()
        color_col = None
        title_suffix = "Movies Top Rated"
    elif content_type == 'tv':
        filtered_data = df_tv.copy()
        color_col = None
        title_suffix = "TV Shows"
    else:
        filtered_data = df_combined.copy()
        color_col = 'type'
        title_suffix = "Todo el Contenido"

    # Filtrar por año
    if year_filter != 'all' and 'release_year' in filtered_data.columns:
        filtered_data = filtered_data[filtered_data['release_year'] == year_filter]

    # Gráfico de dispersión
    if color_col and color_col in filtered_data.columns:
        scatter_fig = px.scatter(
            filtered_data.head(100), x='vote_average', y='popularity',
            color=color_col, size='popularity',
            title=f"Popularidad vs Rating - {title_suffix}",
            labels={'vote_average': 'Rating Promedio', 'popularity': 'Popularidad'},
            hover_data=['title'] if 'title' in filtered_data.columns else None
        )
    else:
        scatter_fig = px.scatter(
            filtered_data.head(100), x='vote_average', y='popularity',
            size='popularity',
            title=f"Popularidad vs Rating - {title_suffix}",
            labels={'vote_average': 'Rating Promedio', 'popularity': 'Popularidad'},
            hover_data=['title'] if 'title' in filtered_data.columns else None
        )

    scatter_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#1f2937'
    )

    # Gráfico de géneros (simulado si no hay datos reales)
    if not df_genres.empty and 'genres' in df_with_genres.columns:
        # Procesar géneros reales
        genre_counts = {}
        for genres in df_with_genres['genres'].dropna():
            for genre in str(genres).split(','):
                genre = genre.strip()
                genre_counts[genre] = genre_counts.get(genre, 0) + 1

        genre_df = pd.DataFrame(list(genre_counts.items()), columns=['Genre', 'Count'])
        genre_df = genre_df.head(10)
    else:
        # Géneros simulados
        genre_df = pd.DataFrame({
            'Genre': ['Action', 'Drama', 'Comedy', 'Thriller', 'Romance'],
            'Count': [25, 20, 18, 15, 12]
        })

    genre_fig = px.pie(
        genre_df, values='Count', names='Genre',
        title="Distribución por Géneros"
    )
    genre_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#1f2937'
    )

    # Top 15 contenido
    top_15 = filtered_data.nlargest(15, 'popularity')
    bar_fig = px.bar(
        top_15, x='popularity', y='title', orientation='h',
        title=f"Top 15 - {title_suffix}",
        color='vote_average' if len(top_15) > 0 else None,
        color_continuous_scale='viridis'
    )
    bar_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#1f2937',
        yaxis={'categoryorder': 'total ascending'}
    )

    # Estadísticas por año
    if 'release_year' in filtered_data.columns:
        yearly_data = filtered_data.groupby('release_year').agg({
            'vote_average': 'mean',
            'popularity': 'mean'
        }).reset_index()

        yearly_fig = px.line(
            yearly_data, x='release_year', y='vote_average',
            title=f"Rating Promedio por Año - {title_suffix}",
            markers=True
        )
    else:
        # Datos simulados
        yearly_fig = px.line(
            x=[2020, 2021, 2022, 2023], y=[7.5, 7.8, 7.6, 7.9],
            title="Rating Promedio por Año"
        )

    yearly_fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#1f2937'
    )

    # Tabla detallada
    table_data = filtered_data.head(20)
    if not table_data.empty:
        table = dbc.Table.from_dataframe(
            table_data[['title', 'vote_average', 'popularity', 'release_date', 'type']].round(2),
            striped=True, bordered=True, hover=True, responsive=True
        )
    else:
        table = html.P("No hay datos disponibles para los filtros seleccionados.")

    return scatter_fig, genre_fig, bar_fig, yearly_fig, table


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
        return create_dashboard2()  # Mantener el dashboard 2 original
    elif pathname == "/dashboard3":
        return create_dashboard3()  # Mantener el dashboard 3 original
    elif pathname == "/contacto":
        return create_contact_page()
    return html.Div([
        html.H1("404: Página no encontrada", className="text-danger"),
        html.P("La página que buscas no existe.")
    ])


# Funciones de los otros dashboards (mantener las originales)
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

    # Estadísticas
    movie_stats = df_movies_popular['vote_average'].describe()
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
                        html.P(f"🎬 Movies Populares: {len(df_movies_popular)}", className="mb-2"),
                        html.P(f"🏆 Movies Top Rated: {len(df_movies_top_rated)}", className="mb-2"),
                        html.P(f"📺 TV Shows: {len(df_tv)}", className="mb-2"),
                        html.P(f"🎭 Géneros: {len(df_genres)}", className="mb-2"),
                        html.Hr(),
                        html.P(f"📊 Total registros: {len(df_combined)}", className="mb-2 fw-bold"),
                        html.P(f"📅 Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}", className="mb-2")
                    ])
                ], style=CARD_STYLE)
            ], width=4)
        ])
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
