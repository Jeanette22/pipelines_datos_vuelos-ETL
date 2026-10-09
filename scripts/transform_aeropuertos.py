"""Etapa de transformación: detalle de aeropuertos -> tabla Hive.

Uso:
    spark-submit --files $HIVE_CONF_DIR/hive-site.xml scripts/transform_aeropuertos.py
"""
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from vuelos_etl.config import Settings  # noqa: E402
from vuelos_etl.pipelines import run_aeropuertos  # noqa: E402
from vuelos_etl.spark_session import get_spark_session  # noqa: E402

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger("transform_aeropuertos")


def main() -> int:
    spark = get_spark_session("transform_aeropuertos")
    try:
        run_aeropuertos(spark, Settings.from_env())
        return 0
    except Exception:
        logger.exception("Falló la transformación de aeropuertos")
        return 1
    finally:
        spark.stop()


if __name__ == "__main__":
    sys.exit(main())
