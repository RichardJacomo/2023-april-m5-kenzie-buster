from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from movies.serializers import MovieSerializer, MovieOrderSerializer
from movies.models import Movie
from movies.permissions import OnlyEmployee
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [OnlyEmployee]

    def post(self, request: Request):
        serializer = MovieSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user)
        return Response(serializer.data, status.HTTP_201_CREATED)
    
    def get(self, request: Request):
        movies = Movie.objects.all().order_by('id')
        result_page = self.paginate_queryset(movies, request, view=self)
        serializer = MovieSerializer(result_page, many=True)
        return self.get_paginated_response(serializer.data)


class MovieViewId(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [OnlyEmployee]
    
    def get(self, request: Request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        serializer = MovieSerializer(movie, many=False)
        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, movie_id):
        movie = get_object_or_404(Movie, pk=movie_id)
        movie.delete()
        return Response(None, status.HTTP_204_NO_CONTENT) 
    

class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = MovieOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user_id=request.user.id, movie_id=movie_id)
        return Response(serializer.data, status.HTTP_201_CREATED)