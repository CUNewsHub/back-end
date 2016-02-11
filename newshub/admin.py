from django.contrib import admin
from .models import Category, Tag, Article, Author, Comment
from django.db.models import Count


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
        'author_link',
        'distinct_views',
        'total_views',
        'like_count',
        'comments',
        'time_uploaded',
        'top_stories_value',
        'featured',
        'z',
        'published',)
    list_filter = ('featured', 'published',)
    list_display_links = ('title',)
    list_editable = ('featured', 'z',)

    def get_queryset(self, request):
        qs = super(ArticleAdmin, self).get_queryset(request)
        return qs.annotate(distinct_v=Count('viewedarticles', distinct=True))\
                 .annotate(like_c=Count('likes', distinct=True))\
                 .annotate(comment_c=Count('comment', distinct=True))

    def distinct_views(self, obj):
        return obj.distinct_v

    distinct_views.admin_order_field = 'distinct_v'
    distinct_views.short_description = 'Distinct inside views'

    def total_views(self, obj):
        total_inside_views = sum([
            x.number_of_views for x in obj.viewedarticles_set.all()])
        return total_inside_views + obj.outside_view_count

    def like_count(self, obj):
        return obj.likes.count()

    like_count.admin_order_field = 'like_c'

    def comments(self, obj):
        return obj.comment_set.count()

    comments.admin_order_field = 'comment_c'

    def author_link(self, obj):
        link = "/admin/newshub/author/%s/" % (obj.author.pk,)
        return '<a href="%s">%s</a>' % (
            link, 'View')

    author_link.allow_tags = True
    author_link.short_description = "Author link"


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


class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'user_made_by',
        'article',
        'article_link',
        'text')
    list_display_links = ('pk',)
    list_filter = ('article',)

    def user_made_by(self, obj):
        link = "/admin/auth/user/%s/" % (obj.made_by.pk,)
        return '<a href="%s">%s</a>' % (
            link, obj.made_by)

    user_made_by.allow_tags = True
    user_made_by.short_description = "User"

    def article_link(self, obj):
        link = '/admin/newshub/article/%s/' % (obj.article.pk,)
        return '<a href="%s">%s</a>' % (
            link, 'View')

    article_link.allow_tags = True
    article_link.short_description = "Article link"

admin.site.register(Author, AuthorAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
