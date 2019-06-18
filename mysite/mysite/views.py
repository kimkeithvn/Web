import datetime
from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum, Count
from django.utils import timezone
from django.core.cache import cache
from blog.models import Blog
from read_statistics.utils import get_seven_days_read_data


def get_today_hot_blogs():
    today = timezone.now().date()
    blogs = Blog.objects \
                .filter(read_details__date=today) \
                .values('id', 'title', read_count=Count('read_details__read_count')) \
                .order_by('-read_count')
    return blogs[:7]


def get_yesterday_hot_blogs():
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    blogs = Blog.objects \
                .filter(read_details__date=yesterday) \
                .values('id', 'title', read_count=Count('read_details__read_count')) \
                .order_by('-read_count')
    return blogs[:7]


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
                .filter(read_details__date__lt=today, read_details__date__gte=date) \
                .values('id', 'title') \
                .annotate(read_count_sum=Sum('read_details__read_count')) \
                .order_by('-read_count_sum')
    return blogs[:7]


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_counts = get_seven_days_read_data(blog_content_type)

    # 获取7天热门博客缓存数据
    hot_blogs_for_7_days = cache.get('hot_blogs_for_7_days')
    if not hot_blogs_for_7_days:
        hot_blogs_for_7_days = get_7_days_hot_blogs()
        cache.set('hot_blogs_for_7_days', hot_blogs_for_7_days, 3600)

    context = {}
    context['dates'] = dates
    context['read_counts'] = read_counts
    context['today_hot_data'] = get_today_hot_blogs()
    context['yesterday_hot_data'] = get_yesterday_hot_blogs()
    context['hot_blogs_for_7_days'] = get_7_days_hot_blogs()
    return render(request, 'home.html', context)


