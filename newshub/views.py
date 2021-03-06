import redis
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.http import JsonResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from .forms import NewArticleForm, ProfileForm, CommentForm, PollForm
from .forms import ChoiceForm, SocietyForm, SocietyDataForm, UpdateSocietyForm
from .forms import LandingTagsForm, TagForm
from .forms import ProfileCreationForm
from .models import Article, Author, Follow, Endorsement, Profile, Poll, Tag
from .models import ViewedArticles, Choice, Feedback, UserFeedback, Society
from .models import Comment, Category
import newshub.models as models
from .decorators import landing_pages_seen
from feed import initialise_category_vector, update_category_vector
from feed import get_personalised_feed
from django.conf import settings
from django.db.models import Q
from endless_pagination.decorators import page_template
from tracking.models import PageVisitor

# from .signals import new_article as new_article_signal


def _get_redis_instance():
    if settings.NEWSHUB_REDIS_PORT is not None:
        r = redis.StrictRedis(host='localhost',
                              port=settings.NEWSHUB_REDIS_PORT,
                              db=0)
        return r
    else:
        return None


@login_required
@landing_pages_seen
@page_template('newshub/index_page.html')
def home(request, template='newshub/index.html', extra_context=None):
    articles = get_personalised_feed(
        _get_redis_instance(), request.user, models)
    if request.is_ajax():
        template = 'newshub/index_page.html'
        page_template = None
    else:
        template = 'newshub/index.html'
        page_template = 'newshub/index_page.html'
        PageVisitor.create_page_visitor(
            'newsfeed', request, newsfeed_type='personal-feed')

    return render(request, template,
                  {'articles': articles, 'type': 'home',
                   'categories': Category.objects.all(),
                   'page_template': page_template})


def top_stories(request, template='newshub/index.html', extra_context=None):
    articles = Article.objects.filter(published=True)\
                      .order_by('-top_stories_value')

    if request.is_ajax():
        template = 'newshub/index_page.html'
        page_template = None
    else:
        template = 'newshub/index.html'
        page_template = 'newshub/index_page.html'
        PageVisitor.create_page_visitor(
            'newsfeed', request, newsfeed_type='top-stories ')

    return render(request, template,
                  {'articles': articles, 'type': 'top-stories',
                   'categories': Category.objects.all(), 'show_menu': True,
                   'page_template': page_template})


@login_required
@landing_pages_seen
@page_template('newshub/index_page.html')
def history(request, template='newshub/index.html', extra_context=None):
    viewed_set = ViewedArticles.objects.filter(
        user=request.user).order_by('-last_viewed_time')
    articles = [x.article for x in viewed_set]

    if request.is_ajax():
        template = 'newshub/index_page.html'
        page_template = None
    else:
        template = 'newshub/index.html'
        page_template = 'newshub/index_page.html'
        PageVisitor.create_page_visitor(
            'newsfeed', request, newsfeed_type='history')

    return render(request, template,
                  {'articles': articles, 'type': 'history',
                   'categories': Category.objects.all(),
                   'page_template': page_template})


def login(request):
    if not request.user.is_authenticated():
        reg_form = ProfileCreationForm()
        if request.method == 'POST':
            form = AuthenticationForm(None, request.POST or None)
            next_ = request.GET.get('next', reverse('newshub:home'))

            if form.is_valid():
                auth_login(request, form.get_user())
                return HttpResponseRedirect(next_)
        else:
            form = AuthenticationForm()
            PageVisitor.create_page_visitor('login_page', request)
        return render(request, 'newshub/login.html',
                      {'form': form, 'reg_form': reg_form})
    else:
        return home(request)


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('newshub:login'))


@login_required
def profile(request):
    return view_profile(request, request.user.pk)


