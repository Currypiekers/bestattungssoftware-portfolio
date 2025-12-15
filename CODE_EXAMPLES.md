# Code-Beispiele für Portfolio

Diese Datei zeigt ausgewählte Code-Ausschnitte, die technische Kompetenz und Best Practices demonstrieren.

---

## 🏗️ Multi-Tenancy: Tenant-Middleware mit JWT

**Datei**: `app/users/middleware.py`

```python
from django.utils.deprecation import MiddlewareMixin
from django_tenants.utils import schema_context
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

class TenantMiddleware(MiddlewareMixin):
    """
    Custom Middleware: Extrahiert Tenant-Info aus JWT und setzt Schema-Context
    
    Problem: Bei JWT-Auth kennt Django nicht automatisch den Tenant
    Lösung: Token enthält company_id → Middleware setzt korrekten Schema-Context
    """
    def process_request(self, request):
        auth = JWTAuthentication()
        try:
            header = auth.get_header(request)
            if header is not None:
                raw_token = auth.get_raw_token(header)
                if raw_token is not None:
                    validated_token = auth.get_validated_token(raw_token)
                    user = auth.get_user(validated_token)

                    if user and hasattr(user, 'company') and user.company:
                        company_name = user.company.schema_name
                        with schema_context(company_name):
                            request.tenant = user.company
        except (InvalidToken, AuthenticationFailed) as e:
            print(f"Invalid token: {e}")
            pass
```

**Warum das wichtig ist:**
- Zeigt Verständnis für Multi-Tenancy-Architekturen
- Sichere Token-Verarbeitung mit Exception-Handling
- Integration von JWT mit Tenant-Schemas

---

## 📄 Dynamisches PDF-System: Platzhalter-Befüllung

**Datei**: `app/dokumente/api_views.py` (vereinfacht)

```python
from pdf_lib import PdfDocument
from dokumente.models import PlatzhalterInstance, Vorlage
from sterbefall.models import Sterbefall

class PDFForSterbefallDetailView(APIView):
    """
    Generiert PDF aus Vorlage + Platzhaltern + Sterbefall-Daten
    
    Flow:
    1. Vorlage laden
    2. Platzhalter-Positionen aus DB holen
    3. Sterbefall-Daten extrahieren
    4. PDF mit Daten befüllen
    5. Return als Download
    """
    def post(self, request, sterbefall_id, pk):
        vorlage = Vorlage.objects.get(pk=pk)
        sterbefall = Sterbefall.objects.get(uuid=sterbefall_id)
        platzhalter_instances = PlatzhalterInstance.objects.filter(
            pdf_template=vorlage
        ).select_related('platzhalter')
        
        # PDF laden
        pdf_doc = PdfDocument(vorlage.vorlage_datei.path)
        
        # Platzhalter befüllen
        for instance in platzhalter_instances:
            field_value = self.get_field_value(
                sterbefall, 
                instance.platzhalter.platzhalter_key
            )
            
            pdf_doc.add_text(
                text=field_value,
                page=instance.page_number,
                x=instance.x_position,
                y=instance.y_position,
                font_size=instance.font_size,
                bold=instance.bold
            )
        
        # PDF zurückgeben
        return pdf_doc.to_response(filename=f"Dokument_{sterbefall_id}.pdf")
    
    def get_field_value(self, sterbefall, field_key):
        """Extrahiert Wert aus Sterbefall-Modell anhand des Keys"""
        if hasattr(sterbefall, field_key):
            return getattr(sterbefall, field_key)
        return ""
```

**Technische Highlights:**
- Dynamische PDF-Generierung
- ORM-Optimierung mit `select_related`
- Flexible Field-Mapping
- Clean Code-Struktur

---

## 💰 Rechnungssystem: Automatische Nummerngenerierung

**Datei**: `app/rechnung/models.py`

