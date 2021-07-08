from random import randint

from django.utils import timezone

from .models import Event, Wallet, Coupon


def resultRandomizer():
    print('resultRandomizer()')
    event_set = Event.objects.filter(is_settled=False)

    for event in event_set:
        if event.end_datetime <= timezone.now():

            for bet in event.types:
                winning_type = randint(1, len(bet['possibilities']))

                for type in bet['possibilities']:
                    if type['id'] == winning_type:
                        winning_type = type['type']

                bet['correct_types'].append(winning_type)
                event.is_settled = True

            event.save()

    couponChecker()


def couponChecker():
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
