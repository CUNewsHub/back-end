from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User

from .forms import NewArticleForm
from .models import Article


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
            article.author = request.user
            article.save()

            return HttpResponse("success")

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

        if not article.published and article.author != request.user:
            raise Http404

        return render(
            request, 'newshub/article/view.html', {'article': article})


@login_required
def edit_article(request, pk=None):
    article = get_object_or_404(Article, pk=pk)

    if article.author != request.user:
        raise Http404

    form = NewArticleForm(request.POST or None, instance=article)

    if form.is_valid():
        form.save()

        return HttpResponseRedirect(
            reverse('newshub:edit_article', args=(pk,)))

    else:
        return render(
            request,
            'newshub/article/add_edit.html',
            {'form': form, 'add': False})


@login_required
def author_articles(request, pk=None):
    if pk is None or pk == request.user.ok:
        articles = Article.objects.filter(author=request.user)
    else:
        articles = Article.objects.filter(author__pk=pk)

    return render(
        request,
        'newshub/article/by_author.html',
        {'articles': articles})
