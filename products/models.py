from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from channels import Group


class Product(models.Model):
    name = models.CharField(max_length=140)

    def __str__(self):
        return f'{self.name}'


@receiver(post_save, sender=Product)
def send_update(sender, instance, created, *args, **kwargs):
    uuid = str(instance.id)
    if created:
        Group("gqp.product-add").send({'added': True})
        return
    print("Message sent to channel", 'gqp.product-updated.{0}'.format(uuid))
    Group('gqp.product-updated.{0}'.format(uuid))\
        .send({'text': "Updated"})
