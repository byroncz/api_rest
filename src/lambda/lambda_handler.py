from rds_handler import RDSHandler
from api_handler import APIHandler
from data_processor import DataProcessor

import os
import json
import logger


logger = logger.setup_logger()

SECRET_ARN = os.environ['SECRET_ARN']
DB_CLUSTER_ARN = os.environ['DB_CLUSTER_ARN']

COLUMN_NAMES = {
    'hired_employees': ['id', 'name', 'datetime', 'department_id', 'job_id'],
    'departments': ['id', 'department'],
    'jobs': ['id', 'job']
}

rds_handler = RDSHandler(secret_arn=SECRET_ARN, resource_arn=DB_CLUSTER_ARN)
api_handler = APIHandler()
data_processor = DataProcessor()

if True:
    rds_handler.build_schema_and_tables_query()


def insertion_job(event):
    
    csv_data, table_name = api_handler.get_data(event)
    if table_name not in COLUMN_NAMES:
        return api_handler.create_response(400, f"Error. tabla no disponible: {table_name}")
    
    processed_data = data_processor.process_csv(csv_data)
    if len(processed_data) > 1000:
        return api_handler.create_response(400, f"Error. Se ha excedido el número máximo de registros: {len(processed_data)}")
    
    insert_query = rds_handler.build_insert_query(table_name, COLUMN_NAMES[table_name], processed_data) 
    logger.info(insert_query)
    
    results = rds_handler.execute_sql(insert_query)
    return api_handler.create_response(200, f"OK. Data insertada.")

def insertion_job(event):
    
    csv_data, table_name = api_handler.get_data(event)
    if table_name not in COLUMN_NAMES:
        return api_handler.create_response(400, f"Error. tabla no disponible: {table_name}")
    
    processed_data = data_processor.process_csv(csv_data)
    if len(processed_data) > 1000:
        return api_handler.create_response(400, f"Error. Se ha excedido el número máximo de registros: {len(processed_data)}")
    
    insert_query = rds_handler.build_insert_query(table_name, COLUMN_NAMES[table_name], processed_data) 
    logger.info(insert_query)
    
    results = rds_handler.execute_sql(insert_query)
    return api_handler.create_response(200, f"OK. Data insertada.")


def deliver_metric(event):
    pass


def handler(event, context):
    
    logger.info(json.dumps(event))
    
    if event['httpMethod'] == 'POST':
        return insertion_job(event) 
        
    if event['httpMethod'] == 'GET':
        return deliver_metric(event) 
    
