# 📁 Repository Structure

```
bestattungssoftware-portfolio/
├── README.md                                  # Projekt-Übersicht & Features
├── CODE_EXAMPLES.md                           # Detaillierte Code-Erklärungen
├── STRUCTURE.md                               # Diese Datei
├── LICENSE                                    # MIT License
├── .gitignore                                 # Git-Ausschlüsse
│
├── screenshots/                               # UI Screenshots
│   ├── README.md                             # Screenshot-Übersicht
│   ├── dashboard.png                         # [Noch zu erstellen]
│   ├── sterbefall-detail.png                 # [Noch zu erstellen]
│   ├── pdf-editor.png                        # [Noch zu erstellen]
│   ├── rechnung-list.png                     # [Noch zu erstellen]
│   └── kalender.png                          # [Noch zu erstellen]
│
└── code-examples/                             # Ausgewählte Code-Beispiele
    ├── backend/                              # Django Backend
    │   ├── users_models.py                   # Tenant-Modell & CustomUser
    │   ├── users_middleware.py               # JWT + Tenant-Routing
    │   ├── users_serializers.py              # Custom JWT mit Tenant-Info
    │   ├── dokumente_models.py               # PDF-Vorlagen & Platzhalter
    │   ├── dokumente_api_views.py            # PDF-Generierung
    │   ├── rechnung_models.py                # Rechnungs-System
    │   ├── rechnung_api_views.py             # Rechnungs-API
    │   ├── sterbefall_models.py              # Sterbefall-Management
    │   └── sterbefall_api_views.py           # Sterbefall-API
    │
    ├── frontend/                             # React Frontend
    │   ├── Api.jsx                           # Axios mit JWT-Interceptor
    │   ├── Auth.jsx                          # Auth-Context
    │   └── package.json                      # Dependencies & Tech Stack
    │
    └── config/                               # Konfiguration
        ├── docker-compose.yml                # Docker Setup
        ├── settings_base.py                  # Django Settings
        ├── urls.py                           # URL-Routing
        └── requirements.txt                  # Python Dependencies
```

## 🔍 File-Übersicht

### Dokumentation
- **README.md**: Haupt-Dokumentation mit Features, Tech Stack und Setup-Anleitung
- **CODE_EXAMPLES.md**: Detaillierte Code-Erklärungen mit Kontext und Best Practices
- **STRUCTURE.md**: Diese Repository-Struktur-Übersicht

### Code-Beispiele
Alle Code-Files sind vollständige, funktionale Beispiele aus dem echten Projekt.

### Backend (Django)
9 Python-Files zeigen:
- Multi-Tenancy-Implementation mit django-tenant-schemas
- REST API-Design mit Django REST Framework
- JWT-Authentifizierung mit Tenant-Awareness
- Dynamisches PDF-System mit Platzhaltern
- Rechnungs-Management mit mehrstufigen Korrekturen
- Sterbefall-Verwaltung mit komplexer Business-Logic

### Frontend (React)
3 Files zeigen:
- API-Client mit JWT-Interceptors
- Authentication-Context-Management
- Tech Stack (React 18, Material-UI, FullCalendar, etc.)

### Konfiguration
4 Files zeigen:
- Docker-Setup für Development
- Django-Settings mit Multi-Tenancy
- URL-Routing-Struktur
- Python-Dependencies

## 📸 Screenshots

Screenshots zeigen die tatsächliche UI des Projekts.
**Hinweis**: Screenshots müssen noch erstellt und hinzugefügt werden.

## 🎯 Was dieses Repo zeigt

### Technische Fähigkeiten
- ✅ Full-Stack-Development (Django + React)
- ✅ Multi-Tenancy-Architektur
- ✅ RESTful API-Design
- ✅ JWT-Authentifizierung
- ✅ Complex Business Logic
- ✅ Docker-Containerisierung

### Code-Qualität
- ✅ Clean Code & DRY-Prinzip
- ✅ Proper Error Handling
- ✅ Security Best Practices
- ✅ Umfassende Dokumentation

### Projekt-Management
- ✅ Strukturierte Architektur
- ✅ Vollständige Dokumentation
- ✅ Production-Ready-Mindset
