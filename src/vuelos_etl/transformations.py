"""Transformaciones puras (DataFrame in -> DataFrame out).

No leen ni escriben nada: eso permite testearlas con datos de ejemplo.
"""
from __future__ import annotations

import re
import unicodedata
from typing import Dict, Iterable, List

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

# Orden de columnas = orden de las tablas Hive (ver sql/01_create_tables.hql).
VUELOS_COLUMNS: List[str] = [
    "fecha",
    "hora_utc",
    "clase_de_vuelo",
    "clasificacion_de_vuelo",
    "tipo_de_movimiento",
    "aeropuerto",
    "origen_destino",
    "aerolinea_nombre",
    "aeronave",
    "pasajeros",
]

# Encabezados del CSV (ya normalizados) -> nombre final de la columna.
# Los que no están acá se conservan tal cual quedan tras normalizar.
VUELOS_ALIASES: Dict[str, str] = {
    "clase_de_vuelo_todos_los_vuelos": "clase_de_vuelo",
    "clasificacion_vuelo": "clasificacion_de_vuelo",
}

AEROPUERTOS_COLUMNS: List[str] = [
    "aeropuerto",
    "oac",
    "iata",
    "tipo",
    "denominacion",
    "coordenadas",
    "latitud",
    "longitud",
    "elev",
    "uom_elev",
    "ref",
    "distancia_ref",
    "direccion_ref",
    "condicion",
    "control",
    "region",
    "uso",
    "trafico",
    "sna",
    "concesionado",
    "provincia",
]

AEROPUERTOS_ALIASES: Dict[str, str] = {
    "local": "aeropuerto",
    "oaci": "oac",
}


def normalize_column_name(name: str) -> str:
    """'Hora UTC' -> 'hora_utc'; 'Clasificación Vuelo' -> 'clasificacion_vuelo'."""
    ascii_name = (
        unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    )
    return re.sub(r"[^a-z0-9]+", "_", ascii_name.lower()).strip("_")


def normalize_columns(df: DataFrame, aliases: Dict[str, str]) -> DataFrame:
    """Normaliza los nombres de columnas y aplica los alias del dataset."""
    new_names = []
    for col in df.columns:
        norm = normalize_column_name(col)
        new_names.append(aliases.get(norm, norm))
    return df.toDF(*new_names)


def require_columns(df: DataFrame, required: Iterable[str], dataset: str) -> None:
    """Falla temprano y con un mensaje claro si falta alguna columna esperada."""
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            f"Al dataset '{dataset}' le faltan columnas: {missing}. "
            f"Columnas encontradas: {df.columns}. "
            "Revisá los alias en transformations.py."
        )


def clean_vuelos(
    informe_2021: DataFrame,
    informe_2022: DataFrame,
    fecha_desde: str,
    fecha_hasta: str,
) -> DataFrame:
    """Une los informes, filtra vuelos domésticos por rango de fechas y tipa columnas.

    Equivale al notebook original (UNION + withColumnRenamed + SQL), con dos
    correcciones: el rango de fechas se compara como fecha (no como texto) y
    el filtro "Domestico OR Doméstico" ya no anula el filtro de fechas.
    """
    df_2021 = normalize_columns(informe_2021, VUELOS_ALIASES)
    df_2022 = normalize_columns(informe_2022, VUELOS_ALIASES)
    require_columns(df_2021, VUELOS_COLUMNS, "informe 2021")
    require_columns(df_2022, VUELOS_COLUMNS, "informe 2022")

    union = df_2021.select(*VUELOS_COLUMNS).unionByName(
        df_2022.select(*VUELOS_COLUMNS)
    )

    es_domestico = F.col("clasificacion_de_vuelo").rlike(r"(?i)dom[eé]stico")
    desde = F.to_date(F.lit(fecha_desde))
    hasta = F.to_date(F.lit(fecha_hasta))

    return (
        union.distinct()  # UNION de SQL elimina duplicados
        .withColumn("fecha", F.to_date(F.col("fecha"), "dd/MM/yyyy"))
        .filter(F.col("fecha").between(desde, hasta))
        .filter(es_domestico)
        .withColumn(
            "pasajeros",
            F.coalesce(F.col("pasajeros").cast("int"), F.lit(0)),
        )
        .select(*VUELOS_COLUMNS)
    )


def clean_aeropuertos(aeropuertos: DataFrame) -> DataFrame:
    """Normaliza el detalle de aeropuertos y conserva solo tráfico nacional.

    - 'local' -> 'aeropuerto', 'oaci' -> 'oac'
    - se descartan 'fir' e 'inhab'
    - 'elev' y 'distancia_ref' pasan a float (nulos de distancia -> 0)
    """
    df = normalize_columns(aeropuertos, AEROPUERTOS_ALIASES)
    require_columns(df, AEROPUERTOS_COLUMNS, "aeropuertos_detalle")

    return (
        df.drop("fir", "inhab")
        .withColumn("elev", F.col("elev").cast("float"))
        .withColumn(
            "distancia_ref",
            F.coalesce(F.col("distancia_ref").cast("float"), F.lit(0.0)),
        )
        .filter(F.lower(F.trim(F.col("trafico"))) == "nacional")
        .select(*AEROPUERTOS_COLUMNS)
    )
