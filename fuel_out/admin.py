from django.contrib import admin
from .models import CustomerConfig
from .models import TrkConfig
from .models import WareHouse
from .models import CardIndent

# Register your models here.

admin.site.register(CustomerConfig)
admin.site.register(TrkConfig)
admin.site.register(CardIndent)
admin.site.register(WareHouse)

