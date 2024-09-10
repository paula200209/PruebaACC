from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Q, Count
from .models import Movie, CountryCoordinates
from .serializers import MovieSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['titulo', 'calificacion', 'pais']
    ordering_fields = ['titulo', 'calificacion']
    ordering = ['titulo']

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('query', '')
        movies = Movie.objects.filter(
            Q(titulo__icontains=query) |
            Q(calificacion__icontains=query) |
            Q(pais__icontains=query)
        )
        serializer = self.get_serializer(movies, many=True)
        return Response({'success': True, 'data': serializer.data})

    @action(detail=False, methods=['get'])
    def summary(self, request):
        summary_data = Movie.objects.values('pais').annotate(count_pais=Count('pais'))
        ratings_data = Movie.objects.values('calificacion').annotate(
            count_calificacion_1=Count('id', filter=Q(calificacion=1)),
            count_calificacion_2=Count('id', filter=Q(calificacion=2)),
            count_calificacion_3=Count('id', filter=Q(calificacion=3)),
            count_calificacion_4=Count('id', filter=Q(calificacion=4)),
            count_calificacion_5=Count('id', filter=Q(calificacion=5))
        )
        return Response({
            'success': True,
            'data': {
                'count_pais': summary_data,
                'count_calificacion': ratings_data
            }
        })

    @action(detail=False, methods=['get'])
    def top(self, request):
        top_movies = Movie.objects.order_by('-calificacion')[:5]
        serializer = self.get_serializer(top_movies, many=True)
        return Response({'success': True, 'data': serializer.data})

    @action(detail=False, methods=['get'])
    def geojson(self, request):
        movies = Movie.objects.all()
        country_coords = {cc.country: (cc.longitude, cc.latitude) for cc in CountryCoordinates.objects.all()}

        features = [
            {
                "type": "Feature",
                "properties": {
                    "titulo": movie.titulo,
                    "calificacion": movie.calificacion,
                    "pais": movie.pais
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": country_coords.get(movie.pais, [None, None])
                }
            }
            for movie in movies
        ]
        return Response({
            "type": "FeatureCollection",
            "features": features
        })
