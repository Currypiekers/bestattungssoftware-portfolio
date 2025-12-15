from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Rechnung, Rechnungsposition
from django.core.cache import cache
from .serializers import RechnungspositionSerializer, RechnungSerializer, StandardRechnungSerializer
from rest_framework import viewsets, filters
from django.db import models
from rest_framework.decorators import action, api_view
from django.db.models import Case, When, Value, IntegerField
from datetime import date, timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone

class StandardRechnungViewSet(viewsets.ModelViewSet):
    queryset = Rechnung.objects.filter(is_standard=True)
    serializer_class = StandardRechnungSerializer

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {self.lookup_field: self.kwargs['pk']}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=True, methods=['post'])
    def add_standard_positions(self, request, pk=None):
        try:
            rechnung = Rechnung.objects.get(pk=pk)
            standard_rechnung_id = request.data.get('standard_rechnung_id')
            if not standard_rechnung_id:
                return Response({'error': 'Standard_rechnung_id is required'}, status=status.HTTP_400_BAD_REQUEST)

            standard_rechnung = Rechnung.objects.get(id=standard_rechnung_id, is_standard=True)
            positions = list(standard_rechnung.rechnungsposition_set.all())
            if not positions:
                return Response({'message': 'No positions available in the standard invoice'}, status=status.HTTP_204_NO_CONTENT)

            new_positions = []
            for position in positions:
                new_position = Rechnungsposition.objects.create(
                    category=position.category,
                    produkt=position.produkt,
                    menge=position.menge,
                    preis=position.preis,
                    mwst=position.mwst,
                    betrag=position.betrag,
                    rechnung=rechnung
                )
                new_positions.append(new_position)

            serializer = RechnungspositionSerializer(new_positions, many=True)
            return Response({'message': 'Positions added successfully', 'positions': serializer.data}, status=status.HTTP_201_CREATED)
        except Rechnung.DoesNotExist:
            return Response({'error': 'Rechnung does not exist'}, status=status.HTTP_404_NOT_FOUND)

class RechnungenForSterbefallView(APIView):
    def get(self, request, sterbefall_id, format=None):
        cache_key = f'rechnungen_for_sterbefall_{sterbefall_id}'
        rechnungen = cache.get(cache_key)
        if not rechnungen:
            rechnungen = Rechnung.objects.filter(sterbefall=sterbefall_id)
            cache.set(cache_key, rechnungen)
        serializer = RechnungSerializer(rechnungen, many=True)
        return Response(serializer.data)

