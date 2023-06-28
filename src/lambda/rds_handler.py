import boto3

import logger


logger = logger.setup_logger()
DATABASE = 'apirest'


class RDSHandler:
    
    def __init__(self, secret_arn, resource_arn):
        self.secret_arn = secret_arn
        self.resource_arn = resource_arn
        self.rds_data_client = boto3.client('rds-data')

    def build_insert_query(self, table_name, column_names, values):

        logger.info("Creando base INSERT query.")
        query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES "
        
        value_placeholders = []
        for row in values:
            str_row = ', '.join(row)
            value_placeholders.append(f"({str_row})")

        query += ', '.join(value_placeholders)

        return query
        
    def build_schema_and_tables_query(self):
        self.execute_sql("""
            CREATE SCHEMA IF NOT EXISTS replica;
            
            DROP TABLE IF EXISTS replica.hired_employees;
            CREATE TABLE replica.hired_employees (
                id INTEGER UNIQUE,
                name VARCHAR(255),
                datetime VARCHAR(255),
                department_id INTEGER,
                job_id INTEGER
            );
            
            DROP TABLE IF EXISTS replica.departments;
            CREATE TABLE replica.departments (
                id INTEGER UNIQUE,
                department VARCHAR(255)
            );
            
            DROP TABLE IF EXISTS replica.jobs;
            CREATE TABLE replica.jobs (
                id INTEGER UNIQUE,
                job VARCHAR(255)
            );
            """
        )

    def execute_sql(self, sql_query):
        
        sql_params = {
            'secretArn': self.secret_arn,
            'resourceArn': self.resource_arn,
            'sql': sql_query,
            'database': DATABASE,
            'includeResultMetadata': True
        }
        logger.info("Accediendo a la base datos.")
        try:
            return self.rds_data_client.execute_statement(**sql_params)
        except:
            logger.exception("Se ha presentado un error al momento de acceder a la base de datos.")