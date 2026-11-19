from django.shortcuts import render
from .models import SchoolInfo, News, Gallery


def home(request):
    school = SchoolInfo.objects.first()
    news = News.objects.all()[:6]
    gallery = Gallery.objects.all()[:8]

    return render(request, 'index.html', {
        'school': school,
        'news': news,
        'gallery': gallery,
    })