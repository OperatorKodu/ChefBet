from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Category, Event


def main(request):
    event_set = Event.objects.order_by('datetime')
    template = loader.get_template('main/main.html')
    context = {
        'event_set': event_set,
    }
    return HttpResponse(template.render(context, request))

def more(request, event_id):
    template = loader.get_template('main/more.html')
    event = get_object_or_404(Event, id = event_id)
    context = {
        'event': event,
    }
    return HttpResponse(template.render(context, request))

def category(request, category_name):
    template = loader.get_template('main/category.html')
    event_set = Event.objects.all().filter(category__name = category_name)
    context = {
        'category_name': category_name,
        'event_set': event_set,
    }
    return HttpResponse(template.render(context, request))

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main')
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

def my_coupons(request):
    response = "Here you can find your active and old coupons"
    return HttpResponse(response)

def test(request):
    template = loader.get_template('main/test.html')
    context = {}
    return HttpResponse(template.render(context, request))
