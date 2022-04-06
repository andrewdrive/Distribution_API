from rest_framework.generics import RetrieveUpdateDestroyAPIView
from api.models import Client
from api.serializers import ClientSerializer


class ClientView(RetrieveUpdateDestroyAPIView):
     queryset = Client.objects.all()
     serializer_class = ClientSerializer







# Create your views here.
