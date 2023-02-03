#                                                 Creando Data Pipeline:
Proceso de ETL: proceso de ingesta, transformación y carga de data al DataWarehouse.

#### Data Pipeles: es un canal de datos donde se usan diferentes tecnologias para procesar y transformar "datos crudos"  desde su origen hacia su destino. Asimismo las fuentes pueden ser tanto internas como externas, en el primer caso  puede ser: b/d transaccional de MongoDB o PostgreSQL, una app de negocios en la nube como Salesforce, Shopify o MailChimp. En el segundo caso es decir "externa", están: Nielsen o Qualtrics. 

En tanto el destino de este canal de datos será el respositorio dónde una empresa almacena para usarla de forma conjunta: estos pueden ser los almacenes de datos "DATAWAREHOUSE"  y los lagos de datos "Data Lakes". Por última a la hora de realizar la transformación  de la data ésta puede ser a través de Spark, Trifacta, dbt, o si es manual usando Python para hacer los scripts, Airflow, etc. En definitiva, después de todos estos pasos es posible generar Visualizaciones de los resultados o analisis esperados, para esto podemos usar Tableau, Google Data Studio, Power BI, etc.


## Jeanette Mansilla
___________________________________________________________________________________________________________________________________________________________________
Tecnologias utilizadas: 
- Spark
- Hive
- Dbeaver
- SQL






<p align="center" width="100%">
    <img width="33%" src= "https://user-images.githubusercontent.com/80054717/214897543-1e3e4d26-128d-4f2d-9d6e-c0f54c2e1120.png">

### ETL (Extract, Transform and Load)
Durante el desarrollo de todo el proyecto se aplica el proceso ETC (extración, transformación y carga) de data al DataWarehouse. En este caso se utilizaron archivos CSV's, con dataset ubicados en datos abiertos del Ministerio de Transporte. 
En el proceso de transformación se normalizó y limpio los dataset: eliminando columnas que no iba a utilizar, eliminando datos nulos, cambio de nombre de las columnas, el tipo de dato, y también se unieron ambos datasets para que sea solo una tabla a consultar.
Para cargar la data se usó SQL, HIVE y AIRFLOW. Este último automatiza el proceso mediante la creación de un Dag, con scripts. 

#### Ingesta de datos: Durante esta etapa se obtiene datos desde diferentes fuentes que luego al ser transformada será información para la organización determinada. De manera que todo esto se agrega al proyecto en el que estás trabajando. Como se mencionó al principio estos datos pueden ser de otras B/D, archivos almacenados o apps. Asimismo puede provenir de manera interna cuando es desde la misma empresa, o externa.

En el siguiente caso de ejemplo obtenemos los datos que están almacenados en un Cloud Provider: Amazon S3. Allí están cargados los CSV. Asimismo otras opciones que podrían presentarse es cuando están almacenados en Cloud Storage de Google Cloud o Blog Storage de Azure.  
Este proceso se lleva adelante desde una consola y después se almacena en un sistema de archivos HDFS- Hadoop (*REPOSITORIO DE DATA), tambien pude ser en un repositorio de algún Cloud Provider, Cloud Storage, Blog Storage. 
    

Para realizar esto utilicé Hadoop almacenado en un Docker, desde allí coloqué los comandos wget -P + especificamos ruta donde queremos dejarlo + la url donde está alojado el dataset. Como puede verse en la siguiente imagen:

