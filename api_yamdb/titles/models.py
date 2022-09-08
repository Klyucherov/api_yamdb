from dataclasses import field
from django.db import models
from reviews.models import Review

import statistics

class Title(models.Model):

    def rating_value(self):
        scores_list = []
        reviews = Title.reviews.filter(pk=self.pk)
        if not reviews:
            return 'None'
        for review in reviews:
            scores_list.append(review.score)
        return statistics.mean(scores_list)

    rating = models.CharField(default=rating_value(), editable=False)