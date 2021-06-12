from django.http import HttpResponse
from django.template import loader
from .models import Category, Event


def index(request):
    category_set = Category.objects.all()
    event_set = Event.objects.order_by('datetime')
    template = loader.get_template('main/index.html')
    context = {
        'category_set': category_set,
        'event_set': event_set,
    }
    return HttpResponse(template.render(context, request))

def subpages(request, page):
    category_set = Category.objects.all()
    event_set = Event.objects.order_by('datetime')
    template = loader.get_template('main/index.html')
    context = {
        'category_set': category_set,
        'event_set': event_set,
        'page': page,
    }
    return HttpResponse(template.render(context, request))

def more(request, event_id):
    category_set = Category.objects.all()
    event = Event.objects.get(id = event_id)
    template = loader.get_template('main/index.html')
    page = 'more'
    context = {
        'category_set': category_set,
        'event': event,
        'page': page,
    }
    return HttpResponse(template.render(context, request))


def my_coupons(request):
    response = "Here you can find your active and old coupons"
    return HttpResponse(response)
