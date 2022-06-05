from datetime import datetime
import json

from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404, HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import UserForm
from .models import Comic, Chapter, User, Library, Rating, BuyList, ChapterImage, Like, Comment, CoinsPurchase, ReadHistory


def index(request: HttpRequest) -> HttpResponse:
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


# TODO: finish this
def comics_list(request: HttpRequest) -> HttpResponse:
    comics = None
    try:
        for key, param in request.GET.lists():
            if key == 'g':
                comics = Comic.objects.filter(genre__in=param)
            elif key == 'name':
                comics = Comic.objects.get(title__contains=param)
            else:
                comics = Comic.objects.all()
    except Comic.DoesNotExist:
        ...

    if comics:
        comics = set(comics)

    print(comics)
    context = {
        'comics': comics
    }

    return render(request, 'comics/series.html', context)


def comic_details(request: HttpRequest, comic_id: int) -> HttpResponse:
    try:
        comic = Comic.objects.get(pk=comic_id)
    except Comic.DoesNotExist:
        raise Http404("Comic does not exist")

    try:
        author_name = User.objects.get(pk=comic.creator_id).username
    except User.DoesNotExist:
        author_name = "Unknown"

    genres = comic.genre.all()[:4]

    chapters = comic.chapter_set.order_by('chapter_num')

    bookmark = None
    rating = None
    buy_list = None
    if request.user.is_authenticated:
        user = User.objects.get(pk=request.user.id)

        try:
            bookmark = user.library_set.get(comic=comic)
        except Library.DoesNotExist:
            ...

        try:
            rating = user.rating_set.get(comic=comic)
        except Rating.DoesNotExist:
            ...

        bought = user.buylist_set.filter(chapter__comic_id=comic)
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
def bookmark_comic(request: HttpRequest, comic_id: int) -> HttpResponse:
    user = User.objects.get(pk=request.user.id)
    comic = Comic.objects.get(pk=comic_id)
    if request.method == 'POST':
        user.library_set.create(comic=comic)
        comic.follows += 1
        comic.save()

        return HttpResponse(status=200)

    elif request.method == 'DELETE':
        library = user.library_set.get(comic=comic)
        library.delete()
        comic.follows -= 1
        comic.save()

        return HttpResponse(status=200)
    return HttpResponse(status=403)


@login_required(login_url='comics:login')
def rate_comic(request: HttpRequest, comic_id: int, rating: int) -> HttpResponse:
    user = User.objects.get(pk=request.user.id)
    comic = Comic.objects.get(pk=comic_id)

    if request.method == 'POST':
        user.rating_set.create(comic=comic, rating=rating)

    elif request.method == 'PUT':
        rating_obj = user.rating_set.get(comic=comic)
        rating_obj.rating = rating
        rating_obj.save()

    elif request.method == 'DELETE':
        rating_obj = user.rating_set.get(comic=comic)
        rating_obj.delete()

    else:
        return HttpResponse(status=403)

    comic_ratings = comic.user_rating.all()
    values = list(comic_ratings.values('rating'))
    val_list = [x['rating'] for x in values]
    if val_list:
        avg_rating = sum(val_list) / len(val_list)
        comic.rating = avg_rating
    else:
        comic.rating = 0
    comic.save()
    return HttpResponse(status=200)


def register(request: HttpRequest) -> HttpResponse:
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
def settings(request):
    ...


@login_required(login_url='comics:login')
def buy_chapter(request: HttpRequest, chapter_id: int) -> HttpResponse:
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)

        try:
            chapter = Chapter.objects.get(pk=chapter_id)
        except Chapter.DoesNotExist:
            raise Http404("Chapter does not exist")

        try:
            user.buylist_set.get(chapter=chapter)
            message = "already bought"
        except BuyList.DoesNotExist:
            if user.coins >= chapter.cost:
                user.coins -= chapter.cost
                user.save()
                user.buylist_set.create(chapter=chapter)
                message = "Successfully bought chapter"
            else:
                message = "Not enough coins"

        context = {
            'message': message,
        }
        return HttpResponse(json.dumps(context), status=200)


@login_required(login_url='comics:login')
def chapter_details(request: HttpRequest, comic_id: int, chapter_id: int) -> Http404 | HttpResponse:
    user = User.objects.get(pk=request.user.id)

    try:
        comic = Comic.objects.get(pk=comic_id)
    except Comic.DoesNotExist:
        return Http404("Comic does not exist")

    try:
        chapter = comic.chapter_set.get(chapter_num=chapter_id)
    except Chapter.DoesNotExist:
        return Http404("Chapter does not exist")

    try:
        user.buylist_set.get(chapter=chapter)
    except BuyList.DoesNotExist:
        return redirect('comics:comic_detail', comic_id)

    comic.watches += 1
    comic.save()

    user_history = user.readhistory_set.get_or_create(chapter=chapter)

    if not user_history[1] and user_history[0].date != datetime.now().date():
        user_history[0].date = datetime.now().date()
        user_history[0].save()

    images = chapter.chapterimage_set.all()

    chapter_list = comic.chapter_set.all()

    prev_chapter = None
    next_chapter = None
    if chapter.chapter_num > 0:
        prev_chapter = comic.chapter_set.get(chapter_num=chapter.chapter_num - 1)

    if chapter.chapter_num < chapter_list.count() - 1:
        next_chapter = comic.chapter_set.get(chapter_num=chapter.chapter_num + 1)

    try:
        like = user.like_set.get(chapter=chapter)
    except Like.DoesNotExist:
        like = None

    comments = chapter.comment_set.all()

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
def like_chapter(request: HttpRequest, chapter_id: int) -> HttpResponse:
    user = User.objects.get(pk=request.user.id)
    chapter = Chapter.objects.get(pk=chapter_id)

    if request.method == 'POST':
        user.like_set.create(chapter=chapter)
        chapter.likes += 1

    elif request.method == 'DELETE':
        like_obj = user.like_set.get(chapter=chapter)
        like_obj.delete()
        chapter.likes -= 1
    else:
        return HttpResponse(status=403)

    chapter.save()
    return HttpResponse(status=200)


@login_required(login_url='comics:login')
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
            comment = user.comment_set.create(chapter=chapter, body=body, reply_to=reply_id)
        else:
            comment = user.comment_set.create(chapter=chapter, body=body)

        return HttpResponse(status=200)


@login_required(login_url='comics:login')
def delete_comment(request: HttpRequest, comment_id: int) -> HttpResponse | Http404:
    if request.method == 'POST':
        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return Http404("Comment does not exist")
        if comment.user_id == request.user.id:
            comment.delete()
            return HttpResponse(status=200)

        return HttpResponse(status=403)


@login_required(login_url='comics:login')
def market(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        try:
            amount = int(request.POST.get('coins_amount'))
        except ValueError:
            message = 'Insert a valid amount of coins'
            return HttpResponse(message, status=400)
        purchase = user.coinspurchase_set.create(coins=amount)
        user.coins += amount
        user.save()

        message = f"Successfully purchased {amount} coins"

        return HttpResponse(message, status=200)
    else:
        return render(request, 'comics/market.html')