def view_profile(request, pk):
    profile_form = None
    # notification_form = None
    society = None
    if pk is None:
        user = request.user
    else:
        user = get_object_or_404(User, pk=pk)

    featured_article_set = user.author.article_set.filter(
        featured=True, published=True)
    if pk is None:
        try:
            profile_form = ProfileForm(
                instance=request.user.profile,
                initial={'email': user.email})
            PageVisitor.create_page_visitor(
                'profile', request, obj=request.user.profile)
        except Profile.DoesNotExist:
            try:
                society = user.society
                profile_form = UpdateSocietyForm(
                    instance=user.society,
                    initial={'email': user.email,
                             'socname': user.first_name})
                PageVisitor.create_page_visitor(
                    'society', request, obj=society)
            except Society.DoesNotExist:
                raise Http404
    else:
        try:
            profile_form = ProfileForm(
                instance=user.profile,
                initial={'email': user.email})
            PageVisitor.create_page_visitor(
                'profile', request, obj=user.profile)
            # notification_form = EmailNotificationForm(
            #    instance=request.user.profile.email_notifications)
        except Profile.DoesNotExist:
            try:
                profile_form = UpdateSocietyForm(
                    instance=user.society,
                    initial={'email': user.email,
                             'socname': user.first_name})
                society = user.society
                PageVisitor.create_page_visitor(
                    'society', request, obj=society)
            except Society.DoesNotExist:
                raise Http404

    return render(request, 'newshub/profile.html',
                  {'user': user, 'profile_form': profile_form,
                   'society': society,
                   'featured_article_set': featured_article_set,
                   'notification_form': None})


@login_required
@landing_pages_seen
def update_profile(request, pk):
    profile = get_object_or_404(Profile, pk=pk)
    if request.user != profile.user or request.method != 'POST':
        raise Http404

    form = ProfileForm(
        request.POST or None, request.FILES or None, instance=profile)

    if form.is_valid():
        form.save()
        user = profile.user
        user.email = form.cleaned_data['email']
        user.save()

    return HttpResponseRedirect(
        reverse('newshub:self_profile'))


@login_required
@landing_pages_seen
def new_article(request):
    if request.method == 'POST':
        form = NewArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user.author
            article.save()
            form.save_m2m()

            # updating redis
            update_category_vector(
                _get_redis_instance(), request.user, article, 'write', models)

            poll_title = request.POST.get('poll', None)

            if poll_title is not None and poll_title != "":
                poll = Poll(title=poll_title, article=article)
                poll.save()

            if request.POST['action'] == 'Save':
                return HttpResponseRedirect(
                    reverse('newshub:edit_article',
                            args=(article.pk,)))
            elif request.POST['action'] == 'Publish':
                article.published = True
                article.save()
                # new_article_signal.send(sender=Article, article=article)
                return HttpResponseRedirect(
                    reverse('newshub:view_article',
                            args=('home', article.pk,)))
    else:
        form = NewArticleForm()

    return render(
        request,
        'newshub/article/add_edit.html',
        {'form': form, 'add': True, 'tag_form': TagForm()})


def view_article(request, action_type, pk=None):
    if request.user.is_authenticated():
        return view_article_logged_in(request, action_type, pk)
    else:
        return HttpResponseRedirect(
            reverse('newshub:view_article_outside', args=(pk,)))


def view_article_outside(request, pk):
    if request.user.is_authenticated():
        return HttpResponseRedirect(
            reverse('newshub:view_article', args=('home', pk)))

    try:
        article = Article.objects.get(url_text=pk)
    except Article.DoesNotExist:
        article = get_object_or_404(Article, pk=pk)
        article.url_text = article.generate_url_text()
        article.save()
        return HttpResponseRedirect(
            reverse('newshub:view_article_outside', args=(article.url_text,)))
    more_articles = Article.objects.order_by('-top_stories_value')\
                                   .filter(published=True)\
                                   .filter(~Q(pk=article.pk))[:5]
    article.outside_view_count += 1
    article.save()

    PageVisitor.create_page_visitor(
        'article', request, obj=article)

    return render(request, 'newshub/article/view.html',
                  {'article': article, 'action_type': 'pre_view',
                   'feedback_set': Feedback.objects.all(),
                   'more_articles': more_articles})


