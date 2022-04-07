from django.utils import timezone
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
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
          now = timezone.now()
          
          obj = serializer.save()
          dist_start_stamp = obj.start_datetime
          dist_finish_stamp = obj.start_datetime
          
          tag_and_num = []
          clients_list = list(obj.clients.values())

          for d in clients_list:
               tag_and_num.append((d['mobile_operator_code'], d['tag']))



          if now > dist_start_stamp and now < dist_finish_stamp:
               pass # clients = Client.objects.filter(tag=obj.)






          





# class ClientView(RetrieveUpdateDestroyAPIView):
#      queryset = Client.objects.all()
#      serializer_class = ClientSerializer

# Create your views here.
