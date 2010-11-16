# -*- coding: utf-8 -*-
from django import template
from django.db.models import get_model

from blog import settings

register = template.Library()

@register.simple_tag
def blog_title():
    return settings.BLOG_TITLE

@register.tag(name='get_months_archive')
def do_get_month_archive(parser, token):
    return MonthArchiveNode()

class MonthArchiveNode(template.Node):
    def __init__(self):
        model_args = ['blog', 'entry']
        self.model = get_model(*model_args)
    def render(self, context):
        context['months_archive'] = self.model.live.dates('pub_date',
                                                          'month',
                                                          'DESC')
        return ''

@register.tag(name='get_content')
def do_get_content(parser, token):

    args = token.split_contents()

    if len(args) != 4:
        raise template.TemplateSyntaxError(
            'get_content tags need three arguments'
        )

    model_args = args[1].split('.')
    if len(model_args) != 2:
        raise template.TemplateSyntaxError(
            "First argument of 'get_content' must be an"
            "'application name'.'model name' string"
        )
    model = get_model(*model_args)
    if model is None:
        raise template.TemplateSyntaxError(
            "%s is an invalid model for 'get_content' tag" % args[1]
        )

    return ContentNode(model, args[3])

class ContentNode(template.Node):

    def __init__(self, model, varname):
        self.model = model
        self.varname = varname

    def render(self, context):
        context[self.varname] = self.model._default_manager.all()
        return ''
