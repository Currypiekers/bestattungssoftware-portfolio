from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.db.models import Q
from .models import Sterbefall, SterbefallDokument
from .serializers import SterbefallSerializer, SterbefallDokumenteSerializer
from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

class SterbefallViewSet(ModelViewSet):
    queryset = Sterbefall.objects.all()
    serializer_class = SterbefallSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        year = self.request.query_params.get('year', None)
        if year:
            queryset = queryset.filter(sterbedaten_todeszeitpunkt__year=year)
        if search_query:
            queryset = queryset.filter(
                Q(auftraggeber_vorname__icontains=search_query) |
                Q(auftraggeber_nachname__icontains=search_query) |
                Q(verstorbener_vorname__icontains=search_query) |
                Q(verstorbener_nachname__icontains=search_query) |
                Q(auftragsnummer__icontains=search_query) |
                Q(
                    Q(auftraggeber_vorname__icontains=search_query.split(' ')[0]) & 
                    Q(auftraggeber_nachname__icontains=search_query.split(' ')[-1])
                ) |
                Q(
                    Q(verstorbener_vorname__icontains=search_query.split(' ')[0]) & 
                    Q(verstorbener_nachname__icontains=search_query.split(' ')[-1])
                )
            )
        return queryset.order_by('-auftragsnummer')

    @action(detail=False, methods=['get'])
    def dashboard_data(self, request):
        year = request.query_params.get('year', None)
        queryset = self.get_queryset()  # Use the existing queryset

        # Durchschnittsalter
        ages = [
            (case.sterbedaten_todeszeitpunkt - case.verstorbener_geburtsdatum).days // 365
            for case in queryset
            if case.sterbedaten_todeszeitpunkt and case.verstorbener_geburtsdatum
        ]
        average_age = sum(ages) / len(ages) if ages else None

        # Geschlechterverteilung
        gender_counts = queryset.values('verstorbener_geschlecht').annotate(count=Count('uuid')).order_by()
        gender_distribution = {
            (item['verstorbener_geschlecht'] or 'Nicht angegeben').strip(): item['count']
            for item in gender_counts
        }

        # Konfessionsverteilung
        konfession_counts = queryset.values('verstorbener_konfession').annotate(count=Count('uuid')).order_by()
        konfession_distribution = {
            (item['verstorbener_konfession'] or 'Nicht angegeben').strip(): item['count']
            for item in konfession_counts
        }

        # Bestattungsartverteilung
        burial_type_counts = queryset.values('bestattungsart').annotate(count=Count('uuid')).order_by()
        burial_type_distribution = {
            (item['bestattungsart'] or 'Nicht angegeben').strip(): item['count']
            for item in burial_type_counts
        }

        return Response({
            'average_age': average_age,
            'gender_distribution': gender_distribution,
            'konfession_distribution': konfession_distribution,
            'burial_type_distribution': burial_type_distribution,
        }, status=status.HTTP_200_OK)

class SterbefallDokumenteApiView(ModelViewSet):
    queryset = SterbefallDokument.objects.all()
    serializer_class = SterbefallDokumenteSerializer