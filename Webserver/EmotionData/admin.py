from django.contrib import admin
import sys
from . import models

# Register models
admin.site.register(models.User)
admin.site.register(models.DataEntry)