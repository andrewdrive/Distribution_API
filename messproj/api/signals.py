from django.db.models.signals import post_save
from django.dispatch import receiver
from api.tasks import send_msg_now
from django.utils import timezone


@receiver(post_save, sender="api.Distribution", dispatch_uid='send_messages_to_clients')
def send_messages(sender, instance, created, **kwargs):
     if created:
          now = timezone.now()
          obj_id = instance.id
          start_datetime = instance.start_datetime
          finish_datetime = instance.finish_datetime
          if now > start_datetime and now < finish_datetime:
               send_msg_now.apply_async(args=(obj_id, ), countdown=0)
          elif start_datetime > now:
               delta = start_datetime - now 
               countdown_in_sec = int(delta.total_seconds())
               send_msg_now.apply_async(args=(obj_id, ), countdown=countdown_in_sec)
