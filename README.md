# Bestattungssoftware - Multi-Tenant SaaS Platform

Eine vollständige **Multi-Tenant SaaS-Lösung** für Bestattungsunternehmen zur Verwaltung von Sterbefällen, Dokumenten, Rechnungen, Kontakten und Terminen. Die Anwendung nutzt **Django Tenant Schemas** für mandantenfähige Datenisolierung und eine moderne **React-Frontend-Architektur** mit Material-UI.

> **Hinweis**: Dieses Projekt ist ein Portfolio-Showcase und nicht öffentlich deployed. Screenshots und Code-Beispiele zeigen die Funktionalität.

---

## 📸 Screenshots & Demo

### Dashboard & Übersicht


![Dashboard]
<img width="1658" height="927" alt="Bildschirmfoto 2025-12-15 um 09 05 40" src="https://github.com/user-attachments/assets/ff261c3a-9b6c-4220-9321-39f59ffeeeba" />
*Haupt-Dashboard mit Analytics und Quick-Actions*

### Sterbefall-Verwaltung
![Sterbefall-Details]<img width="1676" height="925" alt="Bildschirmfoto 2025-12-15 um 10 02 58" src="https://github.com/user-attachments/assets/125a3acb-e29a-4166-8faf-542fa93a5da0" />
*Detailansicht eines Sterbefalls mit allen relevanten Informationen*

### Rechnungsverwaltung
![Rechnungen]<img width="1667" height="928" alt="Bildschirmfoto 2025-12-15 um 10 09 15" src="https://github.com/user-attachments/assets/cd617784-b857-43e6-bf12-e4bbc9e441c7" />
*Übersicht aller Rechnungen mit Filter- und Suchfunktion*


### Kalender & Termine
![Kalender]
<img width="1638" height="926" alt="Bildschirmfoto 2025-12-15 um 10 10 41" src="https://github.com/user-attachments/assets/3df103ca-b5b3-4d6b-b513-35aeceaf8796" />
<img width="1662" height="906" alt="Bildschirmfoto 2025-12-15 um 09 07 08" src="https://github.com/user-attachments/assets/d663f7ae-6527-40c2-b4e7-27c74401b1e1" />
*FullCalendar-Integration mit Terminen und Aufgaben*

### Produktkatalog
![Produkte]
<img width="1662" height="904" alt="Bildschirmfoto 2025-12-15 um 10 13 08" src="https://github.com/user-attachments/assets/aa0f7ad3-bccf-493c-9704-d03a70596d67" />
*Produktverwaltung mit Lagerhaltung*

---

## 🎯 Projektziel

Diese Software ermöglicht es mehreren Bestattungsunternehmen (Tenants), unabhängig voneinander ihre Geschäftsprozesse zu verwalten, während sie dieselbe Anwendungsinstanz nutzen. Jedes Unternehmen erhält eine eigene Subdomain und eine isolierte Datenbank (Schema), wodurch vollständige Datentrennung und Skalierbarkeit gewährleistet werden.

---

## 🏗️ Tech Stack

### Backend
- **Django 3.2** - Web Framework
- **Django REST Framework** - RESTful API
- **PostgreSQL 13** - Relationale Datenbank
- **django-tenant-schemas** - Multi-Tenancy-Architektur
- **JWT Authentication** (rest_framework_simplejwt) - Token-basierte Authentifizierung
- **dj-stripe** - Stripe-Integration für Zahlungen
- **Celery** (geplant) - Asynchrone Task-Verarbeitung
- **WhiteNoise** - Static File Serving
- **Docker & Docker Compose** - Containerisierung

### Frontend
- **React 18** - UI-Library
- **Material-UI (MUI)** - Component Library
- **Axios** - HTTP Client
- **React Router v6** - Client-seitiges Routing
- **FullCalendar** - Kalender-Integration
- **React Beautiful DnD** - Drag & Drop
- **Nivo Charts** - Datenvisualisierung
- **PDF.js & PDF-Lib** - PDF-Verarbeitung und -Anzeige
- **React-PDF** - PDF-Generierung

### DevOps & Tools
- **Docker & Docker Compose** - Development & Production
- **Git** - Versionskontrolle
- **PostgreSQL Backups** - Datenbanksicherung
- **Nginx** (Production) - Reverse Proxy

---

## 📦 Funktionalität & Module

### 1. **Multi-Tenancy (Django Tenant Schemas)**
Jeder Tenant (Bestattungsunternehmen) erhält:
- **Eigene Subdomain** (z.B. `unternehmen1.bestatter-app.de`)
- **Isoliertes Datenbankschema** (keine Datenvermischung)
- **Mandantenspezifische Konfigurationen** (Logo, Header/Footer-Texte, E-Mail-Einstellungen)
- **Skalierbar** für hunderte Tenants auf einer Instanz

