import csv

import logger


logger = logger.setup_logger()


class DataProcessor:

    def process_csv(self, expression, csv_data):
        processed_data = []
        reader = csv.reader(csv_data.splitlines())
        for row in reader:
            formatted_row = self.format_strings(expression, row)
            processed_data.append(formatted_row)
        return processed_data
    
    def format_strings(self, expression, row):
        row_formatted = []
        for i in range(len(expression)):
            if expression[i]:
                row_formatted.append("'" + row[i] + "'" if row[i] else 'null')
                continue
            row_formatted.append(row[i] if row[i] else 'null')
        return ','.join(row_formatted)