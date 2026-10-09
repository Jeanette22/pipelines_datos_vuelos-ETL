#!/usr/bin/env bash
# Ingesta: descarga los CSV desde la fuente pública y los sube a HDFS.
#
# Uso:  bash scripts/ingest.sh
# Config: variables de entorno o archivo .env en la raíz del repo (ver .env.example)
set -euo pipefail

ENV_FILE="${ENV_FILE:-$(dirname "$0")/../.env}"
if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$ENV_FILE"
  set +a
fi

DATA_BASE_URL="${DATA_BASE_URL:-https://data-engineer-edvai.s3.amazonaws.com}"
LANDING_DIR="${LANDING_DIR:-/home/hadoop/landing}"
HDFS_INGEST_DIR="${HDFS_INGEST_DIR:-/ingest}"

FILES=(
  "${INFORME_2021_FILE:-2021-informe-ministerio.csv}"
  "${INFORME_2022_FILE:-202206-informe-ministerio.csv}"
  "${AEROPUERTOS_FILE:-aeropuertos_detalle.csv}"
)

mkdir -p "$LANDING_DIR"
hdfs dfs -mkdir -p "$HDFS_INGEST_DIR"

for file in "${FILES[@]}"; do
  echo "[ingest] Descargando ${file}"
  # -O pisa el archivo si existe (evita los sufijos .csv.1 / .csv.2 de wget -P)
  wget --quiet --tries=3 --timeout=60 \
       -O "${LANDING_DIR}/${file}" "${DATA_BASE_URL%/}/${file}"

  if [[ ! -s "${LANDING_DIR}/${file}" ]]; then
    echo "[ingest] ERROR: ${file} quedó vacío o no se descargó" >&2
    exit 1
  fi

  echo "[ingest] Subiendo ${file} a HDFS:${HDFS_INGEST_DIR}"
  # -f sobreescribe: la ingesta es idempotente
  hdfs dfs -put -f "${LANDING_DIR}/${file}" "${HDFS_INGEST_DIR}/"
done

echo "[ingest] OK"
hdfs dfs -ls "$HDFS_INGEST_DIR"
