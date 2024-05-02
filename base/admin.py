from django.contrib import admin
from .models import Room, Topic, Message, Certificate

class RoomAdmin(admin.ModelAdmin):
    list_filter = ('host__username', 'name', 'created')  # Example filter for the 'created_at' field

class MessageAdmin(admin.ModelAdmin):
    list_filter = ('created', 'user__username')  # Example filters for the 'created_at' and 'topic' fields

class CertificateAdmin(admin.ModelAdmin):
    list_filter = ('created_at', 'user__username')  # Example filters for the 'created_at' and 'user' fields

admin.site.register(Room, RoomAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Certificate, CertificateAdmin)
