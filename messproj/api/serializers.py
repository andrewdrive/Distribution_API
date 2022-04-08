from email.policy import default
from rest_framework import serializers
from api.models import Client, Distribution, Message


class ClientSerializer(serializers.ModelSerializer):
     class Meta:
          model = Client
          fields = '__all__'


class DistributionSerializer(serializers.ModelSerializer):

     clients_filters = serializers.JSONField(default={"tags":[], "operator_nums": []})
     # ОПИСАТЬ НОВЫЙ СЕРИАЛИЗАТОР ЧИСТЫЙ , и ДОБАВИТЬ ВАЛИДАЦИЮ ПО ТЭГАМ И НОМЕРАМ ОПЕРАТОРОВ
     class Meta:
          model = Distribution
          fields = ['start_datetime', 'finish_datetime', 'delivery_text', 'clients_filters']


class MessageSerializer(serializers.ModelSerializer):
     class Meta:
          model = Message
          fields = '__all__'