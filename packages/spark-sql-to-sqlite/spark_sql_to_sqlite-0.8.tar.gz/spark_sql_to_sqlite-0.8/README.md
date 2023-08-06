# spark_sql_to_sqlite

Easily save a Spark dataframe into a SQLite database.

#### Why do you need it

Although you can use jdbc with Spark to write to SQLite, this method is error prone, and doesn't handle complex data types such as Map, Struct and Array.

`spark_sql_to_sqlite` automatically converts these complex data types to json, which can be used in SQLite queries using standard [json functions](https://www.sqlite.org/json1.html) such as json_extract.

It also has sensible defaults to create or replace the SQLite database and table(s) as needed.

#### How To Use

You can use this on Spark environments such as Databricks, where you have a `spark` variable available that represents the SparkContext.

Install it as follows:

```
%pip install spark-sql-to-sqlite
```

Then import it as follows:

```
from spark_sql_to_sqlite import spark_sql_to_sqlite
```

You can now use it as follows:

```
spark_sql_to_sqlite("SELECT * from {catalog}.{schema}.{table}", path_to_sqlite_db, table_name)
```

Example:
```
spark_sql_to_sqlite(spark, "SELECT * FROM hive_metastore.fire.bronze", "/tmp/fire.db", "bronze")
```

The above command will create a SQLite database at `/tmp/fire.db` if it doesn't already exists. It will create or replace the `bronze` table in this database and overwrite it with the results of the Spark SQL query