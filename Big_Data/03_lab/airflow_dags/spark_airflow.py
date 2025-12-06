from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime
import os

SPARK_HOME="/home/owner/Downloads/Big_Data/spark"
SOURCE_FILE="/home/owner/Programming/Year4_Programming/Big_Data/03_lab/spark/spark_local.py"

os.environ["JAVA_HOME"]="/usr/lib/jvm/java-17-openjdk"

with DAG(dag_id="popular-topics-spark", start_date=datetime(2025, 12, 6), schedule="@weekly", catchup=False) as dag:
    spark_job = BashOperator(task_id="spark-job", bash_command=f"{SPARK_HOME}/bin/spark-submit --num-executors 3 --executor-memory 6G --executor-cores 2 --driver-memory 4G --conf spark.memory.fraction=0.6 --conf spark.memory.storeageFraction=0.3 {SOURCE_FILE}")

    spark_job

