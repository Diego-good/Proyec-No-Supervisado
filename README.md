# Features + clustering para mocap de dirección orquestal

## Qué incluye

- `features_clustering.py`: pipeline reproducible de limpieza, extracción de variables biomecánicas, normalización, clustering y evaluación.
- `demo/features_clustering.csv`: features calculadas y etiqueta de cluster para la muestra disponible.
- `demo/metricas_clustering.csv`: Silhouette y Davies-Bouldin para KMeans y clustering jerárquico Ward, k=2..6.
- `demo/reporte_limpieza_metricas.json`: resumen de limpieza, variables usadas y configuración ganadora.
- `demo/figuras/`: comparativa de métricas, PCA coloreado por cluster, secuencia temporal y perfiles medios.

## Datos inspeccionados

El paquete original contiene 62 grabaciones, 120 Hz, 976.408 frames y 63 columnas en el Parquet consolidado. El CSV adjunto es solo una muestra de la primera grabación: 15.063 frames. **La demo incluida se ejecutó sobre esos 15.063 frames, no sobre las 62 grabaciones.** El script permite ejecutar el Parquet completo localmente.

## Tratamiento aplicado

1. Orden temporal por `recording_id` y `frame`.
2. Ceros simultáneos XYZ de un marcador interpretados como oclusión y convertidos a `NaN`.
3. Interpolación lineal de huecos de hasta 12 frames, más relleno de bordes. Las columnas completamente ausentes en una grabación no se inventan.
4. Suavizado Savitzky-Golay (ventana aproximada de 0,075 s; polinomio de orden 2).
5. Derivadas temporales a 120 Hz para velocidad y aceleración; energía cinética relativa `0.5 * v²` con masa unitaria.
6. Ángulos de codo con geometría hombro-codo-muñeca; orientación XY y longitud de batuta cuando existen los marcadores.
7. Estandarización z-score antes del clustering.

La energía reportada es una **proxy relativa**, no energía física absoluta: no hay masas segmentarias calibradas. La interpolación se limita a huecos cortos para no fabricar movimiento en oclusiones largas.

## Resultado de la demo

El criterio automático prioriza mayor Silhouette y usa Davies-Bouldin como desempate. En esta muestra ganó **Ward jerárquico aproximado, k=2**:

- Silhouette: **0,229**
- Davies-Bouldin: **2,154**
- Evaluación de métricas: muestra de 3.000 observaciones.
- Distribución: cluster 0 = 12.350 frames; cluster 1 = 2.713 frames.

La separación es modesta, no una segmentación concluyente. Los clusters deben interpretarse como estados cinemáticos candidatos y validarse con visualización de secuencias, conocimiento de dirección musical y, de ser posible, etiquetas externas.

Ward tiene coste cuadrático: se ajusta a un subconjunto de hasta 3.500 observaciones y el resto se asigna al centroide más cercano. KMeans sí se ajusta sobre todas las filas. Silhouette y Davies-Bouldin se calculan sobre un subconjunto reproducible de hasta 3.000 filas.

## Instalación

```bash
pip install -r requirements.txt
```

Para leer el Parquet se requiere `pyarrow`. Si solo se usa el CSV de muestra, pandas puede leerlo directamente.

## Ejecutar la demo CSV

```bash
python features_clustering.py --input ../Persona_1/muestra_datos.csv --format csv --outdir demo_nueva
```

El CSV original usa `;` como separador y `,` como decimal; el script lo detecta.

## Ejecutar las 62 grabaciones (Parquet)

```bash
python features_clustering.py --input ../Persona_1/datos_crudos.parquet --format parquet --fps 120 --outdir salida_completa
```

La ejecución completa requiere memoria suficiente para aproximadamente 976 mil filas y 38 variables. Para un análisis definitivo se recomienda procesar y guardar por grabación o reducir la frecuencia temporal de clustering (por ejemplo, 30 Hz), especialmente para el ajuste de KMeans.

## Variables principales

- Velocidad, aceleración y energía cinética relativa de muñeca izquierda/derecha, codos y extremo de batuta.
- Posiciones XYZ de dichos marcadores.
- Distancia de cada muñeca al centro de torso.
- Ángulo de ambos codos, ángulo XY y longitud de batuta.
- Velocidad media y asimetría de velocidad entre manos.

Los marcadores ausentes (por ejemplo, batuta en algunos directores) quedan fuera de las variables útiles cuando no contienen datos suficientes; el pipeline no presupone que todos los sujetos tengan idéntico equipamiento.
