from django.shortcuts import render, HttpResponse, Http404, redirect
from django.http import HttpRequest
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView

from ..forms import UserForm
from ..models import Comic, Chapter, User, Library, Rating, BuyList, ChapterImage, Like, Comment
import json


def index(request) -> HttpResponse:
    latest_chapters = Chapter.objects.order_by('-pub_date')[:10]
    latest_chapters = tuple(latest_chapters)
    latest_updates = []

    for chapter in latest_chapters:
        comic = Comic.objects.get(pk=chapter.comic.id)
        latest_updates.append(comic)

    latest_updates = set(latest_updates)
    context = {
        'latest_updates': latest_updates
    }

    return render(request, 'comics/index.html', context)


def comics_list(request) -> HttpResponse:
    comics = None
    try:
        for key, param in request.GET.lists():
            if key == 'g':
                comics = Comic.objects.filter(genre__in=param)
            elif key == 'name':
                comics = Comic.objects.get(title__contains=param)
    except Comic.DoesNotExist:
        ...

    if comics:
        comics = set(comics)

    print(comics)
    context = {
        'comics': comics
    }

    return render(request, 'comics/series.html', context)


def comic_details(request, comic_id) -> HttpResponse:
    try:
        comic = Comic.objects.get(pk=comic_id)
    except Comic.DoesNotExist:
        raise Http404("Comic does not exist")

    try:
        author_name = User.objects.get(pk=comic.creator_id).username
    except User.DoesNotExist:
        author_name = "Unknown"

    genres = comic.genre.all()[:4]

    chapters = Chapter.objects.filter(comic=comic_id).order_by('chapter_num')

    bookmark = None
    rating = None
    buy_list = None
    if request.user.is_authenticated:
        try:
            bookmark = Library.objects.get(user=request.user.id, comic=comic.id)
        except Library.DoesNotExist:
            ...

        try:
            rating = Rating.objects.get(user=request.user.id, comic=comic.id)
        except Rating.DoesNotExist:
            ...

        bought = BuyList.objects.filter(user=request.user.id, chapter__comic_id=comic.id)
        if bought:
            buy_list = [chapter.chapter_id for chapter in bought]

    context = {
        'comic': comic,
        'author_name': author_name,
        'genres': genres,
        'bookmark': bookmark,
        'rating': rating,
        'ratingRange': range(1, 11),
        'chapters': chapters,
        'buy_list': buy_list
    }

    return render(request, 'comics/comic.html', context)


@login_required(login_url='comics:login')
def add_bookmark(request: HttpRequest, comic_id: int) -> HttpResponse:
    if request.method == 'POST':
        user_id = request.user.id
        comic = Comic.objects.get(pk=comic_id)

        try:
            library = Library.objects.get(user=user_id, comic=comic_id)
            library.delete()
            comic.follows -= 1
        except Library.DoesNotExist:
            library = Library.objects.create(user_id=user_id, comic_id=comic_id)
            comic.follows += 1

        comic.save()

        return HttpResponse(comic.follows, status=200)
    return HttpResponse(status=403)


@login_required(login_url='comics:login')
def add_rating(request, comic_id, rating) -> HttpResponse:
    if request.method == 'POST':
        user_id = request.user.id
        comic = Comic.objects.get(pk=comic_id)

        message = ""
        try:
            rating_obj = Rating.objects.get(user_id=user_id, comic=comic)
            if rating == 0:
                rating_obj.delete()
                message = "d"
            else:
                rating_obj.rating = rating
                rating_obj.save()
                message = "u"

        except Rating.DoesNotExist:
            rating_obj = Rating.objects.create(user_id=user_id, comic=comic, rating=rating)
            message = "a"

        comic_ratings = Rating.objects.filter(comic=comic_id)
        values = list(comic_ratings.values('rating'))
        val_list = [x['rating'] for x in values]
        if val_list:
            avg_rating = sum(val_list) / len(val_list)
            comic.rating = avg_rating
        else:
            comic.rating = 0
        comic.save()

        data = {
            'message': message,
            'rating': comic.rating
        }

        return HttpResponse(json.dumps(data), status=200)
    return HttpResponse(status=403)


def register(request):
    if request.method == 'GET':
        form = UserForm()
        context = {
            'form': form
        }
        return render(request, 'registration/signup.html', context)

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('comics:login')
        else:
            context = {
                'form': form,
            }
            return render(request, 'registration/signup.html', context)


@login_required(login_url='comics:login')
def profile(request):
    ...


def user_details(request, user_id):
    ...


@login_required(login_url='comics:login')
def settings(request):
    ...


@login_required(login_url='comics:login')
def logout(request):
    ...


@login_required(login_url='comics:login')
def buy_chapter(request, chapter_id):
    ...


@login_required(login_url='comics:login')
def chapter_details(request, comic_id, chapter_id):
    try:
        chapter = Chapter.objects.get(comic_id=comic_id, chapter_num=chapter_id)
    except Chapter.DoesNotExist:
        return Http404("Chapter does not exist")

    images = ChapterImage.objects.filter(chapter=chapter)

    chapter_list = Chapter.objects.filter(comic_id=comic_id)

    prev_chapter = None
    next_chapter = None
    if chapter.chapter_num > 0:
        prev_chapter = Chapter.objects.get(comic_id=comic_id, chapter_num=chapter.chapter_num - 1)

    if chapter.chapter_num < chapter_list.count() - 1:
        next_chapter = Chapter.objects.get(comic_id=comic_id, chapter_num=chapter.chapter_num + 1)

    like = None
    try:
        like = Like.objects.get(user_id=request.user.id, chapter=chapter)
    except Like.DoesNotExist:
        ...

    comments = Comment.objects.filter(chapter=chapter)

    context = {
        'chapter': chapter,
        'images': images,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,
        'chapter_list': chapter_list,
        'like': like,
        'comments': comments
    }

    return render(request, 'comics/chapter.html', context)


@login_required(login_url='comics:login')
def like_chapter(request, chapter_id):
    if request.method == 'POST':
        user_id = request.user.id
        chapter = Chapter.objects.get(pk=chapter_id)

        try:
            chapter_like = Like.objects.get(user_id=user_id, chapter_id=chapter_id)
            chapter_like.delete()
            chapter.likes -= 1
        except Like.DoesNotExist:
            chapter_like = Like.objects.create(user_id=user_id, chapter_id=chapter_id)
            chapter.likes += 1

        chapter.save()

        return HttpResponse(chapter.likes, status=200)


@login_required(login_url='comics:login')
def add_comment(request, chapter_id):
    if request.method == 'POST':
        user_id = request.user.id
        try:
            chapter = Chapter.objects.get(pk=chapter_id)
        except Chapter.DoesNotExist:
            return Http404("Chapter does not exist")

        reply_id = request.POST.get('reply_to')
        body = request.POST.get('comment')

        if reply_id:
            comment = Comment.objects.create(user_id=user_id, chapter=chapter, reply_id=reply_id, body=body)
        else:
            comment = Comment.objects.create(user_id=user_id, chapter=chapter, body=body)

        return HttpResponse(status=200)


@login_required(login_url='comics:login')
def delete_comment(request, comment_id):
    if request.method == 'POST':

        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Http404("Comment does not exist")
        if comment.user_id == request.user.id:
            comment.delete()
            return HttpResponse(status=200)

        return HttpResponse(status=403)
