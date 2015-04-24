# -*- coding: utf-8 -*-
from django.conf import settings
from django.db.models.signals import post_save
from .models import Customer, Transaction
from templated_email import send_templated_mail


def post_save_receiver(signal, sender, instance, **kwargs):
    """
    Create an account for every user that is register
    """
    if kwargs.get('created'):
        customer = Customer()
        customer.user = instance
        customer.save()

post_save.connect(post_save_receiver, sender=settings.AUTH_USER_MODEL)


def post_save_transaction(signal, instance, **kwargs):
    send_templated_mail(
        template_name='send_heart',
        from_email=settings.FROM_EMAIL,
        recipient_list=[instance.receiver.user.email],
        context={
            'transaction': instance
        })

post_save.connect(post_save_transaction, sender=Transaction)
