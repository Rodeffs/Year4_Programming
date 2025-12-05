from time import time

import findspark
findspark.init()
findspark.find()

import pyspark

from pyspark.sql import DataFrame, SparkSession
from typing import List
import pyspark.sql.types as T
import pyspark.sql.functions as F

def main():
    spark = SparkSession.builder.appName("popular_topics").getOrCreate()

    # Reading the CSV

    print("READING CSV")

    df = spark.read.csv("/home/owner/Downloads/Big_Data/cleaned_papers.csv", header=True, sep=',', quote='"', escape='"', multiLine=True)

    # Adding a column that unifies title and abstract into one

    df = df.withColumn("entry", F.concat_ws(". ", "title", "abstract"))
    df = df.withColumn("entry", F.lower("entry"))  # проще работать в нижнем регистре
    df = df.withColumn("entry", F.regexp_replace(F.col("entry"), r"\s*\n\s*", ' '))  # убрать лишние переносы строки
    df = df.drop("title", "abstract")  # они больше не нужны

    # Now we use regexp to split each row into word combinations

    regexp = r"([^a-z^\s^'^-])|(?:^|[^a-z])['-]|['-](?:^|[^a-z])|'*(?<![a-z-])(?:a|an|the|and|or|as|of|in|on|yet|our|than|then|however|at|but|was|were|which|there|this|that|thus|we|to|for|is|are|where|have|has|been|since|with|such|another|also|by|often|can|could|so|from|its|via|will|hence|should|would|shall|what|although|these|those|do|does|did|under|above|else|if|while|when|who|based|way|very|many|much|due|because|onto|into|out|finally|their|they|may|might|up|down|either|neither|nor|within|according|others|about|therefore|no|not|towards|beyond|behind|over|how|both|without|other|another|more|most|moreover|be|furthermore|why|paper|focuses|well|must|consider|using|used|commonly|some|given|among|able|present|his|her|he|she|obtained|makes|give|make|further|use|introduce|employ|uses|show|allows|gives|introduces|considers|through|take|takes|enable|enables|allow|every|each|called|provide|provides|cannot|allowing|even|though|after|around|upon|you|new)(?![a-z-])'*"
    
    print("SPLITTING INTO WORD COMBINATIONS")

    df = df.select(F.explode(F.split(F.col("entry"), regexp)).alias("entry"))
    df = df.withColumn("entry", F.trim(F.col("entry")))  # обрезаем лишние пробелы
    df = df.filter(F.size(F.split(F.col("entry"), r"\s+")) >= 2)  # за темы считаем комбинации слов >= 2

    # Mapping

    print("MAPPING")

    df = df.withColumn("value", F.lit(1))

    # Reduce

    print("REDUCING")

    df = df.groupBy("entry").agg(F.sum("value").alias("total")).orderBy("total", ascending=False)

    print("WRITING")

    df.write.csv("/home/owner/Downloads/Big_Data/spark_result.csv")


if __name__ == "__main__":
    start_time = time()
    main()
    print("\nExecute time:", time() - start_time)
