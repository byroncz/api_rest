import csv

import logger


logger = logger.setup_logger()


class DataProcessor:

    def process_csv(self, csv_data_location):
        processed_data = []
        reader = csv.reader(csv_data_location.splitlines())
        for row in reader:
            # Realizar cualquier manipulación o transformación necesaria en los datos
            processed_data.append(row)
        return processed_data