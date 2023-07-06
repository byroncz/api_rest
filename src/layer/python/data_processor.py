
import csv

import logger


logger = logger.setup_logger()


class DataProcessor:
    """
    The `DataProcessor` class provides methods for processing CSV data by formatting strings based on an
    expression.
    """
    def process_csv(self, expression, csv_data):
        """
        Process the given CSV data using the provided expression.
        @param expression - the expression to format the strings in each row
        @param csv_data - the CSV data to process
        @return a list of processed data rows
        """
        processed_data = []
        reader = csv.reader(csv_data.splitlines())
        for row in reader:
            formatted_row = self.format_strings(expression, row)
            processed_data.append(formatted_row)
        return processed_data
    
    def format_strings(self, expression, row):
        """
        Format a list of strings based on a given expression and a row of values.
        @param expression - a list of boolean values indicating whether each element in the row should be formatted as a string or not
        @param row - a list of values to be formatted
        @return a comma-separated string of formatted values
        """
        row_formatted = []
        for i in range(len(expression)):
            if expression[i]:
                row_formatted.append("'" + row[i] + "'" if row[i] else 'null')
                continue
            row_formatted.append(row[i] if row[i] else 'null')
        return ','.join(row_formatted)