@login_required
@landing_pages_seen
def view_article_logged_in(request, action_type, pk=None):
    if pk is None:
        raise Http404
    else:
        category = None
        if (action_type != 'home' and action_type != 'history' and
                action_type != 'top-stories'):

            category = get_object_or_404(Category, name=action_type)
        try:
            article = Article.objects.get(url_text=pk)
        except Article.DoesNotExist:
            article = get_object_or_404(Article, pk=pk)
            article.url_text = article.generate_url_text()
            article.save()
            return HttpResponseRedirect(
                reverse('newshub:view_article',
                        args=(action_type, article.url_text,)))

        if not article.published and article.author.user != request.user:
            raise Http404

        obj, created = ViewedArticles.objects.get_or_create(
            user=request.user, article=article)

        # updating redis
        update_category_vector(
            _get_redis_instance(), request.user, article, 'view', models)

        obj.number_of_views += 1

        obj.save()
        article_data = {}
        article_data['article_view_count'] = sum(
            [x.number_of_views for x in ViewedArticles.objects.filter(
                article=article)])

        total_feedback = sum(
            [x.feedback.count() for x in article.user_feedback.all()])

        article_data['article_feedback_sum'] = total_feedback

        f_set = article.get_feedback_set()[:3]

        article_data['feedback_set'] = []

        for feedback in f_set:
            percentage = 100.0 * (
                float(feedback.f_count) / float(total_feedback))
            percentage = int(percentage)
            article_data['feedback_set'].append({
                'obj': feedback,
                'percentage': percentage
            })

        PageVisitor.create_page_visitor(
            'article', request, obj=article)

        comment_form = CommentForm(initial={'article': article})

        try:
            uf = UserFeedback.objects.get(user=request.user, article=article)
        except UserFeedback.DoesNotExist:
            uf = None

        return render(
            request, 'newshub/article/view.html',
            {'article': article, 'action_type': action_type,
             'comment_form': comment_form, 'uf': uf,
             'feedback_set': Feedback.objects.all(),
             'article_data': article_data, 'category': category}
        )


@login_required
@landing_pages_seen
def edit_article(request, pk=None):
    try:
        article = Article.objects.get(url_text=pk)
    except Article.DoesNotExist:
        article = get_object_or_404(Article, pk=pk)
        article.url_text = article.generate_url_text()
        article.save()
        return HttpResponseRedirect(
            reverse('newshub:edit_article',
                    args=(article.url_text,)))

    if article.author.user != request.user:
        raise Http404

    form = NewArticleForm(
        request.POST or None,
        request.FILES or None,
        instance=article)

    if form.is_valid():
        article = form.save()

        if request.POST['action'] == 'Save':
            return HttpResponseRedirect(
                reverse('newshub:edit_article', args=(pk,)))
        elif request.POST['action'] == 'Publish':
            article.published = True
            article.save()
            return HttpResponseRedirect(
                reverse('newshub:view_article', args=('home', pk,)))
        elif request.POST['action'] == 'Published':
            article.published = False
            article.save()
            return HttpResponseRedirect(
                reverse('newshub:edit_article', args=(pk,)))

        return HttpResponseRedirect(
            reverse('newshub:edit_article', args=(pk,)))

    article_data = {}
    article_data['article_view_count'] = sum(
        [x.number_of_views for x in ViewedArticles.objects.filter(
            article=article)])

    total_feedback = sum(
        [x.feedback.count() for x in article.user_feedback.all()])

    article_data['article_feedback_sum'] = total_feedback

    f_set = article.get_feedback_set()[:3]

    article_data['feedback_set'] = []

    for feedback in f_set:
        percentage = 100.0 * (
            float(feedback.f_count) / float(total_feedback))
        percentage = int(percentage)
        article_data['feedback_set'].append({
            'obj': feedback,
            'percentage': percentage
        })

    else:
        return render(
            request,
            'newshub/article/add_edit.html',
            {'form': form,
             'poll_form': PollForm(initial={'article': article}),
             'tag_form': TagForm(),
             'article_data': article_data,
             'add': False})


@login_required
@landing_pages_seen
def author_articles(request):
    articles = Article.objects.filter(author__pk=request.user.author.pk)

    return render(
        request,
        'newshub/article/by_author.html',
        {'articles': articles})


@login_required
@landing_pages_seen
def action(request, action_type):
    if not request.is_ajax():
        raise Http404

    if action_type == 'follow':
        author = request.GET.get('author', None)

        if author is None:
            raise Http404

        try:
            author = Author.objects.get(pk=author)
        except Author.DoesNotExist:
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
        except Author.DoesNotExist:
            raise Http404

        endorsement_count = Endorsement.objects.count()

        if endorsement_count < 4:
            obj, created = Endorsement.objects.get_or_create(
                author=author, endorsed_by=request.user)

            if not created:
                obj.delete()

            success = True
        else:
            created = False
            success = False

        return JsonResponse({'created': created, 'success': success})
    elif action_type == 'like':
        article = request.GET.get('article', None)

        if article is None:
            raise Http404

        try:
            article = Article.objects.get(pk=article)
        except Article.DoesNotExist:
            raise Http404

        if request.user in article.likes.all():
            article.likes.remove(request.user)
            created = False
        else:
            article.likes.add(request.user)
            article.save()
            update_category_vector(
                _get_redis_instance(), request.user, article, 'like', models)
            created = True

        return JsonResponse({'created': created})


