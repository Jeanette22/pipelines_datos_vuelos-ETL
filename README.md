#                                                 *Data pipelines: ejemplo numero uno y pasos:*
Proceso de ETL: proceso de ingesta, transformación y carga de data al DataWarehouse.

#### Data Pipeles: es un canal de datos donde se usan diferentes tecnologias para procesar y transformar "datos crudos"  desde su origen hacia su destino. Asimismo las fuentes pueden ser tanto internas como externas, en el primer caso  puede ser: b/d transaccional de MongoDB o PostgreSQL, una app de negocios en la nube como Salesforce, Shopify o MailChimp. En el segundo caso es decir "externa", están: Nielsen o Qualtrics. 

En tanto el destino de este canal de datos será el respositorio dónde una empresa almacena para usarla de forma conjunta: estos pueden ser los almacenes de datos "DATAWAREHOUSE"  y los lagos de datos "Data Lakes". Por última a la hora de realizar la transformación  de la data ésta puede ser a través de Spark, Trifacta, dbt, o si es manual usando Python para hacer los scripts, Airflow, etc. En definitiva, después de todos estos pasos es posible generar Visualizaciones de los resultados o analisis esperados, para esto podemos usar Tableau, Google Data Studio, Power BI, etc.


### Jeanette Mansilla
_______________________________________________________________________________________________________________________________________________________________________






![team](https://user-images.githubusercontent.com/80054717/214897543-1e3e4d26-128d-4f2d-9d6e-c0f54c2e1120.png)



#### Ingesta de datos: Durante esta etapa se obtiene datos desde diferentes fuentes que luego al ser transformada será información para la organización determinada. De manera que todo esto se agrega al proyecto en el que estás trabajando. Como se mencionó al principio estos datos pueden ser de otras B/D, archivos almacenados o apps. Asimismo puede provenir de manera interna cuando es desde la misma empresa, o externa.

En el siguiente caso de ejemplo obtenemos los datos que están almacenados en un Cloud Provider: Amazon S3. Allí están cargados los CSV. Asimismo otras opciones que podrían presentarse es cuando están almacenados en Cloud Storage de Google Cloud o Blog Storage de Azure.  
Este proceso se lleva adelante desde una consola y después se almacena en un sistema de archivos HDFS- Hadoop (*REPOSITORIO DE DATA), tambien pude ser en un repositorio de algún Cloud Provider, Cloud Storage, Blog Storage. 


Para realizar esto utilicé Hadoop almacenado en un Docker, desde allí coloqué los comandos wget -P + especificamos ruta donde queremos dejarlo + la url donde está alojado el dataset. Como puede verse en la siguiente imagen:
![1](https://user-images.githubusercontent.com/80054717/214900093-df2bc34a-df37-4a14-9f99-79cdc40ca6fd.png)

__________________________________________________________________________________________________________________________________________________________________

HDFS (Hadoop Distributed File System) es el principal componente del ecosistema Hadoop. 
Se utiliza para almacenar datasets grandes con tipos de datos estructurados, semi-estructurados y no estructurados como imágenes, vídeo, datos de sensores, etc. Está optimizado para almacenar enormes cantidades de datos y mantener varias copias para garantizar una alta disponibilidad y la tolerancia a fallos. 
En definitiva es una tecnología fundamental para Big Data, o dicho de otra forma:
Entonces:
-  HDFS divide los ficheros de datos en bloques, generalmente de 128MB de tamaño, estos bloques son replicados y distribuidos en los nodos que componen el clúster.


![5 hdfs ingest](https://user-images.githubusercontent.com/80054717/215556835-54f04b9d-362a-48e4-9c1f-41988bbf502b.png)
![4 hdfs](https://user-images.githubusercontent.com/80054717/215556846-ac123572-64b9-49f0-b033-2e2a4898a19d.png)
![6 hdfs ingest](https://user-images.githubusercontent.com/80054717/215556850-396eb98c-b6cd-4a37-871e-496f6687cc9c.png)
