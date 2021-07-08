import math
from datetime import datetime
from django.utils import timezone
from random import randint

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.template import loader
from rest_framework import viewsets

from .models import Event, Coupon, Wallet
from .serializers import EventsSerializer, CouponsSerializer, UserSerializer, WalletSerializer


def main(request):
    event_set = Event.objects.order_by('start_datetime')
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


def test(request):
    print('couponChecker()')

    def sendPrize(owner, prize):
        wallet = Wallet.objects.get(owner=owner)
        wallet.money += prize
        wallet.save()

    coupons_set = Coupon.objects.filter(is_active=True)

    for coupon in coupons_set:
        bets_count = len(coupon.types)
        correct_types_counter = 0
        settled_events_counter = 0

        for bet in coupon.types:
            event = Event.objects.get(id=bet['event_id'])
            if event.is_settled == False:
                break

            for type in event.types:
                if type['id'] == bet['type_id']:
                    if bet['type'] in type['correct_types']:
                        correct_types_counter += 1
                    break
            settled_events_counter += 1

        if settled_events_counter >= bets_count:
            coupon.is_active = False

            if correct_types_counter >= bets_count:
                coupon.is_winning = True
                sendPrize(coupon.author, coupon.prize)

        coupon.save()
    return HttpResponse("chyba dziala")


def top_up_wallet(request):

    if request.user.is_authenticated:
        template = loader.get_template('main/top_up_wallet.html')
        context = {}
        return HttpResponse(template.render(context, request))

    else:
        return HttpResponseNotFound('<h1>Page was found</h1>')


def my_coupons(request):

    if request.user.is_authenticated:
        template = loader.get_template('main/my_coupons.html')
        coupons_set = Coupon.objects.get_queryset()
        my_coupons_set = coupons_set.filter(author=request.user)
        context = {"my_coupons_set": my_coupons_set}
        return HttpResponse(template.render(context, request))

    else:
        return HttpResponseNotFound('<h1>Page was found</h1>')


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('start_datetime')
    serializer_class = EventsSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer


class CouponsViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all().order_by('id')
    serializer_class = CouponsSerializer

    def perform_create(self, serializer):
        factor = 1;
        for bet in serializer.validated_data['types']:
            event = Event.objects.get(id=bet['event_id'])
            for type in event.types:
                if type['id'] == bet['type_id']:
                    for possibility in type['possibilities']:
                        if bet['type'] == possibility['type']:
                            factor = factor * possibility['odds']
                            break

                    break

        factor = round(factor, 2)
        prize = serializer.validated_data['contribution'] * factor
        prize = round(prize, 2)

        serializer.save(author=self.request.user, odds=factor, prize=prize)


class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def get_queryset(self):
        queryset = self.queryset
        query_set = queryset.filter(owner=self.request.user)
        return query_set

    def get_object(self):
        return get_object_or_404(Wallet, owner=self.request.user)

    def perform_update(self, serializer):
        wallet = Wallet.objects.get(owner=self.request.user)
        print(serializer.validated_data['money'])
        sum = wallet.money + serializer.validated_data['money']
        serializer.save(money=sum)


@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(owner=instance)
