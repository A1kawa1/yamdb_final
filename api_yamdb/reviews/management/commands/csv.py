import csv
import sqlite3

from django.core.management.base import BaseCommand
from reviews.models import Category, Comment, Genre, Review, Title
from user.models import User


class Command(BaseCommand):
    text = 'import data from cas file'

    def handle(self, *args, **options):
        with open('static/data/users.csv', encoding='utf-8') as File:
            reader = csv.DictReader(File)
            for row in reader:
                User.objects.get_or_create(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                )

        with open('static/data/category.csv', encoding='utf-8') as File:
            reader = csv.DictReader(File)
            for row in reader:
                Category.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )

        with open('static/data/titles.csv', encoding='utf-8') as File:
            reader = csv.DictReader(File)
            for row in reader:
                category = Category.objects.get(id=row['category'])
                Title.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category=category,
                )

        with open('static/data/review.csv', encoding='utf-8') as File:
            reader = csv.DictReader(File)
            for row in reader:
                user = User.objects.get(id=row['author'])
                Review.objects.get_or_create(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author=user,
                    score=row['score'],
                    pub_date=row['pub_date'],
                )

        with open('static/data/genre.csv', encoding='utf-8') as File:
            reader = csv.DictReader(File)
            for row in reader:
                Genre.objects.get_or_create(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug'],
                )

        with open('static/data/genre_title.csv', encoding='utf-8') as File:
            reader = csv.DictReader(File)
            con = sqlite3.connect('db.sqlite3')
            cur = con.cursor()
            for row in reader:
                cur.execute(
                    '''
                        INSERT INTO reviews_title_genre(id, title_id, genre_id)
                        VALUES (?, ?, ?);
                    ''',
                    (row['id'], row['title_id'], row['genre_id'])
                )
                con.commit()

        with open('static/data/comments.csv', encoding='utf-8') as File:
            reader = csv.DictReader(File)
            for row in reader:
                user = User.objects.get(id=row['author'])
                Comment.objects.get_or_create(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author=user,
                    pub_date=row['pub_date']
                )
