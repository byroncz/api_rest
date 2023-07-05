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


def deliver_metric(query):
    results = rds_handler.execute_sql(query)
    return api_handler.create_response(200, results['records'])
    

def handler(event, context):
    
    if event['queryStringParameters']['requirements'] == 'employees':
        logger.info(f"Construyendo métrica -employees-.")
        return deliver_metric("""
        SELECT 
            d.department, 
            j.job, 
            COUNT(CASE WHEN EXTRACT(MONTH FROM to_timestamp(he.datetime, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AT TIME ZONE 'UTC') BETWEEN 1 AND 3 THEN 'Q1' END) AS Q1,
            COUNT(CASE WHEN EXTRACT(MONTH FROM to_timestamp(he.datetime, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AT TIME ZONE 'UTC') BETWEEN 4 AND 6 THEN 'Q1' END) AS Q2,
            COUNT(CASE WHEN EXTRACT(MONTH FROM to_timestamp(he.datetime, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AT TIME ZONE 'UTC') BETWEEN 7 AND 9 THEN 'Q1' END) AS Q3,
            COUNT(CASE WHEN EXTRACT(MONTH FROM to_timestamp(he.datetime, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AT TIME ZONE 'UTC') BETWEEN 10 AND 12 THEN 'Q1' END) AS Q4
        FROM replica.hired_employees he
        JOIN replica.departments d ON d.id=he.department_id
        JOIN replica.jobs j ON j.id=he.job_id
        GROUP BY d.department, j.job, he.department_id, he.job_id
        ORDER BY department_id ASC, job_id DESC
        """
        ) 
        
    elif event['queryStringParameters']['requirements'] == 'ids':
        logger.info(f"Construyendo métrica -ids-.")
        return deliver_metric("""
        SELECT 
            d.id,
            d.department
            numero_2022
        FROM (
            SELECT 
                department_id,
                COUNT(*) AS numero_2022
            FROM replica.hired_employees he2022
            WHERE EXTRACT(YEAR FROM to_timestamp(he2022.datetime, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AT TIME ZONE 'UTC') = 2022
            GROUP BY he2022.department_id
        ) cuantos_2022
        JOIN replica.departments d ON d.id=cuantos_2022.department_id
        WHERE numero_2022 > (
            SELECT 
                AVG(numero_2021) promedio_2021
            FROM (
                SELECT 
                    department_id,
                    COUNT(*) AS numero_2021
                FROM replica.hired_employees he2021
                WHERE EXTRACT(YEAR FROM to_timestamp(he2021.datetime, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AT TIME ZONE 'UTC') = 2021
                GROUP BY he2021.department_id
            ) promedio_21
        )
        """
        )  
    else:
        logger.error("Métrica no válida.")
        raise ValueError("Métrica no válida.")
