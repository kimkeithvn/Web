from django.db import models
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class ReadCount(models.Model):
    read_count = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class ReadCountExpandMethod():
    def get_read_count(self):
        try:
            content_type = ContentType.objects.get_for_model(self)
            readcount = ReadCount.objects.get(content_type=content_type, object_id=self.pk)
            return readcount.read_count
        except exceptions.ObjectDoesNotExist:
            return 0


class ReadDetail(models.Model):
    date = models.DateField(default=timezone.now)
    read_count = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

