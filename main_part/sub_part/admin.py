from django.contrib import admin
from . models import Post,category,aboutUs
# Register your models here.

# show particular field in admin site
class postAdmin(admin.ModelAdmin):
    list_display=('title','content','img_url','category')
    search_fields=('title','content')
    list_filter=('category','created_at')

admin.site.register(Post,postAdmin)
admin.site.register(category)
admin.site.register(aboutUs)
