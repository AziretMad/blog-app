from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext as _


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(
            PublishedManager, self
        ).get_queryset().filter(status=Post.PUBLISHED)


class Post(models.Model):
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = (
        (DRAFT, 'черновик'),
        (PUBLISHED, 'опубликовано')
    )
    title = models.CharField(_("Заголовок"), max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(
        User,
        verbose_name=_('Автор'),
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    body = models.TextField(_('Текст'))
    publish = models.DateTimeField(
        _('Дата и время публикации'), default=timezone.now
    )
    created = models.DateTimeField(_('Создано'), auto_now_add=True)
    updated = models.DateTimeField(_('Обновлено'), auto_now_add=True)
    status = models.CharField(
        _('Статус'), max_length=10, choices=STATUS_CHOICES, default=DRAFT
    )
    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)
        verbose_name = _('Пост')
        verbose_name_plural = _('Посты')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'blog:post_detail',
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug
            ]
        )
