from django.http import HttpResponse
from django.template import loader
from .models import Category, Event


def index(request):
    category_set = Category.objects.all()
    event_set = Event.objects.all()
    template = loader.get_template('main/index.html')
    context = {
        'category_set': category_set,
        'event_set': event_set,
    }
    return HttpResponse(template.render(context, request))


def more(request, event_id):
    response = "You're looking at the more types of event %s."
    return HttpResponse(response % event_id)


def my_coupons(request):
    response = "Here you can find your active and old coupons"
    return HttpResponse(response)
