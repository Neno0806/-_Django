from django.contrib import admin
from .models import Tag,Memo

# admin.site.register(Tag)
# admin.site.register(Memo)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    # fields = ['name', 'id']
    list_display = ('id', 'tag_name')

@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text')