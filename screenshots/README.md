# Screenshot-Anleitung für Portfolio

## 📸 Zu erstellende Screenshots

### 1. **Dashboard** (`dashboard.png`)
**Was zeigen:**
- Gesamtübersicht mit Statistiken
- Quick-Actions (Neuer Sterbefall, etc.)
- Charts/Diagramme (Umsatz, offene Rechnungen)
- Navigation-Sidebar

**Tipps:**
- Beispieldaten verwenden (keine echten Namen)
- Vollbildmodus für saubere Darstellung
- Browser-DevTools: `Cmd + Shift + P` → "Screenshot" → "Capture full size screenshot"

---

### 2. **Sterbefall-Detail** (`sterbefall-detail.png`)
**Was zeigen:**
- Tabs (Auftraggeber, Verstorbener, Dokumente, Rechnungen)
- Formular-Felder mit Beispieldaten
- Action-Buttons (Bearbeiten, Dokumente generieren)

---

### 3. **PDF-Editor** (`pdf-editor.png`)
**Was zeigen:**
- PDF-Vorschau auf der linken Seite
- Platzhalter-Liste rechts
- Drag-&-Drop-Marker auf dem PDF
- Konfigurationsfelder (Font-Size, Position)

**Besonders wichtig:** Dies ist ein Unique-Feature!

---

### 4. **Rechnungen-Liste** (`rechnung-list.png`)
**Was zeigen:**
- DataGrid mit mehreren Rechnungen
- Filter-/Suchfunktion
- Status-Badges (Offen, Bezahlt, Entwurf)
- Action-Buttons (Bearbeiten, PDF, E-Mail)

---

### 5. **Rechnung erstellen** (`rechnung-create.png`)
**Was zeigen:**
- Formular für neue Rechnung
- Produktauswahl (Autocomplete)
- Positionsliste mit Preisen
- Summenberechnung

---

### 6. **Kalender** (`kalender.png`)
**Was zeigen:**
- FullCalendar mit Events
- Verschiedene Event-Typen (Termine, Aufgaben)
- Farb-Codierung
- Drag-&-Drop-Funktionalität (optional: GIF erstellen)

---

### 7. **Produktkatalog** (`produkte.png`)
**Was zeigen:**
- DataGrid mit Produkten
- Kategorien
- Preise und Lagerstände
- Such-/Filterfunktion

---

## 🎨 Screenshot-Best-Practices

### Vorbereitung
1. **Testdaten einfügen**:
   ```bash
   docker compose exec app python manage.py shell
   # Beispieldaten erstellen
   ```

2. **Browser-Fenster vorbereiten**:
   - Vollbild (F11 oder Fn + F)
   - Zoom: 100%
   - Keine persönlichen Bookmarks in der Leiste
   - Inkognito-Modus für saubere UI

3. **DevTools nutzen** (Chrome/Firefox):
   - `Cmd + Shift + P` (Mac) / `Ctrl + Shift + P` (Windows)
   - "Capture full size screenshot" eingeben
   - Speichert automatisch das komplette Layout

### Anonymisierung
- Keine echten Namen, E-Mails, Adressen
- Beispiele: "Max Mustermann", "test@example.com"
- Realistische, aber generische Daten

### Dateiformat
- **PNG** für hohe Qualität
- Optimierte Größe (max. 500-800 KB pro Bild)
- Tool: https://tinypng.com/ zum Komprimieren

---

## 🎬 Optional: Demo-Video/GIF

### Empfohlene Szenarien
1. **Sterbefall erstellen** (30 Sek.)
   - Navigation → Neuer Sterbefall → Formular ausfüllen → Speichern

2. **PDF-Platzhalter setzen** (45 Sek.)
   - PDF hochladen → Platzhalter per Drag & Drop setzen → Speichern → PDF generieren

3. **Rechnung erstellen** (30 Sek.)
   - Neuer Auftrag → Produkte hinzufügen → PDF generieren

### Tools
- **macOS**: QuickTime Player (Screenshot-Toolbar → "Bildschirmaufnahme")
- **Windows**: Xbox Game Bar (`Win + G`)
- **GIF erstellen**: https://www.screentogif.com/
- **Video schneiden**: https://www.kapwing.com/

---

## 📐 Empfohlene Auflösung

- **Desktop**: 1920x1080 (Full HD)
- **Responsive**: Zusätzlich 768px (Tablet) oder 375px (Mobile) zeigen
- **Crop**: Nur relevanten Bereich zeigen (keine Taskbar/Menubar)

---

## ✅ Checklist

- [ ] Dashboard-Screenshot
- [ ] Sterbefall-Detailansicht
- [ ] PDF-Editor mit Platzhaltern
- [ ] Rechnungsliste
- [ ] Rechnung-Erstellen-Formular
- [ ] Kalender mit Events
- [ ] Produktkatalog
- [ ] (Optional) Demo-GIF: Sterbefall erstellen
- [ ] (Optional) Demo-GIF: PDF-Platzhalter setzen
- [ ] Alle Bilder komprimiert (<500KB)
- [ ] Keine echten/persönlichen Daten
- [ ] README.md mit Screenshot-Links aktualisiert

---

## 🚀 Nach dem Upload

1. Screenshots in GitHub committen:
   ```bash
   git add screenshots/
   git commit -m "Add portfolio screenshots"
   git push
   ```

2. README-Links prüfen (GitHub zeigt Bilder automatisch an)

3. Optional: GitHub Pages aktivieren für Live-Readme-Vorschau
