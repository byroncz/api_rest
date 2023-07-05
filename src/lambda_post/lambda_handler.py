from rds_handler import RDSHandler
from api_handler import APIHandler
from data_processor import DataProcessor

import os
import json
import logger
import time


logger = logger.setup_logger()

SECRET_ARN = os.environ['SECRET_ARN']
DB_CLUSTER_ARN = os.environ['DB_CLUSTER_ARN']

TABLES = {
    'hired_employees': {
        'column_names': ['id', 'name', 'datetime', 'department_id', 'job_id'],
        'str_format_expression': [False, True, True, False, False]
    },
    'departments': {
        'column_names': ['id', 'department'],
        'str_format_expression': [False, True]
    },
    'jobs': {
        'column_names': ['id', 'job'],
        'str_format_expression': [False, True]
    }
}

rds_handler = RDSHandler(secret_arn=SECRET_ARN, resource_arn=DB_CLUSTER_ARN)
api_handler = APIHandler()
data_processor = DataProcessor()


def insertion_job(event):
    
    csv_data, table_name = api_handler.get_data(event)
    if table_name not in list(TABLES.keys()):
        return api_handler.create_response(400, f"Error. tabla no disponible: {table_name}")
    
    processed_data = data_processor.process_csv(TABLES[table_name]['str_format_expression'], csv_data)
    if len(processed_data) > 1000:
        return api_handler.create_response(400, f"Error. Se ha excedido el número máximo de registros: {len(processed_data)}")
    
    sql_statements = rds_handler.build_batch_insert('replica.'+table_name, TABLES[table_name]['column_names'], processed_data) 
    
    for query in sql_statements:
        print(query)
        rds_handler.execute_sql(query)
        time.sleep(1)
    
    return api_handler.create_response(200, f"OK. Data insertada.")


def handler(event, context):
    
    # logger.info(json.dumps(event))
    
    return insertion_job(event) 
        