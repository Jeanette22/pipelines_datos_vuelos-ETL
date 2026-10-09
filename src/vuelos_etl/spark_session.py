"""Creación de la sesión de Spark con soporte para Hive."""
from __future__ import annotations

import os

from pyspark.sql import SparkSession


def get_spark_session(app_name: str) -> SparkSession:
    """Devuelve (o crea) una SparkSession con Hive habilitado.

    El *master* no se fija en el código: lo define ``spark-submit --master``
    o, si se ejecuta sin spark-submit, la variable de entorno ``SPARK_MASTER``.
    """
    builder = SparkSession.builder.appName(app_name).enableHiveSupport()
    master = os.environ.get("SPARK_MASTER")
    if master:
        builder = builder.master(master)
    return builder.getOrCreate()
