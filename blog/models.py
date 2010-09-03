# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.comments.moderation import CommentModerator, moderator
from django.contrib.sites.models import Site
from django.db import models
from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy as _

from akismet import Akismet
from tagging.fields import TagField


class Category(models.Model):
    name = models.CharField(_('name'),
                            max_length=100,
                            help_text=_('Max 100 characters.'))
    slug = models.SlugField(_('slug'),
                            unique=True,
                            help_text=_('Suggested value automatically '
                                        'generated from title. '
                                        'Must be unique.'))
    class Meta:
        ordering = ['name']
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __unicode__(self):
        return self.name

    def live_entries(self):
        """Returns only live entries."""
        return self.entries.filter(status=Entry.LIVE_STATUS)

    @models.permalink
    def get_absolute_url(self):
        return ('blog_category_detail', (), {'slug': self.slug})

class EntryLiveManager(models.Manager):

    def get_query_set(self):
        return super(EntryLiveManager, self).get_query_set().filter(
            status=self.model.LIVE_STATUS
        )

class Entry(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, _('Live')),
        (DRAFT_STATUS, _('Draft')),
        (HIDDEN_STATUS, _('Hidden')),
    )
    title = models.CharField(_('title'),
                             max_length=200,
                             help_text=_('Max 200 characters.'))
    pub_date = models.DateTimeField(_('publication date'),
                                    default=datetime.datetime.now)
    body = models.TextField(_('body'))

    categories = models.ManyToManyField(Category,
                                        blank=True,
                                        null=True,
                                        related_name='entries',
                                        verbose_name=_('categories'))
    tags = TagField(help_text=_('Separate tags with spaces.'))

    author = models.ForeignKey(_('author'), User)
    slug = models.SlugField(_('slug'),
                            unique_for_date='pub_date',
                            help_text=_('Suggested value automatically '
                                        'generated from title. Must be unique '
                                        'for the publication date.'))
    status = models.IntegerField(_('status'),
                                 choices=STATUS_CHOICES,
                                 default=DRAFT_STATUS)
    enable_comments = models.BooleanField(_('enable comments'), default=True)
    featured = models.BooleanField(_('featured'), default=False)

    objects = models.Manager()
    live = EntryLiveManager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name = _('entry')
        verbose_name_plural = _('entries')

    def __unicode__(self):
        return self.title


    @models.permalink
    def get_absolute_url(self):
        return ('blog_entry_detail', (), {
            'year': self.pub_date.strftime('%Y'),
            'month': self.pub_date.strftime('%m'),
            'day': self.pub_date.strftime('%d'),
            'slug': self.slug
        })

class EntryCommentModerator(CommentModerator):
    auto_moderate_field = 'pub_date'
    moderate_after = 30
    email_notification = True
    enable_field = 'enable_comments'

    def moderate(self, comment, content_object, request):
        already_moderated = super(EntryCommentModerator, self).moderate(
            comment, content_object, request
        )
        if already_moderated:
            return True

        domain = Site.objects.get_current().domain
        akismet_api = Akismet(key=settings.AKISMET_API_KEY,
                              blog_url='http://%s/' % domain)
        if akismet_api.verify_key():
            akismet_data = {'comment_type': 'comment',
                            'referrer': request.META['HTTP_REFERER'],
                            'user_ip': comment.ip_address,
                            'user_agent': request.META['HTTP_USER_AGENT']}

            return akismet_api.comment_check(smart_str(comment.comment),
                                             akismet_data,
                                             build_data=True)
        return False

moderator.register(Entry, EntryCommentModerator)

class Link(models.Model):

    title = models.CharField(_('title'), max_length=200)
    url = models.URLField(_('url'), unique=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name = _('link')
        verbose_name_plural = _('links')
