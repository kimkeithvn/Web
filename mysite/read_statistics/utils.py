import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadCount, ReadDetail


def read_statisitcs_once_read(request, object):
    content_type = ContentType.objects.get_for_model(object)
    key = '%s_%s_read' % (content_type.model, object.pk)

    if not request.COOKIES.get(key):
        # 获取对应总阅读记录，如果不存在，则创建；如果存在，则+1
        readcount, created = ReadCount.objects.get_or_create(content_type=content_type, object_id=object.pk)
        readcount.read_count += 1
        readcount.save()

        # 获取当天阅读数，如果不存在，则创建；如果存在，则+1
        date = timezone.now().date()
        readdetail, created = ReadDetail.objects.get_or_create(content_type=content_type, object_id=object.pk, date=date)
        readdetail.read_count += 1
        readdetail.save()
    return key


def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    dates = []
    read_counts = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_count_sum=Sum('read_count'))
        read_counts.append(result['read_count_sum'] or 0)
    return dates, read_counts


'''def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_count')
    return read_details[:7]

def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_count')
    return read_details[:7]'''

