from datetime import datetime
import json

from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .forms import UserForm
from .models import Comic, Chapter, User, Library, Rating, BuyList, ChapterImage, Like, Comment, CoinsPurchase, ReadHistory


def index(request: HttpRequest) -> HttpResponse:
    latest_chapters = Chapter.objects.order_by('-pub_date')
    # latest_chapters = set(latest_chapters)
    paginator = Paginator(latest_chapters, 10)
    latest_updates = []

    try:
        page = int(request.GET.get('page'))
    except (ValueError, TypeError):
        page = 1

    for chapter in paginator.get_page(page).object_list:
        comic = Comic.objects.get(pk=chapter.comic.id)
        latest_updates.append(comic)

    latest_updates = set(latest_updates)

    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < paginator.num_pages else None

    context = {
        'latest_updates': latest_updates,
        'pages': range(1, paginator.num_pages + 1),
        'current_page': page,
        'next_page': next_page,
        'prev_page': prev_page,
        'max_pages': paginator.num_pages
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
def settings(request: HttpRequest) -> HttpResponse:
    user = User.objects.get(pk=request.user.id)

    if request.method == 'GET':
        library = user.library_set.all()

        comments = user.comment_set.order_by('-created_on')

        history = user.readhistory_set.order_by('-date')

        buy_list = user.buylist_set.order_by('-date')

        my_comics = user.comic_set.all()

        context = {
            'lib_comics': library,
            'comments': comments,
            'history': history,
            'buy_list': buy_list,
            'my_comics': my_comics
        }

        return render(request, 'comics/settings.html', context)


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
        prev_chapter = comic.chapter_set.get(chapter_num=(chapter.chapter_num - 1))

    if chapter.chapter_num < chapter_list.count() - 1:
        next_chapter = comic.chapter_set.get(chapter_num=(chapter.chapter_num + 1))

    print(prev_chapter, next_chapter)

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
            user.comment_set.create(chapter=chapter, body=body, reply_id=reply_id)
        else:
            user.comment_set.create(chapter=chapter, body=body)

        return HttpResponse(status=200)


@login_required(login_url='comics:login')
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


@login_required(login_url='comics:login')
def market(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        try:
            amount = int(request.POST.get('coins_amount'))
        except ValueError:
            message = 'Insert a valid amount of coins'
            return HttpResponse(message, status=400)
        user.coinspurchase_set.create(coins=amount)
        user.coins += amount
        user.save()

        message = f"Successfully purchased {amount} coins"

        return HttpResponse(message, status=200)
    else:
        return render(request, 'comics/market.html')


@login_required(login_url='comics:login')
def delete_history_entry(request: HttpRequest, entry_id: int) -> HttpResponse:
    if request.method == 'DELETE':
        user = User.objects.get(pk=request.user.id)
        user.readhistory_set.get(pk=entry_id).delete()
        return HttpResponse(status=200)


@login_required(login_url='comics:login')
def change_username(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        try:
            new_username = request.POST.get('username')
            print(new_username)
            if new_username:
                user.username = new_username
                user.save()
            else:
                return HttpResponse('Invalid username', status=400)
        except IntegrityError:
            return HttpResponse('Username already taken', status=400)

        return HttpResponse('Username changed successfully', status=200)


@login_required(login_url='comics:login')
def change_password(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        old_password: str = request.POST.get('old_password')
        new_password: str = request.POST.get('new_password')
        confirm_password: str = request.POST.get('confirm_password')

        print(old_password, new_password, confirm_password)

        if not user.check_password(old_password):
            return HttpResponse('Invalid old password', status=400)

        if new_password != confirm_password:
            return HttpResponse('Passwords do not match', status=400)

        if new_password == old_password:
            return HttpResponse('New password must be different from old password', status=400)

        user.set_password(new_password)
        user.save()

        return HttpResponse('Password changed successfully', status=200)


@login_required(login_url='comics:login')
def become_creator(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        user = User.objects.get(pk=request.user.id)
        user.is_creator = True
        user.save()
        return HttpResponse('You are now a creator', status=200)


@login_required(login_url='comics:login')
def delete_comic(request: HttpRequest, comic_id: int) -> HttpResponse:
    if request.method == 'DELETE':
        user = User.objects.get(pk=request.user.id)

        try:
            comic = user.comic_set.get(pk=comic_id)
        except Comic.DoesNotExist:
            return HttpResponse('You cannot delete this comic', status=403)

        comic.delete()
        return HttpResponse('Comic deleted successfully', status=200)
