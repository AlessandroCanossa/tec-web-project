from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, Http404

# Create your views here.
from comics.models import Chapter
from users.models import User
from comments.models import Comment


@login_required(login_url='users:login')
def add_comment(request: HttpRequest, chapter_id: int) -> HttpResponse | Http404:
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        try:
            chapter = Chapter.objects.get(pk=chapter_id)
        except Chapter.DoesNotExist:
            return Http404("Chapter does not exist")

        reply_id = request.POST.get('reply_to')
        body = request.POST.get('comment')

        if reply_id:
            user.comment_set.create(
                chapter=chapter, body=body, reply_id=reply_id)
        else:
            user.comment_set.create(chapter=chapter, body=body)

        return HttpResponse(status=200)


@login_required(login_url='users:login')
def delete_comment(request: HttpRequest, comment_id: int) -> HttpResponse | Http404:
    if request.method == 'DELETE':
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Http404("Comment does not exist")
        if comment.user_id == request.user.id:
            comment.delete()
            return HttpResponse(status=200)

        return HttpResponse(status=403)
