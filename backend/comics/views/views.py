from django.shortcuts import render, HttpResponse, Http404
from ..models import Comic, Chapter, User, Library, Rating


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


def series_list(request) -> HttpResponse:
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

    bookmark = None
    rating = None
    if request.user.is_authenticated:
        try:
            bookmark = Library.objects.get(user=request.user.id, comic=comic.id)
        except Library.DoesNotExist:
            ...

        try:
            rating = Rating.objects.get(user=request.user.id, comic=comic.id)
        except Rating.DoesNotExist:
            ...

    context = {
        'comic': comic,
        'author_name': author_name,
        'genres': genres,
        'bookmark': bookmark,
        'rating': rating,
        'ratingRange': range(1, 11)
    }

    return render(request, 'comics/comic.html', context)