@login_required
@landing_pages_seen
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


@login_required
@landing_pages_seen
def article_add_poll(request):
    poll_form = PollForm(request.POST)
    if poll_form.is_valid():
        if poll_form.cleaned_data['article'].author.user != request.user:
            raise Http404

        poll = poll_form.save()
        return HttpResponseRedirect(
            reverse('newshub:article_edit_poll', args=(poll.pk,)))
    else:
        return HttpResponseRedirect(
            reverse('newshub:edit_article', args=(request.POST['article'])))


@login_required
@landing_pages_seen
def article_delete_poll(request, pk):
    poll = get_object_or_404(Poll, pk=pk)

    article = poll.article

    if poll.article.author.user != request.user:
        raise Http404

    poll.delete()

    return HttpResponseRedirect(
        reverse('newshub:edit_article', args=(article.pk,)))


@login_required
@landing_pages_seen
def article_edit_poll(request, pk):
    poll = get_object_or_404(Poll, pk=pk)

    if poll.article.author.user != request.user:
        raise Http404

    return render(request, 'newshub/article/poll/edit_poll.html',
                  {'poll': poll, 'form': ChoiceForm(initial={'poll': poll})})


@login_required
@landing_pages_seen
def article_poll_add_choice(request):
    if request.method != 'POST':
        raise Http404

    choice_form = ChoiceForm(request.POST)

    if choice_form.is_valid():
        choice = choice_form.save(commit=False)
        if choice.poll.article.author.user != request.user:
            raise Http404

        choice.save()

        return HttpResponseRedirect(
            reverse('newshub:article_edit_poll', args=(choice.poll.pk,)))
    else:
        poll = choice_form.cleaned_data['poll']
        if poll is None:
            raise Http404

        return render(
            request, 'newshub/article/poll/edit_poll.html',
            {'poll': poll, 'form': choice_form})


@login_required
@landing_pages_seen
def article_delete_poll_choice(request, pk):
    choice = get_object_or_404(Choice, pk=pk)

    if choice.poll.article.author.user != request.user:
        raise Http404
    else:
        poll_pk = choice.poll.pk
        choice.delete()

        return HttpResponseRedirect(
            reverse('newshub:article_edit_poll', args=(poll_pk,)))


@login_required
@landing_pages_seen
def article_poll_vote(request, pk):
    if request.method != 'POST':
        raise Http404

    poll = get_object_or_404(Poll, pk=pk)

    choice = request.POST.get('choice', None)

    if choice is None:
        return HttpResponseRedirect(
            reverse('newshub:view_article', args=('home', poll.article.pk)))

    choice = get_object_or_404(Choice, pk=choice)

    if choice not in poll.choice_set.all():
        raise Http404

    if request.user in poll.voted.all() or choice is None:
        return HttpResponseRedirect(
            reverse('newshub:view_article', args=('home', poll.article.pk)))

    choice.votes += 1
    choice.save()

    poll.voted.add(request.user)
    poll.save()

    return HttpResponseRedirect(
        reverse('newshub:view_article', args=('home', poll.article.pk)))


def article_add_feedback(request, a_id, f_id):
    if not request.user.is_authenticated():
        return HttpResponse('notauth')
    if a_id is None or f_id is None:
        raise Http404

    if request.is_ajax is False:
        raise Http404

    feedback = get_object_or_404(Feedback, pk=f_id)
    article = get_object_or_404(Article, pk=a_id)

    try:
        f = UserFeedback.objects.get(user=request.user, article=article)
        if feedback in f.feedback.all():
            f.feedback.remove(feedback)
        else:
            f.feedback.add(feedback)

        f.save()
    except UserFeedback.DoesNotExist:
        uf = UserFeedback.objects.create(user=request.user, article=article)
        uf.add(feedback)

    return HttpResponse('success')


