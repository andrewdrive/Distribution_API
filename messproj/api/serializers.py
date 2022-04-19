from rest_framework import serializers
from api.models import Client, Distribution, Message


class ClientSerializer(serializers.ModelSerializer):
     class Meta:
          model = Client
          fields = ['phone_number', 'mobile_operator_code', 'tag', 'timezone']


class DistributionSerializer(serializers.ModelSerializer):
     start_datetime = serializers.DateTimeField()
     finish_datetime = serializers.DateTimeField()
     delivery_text = serializers.CharField(max_length=255, default='sample text', allow_blank=True)
     clients_filter = serializers.JSONField(default=dict([("tags", []), ("mocs", [])]), help_text='{"tags": [], "mocs": []} *mobile_operator_code = mocs')


     def validate_clients_filter(self, value):
          """ Check if tags and mobile_operator_codes not in filter"""
          json_ = value
          if 'tags' in json_ or 'mocs' in json_: 
               if 'tags' in json_:
                    tags_list = json_['tags']
                    if isinstance(tags_list, list):
                         for tag_ in tags_list:
                              if Client.objects.filter(tag=tag_).exists():
                                   continue
                              else:
                                   raise serializers.ValidationError('Found no client with that tag = {x}'.format(x=tag_))
                    else:
                         raise serializers.ValidationError("Invalid data structure, tags is not a list of values")
               if 'mocs' in json_:
                    mocs_list = json_['mocs']      
                    if isinstance(mocs_list, list):
                         for moc_ in mocs_list:
                              if Client.objects.filter(mobile_operator_code=moc_).exists():
                                   continue
                              else:
                                   raise serializers.ValidationError('Found no client with that mobile operator code = {x}'.format(x=moc_))
                    else:
                         raise serializers.ValidationError("Invalid data structure, mocs is not a list of values")
          else:
               raise serializers.ValidationError("No 'tags' or 'mocs' keys in filter (json)")
          return value

     class Meta:
          model = Distribution
          fields = ['start_datetime', 'finish_datetime', 'delivery_text', 'clients_filter']


class MessageSerializer(serializers.ModelSerializer):
     class Meta:
          model = Message
          fields = ['distribution', 'client', 'delivery_datetime', 'delivery_status']


class CommonStatSerializer(serializers.ModelSerializer):
     class Meta:
          model = Distribution
          fields = ['id', 'delivery_text']
     