![1](https://user-images.githubusercontent.com/80054717/215776416-0def5478-b762-4feb-b831-4633bd504021.png)

__________________________________________________________________________________________________________________________________________________________________

### HDFS (Hadoop Distributed File System) es el principal componente del ecosistema Hadoop. 
Se utiliza para almacenar datasets grandes con tipos de datos estructurados, semi-estructurados y no estructurados como imágenes, vídeo, datos de sensores, etc. Está optimizado para almacenar enormes cantidades de datos y mantener varias copias para garantizar una alta disponibilidad y la tolerancia a fallos. 
En definitiva es una tecnología fundamental para Big Data, o dicho de otra forma:
Entonces:
-  HDFS divide los ficheros de datos en bloques, generalmente de 128MB de tamaño, estos bloques son replicados y distribuidos en los nodos que componen el clúster.

![4 hdfs](https://user-images.githubusercontent.com/80054717/215846349-7f784e20-95d6-4def-8f2b-35bb34b6f566.png)
![5 hdfs ingest](https://user-images.githubusercontent.com/80054717/215846383-832c2be7-c489-4f43-8638-9607346dae2a.png)
![6 hdfs ingest](https://user-images.githubusercontent.com/80054717/215846445-eaf927c5-5fa9-4c79-8a64-6ebd7527ab88.png)




__________________________________________________________________________________________________________________________________________________________________

### Transformación de los DataSets
En esta etapa realice las transformaciones de los dataset para posteriormente hacer las consultas con los filtros ya realizados:
- Lectura de los datasets
- union de los datasets
- creacion de vistas
- Utilice withColumn para cambiar nombres de algunas columnas
- Despues con lenguaje SQL, realicé el filtro de los datos, cambie el tipo de dato, y cambié nulos por '0'
- Inserción de la data a las tablas creadas en HIVE

Durante las transformaciones se filtraron los datos por vuelos domésticos, se eliminaron la columna inhab y fir. 
De esta manera se ingestaron los datos


![8 spark - transformacion aeropuertos](https://user-images.githubusercontent.com/80054717/215560411-e9e80055-a6f9-4bc5-902a-59f55f8300ee.png)

![7 spark - transformacion vuelos](https://user-images.githubusercontent.com/80054717/215560418-5e67dedd-b746-430e-a0fd-2951a06baaa4.png)





__________________________________________________________________________________________________________________________________________________________________
#### Automatización: AIRFLOW
En esta etapa se utilizo los script para automatizar todo el proceso de transformacion del dataset, a traves de un DAG, como puede verse en la imagen:

![dag](https://user-images.githubusercontent.com/80054717/215563619-99660f22-bca6-4867-91be-702a7399356d.png)


__________________________________________________________________________________________________________________________________________________________________
### Resultados: En esta imagen podemos notar la automatización realizada, siguiendo el proceso por si surge algún problema podemos chequearlo en "Log":
![airflow](https://user-images.githubusercontent.com/80054717/215583634-197efa87-ba95-4706-b1aa-48f72419467a.png)






____________________________________________________________________________________________________________________________________________________________________
### Tablas creadas y cargadas en HIVE: 
Modelización de una base de datos
Antes de comenzar a filtrar y/o seleccionar data para cargar y crear bases de datos es necesario tener en cuenta las buenas prácticas para modelizar las tablas.
Es decir saber de antemano el nombre de las tablas, su estructura (tipo de dato) y las relaciones que van a tener. Entonces para eso lo más usado es el "Diagrama de Entidad - Relación" o "DER". Por ende su caracteristica destacada es que puede representar las tablas de manera gráfica y sus relaciones vinculadas. 

Buenas prácticas:
- nombres en minuscula 
- evitar tildes en los nombres de tablas/columnas
- reemplazar espacios por guión bajo: el símbolo “_”

Entonces, en esta etapa me pareció importante crear una base de datos exclusiva, donde solo irían los dataset relacionadas a los vuelos del Ministerio de Transporte
utilicé los comandos: 
- CREATE SCHEMA vuelos_argentina;
- USE vuelos_argentina;
Luego genere las tablas que se ven en la imagen, especificando nombre de las columnas, tipos de datos, y estructura:
![creado tablas HIVE](https://user-images.githubusercontent.com/80054717/216650855-029f5d2a-b93c-43b5-be0b-3f5dcaf976fb.png)
______________________________________________________________________________________________________________________________
![tablas cargadas HIVE](https://user-images.githubusercontent.com/80054717/215584196-2b66ee93-ee39-43e3-8da5-9e880e389292.png)





____________________________________________________________________________________________________________________________________________________________________
### Consultas SQL en Dbeaver: 
Durante esta etapa realicé consultas usando "Dbeaver" sobre los dataset para crear los informes según lo solicitado: 
- Cantidad de vuelos entre las fechas 01/12/2021 y 31/01/2022. Mostrar consulta y Resultado de la query
- Cantidad de pasajeros que viajaron en Aerolíneas Argentinas entre el 01/01/2021 y 30/06/2022. Mostrar consulta y Resultado de la query
- Mostrar fecha, hora, código aeropuerto salida, ciudad de salida, código de aeropuerto de arribo, ciudad de arribo, y cantidad de pasajeros de cada vuelo, entre el 01/01/2022 y el 30/06/2022 ordenados por fecha de manera descendiente. Mostrar consulta y Resultado de la query
- Cuales son las 10 aerolíneas que más pasajeros llevaron entre el 01/01/2021 y el 30/06/2022 exceptuando aquellas aerolíneas que no tengan nombre. Mostrar consulta y Visualización
- Cuales son las 10 aeronaves más utilizadas entre el 01/01/2021 y el 30/06/22 que despegaron desde la Ciudad autónoma de Buenos Aires o de Buenos Aires, exceptuando aquellas aeronaves que no cuentan con nombre. Mostrar consulta y Visualización
- Conclusiones - recomendaciones










____________________________________________________________________________________________________________________________________________________________________
### Graficos - Tableau: Visualización de Data
![Dashboar tableau](https://user-images.githubusercontent.com/80054717/215585244-3ef77c00-8079-45c5-8b02-e72288b3a28e.png)



