from django.contrib import admin
from .models import Profile, SensorData

admin.site.register(Profile)


class SensorDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'number','date1', 'date2', 'interval', 'temp1', 'temp2')

    list_filter = ("name",)
    search_fields = ['name', 'date1', 'date2']

admin.site.register(SensorData, SensorDataAdmin)
