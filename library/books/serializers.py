from rest_framework import serializers

from .models import *


class BooksDetailsSerializer(serializers.ModelSerializer):
    book_title = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    mime_type = serializers.SerializerMethodField()
    bookshelf = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    gid = serializers.SerializerMethodField()

    def get_book_title(self, obj):
        return obj.book.title

    def get_gid(self, obj):
        return obj.book.gutenberg_id
        
    def get_author(self, obj):
        return {
            "author_name": obj.author.name,
            'birth_year': obj.author.birth_year,
            'death_year': obj.author.death_year,
        }

    def get_genre(self, obj):
        sub_list = list(BooksBookSubjects.objects.filter(
            book=obj.book).values_list('subject__name', flat=True))
        genre_list = []
        for item in sub_list:
            split_item = item.split("--")
            if len(split_item) > 1:
                genre_list.append(split_item[-1].strip().lower())
            else:
                genre_list.append(split_item[0])
        return [item.capitalize() for item in list(set(genre_list))] if genre_list else []

    def get_language(self, obj):
        return list(BooksBookLanguages.objects.filter(
            book=obj.book).values_list('language__code', flat=True))

    def get_subject(self, obj):
        return list(BooksBookSubjects.objects.filter(
            book=obj.book).values_list('subject__name', flat=True))

    def get_bookshelf(self, obj):
        return list(BooksBookBookshelves.objects.filter(
            book=obj.book).values_list('bookshelf__name', flat=True))

    def get_mime_type(self, obj):
        qs = BooksFormat.objects.filter(book=obj.book)
        meme_types = [{'mime_type': item.mime_type, 'url': item.url} for item in qs]
        return meme_types

    class Meta:
        model = BooksBookAuthors
        fields = (
            'id','book_title', 'author', 'genre', 'language',
            'subject', 'bookshelf', 'mime_type', 'gid'
            )