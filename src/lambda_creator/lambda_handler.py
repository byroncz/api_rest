from rds_handler import RDSHandler

import os
import logger


logger = logger.setup_logger()

SECRET_ARN = os.environ['SECRET_ARN']
DB_CLUSTER_ARN = os.environ['DB_CLUSTER_ARN']

rds_handler = RDSHandler(secret_arn=SECRET_ARN, resource_arn=DB_CLUSTER_ARN)


def handler(event, context):
    """
    The above function creates a schema and three tables in an RDS database using the RDSHandler class.
    
    :param event: The `event` parameter is used to pass data to the Lambda function when it is
    triggered. It can contain information such as the event source, event details, and any other
    relevant data
    :param context: The `context` parameter is an object provided by the AWS Lambda service. It contains
    information about the runtime environment and the current invocation of the Lambda function. It can
    be used to access details such as the function name, function version, request ID, and more
    """
    logger.info("Creando schema replica y tablas hired_employees, departments, jobs")
            
    rds_handler.execute_sql("""
        DROP TABLE IF EXISTS replica.hired_employees;
        DROP TABLE IF EXISTS replica.departments;
        DROP TABLE IF EXISTS replica.jobs;
        
        CREATE SCHEMA IF NOT EXISTS replica;

        CREATE TABLE replica.departments (
            id INTEGER UNIQUE,
            department VARCHAR(255),
            PRIMARY KEY(id)
        );
        
        CREATE TABLE replica.jobs (
            id INTEGER UNIQUE,
            job VARCHAR(255),
            PRIMARY KEY(id)
        );

        CREATE TABLE replica.hired_employees (
            id INTEGER UNIQUE ,
            name VARCHAR(255),
            datetime VARCHAR(255),
            department_id INTEGER,
            job_id INTEGER,
            PRIMARY KEY(id)
        );
        """
    )
    logger.info("Creacion completada.")