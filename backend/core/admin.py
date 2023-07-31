from django.contrib import admin
from .models import Cake, AboutUs


@admin.register(Cake)
class CakeAdmin(admin.ModelAdmin):
    pass


@admin.register(AboutUs)
class CakeAdmin(admin.ModelAdmin):
    pass
