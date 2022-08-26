from django.db import models

#Classes related to various models associated with the app.
class BooksAuthor(models.Model):
    birth_year = models.SmallIntegerField(blank=True, null=True)
    death_year = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'books_author'
    
    def __str__(self):
        return self.name


class BooksBook(models.Model):
    download_count = models.IntegerField(blank=True, null=True)
    gutenberg_id = models.IntegerField(unique=True)
    media_type = models.CharField(max_length=16)
    title = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'books_book'

    def __str__(self):
        return self.title


class BooksBookAuthors(models.Model):
    book = models.ForeignKey(BooksBook, on_delete=models.CASCADE)
    author = models.ForeignKey(BooksAuthor, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'books_book_authors'
        unique_together = (('book', 'author'),)
    
    def __str__(self):
        return self.book.title + " ---- " + self.author.name 


class BooksBookBookshelves(models.Model):
    book = models.ForeignKey(BooksBook, on_delete=models.CASCADE)
    bookshelf = models.ForeignKey('BooksBookshelf', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'books_book_bookshelves'
        unique_together = (('book', 'bookshelf'),)

    def __str__(self):
        return self.book.title + " --- " + self.bookshelf.name

class BooksBookLanguages(models.Model):
    book = models.ForeignKey(BooksBook, on_delete=models.CASCADE)
    language = models.ForeignKey('BooksLanguage', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'books_book_languages'
        unique_together = (('book', 'language'),)

    def __str__(self):
        return self.book.title + " --- " + self.language.code


class BooksBookSubjects(models.Model):
    book = models.ForeignKey(BooksBook, on_delete=models.CASCADE)
    subject = models.ForeignKey('BooksSubject', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'books_book_subjects'
        unique_together = (('book', 'subject'),)
    
    def __str__(self):
        return self.book.title + " --- " + self.subject.name 


class BooksBookshelf(models.Model):
    name = models.CharField(unique=True, max_length=64)

    class Meta:
        managed = False
        db_table = 'books_bookshelf'

    def __str__(self):
        return self.name


class BooksFormat(models.Model):
    mime_type = models.CharField(max_length=32)
    url = models.CharField(max_length=256)
    book = models.ForeignKey(BooksBook, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'books_format'

    def __str__(self):
        return self.book.title + " --- " + self.mime_type 


class BooksLanguage(models.Model):
    code = models.CharField(unique=True, max_length=4)

    class Meta:
        managed = False
        db_table = 'books_language'

    def __str__(self):
        return self.code


class BooksSubject(models.Model):
    name = models.CharField(max_length=256)

    class Meta:
        managed = False
        db_table = 'books_subject'

    def __str__(self):
        return self.name


class State(models.Model):
    id = models.BigAutoField(primary_key=True)
    birth_year = models.IntegerField()
    death_year = models.IntegerField()
    name = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'state'

    def __str__(self):
        return self.name
