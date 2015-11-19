from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User

from .forms import NewArticleForm
from .models import Article, Author, Follow, Endorsement


@login_required
def home(request):
    articles = Article.objects.filter(published=True)

    return render(request, 'newshub/index.html', {'articles': articles})


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
        return render(request, 'newshub/profile.html', {'user': request.user})
    else:
        user = get_object_or_404(User, pk=pk)
        return render(
            request, 'newshub/profile.html', {'user': user})


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
                    reverse('newshub:edit_article', args=(article.pk,)))
            elif request.POST['action'] == 'Publish':
                return HttpResponseRedirect(
                    reverse('newshub:view_article', args=(article.pk,)))
    else:
        form = NewArticleForm()

    return render(
        request,
        'newshub/article/add_edit.html',
        {'form': form, 'add': True})


@login_required
def view_article(request, pk=None):
    if pk is None:
        raise Http404
    else:
        article = get_object_or_404(Article, pk=pk)

        if not article.published and article.author.user != request.user:
            raise Http404

        return render(
            request, 'newshub/article/view.html', {'article': article})


@login_required
def edit_article(request, pk=None):
    article = get_object_or_404(Article, pk=pk)

    if article.author.user != request.user:
        raise Http404

    form = NewArticleForm(request.POST or None, instance=article)

    if form.is_valid():
        form.save()

        if request.POST['action'] == 'Save':
            return HttpResponseRedirect(
                reverse('newshub:edit_article', args=(pk,)))
        elif request.POST['action'] == 'Publish':
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