@login_required
@landing_pages_seen
def create_society(request):
    if request.method == 'POST':
        form = SocietyForm(request.POST)
        society_data_form = SocietyDataForm(request.POST, request.FILES)
        if form.is_valid() and society_data_form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = 'tmp'
            new_user.save()
            new_user.username = 'society_' + str(new_user.pk + 20)
            s = society_data_form.save(commit=False)
            s.tag_page_seen = True
            s.follow_endorse_page_seen = True
            s.user = new_user
            s.save()
            s.admins.add(request.user)
            new_user.society = s
            new_user.save()
            Author.objects.create(user=new_user)

            auth_logout(request)
            new_user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(request, new_user)

            return render(request, 'newshub/landing_pages/society.html',
                          {'user': new_user})
    else:
        form = SocietyForm()
        society_data_form = SocietyDataForm()
    return render(request, "newshub/societies.html", {
        'form': form,
        'society_data_form': society_data_form
    })


@login_required
@landing_pages_seen
def societies_login(request, pk):
    s = get_object_or_404(Society, pk=pk)

    if request.user not in s.admins.all():
        raise Http404

    auth_logout(request)

    s.user.backend = 'django.contrib.auth.backends.ModelBackend'

    auth_login(request, s.user)

    return HttpResponseRedirect(reverse('newshub:self_profile'))


@login_required
@landing_pages_seen
def update_society(request, pk):
    society = get_object_or_404(Society, pk=pk)
    if request.user != society.user or request.method != 'POST':
        raise Http404

    society_form = UpdateSocietyForm(
        request.POST or None, request.FILES or None, instance=society)

    if society_form.is_valid():
        society_form.save()
        user = society.user
        user.email = society_form.cleaned_data['email']
        user.first_name = society_form.cleaned_data['socname']
        user.save()
    else:
        return render(
            request, 'newshub/profile.html',
            {'user': request.user,
             'society': society, 'society_form': society_form})

    return HttpResponseRedirect(
        reverse('newshub:self_profile') + '#edit-profile')


@login_required
@landing_pages_seen
def articles_by_tags(request, tag_name,
                     template='newshub/index.html', extra_context=None):
    articles = Article.objects.filter(published=True)

    tag = get_object_or_404(Tag, name=tag_name)

    if not tag.approved:
        raise Http404

    articles = articles.filter(tags=tag)

    if request.is_ajax():
        template = 'newshub/index_page.html'
        page_template = None
    else:
        template = 'newshub/index.html'
        page_template = 'newshub/index_page.html'
        PageVisitor.create_page_visitor(
            'tag', request, obj=tag)

    return render(request, template,
                  {'articles': articles, 'type': 'home',
                   'page_template': page_template,
                   'categories': Category.objects.all()})


def _update_landing_pages_tags(user):
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        try:
            profile = user.society
        except Society.DoesNotExist:
            raise Http404

    profile.tag_page_seen = True
    profile.save()


def _update_landing_pages_follow_endorse(user):
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        try:
            profile = user.society
        except Society.DoesNotExist:
            raise Http404

    profile.follow_endorse_page_seen = True
    profile.save()


def _save_tags(user, tag_list):
    for tag in tag_list:
        try:
            t = Tag.objects.get(pk=tag)
            user.tag_set.add(t)
        except Tag.DoesNotExist:
            pass


def _get_landing_pages(user):
    try:
        profile = user.profile
    except Profile.DoesNotExist:
        try:
            profile = user.society
        except Society.DoesNotExist:
            raise Http404

    return (profile.tag_page_seen, profile.follow_endorse_page_seen)


@login_required
def landing_pages_tags(request):
    tag_page_seen, _ = _get_landing_pages(request.user)
    if tag_page_seen:
        return HttpResponseRedirect(reverse('newshub:home'))
    if request.method == 'POST':
        if request.POST['action'] == 'Next':
            tag_list = request.POST.getlist('tags')
            _save_tags(request.user, tag_list)
            _update_landing_pages_tags(request.user)
            initialise_category_vector(
                _get_redis_instance(), request.user, models)
            return HttpResponseRedirect(
                reverse('newshub:self_profile') + '#edit-profile')

    return render(request, 'newshub/landing_pages/tags.html',
                  {'form': LandingTagsForm()})


@login_required
def landing_pages_follow_endorse(request):
    tag_page_seen, follow_endorse_page_seen = _get_landing_pages(request.user)
    if follow_endorse_page_seen:
        return HttpResponseRedirect(
            reverse('newshub:home'))
    else:
        if not tag_page_seen:
            return HttpResponseRedirect(reverse('newshub:landing_pages_tags'))

    if request.method == 'POST':
        if request.POST['action'] == 'Next':
            _update_landing_pages_follow_endorse(request.user)
            return HttpResponseRedirect(reverse('newshub:home'))
    return render(
        request, 'newshub/landing_pages/follow_endorse.html')


