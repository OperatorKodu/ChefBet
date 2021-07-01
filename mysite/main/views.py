from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template import loader
from rest_framework import viewsets

from .models import Event, Coupon, Wallet
from .serializers import EventsSerializer, CouponsSerializer, UserSerializer, WalletSerializer


def main(request):
    event_set = Event.objects.order_by('datetime')
    template = loader.get_template('main/main.html')
    context = {
        'event_set': event_set,
    }
    return HttpResponse(template.render(context, request))


def more(request, event_id):
    template = loader.get_template('main/more.html')
    event = get_object_or_404(Event, id=event_id)
    context = {
        'event': event,
    }
    return HttpResponse(template.render(context, request))


def category(request, category_name):
    template = loader.get_template('main/category.html')
    event_set = Event.objects.all().filter(category__name=category_name)
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
    event_set = Event.objects.order_by('datetime')
    template = loader.get_template('main/test.html')
    context = {
        'event_set': event_set,
    }
    return HttpResponse(template.render(context, request))


def top_up_wallet(request):
    template = loader.get_template('main/top_up_wallet.html')
    context = {}
    return HttpResponse(template.render(context, request))


def my_coupons(request):
    template = loader.get_template('main/my_coupons.html')
    coupons_set = Coupon.objects.get_queryset()
    my_coupons_set = coupons_set.filter(author=request.user)
    context = {"my_coupons_set": my_coupons_set}
    return HttpResponse(template.render(context, request))


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('datetime')
    serializer_class = EventsSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


class CouponsViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all().order_by('id')
    serializer_class = CouponsSerializer


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(owner=self.request.user)
        return query_set

    def get_object(self):
        return get_object_or_404(Wallet, owner=self.request.user)


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(owner=instance)
