"""
A super lightweight SQL CLI tool for data processing
Runs any external .sql file in directory against a data warehouse & outputs as a pandas data frame

$ return-dataframe --run=file_name --dir=folder_name

"""
#!/usr/bin/env python3 
import argparse
from . big_query import execute_sql as ex
from . data_cleaning import read_data as rd

def run_sql():
    cli_parser = argparse.ArgumentParser()

    cli_parser.add_argument('--run', help="Name of sql file")
    cli_parser.add_argument('--dir', help="Diff folders", default="./")
    args = cli_parser.parse_args()

    sqlfile = args.run
    dirname = args.dir

    filepath = rd.read_data(f"./{dirname}/{sqlfile}.sql") 
    df = ex.execute_sql(filepath)

    return df
 
if __name__ == '__main__':
    run_sql()

# todo: update the run_sql function to be able to handle semi-colons or multiple statements 
# todo: add -d and -r for non-verbose cli args
# todo: add a new option that outputs just the table head instead of returning whole df 

