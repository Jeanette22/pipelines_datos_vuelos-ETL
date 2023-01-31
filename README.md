#                                                 *Data pipelines: ejemplo numero uno y pasos:*
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



#### Ingesta de datos: Durante esta etapa se obtiene datos desde diferentes fuentes que luego al ser transformada será información para la organización determinada. De manera que todo esto se agrega al proyecto en el que estás trabajando. Como se mencionó al principio estos datos pueden ser de otras B/D, archivos almacenados o apps. Asimismo puede provenir de manera interna cuando es desde la misma empresa, o externa.

En el siguiente caso de ejemplo obtenemos los datos que están almacenados en un Cloud Provider: Amazon S3. Allí están cargados los CSV. Asimismo otras opciones que podrían presentarse es cuando están almacenados en Cloud Storage de Google Cloud o Blog Storage de Azure.  
Este proceso se lleva adelante desde una consola y después se almacena en un sistema de archivos HDFS- Hadoop (*REPOSITORIO DE DATA), tambien pude ser en un repositorio de algún Cloud Provider, Cloud Storage, Blog Storage. 

    
### ETL 
Durante el desarrollo de todo el proyecto se aplica el proceso ETC (extración, transformación y carga) de data al DataWarehouse. En este caso se utilizaron archivos CSV's, con dataset ubicados en datos abiertos del Ministerio de Transporte. 
En el proceso de transformación se normalizó y limpio los dataset: eliminando columnas que no iba a utilizar, eliminando datos nulos, cambio de nombre de las columnas, el tipo de dato, y también se unieron ambos datasets para que sea solo una tabla a consultar.
Para cargar la data se usó SQL, HIVE y AIRFLOW. Este último automatiza el proceso mediante la creación de un Dag, con scripts. 
    

Para realizar esto utilicé Hadoop almacenado en un Docker, desde allí coloqué los comandos wget -P + especificamos ruta donde queremos dejarlo + la url donde está alojado el dataset. Como puede verse en la siguiente imagen:

![1](https://user-images.githubusercontent.com/80054717/215776416-0def5478-b762-4feb-b831-4633bd504021.png)

__________________________________________________________________________________________________________________________________________________________________

### HDFS (Hadoop Distributed File System) es el principal componente del ecosistema Hadoop. 
Se utiliza para almacenar datasets grandes con tipos de datos estructurados, semi-estructurados y no estructurados como imágenes, vídeo, datos de sensores, etc. Está optimizado para almacenar enormes cantidades de datos y mantener varias copias para garantizar una alta disponibilidad y la tolerancia a fallos. 
En definitiva es una tecnología fundamental para Big Data, o dicho de otra forma:
Entonces:
-  HDFS divide los ficheros de datos en bloques, generalmente de 128MB de tamaño, estos bloques son replicados y distribuidos en los nodos que componen el clúster.

<p align="center" width="100%">
    <img width="33%" src= "https://user-images.githubusercontent.com/80054717/215556835-54f04b9d-362a-48e4-9c1f-41988bbf502b.png">
<p align="center" width="100%">
    <img width="33%" src= "https://user-images.githubusercontent.com/80054717/215556846-ac123572-64b9-49f0-b033-2e2a4898a19d.png">
<p align="center" width="100%">
    <img width="33%" src= "https://user-images.githubusercontent.com/80054717/215556850-396eb98c-b6cd-4a37-871e-496f6687cc9c.png">



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
### Tablas cargadas en HIVE:
![tablas cargadas HIVE](https://user-images.githubusercontent.com/80054717/215584196-2b66ee93-ee39-43e3-8da5-9e880e389292.png)





____________________________________________________________________________________________________________________________________________________________________
### Consultas SQL en Dbeaver: 
Durante esta etapa realicé consultas sobre los dataset para crear los informes según lo solicitado: 
<p align="center" width="100%">
    <img width="33%" src= "https://user-images.githubusercontent.com/80054717/215584666-e54a208d-ed0c-4498-8d3a-beca609d1545.png">
<p align="center" width="100%">
    <img width="33%" src= "https://user-images.githubusercontent.com/80054717/215584882-29fe8cfd-3ebc-4cc9-b50d-3782d42ef477.png">









____________________________________________________________________________________________________________________________________________________________________
### Graficos - Tableau: Visualización de Data
![Dashboar tableau](https://user-images.githubusercontent.com/80054717/215585244-3ef77c00-8079-45c5-8b02-e72288b3a28e.png)



