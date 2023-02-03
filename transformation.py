from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
sc = SparkContext('local')
spark = SparkSession(sc)
import os, sys
from pyspark.sql import HiveContext
hc = HiveContext(sc)



##leo el csv desde HDFS y lo cargo en un dataframe
informe_2021=spark.read.option("header","true").option("delimiter",";").csv("hdfs://172.17.0.2:9000/ingest/2021-informe-ministerio.csv")
informe_2022=spark.read.option("header","true").option("delimiter",";").csv("hdfs://172.17.0.2:9000/ingest/202206-informe-ministerio.csv")


##opcional: si queres ver la data que esta en el DF###
##df.show(5)

##creamos una vista del DF
informe_2021.createOrReplaceTempView("info2021")
informe_2022.createOrReplaceTempView("info2022")


##Filtramos el DF
df_union = spark.sql("select * from info2021 UNION select * from info2022")
df_union.createOrReplaceTempView("dfunion")
df_vuelos=df_union.withColumnRenamed('Fecha','fecha').withColumnRenamed('Hora UTC','horaUTC').withColumnRenamed('Clase de Vuelo (todos los vuelos)','clase_de_vuelos').>

#casteo  y filtros campos
df_vuelos.createOrReplaceTempView("dfinformes")
vuelos21_22= spark.sql("select to_date(Fecha,'dd/MM/yyyy')as fecha,horaUTC, clase_de_vuelos,clasificacion_de_vuelo, tipo_de_movimiento,aeropuerto,origen_destino,aeroli>
#new_df.show(5)


##Creamos una vista con la data filtrada###
vuelos21_22.createOrReplaceTempView("dfvuelos2122")


##insertamos el DF filtrado en la tabla
hc.sql("insert into vuelos_argentina.tabla_aero select * from dfvuelos2122;")
