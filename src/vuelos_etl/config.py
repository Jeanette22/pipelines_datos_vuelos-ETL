"""Configuración centralizada del pipeline.

Todos los valores se leen de variables de entorno (o de un archivo ``.env``
si ``python-dotenv`` está instalado). No hay credenciales ni IPs en el código.
"""
from __future__ import annotations

import os
from dataclasses import dataclass


def _load_dotenv() -> None:
    """Carga ``.env`` si python-dotenv está disponible (opcional)."""
    try:
        from dotenv import load_dotenv
    except ImportError:  # python-dotenv no es obligatorio en el cluster
        return
    load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Parámetros del pipeline."""

    hdfs_namenode: str
    hdfs_ingest_dir: str
    hive_database: str
    vuelos_table: str
    aeropuertos_table: str
    informe_2021_file: str
    informe_2022_file: str
    aeropuertos_file: str
    fecha_desde: str
    fecha_hasta: str
    csv_delimiter: str

    def hdfs_uri(self, filename: str) -> str:
        """URI completa en HDFS de un archivo dentro del directorio de ingesta."""
        base = self.hdfs_namenode.rstrip("/")
        folder = "/" + self.hdfs_ingest_dir.strip("/")
        return f"{base}{folder}/{filename}"

    @classmethod
    def from_env(cls) -> "Settings":
        """Construye la configuración desde variables de entorno."""
        _load_dotenv()
        env = os.environ.get
        return cls(
            hdfs_namenode=env("HDFS_NAMENODE", "hdfs://localhost:9000"),
            hdfs_ingest_dir=env("HDFS_INGEST_DIR", "/ingest"),
            hive_database=env("HIVE_DATABASE", "vuelos_argentina"),
            vuelos_table=env("HIVE_VUELOS_TABLE", "tabla_aero"),
            aeropuertos_table=env("HIVE_AEROPUERTOS_TABLE", "aero_detall"),
            informe_2021_file=env("INFORME_2021_FILE", "2021-informe-ministerio.csv"),
            informe_2022_file=env("INFORME_2022_FILE", "202206-informe-ministerio.csv"),
            aeropuertos_file=env("AEROPUERTOS_FILE", "aeropuertos_detalle.csv"),
            fecha_desde=env("FECHA_DESDE", "2021-01-01"),
            fecha_hasta=env("FECHA_HASTA", "2022-06-30"),
            csv_delimiter=env("CSV_DELIMITER", ";"),
        )
