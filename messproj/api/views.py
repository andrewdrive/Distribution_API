from django.utils import timezone
from rest_framework import viewsets
from rest_framework import permissions
from api.models import Client, Distribution
from api.serializers import ClientSerializer, DistributionSerializer, MessageSerializer
from api.tasks import send_msg_now


class ClientViewSet(viewsets.ModelViewSet):
     queryset = Client.objects.all()
     serializer_class = ClientSerializer
     permission_classes = [permissions.IsAuthenticated]


class DistributionViewSet(viewsets.ModelViewSet):
     queryset = Distribution.objects.all()
     serializer_class = DistributionSerializer
     permission_classes = [permissions.IsAuthenticated]


     def perform_create(self, serializer):
          obj = serializer.save()
          now = timezone.now()
          json_filter = obj.clients_filter
          if now > obj.start_datetime and now < obj.finish_datetime:
               clients_qs = []
               if 'tags' in json_filter:
                    for tag_ in json_filter['tags']:
                         clients_qs.append(Client.objects.filter(tag=tag_))
               if 'mocs' in json_filter:
                    for moc_ in json_filter['mocs']:
                         clients_qs.append(Client.objects.filter(mobile_operator_code=moc_))

               clients_qs = list(set(clients_qs))[0]
               clients_ids = list(clients_qs.values_list('id', flat=True))
               data = {'distribution_id': obj.id, 'clients_ids': clients_ids}
               trace = send_msg_now.apply_async(args=(data,), countdown=0)

               #print('ITS A TRAAAAAAAAACE', trace)
          


# - получения общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по статусам





# - получения детальной статистики отправленных сообщений по конкретной рассылке




# - обработки активных рассылок и отправки сообщений клиентам




# Create your views here.
