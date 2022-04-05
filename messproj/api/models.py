from django.db import models
from django.core.validators import RegexValidator


class Client(models.Model):
     phone_regex = RegexValidator(regex=r'^\d{11}', message="Phone number in the format: '7XXXXXXXXXX'")
     phone_number = models.CharField(validators=[phone_regex], max_length=12, blank=True, verbose_name='номер телефона клиента')
     mobile_operator_code = models.CharField(max_length=3, default=phone_number[1:4], verbose_name='код мобильного оператора')
     tag = models.CharField(max_length=30, blank=True, verbose_name='тег(произвольная метка)')
     import pytz
     TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
     timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC', verbose_name='часовой пояс')


class Distribution(models.Model):
     launch_datetime = models.DateTimeField(null=True, verbose_name='дата и время запуска рассылки')
     delivery_text = models.CharField(max_length=255, verbose_name='')
     client_id = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='distribution_cli_id', verbose_name='') #####!!!!!!!!!!!


class Message(models.Model):
     delivery_datetime = models.DateTimeField(null=True, verbose_name='')
     delivery_status = models.BooleanField(blank=True, default=False, verbose_name='')
     distribution_id = models.ForeignKey(Distribution, on_delete=models.CASCADE, related_name='message_dist_id', verbose_name='')
     client_id = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='message_cli_id', verbose_name='')



# Create your models here.
