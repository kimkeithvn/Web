import threading
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


# 多线程
class SendMail(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject,
                  '',
                  settings.EMAIL_HOST_USER,
                  [self.email],
                  fail_silently=self.fail_silently,
                  html_message=self.text)


class Comment(models.Model):
    # User中的related_name作用： 反向寻找指定（用户）的所有评论
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    comment_text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_user = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)  # 谁的回复

    # root:记录每条评论的主评论， 用于反向筛选一条评论下所有评论
    root = models.ForeignKey('self', related_name='all_reply', null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='child_reply', null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name='user_reply', null=True, on_delete=models.CASCADE)  # 回复谁

    def send_mail(self):
        # 发送邮件通知
        if self.parent is None:
            # 回复博客
            subject = '新的评论'  # 主题
            email = self.content_object.get_author_email()
        else:
            # 回复评论
            subject = '新的回复'  # 主题
            email = self.reply_to.email
        if email != '':
            context = {}
            context['comment_blog_title'] = self.content_object.title
            context['comment_user'] = self.comment_user
            context['comment_time'] = self.comment_time
            context['comment_text'] = self.comment_text
            context['blog_url'] = self.content_object.get_blog_url()
            text = render_to_string('comment/send_email.html', context)
            sendmail = SendMail(subject, text, email)
            sendmail.start()

    def __str__(self):
        return self.comment_text

    class Meta:
        ordering = ['comment_time']


