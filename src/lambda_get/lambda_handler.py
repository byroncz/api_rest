from rds_handler import RDSHandler
from api_handler import APIHandler

import os
import json
import logger


logger = logger.setup_logger()

SECRET_ARN = os.environ['SECRET_ARN']
DB_CLUSTER_ARN = os.environ['DB_CLUSTER_ARN']

api_handler = APIHandler()
rds_handler = RDSHandler(secret_arn=SECRET_ARN, resource_arn=DB_CLUSTER_ARN)


def deliver_metric(event):
    results = rds_handler.execute_sql('SELECT schema_name FROM information_schema.schemata;')
    return api_handler.create_response(200, results)


def handler(event, context):
    
    logger.info(json.dumps(event))
            
    return deliver_metric(event) 
    
