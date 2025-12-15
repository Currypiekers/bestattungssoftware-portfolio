from rest_framework import viewsets
from .models import Vorlage, PlatzhalterInstance, EmailLog
from .serializers import VorlageSerializer, PlatzhalterInstanceSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from sterbefall.models import Sterbefall
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializers import EmailLogSerializer


class VorlageViewSet(viewsets.ModelViewSet):
    queryset = Vorlage.objects.all()
    serializer_class = VorlageSerializer
    

class PlatzhalterInstanceViewSet(viewsets.ModelViewSet):
    queryset = PlatzhalterInstance.objects.all()
    serializer_class = PlatzhalterInstanceSerializer

    

class PDFForSterbefallListView(APIView):
    
    def get(self, request, sterbefall_id, format=None):
        vorlagen = Vorlage.objects.all()
        serializer = VorlageSerializer(vorlagen, many=True)
        return Response(serializer.data)

class PDFForSterbefallDetailView(APIView):
    def get(self, request, sterbefall_id, pk, format=None):
        vorlage = get_object_or_404(Vorlage, pk=pk)
        if not vorlage.vorlage_datei:
            return Response({'error': 'Vorlage file is missing.'}, status=404)

        if not vorlage.vorlage_datei.url.endswith('.pdf'):
            return Response({'error': 'Invalid file format. Expected a PDF file.'}, status=400)

        platzhalter_instances = PlatzhalterInstance.objects.filter(pdf_template=vorlage)
        sterbefall = get_object_or_404(Sterbefall, pk=sterbefall_id)
        serializer = VorlageSerializer(vorlage)
        return Response({
            'vorlage': serializer.data,
            'platzhalter_instances': PlatzhalterInstanceSerializer(platzhalter_instances, many=True).data,
            'sterbefall': sterbefall.pk
        })

class EmailLogListView(generics.ListAPIView):
    serializer_class = EmailLogSerializer

    def get_queryset(self):
        """
        This view should return a list of all email logs
        for the document as determined by the document_name portion of the URL.
        """
        document_name = self.kwargs['document_name']
        return EmailLog.objects.filter(document_name=document_name)
