from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User

from .forms import NewArticleForm, ProfileForm, CommentForm
from .models import Article, Author, Follow, Endorsement, Profile
from .models import ViewedArticles


@login_required
def home(request):
    articles = Article.objects.filter(published=True)

    return render(request, 'newshub/index.html',
                  {'articles': articles, 'type': 'home'})


@login_required
def top_stories(request):
    articles = Article.objects.filter(published=True)

    return render(request, 'newshub/index.html',
                  {'articles': articles, 'type': 'top-stories'})


@login_required
def history(request):
    viewed_set = ViewedArticles.objects.filter(
        user=request.user).order_by('-viewed_time')
    articles = [x.article for x in viewed_set]

    return render(request, 'newshub/index.html',
                  {'articles': articles, 'type': 'history'})


def login(request):
    if not request.user.is_authenticated():
        return render(request, 'newshub/login.html')
    else:
        return HttpResponseRedirect(reverse('newshub:home'))


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('newshub:home'))


@login_required
def profile(request, pk=None):
    if pk is None:
        profile_form = ProfileForm(instance=request.user.profile)
        user = request.user
    else:
        user = get_object_or_404(User, pk=pk)
        profile_form = ProfileForm(instance=user.profile)

    return render(request, 'newshub/profile.html',
                  {'user': user, 'profile_form': profile_form})


@login_required
def update_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.user != profile.user or request.method != 'POST':
        raise Http404

    form = ProfileForm(request.POST, instance=profile)

    if form.is_valid():
        form.save()

        return HttpResponseRedirect(
            reverse('newshub:profile'))

# Articles


@login_required
def new_article(request):
    if request.method == 'POST':
        form = NewArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user.author
            article.save()
            form.save_m2m()

            if request.POST['action'] == 'Save':
                return HttpResponseRedirect(
                    reverse('newshub:edit_article',
                            args=('home', article.pk,)))
            elif request.POST['action'] == 'Publish':
                article.published = True
                article.save()
                return HttpResponseRedirect(
                    reverse('newshub:view_article',
                            args=(article.pk,)))
    else:
        form = NewArticleForm()

    return render(
        request,
        'newshub/article/add_edit.html',
        {'form': form, 'add': True})


@login_required
def view_article(request, action_type, pk=None):
    if pk is None:
        raise Http404
    else:
        article = get_object_or_404(Article, pk=pk)

        if not article.published and article.author.user != request.user:
            raise Http404

        obj, created = ViewedArticles.objects.get_or_create(
            user=request.user, article=article)

        obj.save()

        comment_form = CommentForm(initial={'article': article})

        return render(
            request, 'newshub/article/view.html',
            {'article': article, 'action_type': action_type,
             'comment_form': comment_form})


@login_required
def edit_article(request, pk=None):
    article = get_object_or_404(Article, pk=pk)

    if article.author.user != request.user:
        raise Http404

    form = NewArticleForm(request.POST or None, instance=article)

    if form.is_valid():
        article = form.save()

        if request.POST['action'] == 'Save':
            return HttpResponseRedirect(
                reverse('newshub:edit_article', args=(pk,)))
        elif request.POST['action'] == 'Publish':
            article.published = True
            article.save()
            return HttpResponseRedirect(
                reverse('newshub:view_article', args=(pk,)))

    else:
        return render(
            request,
            'newshub/article/add_edit.html',
            {'form': form, 'add': False})


@login_required
def author_articles(request):
    articles = Article.objects.filter(author__pk=request.user.author.pk)

    return render(
        request,
        'newshub/article/by_author.html',
        {'articles': articles})


@login_required
def action(request, action_type):
    if not request.is_ajax():
        raise Http404

    if action_type == 'follow':
        author = request.GET.get('author', None)

        if author is None:
            raise Http404

        try:
            author = Author.objects.get(pk=author)
        except Author.DoesNotExists:
            raise Http404

        obj, created = Follow.objects.get_or_create(
            author=author, followed_by=request.user)

        if not created:
            obj.delete()

        return JsonResponse({'created': created})
    elif action_type == 'endorse':
        author = request.GET.get('author', None)

        if author is None:
            raise Http404

        try:
            author = Author.objects.get(pk=author)
        except Author.DoesNotExists:
            raise Http404

        obj, created = Endorsement.objects.get_or_create(
            author=author, endorsed_by=request.user)

        if not created:
            obj.delete()

        return JsonResponse({'created': created})
    elif action_type == 'like':
        article = request.GET.get('article', None)

        if article is None:
            raise Http404

        try:
            article = Article.objects.get(pk=article)
        except Article.DoesNotExists:
            raise Http404

        if request.user in article.likes.all():
            article.likes.remove(request.user)
            created = False
        else:
            article.likes.add(request.user)
            article.save()
            created = True

        return JsonResponse({'created': created})


@login_required
def add_comment(request):
    if request.is_ajax():
        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.made_by = request.user
                comment.save()

                return render(request, 'newshub/article/comment.html',
                              {'comment': comment})
        else:
            raise Http404
    else:
        raise Http404
