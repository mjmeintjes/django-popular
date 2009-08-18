from django import template
from django.db.models import get_model
from popular import get_popular_items

register = template.Library()

class ItemsNode(template.Node):
    def __init__(self, model, num_items, num_days, context_var):
        self.model = model
        self.num_items = num_items
        self.num_days = num_days
        self.context_var = context_var

    def render(self, context):
        items = get_popular_items(self.model, self.num_items, self.num_days)
        context[self.context_var] = [x[0] for x in items]
        return ''

@register.tag
def get_recently_popular(parser, token):
    '''
        Tag used to get popular instances of a model.

        {% get_recently_popular model [num_items] [num_days] as context_var %}

        Note that ``model`` must first be registered with ``popular.register``
    '''
    pieces = token.split_contents()
    tagname = pieces[0]
    as_index = pieces.index('as')

    # check tag structure
    if as_index < 2 or as_index > 4 or len(pieces) != as_index+2:
        raise template.TemplateSyntaxError("Syntax for tag is {%% %s app.Model [num_items] [num_days] as context_var %%}" % tagname)

    # get model from tag
    try:
        label, modelname = pieces[1].split('.')
        model = get_model(label, modelname)
    except Exception, e:
        raise template.TemplateSyntaxError('%s is not a valid app.Model reference' % pieces[1])

    # get num items/days if they were provided
    num_items = 5
    num_days = 7
    if as_index > 2:
        num_items = int(pieces[2])
    if as_index > 3:
        num_days = int(pieces[3])

    varname = pieces[-1]
    return ItemsNode(model, num_items, num_days, varname)
