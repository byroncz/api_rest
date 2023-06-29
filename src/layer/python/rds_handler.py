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