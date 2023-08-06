#!/usr/bin/env python3 
import pandas as pd
import google.auth
from google.cloud import bigquery


# Authenticate with GCP & connect bigquery client
credentials, project = google.auth.default()
client = bigquery.Client()

def execute_sql(sql_file):
    query_job = client.query(sql_file)
    result = query_job.result()
    column_names = [field.name for field in result.schema]
    data = pd.DataFrame(data=[row.values() for row in result], columns=column_names)
    return data
