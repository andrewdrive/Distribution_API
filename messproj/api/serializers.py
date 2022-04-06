from rest_framework import serializers
from api.models import Client, Distribution, Message


class ClientSerializer(serializers.ModelSerializer):
     class Meta:
          model = Client
          fields = '__all__'


class DistributionSerializer(serializers.ModelSerializer):
     class Meta:
          model = Distribution
          fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
     class Meta:
          model = Message
          fields = '__all__'