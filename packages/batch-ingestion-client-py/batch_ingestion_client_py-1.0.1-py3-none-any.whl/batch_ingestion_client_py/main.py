from batch_ingestion_client_py.data import Data
from batch_ingestion_client_py.response import Response
import requests
import json


class BatchIngestor:
    def __init__(
        self,
        base_url: str,
    ):
        route = "/w/rest.php/BatchIngestion/v0/batchcreate"
        self.url = base_url + route

    def ingest(self, data: Data):
        json_data = data.serialize()
        response = requests.post(self.url, json=json_data)
        success = response.status_code == 200
        if not success:
            raise Exception(response.text)
        json_res = json.loads(response.text)
        return Response.parse(json_res)
