from django.forms import IntegerField
from django.db.models import Count, Sum, Case, When, Value, IntegerField
from rest_framework.response import Response
from rest_framework import viewsets, mixins
from rest_framework import permissions
from rest_framework.decorators import action
from api.models import Client, Distribution, Message
from api.serializers import ClientSerializer, DistributionSerializer, MessageSerializer, CommonStatSerializer


class ClientViewSet(viewsets.ModelViewSet):
     queryset = Client.objects.all()
     serializer_class = ClientSerializer
     permission_classes = [permissions.IsAuthenticated]


class DistributionViewSet(viewsets.ModelViewSet):
     queryset = Distribution.objects.all()
     serializer_class = DistributionSerializer
     permission_classes = [permissions.IsAuthenticated]
       

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
