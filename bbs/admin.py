from django.contrib import admin
from bbs import models
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'pub_date','last_modify_date', 'status')

class CommentAdmin(admin.ModelAdmin):
    list_display = ('articles', 'parent_comment', 'comment_type', 'comment', 'user', 'date')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'set_as_top_menu', 'position_index')





admin.site.register(models.Articles, ArticleAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.UserProfile)
admin.site.register(models.Category, CategoryAdmin)