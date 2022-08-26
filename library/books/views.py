from django.db.models import Q

from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import *
from .serializers import *
from .pagination import CustomPageNumberPagination

# Class to handle books details listing.

class BooksDetailsListViewset(viewsets.ModelViewSet):
    queryset = BooksBookAuthors.objects.all()
    serializer_class = BooksDetailsSerializer
    pagination_class = CustomPageNumberPagination

    def list(self, request, *args, **kwargs):
        try:
            q = Q()
            limit = request.GET.get('limit')
            qs = self.get_queryset().order_by('-book__download_count')
            paginator = self.pagination_class()
            if limit:
                paginator.page_size = int(limit)
            authors = request.GET.get('authors')
            book_id = request.GET.get('book_id')
            mime_type = request.GET.get('mime_type')
            language = request.GET.get('language')
            topic = request.GET.get('topic')
            title = request.GET.get('title')
            if authors:
                for author in authors.split(','):
                    q = q| Q(author__name__icontains=author)
            if book_id:
                q = q| Q(book__gutenberg_id__in=book_id.split(','))
            if mime_type:
                for obj in mime_type.split(','):
                    q = q| Q(book__booksformat__mime_type__icointains=obj)
            if language:
                for lan in language.split(','):
                    q = q| Q(book__booksbooklanguages__language__code__iexact=lan)
            if topic:
                for obj in topic.split(','):
                    q = q| Q(book__booksbookbookshelves__bookshelf__name__icontains=obj) | Q(
                        book__booksbooksubjects__subject__name__icontains=obj)
            if title:
                for obj in title.split(','):
                    q = q| Q(book__title__icontains=obj)

            # final queryset after applying filters
            final_qs = qs.filter(q)
            result_page = paginator.paginate_queryset(final_qs, request)
            result_data = self.serializer_class(result_page, many=True).data
            data = {
                "message": "Successfully fetched Books list." if final_qs else "No results found.",
                "data": paginator.get_paginated_response(result_data).data,
            }
            status_code = status.HTTP_200_OK
        except Exception as e:
            print(e)
            data = {
                "message": "Error in fetching Books list.",
                "data": {},
            }
            status_code = status.HTTP_400_BAD_REQUEST
        return Response(data, status=status_code)