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
    fields = (
        'author',
        'published',
        'z',)
    list_display = (
        'title',
        'author',
        'distinct_views',
        'total_views',
        'like_count',
        'time_uploaded',
        'z',
        'published',)
    list_filter = ('published',)
    list_display_links = ('title', 'author',)
    list_editable = ('z',)

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        return qs.annotate(distinct_v=Count('viewedarticles', distinct=True))\
                 .annotate(total_v=Sum(
                     'viewedarticles__number_of_views', distinct=True))

    def distinct_views(self, obj):
        return obj.distinct_v

    distinct_views.admin_order_field = 'distinct_v'

    def total_views(self, obj):
        return obj.total_v

    total_views.admin_order_field = 'total_v'

    def like_count(self, obj):
        return obj.likes.count()


class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__',
        'article_num')

    def get_queryset(self, request):
        qs = super(AuthorAdmin, self).get_queryset(request)
        return qs.annotate(a_num=Count('article'))

    def article_num(self, obj):
        return obj.article_set.count()

    article_num.admin_order_field = '-a_num'


admin.site.register(Author, AuthorAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
