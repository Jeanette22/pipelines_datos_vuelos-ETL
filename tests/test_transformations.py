import datetime

import pytest

from vuelos_etl.transformations import (
    AEROPUERTOS_COLUMNS,
    VUELOS_COLUMNS,
    clean_aeropuertos,
    clean_vuelos,
    normalize_column_name,
)

VUELOS_HEADERS = [
    "Fecha",
    "Hora UTC",
    "Clase de Vuelo (todos los vuelos)",
    "Clasificación Vuelo",
    "Tipo de Movimiento",
    "Aeropuerto",
    "Origen / Destino",
    "Aerolinea Nombre",
    "Aeronave",
    "Pasajeros",
]


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("Hora UTC", "hora_utc"),
        ("Clasificación Vuelo", "clasificacion_vuelo"),
        ("Clase de Vuelo (todos los vuelos)", "clase_de_vuelo_todos_los_vuelos"),
        ("Origen / Destino", "origen_destino"),
    ],
)
def test_normalize_column_name(raw, expected):
    assert normalize_column_name(raw) == expected


def _row(fecha, clasificacion, pasajeros, aeronave="CE-150-L"):
    return (fecha, "10:00", "Regular", clasificacion, "Despegue", "AER", "COR",
            "AEROLINEAS ARGENTINAS SA", aeronave, pasajeros)


def test_clean_vuelos_filters_dates_and_domestic(spark):
    d2021 = spark.createDataFrame(
        [
            _row("15/03/2021", "Cabotaje Doméstico", "120"),
            _row("15/03/2021", "Internacional", "80"),
            _row("20/12/2020", "Doméstico", "50"),  # fuera de rango
        ],
        VUELOS_HEADERS,
    )
    d2022 = spark.createDataFrame(
        [
            _row("01/06/2022", "Domestico", None),  # pasajeros nulos -> 0
            _row("15/07/2022", "Doméstico", "30"),  # fuera de rango (con acento)
        ],
        VUELOS_HEADERS,
    )

    result = clean_vuelos(d2021, d2022, "2021-01-01", "2022-06-30")
    rows = {(r.fecha, r.pasajeros) for r in result.collect()}

    assert result.columns == VUELOS_COLUMNS
    assert rows == {(datetime.date(2021, 3, 15), 120), (datetime.date(2022, 6, 1), 0)}


def test_clean_vuelos_fails_with_clear_message_on_missing_columns(spark):
    bad = spark.createDataFrame([("x",)], ["otra_columna"])
    with pytest.raises(ValueError, match="faltan columnas"):
        clean_vuelos(bad, bad, "2021-01-01", "2022-06-30")


def test_clean_aeropuertos_keeps_only_national_traffic(spark):
    headers = [
        "local", "oaci", "iata", "tipo", "denominacion", "coordenadas", "latitud",
        "longitud", "elev", "uom_elev", "ref", "distancia_ref", "direccion_ref",
        "condicion", "control", "region", "uso", "trafico", "sna", "concesionado",
        "provincia", "fir", "inhab",
    ]

    def row(local, trafico, distancia):
        return (local, "SAXX", "XXX", "Aeródromo", "Nombre", "c", "-1", "-2", "100",
                "M", "Córdoba", distancia, "N", "Publico", "CIV", "CEN", "Publico",
                trafico, "SI", "NO", "Córdoba", "SACF", "NO")

    df = spark.createDataFrame(
        [row("COR", "Nacional", None), row("EZE", "Internacional", "5")], headers
    )

    result = clean_aeropuertos(df)

    assert result.columns == AEROPUERTOS_COLUMNS
    assert "fir" not in result.columns and "inhab" not in result.columns
    only = result.collect()
    assert len(only) == 1
    assert only[0].aeropuerto == "COR"
    assert only[0].distancia_ref == 0.0
