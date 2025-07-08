from django.contrib import admin
from .models import User

# User admin is now managed in exom_store, not in Django admin.
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
