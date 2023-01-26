# Data_pipelines_ejemplos_pasos1
Proceso de ETL: proceso de ingesta, transformación y carga de data al DataWarehouse.

Proceso de ETL: proceso de ingesta, transformación y carga de data al DataWarehouse. 

## Data Pipeles: es un canal de datos donde se usan diferentes tecnologias para procesar y transformar "datos crudos"  desde su origen hacia su destino. Asimismo las fuentes pueden ser tanto internas como externas, en el primer caso  puede ser: b/d transaccional de MongoDB o PostgreSQL, una app de negocios en la nube como Salesforce, Shopify o MailChimp. En el segundo caso es decir "externa", están: Nielsen o Qualtrics. 

##En tanto el destino de este canal de datos será el respositorio dónde una empresa almacena para usarla de forma conjunta: estos pueden ser los almacenes de datos "DATAWAREHOUSE"  y los lagos de datos "Data Lakes". Por última a la hora de realizar la transformación  de la data ésta puede ser a través de Spark, Trifacta, dbt, o si es manual usando Python para hacer los scripts, Airflow, etc. En definitiva, después de todos estos pasos es posible generar Visualizaciones de los resultados o analisis esperados, para esto podemos usar Tableau, Google Data Studio, Power BI, etc.
