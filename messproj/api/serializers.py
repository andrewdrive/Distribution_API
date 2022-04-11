from rest_framework import serializers
from api.models import Client, Distribution, Message


class ClientSerializer(serializers.ModelSerializer):
     class Meta:
          model = Client
          fields = '__all__'


class DistributionSerializer(serializers.ModelSerializer):
     start_datetime = serializers.DateTimeField()
     finish_datetime = serializers.DateTimeField()
     delivery_text = serializers.CharField(max_length=255, default='sample text', allow_blank=True)
     clients_filter = serializers.JSONField(default=dict([("tags", []), ("mocs", [])]), help_text='{"tags": [], "mocs": []} *mobile_operator_code = mocs')

     
     def validate_clients_filter(self, value):
          """ Check if tags and nums not in filters"""
          json_ = value
          if 'tags' in json_: 
               tags_list = json_['tags']
               if isinstance(tags_list, list):
                    for tag_ in tags_list:
                         if Client.objects.filter(tag=tag_).exists():
                              continue
                         else:
                              raise serializers.ValidationError('Found no client with that tag = {x}'.format(x=tag_))
          if 'mocs' in json_:     
               mocs_list = json_['mocs']      
               if isinstance(mocs_list, list):
                    for moc_ in mocs_list:
                         if Client.objects.filter(mobile_operator_code=moc_).exists():
                              continue
                         else:
                              raise serializers.ValidationError('Found no client with that mobile operator code')
          else:
               raise serializers.ValidationError("No 'tags' or 'mocs' keys in filter (json)")
          return value


     class Meta:
          model = Distribution
          fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
     class Meta:
          model = Message
          fields = '__all__'