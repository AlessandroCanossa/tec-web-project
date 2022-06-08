from django.contrib import admin

# Register your models here.
from users.models import User, CoinsPurchase


class UserModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_creator', 'date_joined')
    list_filter = ('is_creator',)
    search_fields = ('username__contains',)
    exclude = ('last_login', 'groups', 'is_active', 'date_joined', 'user_permissions', 'is_superuser')


class CoinsPurchaseModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'coins', 'date')
    list_filter = ('date',)
    search_fields = ('user__username__contains',)
    exclude = ('date',)


admin.site.register(User, UserModelAdmin)
admin.site.register(CoinsPurchase, CoinsPurchaseModelAdmin)
