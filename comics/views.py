import json
from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.http import HttpRequest, Http404, HttpResponse
from django.shortcuts import render, redirect

from .forms import ComicForm, ChapterForm, ChapterImageForm
from .models import Comic, Chapter, Rating, Like, Genre, Library, BuyList
from users.models import User


def index(request: HttpRequest) -> HttpResponse:
    latest_chapters = Chapter.objects.order_by('-pub_date')
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

    context = {
        'latest_updates': latest_updates,
        'next': paginator.get_page(page).has_next(),
        'prev': paginator.get_page(page).has_previous(),
        'next_page': page + 1,
        'prev_page': page - 1,
    }

    return render(request, 'comics/index.html', context)


def comics_list(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        name = request.GET.get('p')
        genres = request.GET.getlist('g')
        status = request.GET.get('s')
        order_by = request.GET.get('o')
        try:
            page = int(request.GET.get('page'))
        except (ValueError, TypeError):
            page = 1

        if name:
            comics = Comic.objects.filter(title__contains=name)
        elif genres:
            comics = Comic.objects.filter(genre__in=genres).distinct()
        elif status:
            comics = Comic.objects.filter(status=status)
        else:
            comics = Comic.objects.all()

        if order_by == 'rating_up':
            comics = comics.order_by('-rating')
        elif order_by == 'rating_down':
            comics = comics.order_by('rating')
        elif order_by == 'alpha_up':
            comics = comics.order_by('title')
        elif order_by == 'alpha_down':
            comics = comics.order_by('-title')
        elif order_by == 'views_up':
            comics = comics.order_by('-watches')
        elif order_by == 'views_down':
            comics = comics.order_by('watches')

        comics_page = Paginator(comics, 10)

        context = {
            'comics': comics_page.get_page(page).object_list,
            'next': comics_page.get_page(page).has_next(),
            'next_page': page + 1,
            'prev': comics_page.get_page(page).has_previous(),
            'prev_page': page - 1,
            'genres': Genre.objects.all(),
            'status': Comic.STATUS,
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


@login_required(login_url='users:login')
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


@login_required(login_url='users:login')
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

    if chapter.comic.creator_id != user.id:
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

    images = chapter.chapterimage_set.order_by('image')

    chapter_list = comic.chapter_set.all()

    prev_chapter = None
    next_chapter = None
    if chapter.chapter_num > 0:
        try:
            prev_chapter = comic.chapter_set.get(chapter_num=(chapter.chapter_num - 1))
        except Chapter.DoesNotExist:
            pass

    if chapter.chapter_num < chapter_list.count() - 1:
        try:
            next_chapter = comic.chapter_set.get(chapter_num=(chapter.chapter_num + 1))
        except Chapter.DoesNotExist:
            pass

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


@login_required(login_url='users:login')
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


@login_required(login_url='users:login')
@permission_required('comics.delete_comic')
def delete_comic(request: HttpRequest, comic_id: int) -> HttpResponse:
    if request.method == 'DELETE':
        user = User.objects.get(pk=request.user.id)

        try:
            comic = user.comic_set.get(pk=comic_id)
        except Comic.DoesNotExist:
            return HttpResponse('You cannot delete this comic', status=403)

        comic.delete()
        return HttpResponse('Comic deleted successfully', status=200)


@login_required(login_url='users:login')
@permission_required('comics.delete_chapter')
def delete_chapter(request: HttpRequest, chapter_id: int) -> HttpResponse:
    if request.method == 'DELETE':
        user = User.objects.get(pk=request.user.id)
        chapter = Chapter.objects.get(pk=chapter_id)

        if chapter.comic.creator_id != user.id:
            return HttpResponse('You cannot delete this chapter', status=403)

        chapter.delete()
        return HttpResponse('Chapter deleted successfully', status=200)


@login_required(login_url='users:login')
@permission_required('comics.add_comic')
def new_comic(request: HttpRequest) -> HttpResponse:
    user = User.objects.get(pk=request.user.id)

    if request.method == 'GET':
        form = ComicForm()
        return render(request, 'comics/new_comic.html', {'form': form})

    if request.method == 'POST':
        form = ComicForm(request.POST, request.FILES)
        if form.is_valid():
            comic = user.comic_set.create(
                title=form.cleaned_data['title'],
                summary=form.cleaned_data['summary'],
                cover=form.cleaned_data['cover'],
                creator=user
            )
            comic.genre.set(form.cleaned_data['genres'])
            comic.save()

            return redirect('comics:comic_detail', comic_id=comic.id)
        else:
            return render(request, 'comics/new_comic.html', {'form': form})


@login_required(login_url='users:login')
@permission_required('comics.add_chapter')
def new_chapter(request: HttpRequest, comic_id: int) -> HttpResponse:
    comic = Comic.objects.get(pk=comic_id)
    user = User.objects.get(pk=request.user.id)

    if user.id != comic.creator_id:
        return HttpResponse('You cannot add a chapter to this comic', status=403)

    if request.method == 'GET':
        ch_form = ChapterForm()
        img_form = ChapterImageForm()
        context = {
            'ch_form': ch_form,
            'img_form': img_form,
            'comic': comic
        }
        return render(request, 'comics/new_chapter.html', context)

    if request.method == 'POST':
        # print(request.FILES, request.POST)
        ch_form = ChapterForm(request.POST)
        img_form = ChapterImageForm(request.POST, request.FILES)
        images = request.FILES.getlist('images')
        if ch_form.is_valid() and img_form.is_valid():
            chapter = comic.chapter_set.create(
                chapter_num=ch_form.cleaned_data['chapter_number'],
            )
            for image in images:
                chapter.chapterimage_set.create(
                    image=image
                )
            return redirect('comics:comic_detail', comic_id=comic.id)
        else:
            context = {
                'ch_form': ch_form,
                'img_form': img_form,
                'comic': comic
            }
            return render(request, 'comics/new_chapter.html', context)

    return render(request, 'comics/new_chapter.html')


@login_required(login_url='users:login')
@permission_required('comics.modify_comic')
def change_comic_status(request: HttpRequest, comic_id: int, status_id: str) -> HttpResponse:
    if request.method == 'PUT':
        user = User.objects.get(pk=request.user.id)
        comic = Comic.objects.get(pk=comic_id)

        if user.id != comic.creator_id:
            return HttpResponse('You cannot change the status of this comic', status=403)

        comic.status = status_id
        comic.save()

        return HttpResponse('Comic status changed successfully', status=200)


@login_required(login_url='users:login')
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


@login_required(login_url='users:login')
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


@login_required(login_url='users:login')
def delete_history_entry(request: HttpRequest, entry_id: int) -> HttpResponse:
    if request.method == 'DELETE':
        user = User.objects.get(pk=request.user.id)
        user.readhistory_set.get(pk=entry_id).delete()
        return HttpResponse(status=200)
