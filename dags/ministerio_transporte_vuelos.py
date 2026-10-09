"""DAG de Airflow: ingesta -> transformación (Spark) -> carga en Hive.

Se copia (o enlaza) a la carpeta ``dags/`` de Airflow. Rutas y host se
configuran por variables de entorno del scheduler; no hay IPs en el código.
"""
from __future__ import annotations

import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

REPO_DIR = os.environ.get("ETL_REPO_DIR", "/home/hadoop/pipelines_datos_vuelos-ETL")
SPARK_SUBMIT = os.environ.get("SPARK_SUBMIT_BIN", "/home/hadoop/spark/bin/spark-submit")
HIVE_SITE_XML = os.environ.get("HIVE_SITE_XML", "/home/hadoop/hive/conf/hive-site.xml")
# Si Airflow corre en otro contenedor/host que Spark, ej.: "hadoop@172.17.0.2"
SPARK_SSH_TARGET = os.environ.get("SPARK_SSH_TARGET", "")


def _spark_submit(script: str) -> str:
    """Comando spark-submit, opcionalmente ejecutado por SSH en el nodo de Spark."""
    cmd = f"{SPARK_SUBMIT} --files {HIVE_SITE_XML} {REPO_DIR}/scripts/{script}"
    return f"ssh {SPARK_SSH_TARGET} {cmd}" if SPARK_SSH_TARGET else cmd


default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="Ministerio-de-Transporte-Vuelos",
    description="ETL de vuelos domésticos 2021-2022: HDFS -> Spark -> Hive",
    default_args=default_args,
    schedule="0 0 * * *",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    tags=["ingest", "transform"],
) as dag:

    # El espacio final evita que Airflow trate el comando como un template .sh
    ingest_data = BashOperator(
        task_id="ingest_data",
        bash_command=f"/usr/bin/env bash {REPO_DIR}/scripts/ingest.sh ",
    )

    transform_vuelos = BashOperator(
        task_id="transform_vuelos",
        bash_command=_spark_submit("transform_vuelos.py"),
    )

    transform_aeropuertos = BashOperator(
        task_id="transform_aeropuertos",
        bash_command=_spark_submit("transform_aeropuertos.py"),
    )

    fin_proceso = EmptyOperator(task_id="fin_proceso")

    # Secuencial como en el original: con el metastore Derby embebido de Hive
    # dos spark-submit en paralelo se bloquean entre sí.
    ingest_data >> transform_vuelos >> transform_aeropuertos >> fin_proceso