#### Code-Ausschnitt: Tenant-Modell
```python
# app/users/models.py
from tenant_schemas.models import TenantMixin

class Company(TenantMixin):
    """
    Tenant-Modell: Jedes Unternehmen ist ein separater Tenant
    mit eigenem Schema und Domain
    """
    inhaber_vorname = models.CharField(max_length=100, null=True, blank=True)
    inhaber_nachname = models.CharField(max_length=100, null=True, blank=True)
    unternehmensname = models.CharField(max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to='company_logo/', null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    paid_until = models.DateField(null=True)
    on_trial = models.BooleanField(default=True)
    header_text = models.TextField(null=True, blank=True)
    footer_text = models.TextField(null=True, blank=True)
```

#### Settings-Konfiguration
```python
# app/settings/base.py
SHARED_APPS = [
    'tenant_schemas',
    'django.contrib.auth',
    'users',  # Tenant-Management
    'djstripe',  # Zahlungen
]

TENANT_APPS = [
    'produkte',
    'sterbefall',
    'dokumente',
    'rechnung',
    'kalender',
    'kontakte',
]

DATABASE_ROUTERS = [
    'tenant_schemas.routers.TenantSyncRouter',
]
```

---

### 2. **Sterbefall-Management**
Verwaltung von Sterbefällen mit umfangreichen Daten zu Verstorbenen und Auftraggebern.

**Features:**
- Automatische Auftragsnummern-Generierung
- Vollständige Erfassung von Auftraggeber- und Verstorbenendaten
- Status-Tracking (Aufnahme, Bearbeitung)
- Verknüpfung mit Dokumenten, Rechnungen und Terminen

#### Code-Ausschnitt: Sterbefall-Modell
```python
# app/sterbefall/models.py
class Sterbefall(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    auftragsnummer = models.IntegerField(unique=True, editable=False)
    auftrags_datum = models.DateField(auto_now_add=True)
    
    # Auftraggeber
    auftraggeber_vorname = models.CharField(max_length=200)
    auftraggeber_nachname = models.CharField(max_length=200)
    auftraggeber_email = models.CharField(max_length=250)
    
    # Verstorbener
    verstorbener_vorname = models.CharField(max_length=200)
    verstorbener_nachname = models.CharField(max_length=200)
    verstorbener_sterbedatum = models.DateField()
```

---

### 3. **Dynamisches Dokumenten-Management**
Erstellung von PDF-Dokumenten mit dynamischen Platzhaltern (z.B. Namen, Daten aus Sterbefällen).

**Features:**
- Upload von PDF-Vorlagen
- Drag-&-Drop-Platzierung von Platzhaltern im Frontend
- Automatische Befüllung mit Daten aus Sterbefällen
- Verkettung von Platzhaltern für mehrzeilige Texte
- E-Mail-Versand mit Protokollierung

#### Code-Ausschnitt: Platzhalter-System
```python
# app/dokumente/models.py
class PlatzhalterInstance(models.Model):
    """
    Repräsentiert einen Platzhalter an einer bestimmten Position
    in einem PDF-Template
    """
    pdf_template = models.ForeignKey(Vorlage, on_delete=models.CASCADE)
    platzhalter = models.ForeignKey(Platzhalter, on_delete=models.CASCADE)
    page_number = models.IntegerField()
    x_position = models.FloatField()
    y_position = models.FloatField()
    font_size = models.IntegerField(default=11)
    font_color = models.CharField(max_length=50, default='black')
    bold = models.BooleanField(default=False)
    chain_id = models.CharField(max_length=50, null=True)  # Verkettung
    chain_position = models.IntegerField(null=True)
```

---

### 4. **Rechnungs- & Produktverwaltung**
Vollständiges Rechnungssystem mit Produktkatalog und mehrstufigen Rechnungen.

**Features:**
- Angebote und Rechnungen erstellen
- Produktverwaltung mit Lagerhaltung
- Mehrstufige Rechnungen (Korrektur-Rechnungen)
- Status-Tracking (Entwurf, Offen, Bezahlt, Storniert)
- Automatische Rechnungsnummern-Generierung
- Standardrechnungen als Vorlagen

#### Code-Ausschnitt: Rechnungsmodell
```python
# app/rechnung/models.py
class Rechnung(models.Model):
    STATUS_CHOICES = (
        ('ENTWURF', 'Entwurf'),
        ('OFFEN', 'Offen'),
        ('BEZAHLT', 'Bezahlt'),
        ('STORNIERT', 'Storniert'),
    )
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    rechnungsstufe = models.IntegerField(default=1)
    original_rechnung = models.ForeignKey('self', on_delete=models.SET_NULL, 
                                         null=True, related_name='korrektur_rechnungen')
    sterbefall = models.ForeignKey(Sterbefall, on_delete=models.CASCADE)
    rechnungsnummer = models.CharField(max_length=200, editable=False)
    betrag_summe = models.DecimalField(max_digits=10, decimal_places=2)
    zahlungsziel = models.DateField(null=True, blank=True)
```

