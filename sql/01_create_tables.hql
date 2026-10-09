-- Ejecutar con:  hive -f sql/01_create_tables.hql
-- Buenas prácticas aplicadas: nombres en minúscula, sin tildes y con guión bajo.

CREATE SCHEMA IF NOT EXISTS vuelos_argentina;
USE vuelos_argentina;

-- Vuelos domésticos 2021-2022 (salida del job transform_vuelos.py)
CREATE EXTERNAL TABLE IF NOT EXISTS tabla_aero (
  fecha                  DATE,
  hora_utc               STRING,
  clase_de_vuelo         STRING,
  clasificacion_de_vuelo STRING,
  tipo_de_movimiento     STRING,
  aeropuerto             STRING,
  origen_destino         STRING,
  aerolinea_nombre       STRING,
  aeronave               STRING,
  pasajeros              INT
)
COMMENT 'informes'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/table/informes21_22';

-- Detalle de aeropuertos de tráfico nacional (salida de transform_aeropuertos.py)
CREATE EXTERNAL TABLE IF NOT EXISTS aero_detall (
  aeropuerto    STRING,
  oac           STRING,
  iata          STRING,
  tipo          STRING,
  denominacion  STRING,
  coordenadas   STRING,
  latitud       STRING,
  longitud      STRING,
  elev          FLOAT,
  uom_elev      STRING,
  ref           STRING,
  distancia_ref FLOAT,
  direccion_ref STRING,
  condicion     STRING,
  control       STRING,
  region        STRING,
  uso           STRING,
  trafico       STRING,
  sna           STRING,
  concesionado  STRING,
  provincia     STRING
)
COMMENT 'aeropuertos'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/table/aeropuertos';
