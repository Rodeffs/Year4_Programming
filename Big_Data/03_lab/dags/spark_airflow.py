from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime
import os

SPARK_HOME="/home/owner/Downloads/Big_Data/spark"
SOURCE_FILE="/home/owner/Programming/Year4_Programming/Big_Data/03_lab/spark/spark_local.py"
INPUT_FILE="/home/owner/Downloads/Big_Data/cleaned_papers.csv"
OUTPUT_DIR="/home/owner/Downloads/Big_Data/spark_output"
RESULT_FILE="/home/owner/Downloads/Big_Data/spark_result.txt"

os.environ["JAVA_HOME"]="/usr/lib/jvm/java-17-openjdk"

with DAG(dag_id="popular-topics-spark", start_date=datetime(2025, 12, 6), schedule="@hourly", catchup=False) as dag:
    spark_job = BashOperator(task_id="spark-job", bash_command=f"{SPARK_HOME}/bin/spark-submit --input {INPUT_FILE} --output {OUTPUT_DIR} --deploy-mode cluster --num-executors 4 --executor_memory 4G --executor-cores 2 {SOURCE_FILE}")

    sort_results = BashOperator(task_id="sorting-results", bash_command=f"cat {OUTPUT_DIR}/part-* | sort -t';' -k2,2nr > {RESULT_FILE}")

    spark_job >> sort_results

