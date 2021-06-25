from django.contrib import admin
from django.db import models
from django_json_widget.widgets import JSONEditorWidget
from .models import Event, Category, Coupon, Wallet

# Register your models here.

admin.site.register(Category)
admin.site.register(Coupon)
admin.site.register(Wallet)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }