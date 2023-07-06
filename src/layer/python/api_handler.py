
import json

import logger


logger = logger.setup_logger()


.
class APIHandler:
    """
    The APIHandler class provides methods for extracting data from an event object and creating a
    response object
    """
    def get_data(self, event):
        """
        This method is used to extract data from an event object. It expects the event object to have a "body" field. 
        If the "body" field is present and not empty, it splits the body string by '&' and returns the first element 
        and the second element split by 'Tabla='. If the "body" field is not present or empty, it logs an error
        message and raises a ValueError.
        @param event - the event object containing the data
        @return a tuple containing the first element of the split body string and the second element split by 'Tabla='
        """
        if "body" in event and event["body"]:
            raw_data = event["body"].split('&')
            return raw_data[0], raw_data[1].split('Tabla=')[1]
        else:
            logger.error("No se proporcionó el cuerpo de la solicitud.")
            raise ValueError("No se proporcionó el cuerpo de la solicitud.")

    def create_response(self, status_code, message):
        """
        Create a response object with the given status code and message.
        @param status_code - the status code of the response
        @param message - the message to include in the response body
        @return a response object with the specified status code, headers, and body
        """
        return {
            "statusCode": status_code,            
            'headers': {
                'Content-Type': 'text/plain; charset=utf-8'
            },
            "body": json.dumps({"message": message})
        }