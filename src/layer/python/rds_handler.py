import boto3

import logger


logger = logger.setup_logger()
DATABASE = 'apirest'


class RDSHandler:
    """
    The `RDSHandler` class provides methods for building and executing SQL queries on an RDS database
    using the `boto3` library.
    """
    def __init__(self, secret_arn, resource_arn):
        self.secret_arn = secret_arn
        self.resource_arn = resource_arn
        self.rds_data_client = boto3.client('rds-data')
        
    def build_batch_insert(self, table_name, column_names, values):
        """
        Build batch insert queries for a given table, column names, and values.
        @param table_name - the name of the table to insert into
        @param column_names - the names of the columns to insert into
        @param values - the values to insert
        @return a list of batch insert queries
        """
        devided_values = [values[i:i+10] for i in range(0, len(values), 10)]
        return [self.build_insert_query(table_name, column_names, value ) for value in devided_values]

    def build_insert_query(self, table_name, column_names, values):
        """
        Build an SQL insert query for a given table, column names, and values.
        @param table_name - the name of the table to insert into
        @param column_names - a list of column names
        @param values - a list of values to insert
        @return The SQL insert query as a string
        """
        query = f"INSERT INTO {table_name} ({', '.join(column_names)}) VALUES "
        
        value_placeholders = []
        for row in values:
            value_placeholders.append(f"({row})")

        query += ', '.join(value_placeholders)

        return query

    def execute_sql(self, sql_query):
        """
        Execute an SQL query on the specified database using the RDS Data API.
        @param sql_query - the SQL query to execute
        @return the result of the SQL query execution
        """
        
        sql_params = {
            'secretArn': self.secret_arn,
            'resourceArn': self.resource_arn,
            'sql': sql_query,
            'database': DATABASE,
            'includeResultMetadata': True
        }
        logger.info("Accediendo a la base datos.")
        # try:
        return self.rds_data_client.execute_statement(**sql_params)
        # except:
        #     logger.exception("Se ha presentado un error al momento de acceder a la base de datos.")
    
