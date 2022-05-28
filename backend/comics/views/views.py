from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from ..models import Comic, Chapter


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
