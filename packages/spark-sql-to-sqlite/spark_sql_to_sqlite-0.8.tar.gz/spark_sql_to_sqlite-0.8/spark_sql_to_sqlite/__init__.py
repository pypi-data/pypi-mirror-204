# Spark SQL Query To SQLite databse

def spark_sql_to_sqlite(spark, sql_query, path_to_sqlite_db, table_name):
    spark_df = spark.sql(sql_query)
    json_df = spark_nested_to_json(spark_df)
    return spark_to_sqlite(json_df, path_to_sqlite_db, table_name)

def spark_nested_to_json(spark_df):
    # Convert maps, structs and arrays to json
    output_df = spark_df
    from pyspark.sql.functions import to_json, col
    for column in spark_df.dtypes:
        if 'map<' in column[1] or 'struct<' in column[1] or 'array<' in column[1]:
            output_df = output_df.withColumn(column[0], to_json(col(column[0])))
    return output_df

def spark_to_sqlite(spark_df, database, table):
    import sqlite3
    con = sqlite3.connect(database)
    spark_df.toPandas().to_sql(table, con, if_exists='replace')
    con.close()
    return True
