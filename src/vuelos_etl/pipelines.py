"""Orquestación de cada etapa: leer CSV (HDFS) -> transformar -> escribir en Hive."""
from __future__ import annotations

import logging

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.utils import AnalysisException

from vuelos_etl.config import Settings
from vuelos_etl.transformations import clean_aeropuertos, clean_vuelos

logger = logging.getLogger(__name__)


def read_csv(spark: SparkSession, uri: str, delimiter: str) -> DataFrame:
    """Lee un CSV con encabezado desde HDFS."""
    logger.info("Leyendo %s", uri)
    try:
        return (
            spark.read.option("header", "true")
            .option("delimiter", delimiter)
            .csv(uri)
        )
    except AnalysisException as exc:
        raise RuntimeError(
            f"No se pudo leer {uri}. ¿Corrió la ingesta (scripts/ingest.sh)?"
        ) from exc


def write_to_hive(df: DataFrame, database: str, table: str) -> None:
    """Escribe el DataFrame en una tabla Hive existente.

    Usa ``overwrite`` para que re-ejecutar el DAG no duplique filas
    (el ``insert into`` original agregaba los datos de nuevo en cada corrida).
    """
    target = f"{database}.{table}"
    logger.info("Escribiendo en %s", target)
    df.write.mode("overwrite").insertInto(target)


def run_vuelos(spark: SparkSession, settings: Settings) -> int:
    """Transforma los informes 2021-2022 y los carga en Hive. Devuelve filas cargadas."""
    informe_2021 = read_csv(
        spark, settings.hdfs_uri(settings.informe_2021_file), settings.csv_delimiter
    )
    informe_2022 = read_csv(
        spark, settings.hdfs_uri(settings.informe_2022_file), settings.csv_delimiter
    )
    vuelos = clean_vuelos(
        informe_2021, informe_2022, settings.fecha_desde, settings.fecha_hasta
    ).cache()
    write_to_hive(vuelos, settings.hive_database, settings.vuelos_table)
    rows = vuelos.count()
    logger.info("Vuelos cargados: %d", rows)
    return rows


def run_aeropuertos(spark: SparkSession, settings: Settings) -> int:
    """Transforma el detalle de aeropuertos y lo carga en Hive."""
    aeropuertos = read_csv(
        spark, settings.hdfs_uri(settings.aeropuertos_file), settings.csv_delimiter
    )
    detalle = clean_aeropuertos(aeropuertos).cache()
    write_to_hive(detalle, settings.hive_database, settings.aeropuertos_table)
    rows = detalle.count()
    logger.info("Aeropuertos cargados: %d", rows)
    return rows