class RechnungViewSet(viewsets.ModelViewSet):
    queryset = Rechnung.objects.all()
    serializer_class = RechnungSerializer

    def retrieve(self, request, sterbefall_id=None, rechnung_id=None, *args, **kwargs):
        instance = self.get_object()
        response = super().retrieve(request, *args, **kwargs)
        return response

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {self.lookup_field: self.kwargs['pk']}
        obj = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, pk=None, *args, **kwargs):
        rechnung = self.get_object()
        serializer = self.get_serializer(rechnung, data=request.data, partial=True)
        if serializer.is_valid():
            try:
                # Check if the status is being changed from "ENTWURF"
                if rechnung.status == 'ENTWURF' and serializer.validated_data.get('status') != 'ENTWURF':
                    serializer.validated_data['rechnungsdatum'] = date.today()
                    serializer.validated_data['zahlungsziel'] = date.today() + timedelta(days=21)

                serializer.save()
                self.log_event(rechnung, f'STATUS GEÄNDERT ZU {rechnung.status}')
                return Response(serializer.data)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, *args, **kwargs):
        rechnung = self.get_object()
        if rechnung.is_geschrieben:
            return Response(
                {"error": "Rechnung kann nicht mehr gelöscht werden, da sie bereits geschrieben ist."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def create_korrektur(self, request, pk=None):
        """Erstellt eine Korrekturrechnung."""
        original_rechnung = self.get_object()

        if original_rechnung.status == 'ENTWURF':
             return Response(
                {"error": "Rechnung muss zuerst Offen sein."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if original_rechnung.status in ['STORNIERT']:
            return Response(
                {"error": "Rechnung ist bereits Storniert."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Erstelle eine neue Rechnung mit Bezug zur Originalrechnung
        korrektur_rechnung = Rechnung.objects.create(
            sterbefall=original_rechnung.sterbefall,
            rechnungsdatum=original_rechnung.rechnungsdatum,
            anrede = original_rechnung.anrede,
            titel = original_rechnung.titel,
            auftraggerber_vorname = original_rechnung.auftraggerber_vorname,
            auftraggeber_nachname = original_rechnung.auftraggeber_nachname,
            strasse = original_rechnung.strasse,
            plz = original_rechnung.plz,
            stadt = original_rechnung.stadt,
            land = original_rechnung.land,
            verstorbenen_vorname = original_rechnung.verstorbenen_vorname,
            verstorbenen_nachname = original_rechnung.verstorbenen_nachname,
            textblock = original_rechnung.textblock,
            original_rechnung=original_rechnung,
            rechnungsstufe=original_rechnung.rechnungsstufe + 1,
        )

        # Kopiere Rechnungspositionen
        for position in original_rechnung.rechnungsposition_set.all():
            Rechnungsposition.objects.create(
                category=position.category,
                produkt=position.produkt,
                menge=position.menge,
                preis=position.preis,
                mwst=position.mwst,
                betrag=position.betrag,
                rechnung=korrektur_rechnung
            )

        serializer = self.get_serializer(korrektur_rechnung)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def add_standard_positions(self, request, pk=None):
        try:
            rechnung = Rechnung.objects.get(pk=pk)
            standard_rechnung_id = request.data.get('standard_rechnung_id')
            if not standard_rechnung_id:
                return Response({'error': 'Standard_rechnung_id is required'}, status=status.HTTP_400_BAD_REQUEST)

            standard_rechnung = Rechnung.objects.get(id=standard_rechnung_id, is_standard=True)
            positions = list(standard_rechnung.rechnungsposition_set.all())
            if not positions:
                return Response({'message': 'No positions available in the standard invoice'}, status=status.HTTP_204_NO_CONTENT)

            new_positions = []
            for position in positions:
                new_position = Rechnungsposition.objects.create(
                    category=position.category,
                    produkt=position.produkt,
                    menge=position.menge,
                    preis=position.preis,
                    mwst=position.mwst,
                    betrag=position.betrag,
                    rechnung=rechnung
                )
                new_positions.append(new_position)

            serializer = RechnungspositionSerializer(new_positions, many=True)
            return Response({'message': 'Positions added successfully', 'positions': serializer.data}, status=status.HTTP_201_CREATED)
        except Rechnung.DoesNotExist:
            return Response({'error': 'Rechnung does not exist'}, status=status.HTTP_404_NOT_FOUND)


    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        """Ändert den Status einer Rechnung."""
        rechnung = self.get_object()
        new_status = request.data.get('status')

        if not new_status or new_status not in [choice[0] for choice in Rechnung.STATUS_CHOICES]:
            return Response({"error": "Ungültiger Status."}, status=status.HTTP_400_BAD_REQUEST)

        allowed_transitions = {
            'ENTWURF': ['OFFEN', 'STORNIERT'],
            'OFFEN': ['BEZAHLT', 'STORNIERT'],
            'BEZAHLT': [],
            'STORNIERT': []
        }

        if new_status not in allowed_transitions.get(rechnung.status, []):
            return Response(
                {"error": f"Statusänderung von {rechnung.status} zu {new_status} ist nicht erlaubt."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if rechnung.status == 'ENTWURF' and new_status == 'OFFEN':
            rechnung.rechnungsdatum = date.today()
            rechnung.zahlungsziel = date.today() + timedelta(days=21)

        rechnung.status = new_status
        rechnung.save()
        self.log_event(rechnung, f'STATUS GEÄNDERT ZU {new_status}')
        serializer = self.get_serializer(rechnung)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def herunterladen(self, request, pk=None):
        """Protokolliert das Herunterladen der Rechnung."""
        rechnung = self.get_object()
        self.log_event(rechnung, 'HERUNTERGELADEN')
        serializer = self.get_serializer(rechnung)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def log_event(self, rechnung, event_type):
        user = self.request.user.username if self.request and self.request.user else 'System'
        event = {
            'timestamp': timezone.now().isoformat(),
            'event_type': event_type,
            'user': user,
        }
        rechnung.protokoll.append(event)
        rechnung.save()

class RechnungspositionViewSet(viewsets.ModelViewSet):
    serializer_class = RechnungspositionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['produkt']

    def get_queryset(self):
        rechnung_id = self.kwargs['rechnung_id']
        return Rechnungsposition.objects.filter(rechnung=rechnung_id)

    def list(self, request, sterbefall_id=None, rechnung_id=None):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, sterbefall_id=None, rechnung_id=None, pk=None):
        queryset = self.get_queryset()
        rechnungsposition = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(rechnungsposition)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, sterbefall_id=None, rechnung_id=None, pk=None):
        queryset = self.get_queryset()
        rechnungsposition = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(rechnungsposition, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, sterbefall_id=None, rechnung_id=None, pk=None):
        queryset = self.get_queryset()
        rechnungsposition = get_object_or_404(queryset, pk=pk)
        self.perform_destroy(rechnungsposition)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def rechnungsposition_category_summary(request, year=None):
    """
    Gibt eine Zusammenfassung der Rechnungspositionen nach Kategorie für ein gegebenes Jahr zurück.
    """
    if year is None:
        return Response({"error": "Year parameter is required."}, status=400)

    try:
        year = int(year)
    except ValueError:
        return Response({"error": "Invalid year format. Year must be an integer."}, status=400)

    # Filtere Rechnungspositionen nach Jahr (basierend auf Rechnungsdatum)
    rechnungspositionen = Rechnungsposition.objects.filter(
        rechnung__rechnungsdatum__year=year
    )

    # Aggregiere die Beträge nach Kategorie
    category_summary = rechnungspositionen.aggregate(
        total_exp=models.Sum(Case(
            When(category='EXP', then='betrag'),
            default=Value(0),
            output_field=models.DecimalField()
        )),
        total_ext=models.Sum(Case(
            When(category='EXT', then='betrag'),
            default=Value(0),
            output_field=models.DecimalField()
        )),
        total_own=models.Sum(Case(
            When(category='OWN', then='betrag'),
            default=Value(0),
            output_field=models.DecimalField()
        ))
    )

    # Formatiere die Daten für den BarChart
    data = [
        {'category': 'EXP', 'total_betrag': float(category_summary['total_exp'] or 0)},
        {'category': 'EXT', 'total_betrag': float(category_summary['total_ext'] or 0)},
        {'category': 'OWN', 'total_betrag': float(category_summary['total_own'] or 0)},
    ]

    return Response(data)