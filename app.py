import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from datetime import datetime
import json
import os

# --- FUNCIÓN PARA REGISTRAR EN LA BITÁCORA ---
LOG_FILE = "bitacora_mlops.jsonl"

def registrar_evento(accion, detalles):
    """Guarda un evento en el archivo JSONL para MLOps."""
    registro = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "accion": accion,
        "detalles": detalles
    }
    # Abre el archivo en modo 'append' (añadir al final)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(registro) + "\n")

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(
    page_title="Dashboard Dirección Orquestal | MLOps",
    page_icon="🎼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ESTILOS CSS (UI Premium + Menú Estático) ---
st.markdown("""
<style>
    /* Tema Oscuro Base */
    .stApp { background-color: #0E1117; }
    
    /* FORZAR BARRA LATERAL ESTÁTICA Y OSCURA */
    [data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid #1F2937;
        min-width: 300px !important;
        max-width: 300px !important;
    }
    /* Ocultar el botón de colapsar menú */
    [data-testid="collapsedControl"] { display: none; }
    
    /* Tipografía general */
    h1, h2, h3, h4 { font-family: 'Inter', sans-serif !important; color: #F9FAFB !important; }
    p, li, div.stMarkdown { font-family: 'Inter', sans-serif; color: #D1D5DB; line-height: 1.7; font-size: 0.95rem; }
    
    /* Tarjetas KPI */
    .metric-box {
        background-color: #111827;
        border: 1px solid #1F2937;
        border-radius: 8px;
        padding: 20px;
        border-left: 4px solid #3B82F6;
        margin-bottom: 15px;
        transition: transform 0.2s ease;
    }
    .metric-box:hover { transform: translateY(-3px); }
    .metric-box.green { border-left: 4px solid #10B981; }
    .metric-box.orange { border-left: 4px solid #F59E0B; }
    .metric-box.purple { border-left: 4px solid #8B5CF6; }
    
    .metric-label { font-size: 0.75rem; color: #9CA3AF; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; }
    .metric-value { font-family: 'Courier New', monospace; font-size: 2.2rem; color: #F9FAFB; font-weight: bold; margin-top: 5px; }
    .metric-sub { font-size: 0.8rem; color: #6B7280; margin-top: 5px; }

    /* Header superior */
    .top-header {
        background-color: #111827; padding: 20px 30px; border-radius: 10px;
        border: 1px solid #1F2937; display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 30px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .header-title { font-size: 1.8rem; font-weight: 700; margin: 0; color: #F9FAFB; letter-spacing: -0.5px; }
    .header-subtitle { font-size: 0.95rem; color: #9CA3AF; margin: 5px 0 0 0; }
    .status-badge {
        background-color: rgba(16, 185, 129, 0.1); color: #10B981; 
        padding: 8px 16px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; border: 1px solid #10B981;
    }

    /* Bloques de análisis de texto (Notas técnicas) */
    .analysis-block {
        background-color: #1F2937; border-radius: 8px; padding: 25px;
        border-left: 4px solid #F59E0B; margin-top: 20px; margin-bottom: 30px;
    }
    .analysis-block h4 { margin-top: 0; color: #F59E0B !important; font-size: 1.2rem; margin-bottom: 15px; }
    .analysis-block p { margin-bottom: 10px; color: #D1D5DB; font-size: 0.95rem; text-align: justify; }
    .analysis-block ul { margin-bottom: 0; color: #D1D5DB; font-size: 0.95rem; }
    .analysis-block li { margin-bottom: 8px; }

    /* Estilos de pestañas */
    .stTabs [data-baseweb="tab"] { padding: 10px 20px; background-color: #111827; border-radius: 5px; color: #9CA3AF; }
    .stTabs [aria-selected="true"] { background-color: #3B82F6 !important; color: white !important; font-weight: bold; }

    /* Ocultar menús por defecto */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- 3. CARGA DE DATOS ---
@st.cache_data
def cargar_datos():
    df = pd.read_csv("demo/features_clustering.csv") if os.path.exists("demo/features_clustering.csv") else None
    metricas = json.load(open("demo/reporte_limpieza_metricas.json")) if os.path.exists("demo/reporte_limpieza_metricas.json") else {}
    return df, metricas

df, metricas = cargar_datos()

# --- 4. BARRA LATERAL ESTÁTICA ---
with st.sidebar:
    st.markdown("### 🎼 DIRECCIÓN ORQUESTAL")
    st.markdown("<p style='color: #6B7280; font-size: 0.8rem;'>Análisis No Supervisado (DAT-255)</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    seccion_actual = option_menu(
        menu_title="SECCIONES",
        options=["Panorama General", "Análisis Visual & Datos", "Modelos & Inferencia", "Bitácora MLOps", "Metodología & Gobernanza"],
        icons=["house", "bar-chart", "cpu", "journal-text", "gear"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "#111827"},
            "icon": {"color": "#9CA3AF", "font-size": "16px"}, 
            "nav-link": {"font-size": "14px", "text-align": "left", "margin":"5px 0", "color": "#9CA3AF"},
            "nav-link-selected": {"background-color": "#1E3A8A", "color": "white", "font-weight": "bold"},
        }
    )
    
    st.markdown("---")
    st.markdown("""
    <div style="background-color: #1F2937; padding: 15px; border-radius: 8px; border-left: 3px solid #10B981;">
        <div style="font-size: 0.7rem; color: #9CA3AF; text-transform: uppercase; letter-spacing: 1px;">Modelo Activo</div>
        <div style="color: #10B981; font-weight: bold; font-size: 1.1rem; margin-top: 5px;">🟢 Ward Jerárquico (k=3)</div>
        <div style="font-size: 0.75rem; color: #6B7280; margin-top: 5px;">v1.0.0 - Entorno de Producción</div>
    </div>
    """, unsafe_allow_html=True)

# --- 5. HEADER SUPERIOR ---
st.markdown(f"""
<div class="top-header">
    <div>
        <h1 class="header-title">{seccion_actual}</h1>
        <p class="header-subtitle">Exploración analítica y descubrimiento de patrones cinemáticos</p>
    </div>
    <div>
        <span class="status-badge">● Sistema Operativo</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 6. CONTENIDO DE LAS SECCIONES ---

if seccion_actual == "Panorama General":
    st.markdown("""
    ### Resumen Ejecutivo del Estudio
    La dirección orquestal es un acto de comunicación complejo. A través de la captura de movimiento (mocap) de alta precisión, este proyecto transforma el arte gestual en datos cuantificables. 
    
    Utilizando un pipeline de **aprendizaje no supervisado**, procesamos más de **976,000 frames** de movimiento de 6 directores interpretando obras de Mozart, Dvořák y Bartók. El objetivo no es predecir, sino descubrir la estructura oculta del movimiento: identificar estados cinemáticos recurrentes que permitan objetivar la diferencia entre un gesto fluido (*legato*) y uno de ataque (*staccato*).
    """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-box"><div class="metric-label">Frames Totales</div><div class="metric-value">976K</div><div class="metric-sub">Frecuencia: 120 Hz</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box green"><div class="metric-label">Clústeres (k)</div><div class="metric-value">3</div><div class="metric-sub">Selección automática</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"><div class="metric-label">Índice Silhouette</div><div class="metric-value">0.231</div><div class="metric-sub">Cohesión intra-grupo</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-box orange"><div class="metric-label">Davies-Bouldin</div><div class="metric-value">1.70</div><div class="metric-sub">Similitud inter-grupo</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Inspección de Datos Crudos Procesados")
    st.write("La tabla inferior muestra una porción del dataset final. Cada fila representa un frame capturado a una fracción de segundo. Las columnas reflejan las variables biomecánicas calculadas, como velocidades y aceleraciones de las manos y la batuta.")
    
    if df is not None:
        st.dataframe(df.head(10), use_container_width=True)

elif seccion_actual == "Análisis Visual & Datos":
    st.markdown("### Análisis de Rendimiento y Evaluación Visual")
    st.write("""
    En esta sección desglosamos la evidencia visual generada por el pipeline. La calidad de un modelo no supervisado no se mide por su precisión, sino por su capacidad para encontrar estructuras lógicas y cohesivas en los datos. A continuación, se presentan los cuatro pilares de nuestra evaluación.
    """)
    
    tab_graf1, tab_graf2, tab_graf3, tab_graf4 = st.tabs(["📈 Métricas de Modelos", "🔍 Reducción PCA", "⏱️ Secuencia Temporal", "📊 Perfiles de Clúster"])
    
    with tab_graf1:
        if os.path.exists("demo/figuras/01_metricas_modelos.png"):
            st.image("demo/figuras/01_metricas_modelos.png", use_column_width=True)
        
        st.markdown("""
        <div class="analysis-block">
            <h4>Interpretación de las Métricas de Agrupamiento</h4>
            <p><b>Índice Silhouette (Mayor es mejor):</b> Este gráfico mide la separación entre los clústeres. Observamos un pico claro en <b>k=3</b> (aproximadamente 0.231). Esto indica que dividir el movimiento en 3 estados es la configuración matemáticamente más sólida. A partir de k=4, el índice cae drásticamente, lo que significa que se están forzando divisiones artificiales en el movimiento.</p>
            <p><b>Índice Davies-Bouldin (Menor es mejor):</b> Mide la similitud promedio entre clústeres. Ambos algoritmos (Ward y K-Means) mantienen valores estables y bajos (alrededor de 1.70) para k=2 y k=3, confirmando que la estructura de 3 grupos es robusta. El comportamiento irregular de Ward en k=5 y k=6 sugiere sobreajuste.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with tab_graf2:
        if os.path.exists("demo/figuras/02_pca_clusters.png"):
            st.image("demo/figuras/02_pca_clusters.png", use_column_width=True)
            
        st.markdown("""
        <div class="analysis-block">
            <h4>Análisis de Componentes Principales (PCA)</h4>
            <p>El PCA reduce las 12 variables biomecánicas a solo 2 dimensiones (PC1 y PC2) para que podamos visualizar los datos en un plano. Juntas, estas dos dimensiones explican el <b>43% de la varianza total</b> del movimiento.</p>
            <p>El <b>Clúster 0 (azul)</b> forma una masa densa y compacta en el centro-izquierda. Esto representa el "estado base" del director: movimientos suaves y repetitivos. El <b>Clúster 2 (celeste)</b> se dispersa hacia la derecha y hacia abajo, capturando los movimientos más erráticos y veloces. El <b>Clúster 1 (marrón)</b> se aísla en la parte superior, representando posturas estáticas o preparatorias.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with tab_graf3:
        if os.path.exists("demo/figuras/03_clusters_tiempo.png"):
            st.image("demo/figuras/03_clusters_tiempo.png", use_column_width=True)
            
        st.markdown("""
        <div class="analysis-block">
            <h4>Dinámica Temporal del Gesto</h4>
            <p>Este gráfico es fundamental para entender la música. Muestra qué clúster se activó en cada segundo de la grabación (los 125 segundos de la primera muestra).</p>
            <p>Se observa que el director <b>no permanece en un solo estado</b>. El Clúster 0 (sostenimiento) actúa como la línea base. Sin embargo, el Clúster 2 (ataques) aparece en ráfagas intermitentes (por ejemplo, entre los segundos 20-45 y 54-91). Estas transiciones frecuentes reflejan los cambios de dinámica y las entradas de los instrumentos. La alternancia rápida indica que el modelo captura la naturaleza dinámica de la dirección.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with tab_graf4:
        if os.path.exists("demo/figuras/04_perfiles_clusters.png"):
            st.image("demo/figuras/04_perfiles_clusters.png", use_column_width=True)
            
        st.markdown("""
        <div class="analysis-block">
            <h4>Perfilado de las Variables Biomecánicas</h4>
            <p>Esta gráfica de barras (z-score) nos dice <b>qué hace diferente a cada clúster</b>. Las variables han sido estandarizadas, por lo que 0 es el promedio.</p>
            <ul>
                <li><b>Clúster 2 (Verde):</b> Tiene valores muy altos (+1.5) en "velocidad de mano" y "energía cinética". Es el clúster del <b>Staccato</b> y los ataques fuertes.</li>
                <li><b>Clúster 1 (Naranja):</b> Destaca por posiciones específicas (ejes X e Y) más que por velocidad. Representa gestos de señalización o preparación hacia una sección de la orquesta.</li>
                <li><b>Clúster 0 (Azul):</b> Valores ligeramente negativos (-0.3) en velocidad y energía. Es el clúster del <b>Legato</b>, el flujo continuo del compás.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

elif seccion_actual == "Modelos & Inferencia":
    st.markdown("### Benchmark y Configuración de Algoritmos")
    st.write("Para garantizar la robustez del análisis, se implementaron y compararon dos enfoques de clustering. El objetivo era encontrar el algoritmo que mejor manejara el ruido de las oclusiones (pérdida de marcadores) y la alta dimensionalidad de los datos.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="metric-box"><div class="metric-label">Algoritmo Seleccionado</div><div class="metric-value">Ward</div><div class="metric-sub">Aglomerativo Jerárquico</div></div>', unsafe_allow_html=True)
    with col_b:
        st.markdown('<div class="metric-box purple"><div class="metric-label">Variables Utilizadas</div><div class="metric-value">12</div><div class="metric-sub">Cinemática de manos y batuta</div></div>', unsafe_allow_html=True)

    st.markdown("""
    ### ¿Por qué Ward y no K-Means?
    Aunque K-Means es más rápido, **Ward Jerárquico** minimiza la varianza interna de los grupos, lo que genera clústeres más equilibrados y esféricos, ideales para datos biomecánicos continuos. Dado que Ward tiene un costo computacional cuadrático O(n²), se aplicó una estrategia de aproximación: se entrenó sobre una muestra representativa de 3,500 frames y luego se asignaron los casi 1 millón de frames restantes al centroide más cercano.
    """)
    
    if os.path.exists("demo/metricas_clustering.csv"):
        st.markdown("#### Tabla Comparativa de Rendimiento")
        df_metricas = pd.read_csv("demo/metricas_clustering.csv")
        st.dataframe(df_metricas, use_container_width=True)
        st.caption("Nota: Los valores de Silhouette y Davies-Bouldin se calcularon sobre un subconjunto de 3,000 observaciones para optimizar tiempos.")

elif seccion_actual == "Bitácora MLOps":
    st.markdown("### Bitácora de Análisis y Trazabilidad (MLOps)")
    st.write("""
    En un entorno de producción, es vital auditar cada paso del pipeline. Esta sección documenta los **Hitos de Ingeniería de Datos** extraídos directamente del reporte técnico del modelo. 
    Garantiza que cada decisión (limpieza, escalado, modelado) sea reproducible y auditable.
    """)
    
    # Intentamos leer el JSON de la Persona 2
    if os.path.exists("demo/reporte_limpieza_metricas.json"):
        with open("demo/reporte_limpieza_metricas.json", "r", encoding="utf-8") as f:
            reporte = json.load(f)
            
        # Extraemos la info del JSON (con valores por defecto por si acaso)
        # Nota: Ajusta estas claves según la estructura exacta del JSON de tu compañera
        algoritmo = reporte.get('algoritmo', 'Ward Jerárquico')
        k_optimo = reporte.get('k_optimo', 3)
        total_frames = reporte.get('total_frames', '15,063')
        variables = reporte.get('variables_usadas', 12)
        silhouette = reporte.get('metricas', {}).get('silhouette', 0.231)
        
        # Creamos los "Hitos" visuales
        hitos = [
            {
                "id": "HITO-01",
                "titulo": "Ingesta y Consolidación de Datos",
                "desc": f"Se procesaron los archivos C3D de la Universidad de Edimburgo. Los datos fueron convertidos de milímetros a metros y consolidados en un DataFrame de {total_frames} frames.",
                "estado": "COMPLETADO",
                "color": "#3B82F6" # Azul
            },
            {
                "id": "HITO-02",
                "titulo": "Limpieza y Tratamiento de Señal",
                "desc": "Se identificaron oclusiones (valores 0.0 simultáneos en X, Y, Z). Se aplicó interpolación lineal para huecos menores a 12 frames y un filtro Savitzky-Golay para suavizar el ruido sin perder la forma del gesto.",
                "estado": "COMPLETADO",
                "color": "#10B981" # Verde
            },
            {
                "id": "HITO-03",
                "titulo": "Ingeniería de Características (Features)",
                "desc": f"Se calcularon {variables} variables biomecánicas derivadas: velocidad, aceleración, energía cinética, ángulos articulares y distancias al torso. Estandarización Z-Score aplicada.",
                "estado": "COMPLETADO",
                "color": "#8B5CF6" # Morado
            },
            {
                "id": "HITO-04",
                "titulo": "Modelado y Selección de Algoritmo",
                "desc": f"Se evaluaron K-Means y {algoritmo} para k=2 hasta k=6. El criterio de Silhouette seleccionó k={k_optimo} como la mejor configuración.",
                "estado": "COMPLETADO",
                "color": "#F59E0B" # Naranja
            },
            {
                "id": "HITO-05",
                "titulo": "Evaluación y Despliegue",
                "desc": f"El modelo final obtuvo un Silhouette Score de {silhouette}. Los resultados fueron exportados a CSV/JSON y desplegados en esta interfaz web interactiva.",
                "estado": "EN PRODUCCIÓN",
                "color": "#EF4444" # Rojo
            }
        ]
        
        # Renderizar los hitos en tarjetas
        for hito in hitos:
            st.markdown(f"""
            <div style="background-color: #111827; border: 1px solid #1F2937; border-radius: 8px; padding: 20px; margin-bottom: 15px; border-left: 5px solid {hito['color']};">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <span style="font-family: monospace; color: #6B7280; font-weight: bold;">[{hito['id']}]</span>
                        <strong style="color: #F9FAFB; font-size: 1.1rem;">{hito['titulo']}</strong>
                    </div>
                    <span style="color: {hito['color']}; font-size: 0.75rem; background: {hito['color']}20; padding: 4px 10px; border-radius: 12px; font-weight: bold; border: 1px solid {hito['color']}50;">
                        {hito['estado']}
                    </span>
                </div>
                <div style="color: #D1D5DB; font-size: 0.95rem; line-height: 1.5;">
                    {hito['desc']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        # Un pequeño panel inferior para ver el JSON crudo
        with st.expander("🔍 Ver Reporte Técnico Completo (JSON)"):
            st.json(reporte)
            
    else:
        st.warning("⚠️ No se encontró el archivo 'reporte_limpieza_metricas.json' en la carpeta demo. Asegúrate de que esté presente para ver la bitácora de auditoría.")

elif seccion_actual == "Metodología & Gobernanza":
    st.markdown("### Marco de Trabajo: CRISP-DM")
    st.write("Este proyecto no es un simple script, es un ciclo de vida completo de ciencia de datos. Se utilizó la metodología estándar **CRISP-DM** (Cross-Industry Standard Process for Data Mining), la cual garantiza que el modelo resuelva un problema real y no solo sea un ejercicio matemático.")
    
    st.markdown("""
    <div class="analysis-block" style="border-left-color: #3B82F6;">
        <h4 style="color: #3B82F6 !important;">Fases de Desarrollo del Proyecto</h4>
        <ul>
            <li><b>1. Comprensión del Negocio:</b> El reto es objetivar el arte. ¿Podemos medir matemáticamente la diferencia entre un gesto fluido y uno de ataque?</li>
            <li><b>2. Comprensión de los Datos:</b> Análisis de 62 archivos C3D de la Universidad de Edimburgo. Los datos presentan oclusiones (marcadores perdidos) y ruido de alta frecuencia.</li>
            <li><b>3. Preparación de Datos:</b> Implementación de un pipeline de limpieza: interpolación lineal (huecos de hasta 12 frames) y suavizado Savitzky-Golay (ventana 0.075s) para no perder la forma de la señal.</li>
            <li><b>4. Modelado:</b> Selección y entrenamiento de K-Means y Ward Jerárquico.</li>
            <li><b>5. Evaluación:</b> Uso de métricas internas (Silhouette, Davies-Bouldin) para validar la cohesión de los clústeres.</li>
            <li><b>6. Despliegue:</b> Construcción de esta interfaz interactiva en Streamlit, optimizada para el análisis visual y la auditoría (MLOps).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.success("✅ Proyecto auditado y validado. Todos los artefactos (datos, scripts y modelos) se encuentran empaquetados y listos para su reproducción.")