---

### 5. **Kalender & Aufgaben-Management**
FullCalendar-Integration zur Verwaltung von Terminen und Aufgaben.

**Features:**
- Haupttermine (z.B. Beerdigungen)
- Aufgabenverwaltung mit Fristen
- Vordefinierte Tasks für wiederkehrende Prozesse
- Drag-&-Drop-Unterstützung
- Farb-Codierung nach Status

---

### 6. **Kontaktverwaltung**
Zentrale Verwaltung von Kontakten (Bestatter, Ärzte, Friedhöfe, etc.).

---

### 7. **Benutzer- & Rechteverwaltung**
- **Multi-Tenant-fähige Benutzer**: Jeder Nutzer gehört zu einem Tenant
- **Rollen-System**: Admin, Mitarbeiter, etc.
- **JWT-Authentifizierung** mit Token-Blacklisting
- **Auto-Logout** bei Inaktivität

#### Code-Ausschnitt: JWT Token mit Tenant-Info
```python
# app/users/serializers.py
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Tenant-Informationen im Token
        data.update({
            'user_id': self.user.id,
            'username': self.user.username,
            'company_name': self.user.company.name if self.user.company else None,
            'company_id': self.user.company.id if self.user.company else None
        })
        return data
```

---

## 🎨 Frontend-Architektur

### React-Komponenten-Struktur
```
src/
├── components/
│   ├── Api.jsx              # Axios-Instanz mit JWT-Interceptor
│   ├── Auth.jsx             # Authentifizierungs-Context
│   ├── PdfViewer.tsx        # PDF-Anzeige und -Bearbeitung
│   ├── DatePickerField.jsx  # Wiederverwendbare Inputs
│   └── Charts/              # Nivo-Chart-Komponenten
├── scenes/
│   ├── sterbefall/          # Sterbefall-Verwaltung
│   ├── rechnung/            # Rechnungsverwaltung
│   ├── dokumente/           # Dokumenten-Editor
│   ├── kalender/            # FullCalendar-Integration
│   └── dashboard/           # Analytics & Übersichten
└── utils/
    └── api/                 # API-Helper-Funktionen
```

### API-Client mit Tenant-Awareness
```javascript
// frontend/src/components/Api.jsx
import axios from 'axios';

const api = axios.create();

api.interceptors.request.use(
  function (config) {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    return config;
  },
  function (error) {
    return Promise.reject(error);
  }
);

export default api;
```

---

## 🔐 Sicherheit

- **CSRF-Protection** auf allen POST/PUT/DELETE-Requests
- **JWT-Token-Blacklisting** bei Logout
- **Tenant-Isolation** auf Datenbankebene
- **Auto-Logout** bei Inaktivität
- **Environment-basierte Secrets** (.env-Dateien)
- **Password-Hashing** mit Django's PBKDF2

---

## 🚀 Deployment

### Docker-Compose Setup
```yaml
# docker-compose.yml
services:
  app:
    build: ./docker/app/dev
    depends_on:
      - postgres
    volumes:
      - ./app:/app
    env_file:
      - ./.envs/.dev/.app
      - ./.envs/.dev/.postgres
    ports:
      - "8000:8000"

  postgres:
    image: "postgres:13.1"
    volumes:
      - database:/var/lib/postgresql/data
    env_file:
      - ./.envs/.dev/.postgres
```

### Setup-Schritte
```bash
# 1. Repository klonen
git clone <repository-url>
cd coverM

# 2. Environment-Variablen konfigurieren
# Erstelle .envs/.dev/.app und .envs/.dev/.postgres

# 3. Container starten
docker compose up -d

# 4. Shared-Migrations ausführen
docker compose exec app python manage.py migrate_schemas --shared

# 5. Tenant erstellen
docker compose exec app python manage.py shell -c "
from users.models import Company
Company.objects.create(
    domain_url='unternehmen1.localhost',
    schema_name='unternehmen1',
    name='Mein Bestattungsunternehmen'
)"

# 6. Superuser erstellen
docker compose exec app python manage.py createsuperuser

# 7. Frontend starten
cd frontend
npm install
npm start
```

---

## 📊 Skalierbarkeit

### Tenant-Architektur
- **Horizontale Skalierung**: Neue Tenants können ohne Code-Änderungen hinzugefügt werden
- **Datenisolierung**: Jeder Tenant hat sein eigenes PostgreSQL-Schema
- **Shared Infrastructure**: Alle Tenants nutzen dieselbe Codebase
- **Performance**: Indizierung pro Schema, keine Cross-Tenant-Queries

