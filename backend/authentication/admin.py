from django.contrib import admin
from authentication.models import UserData, NonceSignRequest


admin.site.register(UserData)
admin.site.register(NonceSignRequest)