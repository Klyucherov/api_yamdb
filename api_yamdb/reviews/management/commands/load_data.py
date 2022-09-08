from csv import DictReader
from django.core.management import BaseCommand

from reviews.models import Review, Comment
from titles.models import Category, Genre, GenreTitle, Title
from users.models import User


CSV_MODELS = {
    Category: 'category.csv',
    Comment: 'comments.csv',
    Genre: 'genre.csv',
    GenreTitle: 'genre_title.csv',
    Review: 'review.csv',
    Title: 'titles.csv',
    User: 'users.csv'
}

class Command(BaseCommand):
    help = "Loads data from static/data/*.csv files"

    def handle(self, *args, **options):
        for model in CSV_MODELS.keys():
            model.objects.all().delete()

        for model, file in CSV_MODELS:
            for row in DictReader(
                open('static/data/'+ file, mode='r', encoding='utf-8')
            ):
                model.objects.get_or_create(**row)
        self.stdout.write(self.style.SUCCESS("Success!"))
