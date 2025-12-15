from django.db import models
from sterbefall.models import Sterbefall
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from django.contrib.postgres.fields import JSONField

class Rechnung(models.Model):
    STATUS_CHOICES = (
        ('ENTWURF', 'Entwurf'),
        ('OFFEN', 'Offen'),
        ('BEZAHLT', 'Bezahlt'),
        ('STORNIERT', 'Storniert'),
    )

    RECHNUNG_TYP_CHOICES = (
        ('RECHNUNG', 'Rechnung'),
        ('ANGEBOT', 'Angebot'),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ENTWURF'
    )
    rechnungsstufe = models.IntegerField(default=1)
    original_rechnung = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='korrektur_rechnungen'
    )
    rechnung_typ = models.CharField(
        max_length=10,
        choices=RECHNUNG_TYP_CHOICES,
        default='RECHNUNG'
    )
    is_standard = models.BooleanField(default=False)
    standard_name = models.CharField(max_length=200, blank=True, null=True)
    sterbefall = models.ForeignKey(Sterbefall, on_delete=models.CASCADE, null=True, blank=True)
    rechnungsdatum = models.DateField(null=True, blank=True)
    zahlungsziel = models.DateField(null=True, blank=True)
    betrag_summe = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=True, blank=True)
    rechnungsnummer = models.CharField(max_length=200, null=True, blank=True, editable=False)
    anrede = models.CharField(max_length=200, null=True, blank=True)
    titel = models.CharField(max_length=200, null=True, blank=True)
    auftraggerber_vorname = models.CharField(max_length=200, null=True, blank=True)
    auftraggeber_nachname = models.CharField(max_length=200, null=True, blank=True)
    strasse = models.CharField(max_length=200, null=True, blank=True)
    plz = models.CharField(max_length=200, null=True, blank=True)
    stadt = models.CharField(max_length=200, null=True, blank=True)
    land = models.CharField(max_length=200, null=True, blank=True)
    verstorbenen_vorname = models.CharField(max_length=200, null=True, blank=True)
    verstorbenen_nachname = models.CharField(max_length=200, null=True, blank=True)
    textblock = models.TextField(null=True, blank=True)
    is_geschrieben = models.BooleanField(default=False)
    protokoll = JSONField(null=True, blank=True, default=list)

    class Meta:
        app_label = 'rechnung'

    def save(self, *args, **kwargs):
        if self.status == 'OFFEN' and self.pk:
            original = Rechnung.objects.get(pk=self.pk)
            if original.status == 'ENTWURF' and self.status == 'OFFEN':
                self.rechnungsdatum = date.today()
                self.zahlungsziel = date.today() + timedelta(days=21)

        if self.status == 'BEZAHLT' and self.is_geschrieben:
            raise ValidationError("Eine bezahlte Rechnung kann nicht mehr bearbeitet werden.")

        if self._state.adding:
            if self.sterbefall:
                auftragsnummer = self.sterbefall.auftragsnummer
                rechnung_typ_prefix = "R" if self.rechnung_typ == "RECHNUNG" else "A"  # "R" für Rechnung, "A" für Angebot
                existing_rechnungen = Rechnung.objects.filter(
                    sterbefall=self.sterbefall,
                    rechnung_typ=self.rechnung_typ  # Filtern nach Rechnungstyp
                ).count()
                if existing_rechnungen == 0:
                    self.rechnungsnummer = f"{rechnung_typ_prefix}{auftragsnummer}"
                else:
                    self.rechnungsnummer = f"{rechnung_typ_prefix}{auftragsnummer}/{existing_rechnungen + 1}"

                if not self.anrede:
                    self.anrede = self.sterbefall.auftraggeber_anrede
                if not self.titel:
                    self.titel = self.sterbefall.auftraggeber_titel
                if not self.auftraggerber_vorname:
                    self.auftraggerber_vorname = self.sterbefall.auftraggeber_vorname
                if not self.auftraggeber_nachname:
                    self.auftraggeber_nachname = self.sterbefall.auftraggeber_nachname
                if not self.verstorbenen_vorname:
                    self.verstorbenen_vorname = self.sterbefall.verstorbener_vorname
                if not self.verstorbenen_nachname:
                    self.verstorbenen_nachname = self.sterbefall.verstorbener_nachname
                if not self.strasse:
                    self.strasse = self.sterbefall.auftraggeber_strasse
                if not self.plz:
                    self.plz = self.sterbefall.auftraggeber_plz
                if not self.stadt:
                    self.stadt = self.sterbefall.auftraggeber_stadt
                if not self.land:
                    self.land = self.sterbefall.auftraggeber_land

        super().save(*args, **kwargs)

class Rechnungsposition(models.Model):
    class Meta:
        app_label = 'rechnung'

    CATEGORIES = (
        ('EXP', 'Auslagen'),
        ('EXT', 'Fremdleistung'),
        ('OWN', 'Eigeneleistung'),
    )

    category = models.CharField(max_length=3, choices=CATEGORIES, null=True, blank=True)
    produkt = models.CharField(max_length=250, null=True, blank=True)
    rechnung = models.ForeignKey(Rechnung, on_delete=models.CASCADE)
    menge = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    preis = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    mwst = models.DecimalField(max_digits=2, decimal_places=0, null=True, blank=True)
    betrag = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Speichere die ursprüngliche Menge vor dem Speichern
        if self.pk:
            try:
                original = Rechnungsposition.objects.get(pk=self.pk)
                self._original_menge = original.menge
            except Rechnungsposition.DoesNotExist:
                self._original_menge = 0  # Oder einen anderen Standardwert
        else:
            self._original_menge = 0

        super().save(*args, **kwargs)