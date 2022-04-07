from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions
from api.models import Client
from api.serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
     queryset = Client.objects.all()
     serializer_class = ClientSerializer
     permission_classes = [permissions.IsAuthenticated]

     

# class ClientView(RetrieveUpdateDestroyAPIView):
#      queryset = Client.objects.all()
#      serializer_class = ClientSerializer

# Create your views here.
