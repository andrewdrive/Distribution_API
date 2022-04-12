import requests
from messproj.celery.main import app
from messproj.settings import BEARER_TOKEN
from typing import Dict


class BearerAuth(requests.auth.AuthBase):
     def __init__(self, token):
          self.token = token
     def __call__(self, r):
          r.headers['authorization'] = 'Bearer ' + self.token
          return r


class RequestSender:
     def __init__(self, endpoint, msgId, request_body):
          self.endpoint = endpoint
          self.msgId = msgId
          self.request_body = request_body

     def send_request_to_api(self):
          headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
          data = {'id': self.request_body['id'], 'phone': self.request_body['phone'], 'text': self.request_body['text']}
          api_url = self.endpoint + '{msgId}'.format(msgId=self.msgId)
          response = requests.post(api_url, headers, data, auth=BearerAuth(token=BEARER_TOKEN))
          return response.json()


@app.task
def send_message_to_clients(data: Dict):
     url = 'https://probe.fbrq.cloud/v1/send/'

     dist_id = data['distribution_id']
     clients_ids = data['clients_ids']

     r_body = {}

     rs = RequestSender(endpoint=url, msgId=..., request_body=r_body)

     pass