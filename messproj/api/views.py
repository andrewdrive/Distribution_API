from django.utils import timezone
from rest_framework import viewsets
from rest_framework import permissions
from api.models import Client, Distribution, Message
from api.serializers import ClientSerializer, DistributionSerializer


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


               clients_qs = set(clients_qs)
               print(clients_qs)
          # логика запуска отправки клинетам после создания Рассылки 






# Create your views here.
