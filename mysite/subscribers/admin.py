from pyexpat import model
from django.contrib import admin

from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register
)
from .models import Subscriber

class SubscriberAdmin(ModelAdmin):
    """Subscriber admin."""

    model = Subscriber
    menu_label = "Subscriber    "
    menu_icon = "placeholder"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ("email", "name", )
    search_fields = ("email", "name", )

modeladmin_register(SubscriberAdmin)

