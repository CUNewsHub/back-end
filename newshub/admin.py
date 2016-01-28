from django.contrib import admin
from .models import Category, Tag, Article, Author
from django.db.models import Count, Sum


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'approved',)
    list_filter = ('approved', 'category')
    list_editable = ('approved', )


class CategoryAdmin(admin.ModelAdmin):
    pass


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'author',
        'distinct_views',
        'total_views',
        'likes',
        'time_uploaded',
        'published')
    list_filter = ('published',)
    list_display_links = ('title', 'author',)

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        return qs.annotate(distinct_v=Count('viewedarticles'))\
                 .annotate(like_c=Count('likes'))\
                 .annotate(total_v=Sum('viewedarticles__number_of_views'))

    def likes(self, obj):
        return obj.like_c

    likes.admin_order_field = 'like_c'

    def distinct_views(self, obj):
        return obj.distinct_v

    distinct_views.admin_order_field = 'distinct_v'

    def total_views(self, obj):
        return obj.total_v

    total_views.admin_order_field = 'total_v'


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Author, AuthorAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
