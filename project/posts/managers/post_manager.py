from django.db import models
from django.db.models.aggregates import Count


class PostQuerySet(models.QuerySet):
    def annotate_total_likes(self):
        return self.annotate(
            total_likes=Count('likes')
        )

    def annotate_total_comments(self):
        return self.annotate(
            total_comments=Count('comments')
        )

    def annotate_total_tags(self):
        return self.annotate(
            total_tags=Count('tags')
        )

    def annotate_total_shares(self):
        return self.annotate(
            total_shares=Count('shares')
        )


class PostManager(models.Manager):
    def get_queryset(self):
        return PostQuerySet(self.model, using=self._db)

    def published(self):
        """Return Published posts"""
        queryset = self.get_queryset().filter(
            is_published=True,
        ).exclude(
            models.Q(privacy=2) |  # PRIVATE
            models.Q(privacy=3)   # FRIENDS
        )
        return queryset

    def annotate_total_likes(self):
        return self.get_queryset().annotate_total_likes()

    def annotate_total_comments(self):
        return self.get_queryset().annotate_total_comments()

    def annotate_total_tags(self):
        return self.get_queryset().annotate_total_tags()

    def annotate_total_shares(self):
        return self.get_queryset().annotate_total_shares()
