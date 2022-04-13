import requests
from messproj.celery.main import app
from messproj.settings import BEARER_TOKEN
from typing import Dict
from api.models import Message, Client
from datetime import datetime


class BearerAuth(requests.auth.AuthBase):
     def __init__(self, token):
          self.token = token

     def __call__(self, r):
          r.headers['authorization'] = 'Bearer ' + self.token
          return r


class RequestSender:
     def __init__(self, endpoint):
          self.endpoint = endpoint

     def send_request_to_api(self, msgId, request_body):
          headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
          data = {'id': request_body['id'], 'phone': request_body['phone'], 'text': request_body['text']}
          api_url = self.endpoint + '{msgId}'.format(msgId=msgId)
          response = requests.post(api_url, headers, data, auth=BearerAuth(token=BEARER_TOKEN))
          return response.json()


@app.task
def send_msg_now(data: Dict):
     url = 'https://probe.fbrq.cloud/v1/send/'


     # в таске надо принять все параметры с создаваемой рассылки и начать создавать сообщения в базе
     # если сообщение отправлено успешно и получен респонс 200 то создаем обьект, если нет, то делаем свой респонс на апи


     dist_id = data['distribution_id']
     clients_ids = data['clients_ids']

     for client_id in clients_ids:
          msg = Message(distribution_id=dist_id,
                        client_id=client_id,
                        delivery_datetime=datetime.now(),
                        delivery_status=True
               )
          
          request_body = {'id': ..., 'phone': ..., 'text': ...}

          pass
          

     rs = RequestSender(endpoint=url, msgId=..., request_body=request_body)

     pass