from multiprocessing.sharedctypes import Value
from django.forms import IntegerField
from django.utils import timezone
from django.db.models import Count, Sum, Case, When, Value, IntegerField
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework.decorators import action
from api.models import Client, Distribution, Message
from api.serializers import ClientSerializer, DistributionSerializer, MessageSerializer, CommonStatSerializer
from api.tasks import send_msg_now


class ClientViewSet(viewsets.ModelViewSet):
     queryset = Client.objects.all()
     serializer_class = ClientSerializer
     permission_classes = [permissions.IsAuthenticated]


class DistributionViewSet(viewsets.ModelViewSet):
     queryset = Distribution.objects.all()
     serializer_class = DistributionSerializer
     permission_classes = [permissions.IsAuthenticated]


     def create(self, request, *args, **kwargs):
          serializer = self.get_serializer(data=request.data)
          serializer.is_valid(raise_exception=True)
          extra_data = self.perform_create(serializer)
          headers = self.get_success_headers(serializer.data)
          augmented_serializer_data = dict(serializer.data)
          augmented_serializer_data.update(extra_data)
          return Response(augmented_serializer_data, status=status.HTTP_201_CREATED, headers=headers)


     def perform_create(self, serializer):
          obj = serializer.save()
          now = timezone.now()
          json_filter = obj.clients_filter
          if now > obj.start_datetime and now < obj.finish_datetime:
               clients_qs = Client.objects.none()
               if 'tags' in json_filter:
                    for tag_ in json_filter['tags']:
                         clients_qs = clients_qs.union(Client.objects.filter(tag=tag_))
               if 'mocs' in json_filter:
                    for moc_ in json_filter['mocs']:
                         clients_qs = clients_qs.union(Client.objects.filter(mobile_operator_code=moc_))
     
               clients_ids = list(clients_qs.values_list('id', flat=True))
               data = {'distribution_id': obj.id, 'clients_ids': clients_ids}
               send_msg_now.apply_async(args=(data,), countdown=0)


          elif obj.start_datetime > now:
               delta = obj.start_datetime - now 
               countdown_in_sec = int(delta.total_seconds())
               send_msg_now.apply_async(args=(data,), coutdown=countdown_in_sec)
          
          data.pop('distribution_id', None)
          return data



# -  GET получения общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по статусам
     @action(methods=['GET'], detail=False, url_path='common_msg_stat', url_name='common_msg_stat')
     def common_stat(self, request):
          qs = Distribution.objects.annotate(
                                             total_msg=Count('message'),
                                             delivered_msg=Sum(
                                                  Case(
                                                       When(message__delivery_status__isnull=False, then=Value(1)),
                                                       default=Value(0),
                                                       output_field=IntegerField()
                                                  )
                                             ),
                                             undelivered_msg=Sum(
                                                  Case(
                                                       When(message__delivery_status__isnull=True, then=Value(1)),
                                                       default=Value(0),
                                                       output_field=IntegerField()
                                                  )
                                             )
                                        )

          serializer = CommonStatSerializer(qs, many=True)
          for qs_dist, serializer_dist in zip(qs, serializer.data):
               if qs_dist.id == serializer_dist['id']:
                    d = {"messages": {'delivered': qs_dist.delivered_msg, 'undelivered': qs_dist.undelivered_msg}}
                    serializer_dist.update(d)

          return Response(serializer.data)


class MessageViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
     queryset = Message.objects.all()
     serializer_class = MessageSerializer
     permission_classes = [permissions.IsAuthenticated]

     # -  GET получения детальной статистики отправленных сообщений по конкретной рассылке
     @action(methods=['GET'], detail=True, url_path='msg_stat_by_dist', url_name='message_stat_by_detail_distrib')
     def detail_message_stat(self, request, pk):
          try:
               Distribution.objects.get(pk=pk)
               queryset = Message.objects.filter(distribution=pk)
          except Distribution.DoesNotExist:
               return Response('Distribution with id={} does not exists'.format(pk))
          serializer = MessageSerializer(queryset, many=True)
          return Response(serializer.data)




# Create your views here.
    # select ad.*, count(am.id) as total_msg, sum(am.delivery_status::int) as delivered_msg, (count(am.id) - sum(am.delivery_status::int)) as undelivered_msg 
          # from api_distribution ad left join api_message am 
          # on am.distribution_id_id = ad.id 
          # group by ad.id 
          # ;