```python
from django.db import models, transaction
from django.core.exceptions import ValidationError

class Rechnung(models.Model):
    STATUS_CHOICES = (
        ('ENTWURF', 'Entwurf'),
        ('OFFEN', 'Offen'),
        ('BEZAHLT', 'Bezahlt'),
        ('STORNIERT', 'Storniert'),
    )
    
    rechnungsnummer = models.CharField(max_length=200, editable=False, unique=True)
    rechnungsstufe = models.IntegerField(default=1)
    original_rechnung = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='korrektur_rechnungen'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    sterbefall = models.ForeignKey('sterbefall.Sterbefall', on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        """
        Automatische Rechnungsnummer-Generierung mit Race-Condition-Schutz
        
        Format: 
        - Erstrechnung: RE-2025-00001
        - Korrektur: RE-2025-00001-K2
        """
        if not self.rechnungsnummer:
            with transaction.atomic():
                if self.original_rechnung:
                    # Korrektur-Rechnung
                    stufe = self.original_rechnung.korrektur_rechnungen.count() + 1
                    self.rechnungsstufe = stufe
                    self.rechnungsnummer = f"{self.original_rechnung.rechnungsnummer}-K{stufe}"
                else:
                    # Neue Rechnung
                    year = timezone.now().year
                    last_rechnung = Rechnung.objects.filter(
                        rechnungsnummer__startswith=f'RE-{year}-'
                    ).order_by('-rechnungsnummer').first()
                    
                    if last_rechnung:
                        last_number = int(last_rechnung.rechnungsnummer.split('-')[2][:5])
                        new_number = last_number + 1
                    else:
                        new_number = 1
                    
                    self.rechnungsnummer = f'RE-{year}-{new_number:05d}'
        
        super().save(*args, **kwargs)
```

**Best Practices:**
- Transaction-Sicherheit gegen Race Conditions
- Selbst-Referenzierende Foreign Keys für Korrektur-Rechnungen
- Custom Save-Logic für Business-Requirements

---

## 🔐 JWT mit Tenant-Informationen

**Datei**: `app/users/serializers.py`

```python
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Erweitert Standard-JWT mit Tenant-Informationen
    
    Vorteil: Frontend kennt sofort den Tenant nach Login
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Custom Claims hinzufügen
        data.update({
            'user_id': self.user.id,
            'username': self.user.username,
            'role': getattr(self.user, 'role', None),
            'company_name': self.user.company.name if self.user.company else None,
            'company_id': self.user.company.id if self.user.company else None
        })
        return data
    
    @classmethod
    def get_token(cls, user):
        """Fügt Claims zum JWT hinzu"""
        token = super().get_token(user)
        token['username'] = user.username
        token['company_name'] = user.company.name if user.company else None
        return token
```

---

## ⚛️ React: API-Client mit Interceptor

**Datei**: `frontend/src/components/Api.jsx`

```javascript
import axios from 'axios';

/**
 * Zentrale Axios-Instanz mit JWT-Interceptor
 * 
 * Vorteile:
 * - DRY: Kein Token-Handling in jedem Request
 * - Zentrale Error-Behandlung
 * - Einfaches Token-Refresh (erweiterbar)
 */
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 10000,
});

// Request-Interceptor: JWT automatisch anhängen
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response-Interceptor: Globale Error-Behandlung
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token abgelaufen → Logout
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default api;
```

---

## 🧪 Django Signal: Auto-Auftragsnummern

**Datei**: `app/sterbefall/signals.py`

```python
from django.db.models.signals import pre_save
from django.dispatch import receiver
from sterbefall.models import Sterbefall

@receiver(pre_save, sender=Sterbefall)
def generate_auftragsnummer(sender, instance, **kwargs):
    """
    Signal: Generiert automatisch einzigartige Auftragsnummer
    
    Wird vor dem Speichern ausgeführt
    Format: Fortlaufende Nummer pro Tenant
    """
    if not instance.auftragsnummer:
        last_sterbefall = Sterbefall.objects.order_by('-auftragsnummer').first()
        
        if last_sterbefall and last_sterbefall.auftragsnummer:
            instance.auftragsnummer = last_sterbefall.auftragsnummer + 1
        else:
            instance.auftragsnummer = 1001  # Startnummer
```

---

## 📊 React: Custom Hook für API-Calls

**Datei**: `frontend/src/hooks/useApi.js`

```javascript
import { useState, useEffect } from 'react';
import api from '../components/Api';

/**
 * Custom Hook: Vereinfacht API-Calls mit Loading/Error-States
 * 
 * Verwendung:
 * const { data, loading, error } = useApi('/api/sterbefall/');
 */
export const useApi = (url, options = {}) => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await api.get(url, options);
        setData(response.data);
        setError(null);
      } catch (err) {
        setError(err.message);
        setData(null);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [url]); // Re-fetch bei URL-Änderung

  return { data, loading, error };
};
```

**React Best Practices:**
- Custom Hooks für wiederverwendbare Logic
- Proper Cleanup mit useEffect
- Type-Safe Error-Handling

---

## 🎯 Key Takeaways

Diese Code-Beispiele zeigen:
- ✅ **Multi-Tenancy**: Schema-basierte Datenisolierung
- ✅ **Security**: JWT, CSRF, Transaction-Safety
- ✅ **Clean Code**: DRY, Separation of Concerns
- ✅ **Modern React**: Hooks, Context, Interceptors
- ✅ **Business Logic**: Automatisierung, Validierung
- ✅ **Performance**: select_related, Indexing
