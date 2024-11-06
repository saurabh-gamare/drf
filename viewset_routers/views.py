from rest_framework.decorators import action, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authentication import TokenAuthentication


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class BookViewSet2(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated] 

    # Custom action to get books by a specific author
    @action(detail=False, methods=['get'], url_path='by-author/{author}')
    def get_books_by_author(self, request, author=None):
        books = self.queryset.filter(author__iexact=author)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
    

class BookViewSet3(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Allow anyone to list books
    @permission_classes([AllowAny])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    # Only authenticated users can retrieve a specific book
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAuthenticated])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    # Only admin users can create, update, or delete books
    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAdminUser])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAdminUser])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @authentication_classes([TokenAuthentication])
    @permission_classes([IsAdminUser])
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class BookViewSet(viewsets.ViewSet):
    #In viewsets.ViewSet we have to manually add the methods like list, retrieve, create, etc.
    #But in viewsets.ModelViewSet we just need to add the queryset and serializer_class

    def list(self, request):
        # Your logic for listing books
        pass
    
    def retrieve(self, request, pk=None):
        # Your logic for retrieving a single book
        pass

    def create(self, request):
        # Your logic for creating a book
        pass
