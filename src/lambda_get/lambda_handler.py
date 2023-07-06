from rds_handler import RDSHandler
from api_handler import APIHandler

import os
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
    """
    The code defines a Lambda function that handles API requests and retrieves data from an RDS database
    based on the specified requirements. In this particular case, this Lambda function is used to deliver 
    the answer requested by excercises 1 and 2 of the technical test.
    
    :param query: The `query` parameter is a SQL query that will be executed on the RDS database. It is
    used to retrieve the data needed to construct the metric
    :return: The `handler` function returns the result of the `deliver_metric` function, which is a
    response object created by the `api_handler.create_response` method. The response object contains
    the HTTP status code (200) and the results of the SQL query executed by the
    `rds_handler.execute_sql` method.
    """
    if event['queryStringParameters']['requirements'] == 'employees':
        logger.info(f"Construyendo métrica -employees-.")
        return deliver_metric("""
        SELECT 
            d.department, 
            j.job, 
            COUNT(CASE WHEN EXTRACT(MONTH FROM to_timestamp(he.datetime, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AT TIME ZONE 'UTC') BETWEEN 1 AND 3 THEN 'Q1' END) AS Q1,
            COUNT(CASE WHEN EXTRACT(MONTH FROM to_timestamp(he.datetime, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AT TIME ZONE 'UTC') BETWEEN 4 AND 6 THEN 'Q2' END) AS Q2,
            COUNT(CASE WHEN EXTRACT(MONTH FROM to_timestamp(he.datetime, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AT TIME ZONE 'UTC') BETWEEN 7 AND 9 THEN 'Q3' END) AS Q3,
            COUNT(CASE WHEN EXTRACT(MONTH FROM to_timestamp(he.datetime, 'YYYY-MM-DD"T"HH24:MI:SS"Z"') AT TIME ZONE 'UTC') BETWEEN 10 AND 12 THEN 'Q4' END) AS Q4
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
            d.department,
            numero_2022 AS hired
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
