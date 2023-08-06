#!/usr/bin/env python3
import argparse
import pandas as pd
import google.auth
from google.cloud import bigquery
from google.cloud import bigquery_storage_v1
import pandas_gbq
from tabulate import tabulate

# Authenticate with GCP & connect bigquery client
credentials, project = google.auth.default()
client = bigquery.Client()
storage_client = bigquery_storage_v1.BigQueryReadClient(credentials=credentials)

# Set cli parser as a global variable
cli_parser = argparse.ArgumentParser()
cli_parser.add_argument('--run', help="SQL filename to process")
cli_parser.add_argument('--ftype', help="Use if .sqlx file")
args = cli_parser.parse_args()


# var = 'test.sql'

def read_data(filepath):
    with open(filepath, 'r') as file:
        data = file.read()
    return data

def execute_sql(sql_file):
    # Fetch data directly into a DataFrame using pandas_gbq
    data = pandas_gbq.read_gbq(
        sql_file,
        project_id=project,
        credentials=credentials,
        use_bqstorage_api=True,
    )
    return data

def output_df_head():
    sqlfile = args.run 
    file = read_data(f"./{sqlfile}.sql")
    df = execute_sql(file)

    print(tabulate(df.head(), headers='keys', tablefmt='psql', showindex=False))

