from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(listing)
admin.site.register(Bid)
admin.site.register(WatchList)
admin.site.register(Winner)