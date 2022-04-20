import requests
from requests.structures import CaseInsensitiveDict
from messproj.celery.main import app
from messproj.settings import BEARER_TOKEN
from api.models import Message, Client, Distribution
from django.utils import timezone


class RequestSender:
     def __init__(self, endpoint):
          self.endpoint = endpoint

     def send_request_to_api(self, msgId, request_body):
          headers = CaseInsensitiveDict()
          headers['accept'] = 'application/json'
          headers['Content-Type'] = 'application/json'
          headers['Authorization'] = 'Bearer ' + BEARER_TOKEN
          data = """
          {{            
            "id": {id}, 
            "phone": {phone}, 
            "text": "{text}"
          }}
          """.format(id=request_body['id'], phone=request_body['phone'], text=request_body['text'])
          api_url = self.endpoint + '{}'.format(msgId)
          response = requests.post(api_url, headers=headers, data=data)
          return response


def get_clients_ids(id_: int):
          obj = Distribution.objects.get(pk=id_)
          json_filter = obj.clients_filter
          clients_qs = Client.objects.none()
          if 'tags' in json_filter:
               clients_qs = clients_qs.union(Client.objects.filter(tag__in=json_filter["tags"]))
               clients_ids = list(clients_qs.values_list('id', flat=True))
          if 'mocs' in json_filter:
               clients_qs = clients_qs.union(Client.objects.filter(mobile_operator_code__in=json_filter["mocs"]))
               clients_ids = list(clients_qs.values_list('id', flat=True))
          if len(clients_qs) == 0:
               clients_qs = Client.objects.all()
               clients_ids = clients_qs.values_list('id', flat=True)
               
          return clients_ids


@app.task
def send_msg_now(obj_id: int):
     

     url = 'https://probe.fbrq.cloud/v1/send/'
     rs = RequestSender(endpoint=url)
     dist_id = obj_id
     clients_ids = get_clients_ids(dist_id)
     dist = Distribution.objects.get(pk=dist_id)
    
     for client_id in clients_ids:
          cli = Client.objects.get(pk=client_id)
          msg = Message(distribution_id=dist_id, client_id=cli.id, delivery_datetime=timezone.now(), delivery_status=False)
          msg.save()
          request_body = {'id': msg.id, 'phone': int(cli.phone_number), 'text': dist.delivery_text}
          response = rs.send_request_to_api(msg.id, request_body)
          # print(response)
          if response.status_code == 200:
               msg.delivery_status = True
               msg.save()
          else:
               msg.delivery_status = False
               msg.save()