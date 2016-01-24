def initialise_category_vector(redis, user, models):
    categories = models.Category.objects.all()
    category_vector = {c.pk: 5.0 for c in categories}

    tag_set = user.tag_set.all()

    for tag in tag_set:
        category_vector[tag.category.pk] += 3.0

    redis.set('category_vector_'+str(user.pk), category_vector)


def get_occurrence_category_vector(article, models):
    occ_category_vector = {c.pk: 0.0 for c in models.Category.objects.all()}
    tag_num = 0

    for tag in article.tags.all():
        occ_category_vector[tag.category.pk] += 1.0
        tag_num += 1

    # normalise
    for k in occ_category_vector:
        occ_category_vector[k] /= tag_num

    return occ_category_vector


def update_category_vector(redis, user, article, action, models):
    try:
        user_category_vector = eval(redis.get('category_vector_'+str(user.pk)))
    except TypeError:
        initialise_category_vector(redis, user, models)
        user_category_vector = eval(redis.get('category_vector_'+str(user.pk)))
    update_num = 0.0

    occ_category_vector = get_occurrence_category_vector(article, models)

    if action == 'view':
        update_num = 0.1
    elif action == 'like':
        update_num = 1.0
    elif action == 'write':
        update_num = 2.0

    for c_pk in user_category_vector:
        user_category_vector[c_pk] += occ_category_vector[c_pk]*update_num

    redis.set('category_vector_'+str(user.pk), user_category_vector)


def get_personalised_feed(redis, user, models):
    feed_ids = redis.lrange('personalised_feed_'+str(user.pk), 0, -1)

    if feed_ids == []:
        return models.Article.objects.filter(published=True)\
                             .order_by('-time_uploaded')
    else:
        return [models.Article.objects.get(pk=x) for x in feed_ids]
