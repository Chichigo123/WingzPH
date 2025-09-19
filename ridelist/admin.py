from django.contrib import admin

from ridelist.models import Ride, Ride_Event, User


class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "role")
    ordering = ("first_name", "last_name", "role")

class RideAdmin(admin.ModelAdmin):
    list_display = ("id_rider", "id_driver", "status", "pickup_time")
    ordering = ("-pickup_time", "status")

class Ride_EventAdmin(admin.ModelAdmin):
    list_display = ("id_ride", "description", "created_at")
    ordering = ("id_ride", "created_at")


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Ride, RideAdmin)
admin.site.register(Ride_Event, Ride_EventAdmin)
