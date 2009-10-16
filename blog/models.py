# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.db import models

from tagging.fields import TagField

class Category(models.Model):
    name = models.CharField(max_length=100, help_text='Max 100 characters')
    slug = models.SlugField(unique=True, help_text='Suggested value'
                                                   'automatically generated'
                                                   'from title. '
                                                   'Must be unique.')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('blog_category_detail', (), {'slug': self.slug})

class LiveEntryManager(models.Manager):

    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(
            status=self.model.LIVE_STATUS
        )

class Entry(models.Model):
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )
    title = models.CharField(max_length=200, help_text='Max 200 characters')
    pub_date = models.DateTimeField('Publication date',
                                    default=datetime.datetime.now)
    body = models.TextField()


    categories = models.ManyToManyField(Category, related_name='entries')
    tags = TagField(help_text='Separate tags with spaces.')

    author = models.ForeignKey(User)
    slug = models.SlugField(unique_for_date='pub_date',
                            help_text='Suggested value automatically generated'
                                      'from title. Must be unique for the'
                                      'publication date.')
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT_STATUS)
    enable_comments = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)

    objects = models.Manager()
    live = LiveEntryManager()

    class Meta:
        ordering = ['-pub_date']
        verbose_name_plural = 'entries'

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

class Link(models.Model):

    title = models.CharField(max_length=200)
    url = models.URLField(unique=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'links'
