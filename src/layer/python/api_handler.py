import json

import logger


logger = logger.setup_logger()


class APIHandler:

    def get_data(self, event):
        if "body" in event and event["body"]:
            raw_data = event["body"].split('&')
            return raw_data[0], raw_data[1].split('Tabla=')[1]
        else:
            logger.error("No se proporcionó el cuerpo de la solicitud.")
            raise ValueError("No se proporcionó el cuerpo de la solicitud.")

    def create_response(self, status_code, message):
        return {
            "statusCode": status_code,            
            'headers': {
                'Content-Type': 'text/plain; charset=utf-8'
            },
            "body": json.dumps({"message": message})
        }