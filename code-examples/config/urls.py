from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from rest_framework_simplejwt.views import TokenObtainPairView
from users.serializers import CustomTokenObtainPairSerializer
from sterbefall.api_views import SterbefallViewSet, SterbefallDokumenteApiView
from produkte.api_views import ProduktSearchView, ProdukteViewSet
from rechnung.api_views import RechnungViewSet, RechnungspositionViewSet, StandardRechnungViewSet, RechnungenForSterbefallView, rechnungsposition_category_summary
from users.api_views import UserManagementViewSet, CompanyViewSet, EmailSettingsViewSet, send_email, BankAccountViewSet
from kontakte.api_views import KontakeViewSet
from dokumente.api_views import VorlageViewSet,  PlatzhalterInstanceViewSet,  PDFForSterbefallListView, PDFForSterbefallDetailView
from platzhalter.api_views import PlatzhalterViewSet
from kalender.api_views import HauptterminViewSet, AufgabeViewSet, PredefinedTaskViewSet
from dokumente import api_views as dokumente_api_views

router = routers.DefaultRouter()

router.register(r'sterbefall', SterbefallViewSet, basename='sterbefall')
router.register(r'sterbefalldokumente', SterbefallDokumenteApiView, basename='sterbefalldokumente')
router.register(r'standardrechnung', StandardRechnungViewSet , basename='standardrechnung')
router.register(r'rechnung', RechnungViewSet , basename='rechnung')
router.register(r'rechnungsposition', RechnungspositionViewSet , basename='rechnungsposition')
router.register(r'produkte', ProdukteViewSet , basename='produkte')
router.register(r'kontakte', KontakeViewSet, basename='kontakte')
router.register(r'users', UserManagementViewSet, basename='users')
router.register(r'company', CompanyViewSet, basename='company')
router.register(r'bankaccount', BankAccountViewSet, basename='bankaccount') # Registriere den ViewSet
router.register(r'emailsettings', EmailSettingsViewSet, basename='emailsettings') # Registriere den ViewSet
router.register(r'vorlage', VorlageViewSet, basename='vorlage')
router.register(r'platzhalterinstance', PlatzhalterInstanceViewSet, basename='platzhalterinstance')
router.register(r'platzhalter', PlatzhalterViewSet, basename='platzhalter')
router.register(r'haupttermin', HauptterminViewSet, basename='haupttermin')
router.register(r'aufgabe', AufgabeViewSet, basename='aufgabe')
router.register(r'predefinedtask', PredefinedTaskViewSet, basename='predefinedtask')


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='token_obtain_pair'),
    path('api/', include(router.urls)),

    path('api/send_email/', send_email, name='send_email'),

    #Rechnungsposition im Auftrag hinzufügen
    path('api/sterbefall/<uuid:sterbefall_id>/rechnung/', RechnungenForSterbefallView.as_view(), name='sterbefall-rechnungen'),
    path('api/sterbefall/<uuid:sterbefall_id>/rechnung/<int:rechnung_id>/', RechnungspositionViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'}), name='rechnungsp'),
    path('api/sterbefall/<uuid:sterbefall_id>/rechnung/<int:rechnung_id>/<int:pk>/', RechnungspositionViewSet.as_view({'get': 'retrieve', 'post': 'create','put': 'update', 'delete': 'destroy'}), name='rechnungspositionen'),
    #Rechnungsposition einer Standardrechnung hinzufügen
    path('api/standardrechnung/rechnung/<int:rechnung_id>/', RechnungspositionViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'}), name='standardrechnungsp'),
    path('api/standardrechnung/rechnung/<int:rechnung_id>/<int:pk>/', RechnungspositionViewSet.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='standardrechnungspositionen'),

    #produkt zur rechnungsposition Hinzufügen
    path('api/sterbefall/<uuid:sterbefall_id>/rechnung/<int:rechnung_id>/<int:pk>/update_product/', RechnungspositionViewSet.as_view({'post': 'update_product'}), name='update_product'),
    
    #Standardrechnung zur Rechnung hinzufügen
    path('api/rechnungen/<int:pk>/add_standard_positions/', RechnungViewSet.as_view({
        'post': 'add_standard_positions', 'get': 'retrieve', 
    }), name='add_standard_positions'),

    path('api/rechnungspositionen/category_summary/<int:year>/', rechnungsposition_category_summary, name='rechnungsposition_category_summary'),
    
    #pdf für sterbefall
    path('api/sterbefall/<uuid:sterbefall_id>/pdfs/', PDFForSterbefallListView.as_view(), name='sterbefall-pdfs'),
    path('api/sterbefall/<uuid:sterbefall_id>/pdfs/<int:pk>/', PDFForSterbefallDetailView.as_view(), name='replace-placeholders'),
    path('api/produkt_search/', ProduktSearchView.as_view(), name='produkt_search'),

    path('api/emaillogs/<str:document_name>/', dokumente_api_views.EmailLogListView.as_view(), name='email-log-list'),

    path(
        route='stripe/',
        view=include(
            "djstripe.urls",
            namespace="djstripe"
        ),
    ),

    path(
        route='auth/',
        view=include('allauth.urls')
    ),

    path(
        route='admin/',
        view=admin.site.urls,
    ),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)