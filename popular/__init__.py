import datetime
from django.conf import settings
from django.core.urlresolvers import resolve, Resolver404
from googleanalytics import Connection
from googleanalytics.exception import GoogleAnalyticsClientError

__VERSION__ = '0.0.3'

registered_models = {}

_ga_acct = None
def get_analytics_account():
    global _ga_acct
    if not _ga_acct:
        connection = Connection(settings.GOOGLE_ANALYTICS_EMAIL, settings.GOOGLE_ANALYTICS_PASSWORD)
        _ga_acct = connection.get_account(settings.GOOGLE_ANALYTICS_ID)
    return _ga_acct

def register(model, regex, lookup_func=None):
    """
        register a model to be used with the get_recently_popular templatetag

        An example call may look like::
            popular.register(Post, '^/blog/[0-9]{4}/', url_to_post)

        This tells popular to use Google Analytics results that match the
        given regex to determine the most popular Posts.  The third (optional)
        parameter is a function that is used to resolve a url to an object
        of the given type.
    """
    if lookup_func is None:
        def default_lookup_func(url):
            view,_,pieces = resolve(url)
            return model.objects.get(**pieces)
        lookup_func = default_lookup_func
    registered_models[model] = (regex, lookup_func)

def get_popular_items(model, num=5, days_ago=7,
                      start_date=None, end_date=None):
    """
        Get the most popular instances of a particular model.

        Using the information given when the model was registered (see
        ``register``) look up the most popular items meeting the given
        criteria.

        Optional Parameters:
            num
                Number of items to look up. (default: 5)
            days_ago
                Number of days into the past to consider. (default: 7)
            start_date
                ``datetime`` object to start lookup range
            end_date
                ``datetime`` object to end lookup range
    """
    if model not in registered_models:
        raise ValueError('%s not in registry, call popular.register first' % model._meta.object_name)
    regex, lookup_func = registered_models[model]

    if end_date is None:
        end_date = datetime.datetime.now()
    if start_date is None:
        start_date = end_date - datetime.timedelta(days_ago)

    acct = get_analytics_account()
    try:
        data = acct.get_data(start_date=start_date, end_date=end_date,
                             dimensions=['pagePath'], metrics=['pageviews'],
                             filters=[['pagePath', '=~', regex]],
                             sort=['-pageviews'], max_results=num)

        objects = []
        for item in data:
            try:
                url = item.dimension.split('?')[0]
                obj = lookup_func(url)
                objects.append((obj, item.metric))
            except (model.DoesNotExist, Resolver404):
                pass
        return objects
    except GoogleAnalyticsClientError:
        return None