### Performance-Optimierungen
- **Database-Indexing** auf häufig abgefragten Feldern
- **Query-Optimierung** mit `select_related` und `prefetch_related`
- **Static File Caching** mit WhiteNoise
- **JWT statt Sessions** für stateless Authentication

---

## 📈 Zukünftige Features

- [ ] **Celery** für asynchrone E-Mail-Versendung
- [ ] **Redis** für Caching und Session-Storage
- [ ] **Stripe-Integration** für Abonnement-Zahlungen
- [ ] **Elasticsearch** für erweiterte Suchfunktionen
- [ ] **PDF-Signatur** mit digitalen Zertifikaten
- [ ] **Mobile App** (React Native)
- [ ] **Reporting & Analytics** Dashboard

---

## 🛠️ Entwicklungs-Workflow

### Backend
```bash
# Django Shell
docker compose exec app python manage.py shell

# Migrations erstellen
docker compose exec app python manage.py makemigrations

# Tests ausführen
docker compose exec app python manage.py test

# Logs anzeigen
docker compose logs -f app
```

### Frontend
```bash
# Development Server
npm start

# Production Build
npm run build

# Tests
npm test
```

---

## 📝 Lizenz

Dieses Projekt ist für Portfolio-Zwecke erstellt und nicht unter Open-Source-Lizenz veröffentlicht.

---

## 👨‍💻 Kontakt

**Moritz Jessen**
- GitHub: [Dein GitHub-Profil]
- E-Mail: jessen.moritz@yahoo.de
- LinkedIn: [Dein LinkedIn-Profil]

---

## 🌟 Highlights für Recruiter

✅ **Multi-Tenancy** mit Django Tenant Schemas  
✅ **RESTful API** mit Django REST Framework  
✅ **JWT-Authentifizierung** mit Token-Blacklisting  
✅ **React 18** mit modernen Hooks und Context API  
✅ **Material-UI** für konsistentes Design  
✅ **Docker-Containerisierung** für einfaches Deployment  
✅ **PostgreSQL** mit komplexen Relationen und Constraints  
✅ **PDF-Verarbeitung** mit dynamischen Platzhaltern  
✅ **FullCalendar-Integration** für Terminverwaltung  
✅ **Stripe-Integration** für Zahlungen (in Entwicklung)

---

## 📁 Projekt-Struktur

```
coverM/
├── app/                          # Django Backend
│   ├── dokumente/               # Dokumentenverwaltung
│   │   ├── models.py           # PDF-Vorlagen, Platzhalter
│   │   ├── api_views.py        # REST API Endpoints
│   │   └── serializers.py      # DRF Serializers
│   ├── sterbefall/             # Sterbefall-Management
│   ├── rechnung/               # Rechnungssystem
│   ├── kalender/               # Terminverwaltung
│   ├── kontakte/               # Kontaktverwaltung
│   ├── produkte/               # Produktkatalog
│   ├── users/                  # User & Tenant Management
│   │   ├── models.py           # Company (Tenant), CustomUser
│   │   ├── middleware.py       # JWT & Tenant-Routing
│   │   └── serializers.py      # Auth & Token Logic
│   └── settings/
│       ├── base.py             # Shared Settings
│       └── dev.py              # Development Settings
├── frontend/                    # React Frontend
│   ├── src/
│   │   ├── components/         # Wiederverwendbare Komponenten
│   │   │   ├── Api.jsx         # Axios mit JWT-Interceptor
│   │   │   ├── PdfViewer.tsx   # PDF-Editor
│   │   │   └── Charts/         # Datenvisualisierung
│   │   ├── scenes/             # Haupt-Views
│   │   │   ├── dashboard/
│   │   │   ├── sterbefall/
│   │   │   ├── rechnung/
│   │   │   ├── dokumente/
│   │   │   └── kalender/
│   │   └── theme.js            # Material-UI Theme
│   └── package.json
├── docker/                      # Docker-Konfiguration
├── requirements/                # Python Dependencies
├── docker-compose.yml
└── README.md
```

---

## 💡 Best Practices & Code-Qualität

### Backend
- **DRY-Prinzip**: Wiederverwendbare Serializers und ViewSets
- **Type Hints**: Saubere Python-Typisierung
- **Migrations**: Strukturierte Datenbankmigrationen
- **Signals**: Event-driven Logic (z.B. automatische Auftragsnummern)
- **Custom Middleware**: Tenant-Routing und JWT-Handling

### Frontend
- **Component Composition**: Kleine, wiederverwendbare Komponenten
- **Custom Hooks**: Geteilte Business Logic
- **Error Handling**: Zentrales Error-Management
- **Performance**: Lazy Loading und Code-Splitting
- **Responsive Design**: Mobile-First-Ansatz mit MUI

### Testing (in Entwicklung)
- Unit Tests für kritische Business Logic
- Integration Tests für API-Endpoints
- E2E-Tests mit Cypress (geplant)
