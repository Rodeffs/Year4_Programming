from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

HADOOP_HOME="/home/owner/Downloads/Big_Data/hadoop"
HADOOP_STREAMING=f"{HADOOP_HOME}/share/hadoop/tools/lib/hadoop-streaming-3.4.2.jar"
SOURCE_DIR="/home/owner/Programming/Year4_Programming/Big_Data/03_lab/hadoop"
INPUT_DIR="/home/owner/Downloads/Big_Data/split"
OUTPUT_DIR="/home/owner/Downloads/Big_Data/hadoop_output"
RESULT_FILE="/home/owner/Downloads/Big_Data/hadoop_result.txt"

dag = DAG(dag_id="popular_topics_hadoop", start_date=datetime(2025, 12, 6), schedule="@hourly", catchup=False)

with dag:
    hadoop_mapreduce = BashOperator(task_id="hadoop_mapreduce", bash_command=f"{HADOOP_HOME}/bin/hadoop jar {HADOOP_STREAMING} -input {INPUT_DIR} -output {OUTPUT_DIR} -mapper python {SOURCE_DIR}/mapper.py -reducer python {SOURCE_DIR}/reducer.py")

    sort_results = BashOperator(task_id="sorting_results", bash_command=f"cat {OUTPUT_DIR}/part-* | sort -t';' -k2,2nr > {RESULT_FILE}")

    hadoop_mapreduce >> sort_results

