from email.policy import default
from rest_framework import serializers
from api.models import Client, Distribution, Message


class ClientSerializer(serializers.ModelSerializer):
     class Meta:
          model = Client
          fields = '__all__'


# class DistributionSerializer(serializers.ModelSerializer):

#      clients_filters = serializers.JSONField(default={"tags":[], "operator_nums": []})
#      # ОПИСАТЬ НОВЫЙ СЕРИАЛИЗАТОР ЧИСТЫЙ , и ДОБАВИТЬ ВАЛИДАЦИЮ ПО ТЭГАМ И НОМЕРАМ ОПЕРАТОРОВ
#      class Meta:
#           model = Distribution
#           fields = ['start_datetime', 'finish_datetime', 'delivery_text', 'clients_filters']


class DistributionSerializer(serializers.Serializer):
     start_datetime = serializers.DateTimeField()
     finish_datetime = serializers.DateTimeField()
     delivery_text = serializers.CharField(max_length=255, default='sample text', allow_blank=True)
     clients_filters = serializers.JSONField(default=dict([("tags", []), ("operator_nums", [])]))

     def validate_clients_filters(self, value):
          """ Check if tags and nums not in filters"""
          def check_for_list(obj):
               return isinstance(obj, list)

          json_ = value
          if 'tags' in json_ and 'operator_nums' in json_:
               tags_list = json_['tags']
               operator_nums_list = json_['operator_nums']
               if check_for_list(tags_list):
                    for tag_ in tags_list:
                         if Client.objects.filter(tag=tag_).exists():
                              continue
                         else:
                              raise serializers.ValidationError('Found no client with that tag')
               if check_for_list(operator_nums_list):
                    for num_ in operator_nums_list:
                         if Client.objects.filter(mobile_operator_code=num_).exists():
                              continue
                         else:
                              raise serializers.ValidationError('Found no client with that mobile operator code')
                    return value
          else:
               raise serializers.ValidationError('No tags or operator_nums keys in filter (json)')


class MessageSerializer(serializers.ModelSerializer):
     class Meta:
          model = Message
          fields = '__all__'