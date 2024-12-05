from django.contrib import admin
from .models import Category, ChatHistory,Customer,Product,Order,Profile
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)
admin.site.register(ChatHistory)

#mix profile info and user info
class ProfileInline(admin.StackedInline):
    model=Profile

#extend user model
class UserAdmin(admin.ModelAdmin):
    model=User
    field=["username","fisrt_name","last_name","email"]
    inlines=[ProfileInline]

#unregister the old way
admin.site.unregister(User)

#Re-register the new way 
admin.site.register(User,UserAdmin)

