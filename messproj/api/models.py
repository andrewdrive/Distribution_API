import pytz
from django.db import models
from django.core.validators import RegexValidator


TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class Client(models.Model):
     phone_regex = RegexValidator(regex=r'^\d{11}', message="Phone number in the format: '7XXXXXXXXXX'")
     phone_number = models.CharField(validators=[phone_regex], max_length=12, blank=True, verbose_name='номер телефона клиента')
     mobile_operator_code = models.CharField(max_length=3, default='000', verbose_name='код мобильного оператора')
     tag = models.CharField(max_length=30, blank=True, verbose_name='тег(произвольная метка)')
     timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC', verbose_name='часовой пояс')

     class Meta:
          ordering = ['phone_number']

     def __str__(self):
          return str((self.mobile_operator_code, self.tag))
     
     def save(self, *args, **kwargs):
          self.mobile_operator_code = self.phone_number[1:4]
          super(Client, self).save(*args, **kwargs)


class Distribution(models.Model):
     start_datetime = models.DateTimeField(null=True, verbose_name='дата и время запуска рассылки')
     finish_datetime = models.DateTimeField(null=True, verbose_name='дата и время окончания рассылки')
     delivery_text = models.CharField(max_length=255, verbose_name='текст сообщения для доставки клиенту')
     clients = models.ManyToManyField(Client, related_name='distribution_cli_filter', verbose_name="""фильтр \
                                        свойств клиентов, на которых должна быть произведена рассылка(код мобильного оператора, тег)""")
     
     class Meta:
          ordering = ['start_datetime']

     def __str__(self):
          return self.delivery_text


class Message(models.Model):
     distribution_id = models.ForeignKey(Distribution, on_delete=models.CASCADE, related_name='message_dist_id', verbose_name='id рассылки, в рамках которой было отправлено сообщение')
     client_id = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='message_cli_id', verbose_name='id клиента, которому отправили')
     delivery_datetime = models.DateTimeField(null=True, verbose_name='дата и время создания(отправки)')
     delivery_status = models.BooleanField(blank=True, default=False, verbose_name='статус отправки')
   
     class Meta:
          ordering = ['delivery_datetime']

     def __str__(self):
          return str(self.delivery_datetime)


# Create your models here.
