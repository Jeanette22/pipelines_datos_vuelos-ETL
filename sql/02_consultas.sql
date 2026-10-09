-- Consultas de análisis (DBeaver / Hive). Base: vuelos_argentina
-- Nota: las consultas 1, 2, 4 y 5 fueron reconstruidas a partir del enunciado;
-- la consulta 3 es la original. Verificá los valores de texto (p. ej. provincia
-- y tipo_de_movimiento) contra tus datos antes de publicar resultados.

-- 1) Cantidad de vuelos entre el 01/12/2021 y el 31/01/2022
SELECT COUNT(*) AS cantidad_vuelos
FROM vuelos_argentina.tabla_aero
WHERE fecha BETWEEN '2021-12-01' AND '2022-01-31';

-- 2) Pasajeros de Aerolíneas Argentinas entre el 01/01/2021 y el 30/06/2022
SELECT aerolinea_nombre, SUM(pasajeros) AS total_pasajeros
FROM vuelos_argentina.tabla_aero
WHERE fecha BETWEEN '2021-01-01' AND '2022-06-30'
  AND aerolinea_nombre = 'AEROLINEAS ARGENTINAS SA'
GROUP BY aerolinea_nombre;

-- 3) Detalle de vuelos con ciudad de salida y arribo (01/01/2022 - 30/06/2022)
SELECT
    a.fecha           AS fecha_partida,
    a.hora_utc        AS hora_partida,
    a.aeropuerto      AS cod_aeropuerto_salida,
    b.ref             AS ciudad_salida,
    a.origen_destino  AS cod_aeropuerto_arribo,
    c.ref             AS ciudad_arribo,
    a.pasajeros       AS pasajeros
FROM vuelos_argentina.tabla_aero a
INNER JOIN vuelos_argentina.aero_detall b ON a.aeropuerto     = b.aeropuerto
INNER JOIN vuelos_argentina.aero_detall c ON a.origen_destino = c.aeropuerto
WHERE a.fecha BETWEEN '2022-01-01' AND '2022-06-30'
ORDER BY a.fecha DESC;

-- 4) Top 10 aerolíneas por pasajeros (01/01/2021 - 30/06/2022), sin nombres vacíos
SELECT aerolinea_nombre, SUM(pasajeros) AS total_pasajeros
FROM vuelos_argentina.tabla_aero
WHERE fecha BETWEEN '2021-01-01' AND '2022-06-30'
  AND aerolinea_nombre IS NOT NULL
  AND TRIM(aerolinea_nombre) NOT IN ('', '0')
GROUP BY aerolinea_nombre
ORDER BY total_pasajeros DESC
LIMIT 10;

-- 5) Top 10 aeronaves con despegues desde Buenos Aires / CABA (01/01/2021 - 30/06/2022)
SELECT a.aeronave, COUNT(*) AS cantidad_vuelos
FROM vuelos_argentina.tabla_aero a
INNER JOIN vuelos_argentina.aero_detall b ON a.aeropuerto = b.aeropuerto
WHERE a.fecha BETWEEN '2021-01-01' AND '2022-06-30'
  AND LOWER(a.tipo_de_movimiento) LIKE 'despegue%'
  AND UPPER(b.provincia) IN ('BUENOS AIRES', 'CIUDAD AUTÓNOMA DE BUENOS AIRES')
  AND a.aeronave IS NOT NULL
  AND TRIM(a.aeronave) NOT IN ('', '0')
GROUP BY a.aeronave
ORDER BY cantidad_vuelos DESC
LIMIT 10;
