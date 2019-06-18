from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from .forms import CommentForm


def submit_comment(request):
    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}  # 返回数据字典
    if comment_form.is_valid():
        # 检查通过，保存数据
        comment = Comment()
        comment.comment_user = comment_form.cleaned_data['user']
        comment.comment_text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if parent is not None:
            comment.root = parent.root if parent.root is not None else parent
            comment.parent = parent
            comment.reply_to = parent.comment_user
        comment.save()

        # 发送邮件通知
        comment.send_mail()

        # 返回数据
        data['states'] = 'SUCCESS'
        data['comment_user'] = comment.comment_user.get_nickname_or_username()
        data['comment_time'] = comment.comment_time.timestamp()
        data['comment_text'] = comment.comment_text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        data['reply_to'] = comment.reply_to.get_nickname_or_username() if parent is not None else ''
        data['root_pk'] = comment.root.pk if comment.root is not None else ''
        data['pk'] = comment.pk
    else:
        data['states'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
        # return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
    return JsonResponse(data)

