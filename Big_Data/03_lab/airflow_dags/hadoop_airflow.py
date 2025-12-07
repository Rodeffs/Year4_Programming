from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
import os
from datetime import datetime

HADOOP_HOME="/home/owner/Downloads/Big_Data/hadoop"
HADOOP_STREAMING=f"{HADOOP_HOME}/share/hadoop/tools/lib/hadoop-streaming-3.4.2.jar"
SOURCE_DIR="/home/owner/Programming/Year4_Programming/Big_Data/03_lab/hadoop"
INPUT_FILE="/home/owner/Downloads/Big_Data/cleaned_papers.txt"
INPUT_DIR="/home/owner/Downloads/Big_Data/hadoop_input"
OUTPUT_DIR="/home/owner/Downloads/Big_Data/hadoop_output"
RESULT_FILE="/home/owner/Downloads/Big_Data/hadoop_result.txt"

os.environ["JAVA_HOME"]="/usr/lib/jvm/java-17-openjdk"

with DAG(dag_id="popular-topics-hadoop", start_date=datetime(2025, 12, 6), schedule="@weekly", catchup=False) as dag:
    hadoop_hdfs = BashOperator(task_id="hadoop-hdfs-init", bash_command=f"{HADOOP_HOME}/bin/hdfs dfs -mkdir {INPUT_DIR}; {HADOOP_HOME}/bin/hdfs dfs -put {INPUT_FILE} {INPUT_DIR}")

    hadoop_mapreduce = BashOperator(task_id="hadoop-mapreduce", bash_command=f"{HADOOP_HOME}/bin/hadoop jar {HADOOP_STREAMING} -input {INPUT_DIR} -output {OUTPUT_DIR} -mapper 'python {SOURCE_DIR}/mapper.py' -reducer 'python {SOURCE_DIR}/reducer.py'")

    sort_results = BashOperator(task_id="sorting-results", bash_command=f"{HADOOP_HOME}/bin/hdfs dfs -cat {OUTPUT_DIR}/part-* | sort -t';' -k2,2nr > {RESULT_FILE}")

    cleanup = BashOperator(task_id="cleaning-up", bash_command=f"rm -rf {OUTPUT_DIR} {INPUT_DIR}")

    hadoop_hdfs >> hadoop_mapreduce >> sort_results >> cleanup