@login_required
@landing_pages_seen
def add_tag(request):
    if request.method != 'POST' and not request.is_ajax():
        raise Http404

    tag_form = TagForm(request.POST)

    data = {}

    if tag_form.is_valid():
        tag = tag_form.save()
        data['success'] = True
        data['tag'] = {
            'name': tag.name,
            'id': tag.pk
        }
    else:
        data['success'] = False
        data['error_msg'] = "This tag already exists"
    return JsonResponse(data)


@login_required
@landing_pages_seen
def article_make_featured(request):
    if request.method != 'POST' and not request.is_ajax():
        raise Http404

    id_article = request.POST.get('id_article', None)

    if id_article is None:
        raise Http404

    article = get_object_or_404(Article, pk=id_article)

    if request.user != article.author.user:
        raise Http404
    data = {}

    if article.featured:
        article.featured = False
        article.save()
        data['success'] = True
        data['feature'] = False
        data['id_article'] = article.pk
    else:
        if article.author.article_set.filter(featured=True).count() >= 3:
            data['success'] = False
            data['error'] = "You have already featured 3 articles"
        else:
            article.featured = True
            article.save()
            data['success'] = True
            data['feature'] = True
            data['id_article'] = article.pk

    return JsonResponse(data)


@login_required
@landing_pages_seen
def delete_comment(request):
    if request.method == 'POST' and request.is_ajax():
        comment_pk = request.POST.get('comment_pk', None)
        if comment_pk is None:
            raise Http404
        else:
            comment = get_object_or_404(Comment, pk=comment_pk)
            if comment.made_by == request.user:
                comment.delete()
                return JsonResponse({
                    'success': True,
                    'comment_pk': comment_pk})
            else:
                raise Http404
    else:
        raise Http404


@login_required
@landing_pages_seen
def edit_comment(request):
    if request.method == 'POST' and request.is_ajax():
        comment_pk = request.POST.get('comment_pk', None)
        comment_text = request.POST.get('comment_text', None)

        if comment_pk is None:
            raise Http404

        if comment_text is None or comment_text == '':
            raise Http404

        comment = get_object_or_404(Comment, pk=comment_pk)
        if comment.made_by != request.user:
            raise Http404
        comment.text = comment_text
        comment.save()

        return render(request, 'newshub/article/comment.html',
                      {'comment': comment})
    else:
        raise Http404


@login_required
@landing_pages_seen
def society_change_password(request):
    try:
        request.user.society
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect(
                    reverse('newshub:society_change_password_confirmation'))
        else:
            form = PasswordChangeForm(request.user)
        data = {
            'form': form
        }

        return render(request, 'newshub/society_change_password.html', data)
    except Society.DoesNotExist:
        raise Http404


def articles_by_category(request, category,
                         template='newshub/index.html', extra_context=None):
    category = get_object_or_404(Category, name=category)

    articles = Article.objects.filter(tags__category=category)\
                              .filter(published=True)\
                              .order_by('-top_stories_value')\
                              .distinct()

    if request.is_ajax():
        template = 'newshub/index_page.html'
        page_template = None
    else:
        template = 'newshub/index.html'
        page_template = 'newshub/index_page.html'
        PageVisitor.create_page_visitor(
            'category', request, obj=category)

    return render(request, template,
                  {'articles': articles, 'type': category.name,
                   'category': category,
                   'categories': Category.objects.all(), 'show_menu': True,
                   'page_template': page_template})


def register(request):
    if request.method == 'POST':
        form = ProfileCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user, picture=form.cleaned_data['profile_picture'])
            Author.objects.create(user=user)

            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth_login(request, user)

            return HttpResponseRedirect(reverse('newshub:home'))
    else:
        form = ProfileCreationForm()

    return render(
        request,
        'newshub/register.html',
        {'form': form})


@login_required
def update_notification_settings(request):
    pass
#     if request.method == 'POST':
#         form = EmailNotificationForm(
#             request.POST or None,
#             instance=request.user.profile.email_notifications)
#         if form.is_valid():
#             form.save()
#         else:
#             raise Http404

#         return HttpResponseRedirect(
#             reverse('newshub:self_profile') + '#notification-settings')
#     else:
#         raise Http404
