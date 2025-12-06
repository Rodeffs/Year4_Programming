from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime
import os

SPARK_HOME="/home/owner/Downloads/Big_Data/spark"
SOURCE_FILE="/home/owner/Programming/Year4_Programming/Big_Data/03_lab/spark/spark_local.py"
OUTPUT_DIR="/home/owner/Downloads/Big_Data/spark_output"
RESULT_FILE="/home/owner/Downloads/Big_Data/spark_result.txt"

os.environ["JAVA_HOME"]="/usr/lib/jvm/java-17-openjdk"

with DAG(dag_id="popular-topics-spark", start_date=datetime(2025, 12, 6), schedule="@weekly", catchup=False) as dag:
    spark_job = BashOperator(task_id="spark-job", bash_command=f"{SPARK_HOME}/bin/spark-submit --num-executors 3 --executor-memory 6G --executor-cores 2 --driver-memory 4G --conf spark.memory.fraction=0.6 --conf spark.memory.storeageFraction=0.3 {SOURCE_FILE}")
    
    concat_results = BashOperator(task_id="concatanating-results", bash_command=f"cat {OUTPUT_DIR}/part-* > {RESULT_FILE}")

    cleanup = BashOperator(task_id="cleaning-up", bash_command=f"rm -rf {OUTPUT_DIR}")

    spark_job >> concat_results >> cleanup

