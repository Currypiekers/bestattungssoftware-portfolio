from django.db import models
import uuid
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class Sterbefall(models.Model):
    class Meta:
        app_label = 'sterbefall'
    aufnahme_von = models.CharField(max_length= 250, null = True, blank=True)
    anlage_von = models.CharField(max_length= 250, null = True, blank=True)
    zuletzt_bearbeitet_von = models.CharField(max_length= 250, null = True, blank=True)
    auftragsnummer = models.IntegerField(unique=True, editable=False, null=True, blank=True)
    auftrags_datum = models.DateField(auto_now_add=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, blank=True)
    info = models.TextField(null=True, blank=True)
    auftraggeber_titel = models.CharField(max_length=17,  null= True, blank=True)
    auftraggeber_anrede = models.CharField(max_length=17, null= True, blank=True)
    auftraggeber_vorname = models.CharField(max_length= 200, null = True, blank=True)
    auftraggeber_nachname = models.CharField(max_length= 200, null = True, blank=True)
    auftraggeber_beziehungZumVerstorbenen = models.CharField( max_length=17, null= True, blank=True)
    auftraggeber_geburtsdatum = models.DateField( max_length= 250, null = True, blank=True)
    auftraggeber_strasse = models.CharField(max_length= 250, null = True, blank=True)
    auftraggeber_plz = models.CharField(max_length= 250, null = True, blank=True)
    auftraggeber_stadt = models.CharField(max_length= 250, null = True, blank=True)
    auftraggeber_land = models.CharField(max_length= 250, null = True, blank=True)

    auftraggeber_telefon = models.CharField(max_length= 250, null = True, blank=True)
    auftraggeber_mobil = models.CharField(max_length= 250, null = True, blank=True)
    auftraggeber_email = models.CharField(max_length= 250, null = True, blank=True)
    auftraggeber_familienstand= models.CharField(max_length=19,  null= True, blank=True)
    auftraggeber_rufname = models.CharField(max_length= 250, null = True, blank=True)
    auftraggeber_geburtsort = models.CharField(max_length= 250, null = True, blank=True)
    auftraggeber_beruf = models.CharField(max_length=250, null = True, blank=True)
    #Auftraggeber Bankverbindung
    auftraggeber_kontoinhaber = models.CharField(max_length=250, null = True, blank=True)
    auftraggeber_iban = models.CharField(max_length=250, null = True, blank=True)
    auftraggeber_bic = models.CharField(max_length=250, null = True, blank=True)
    auftraggeber_bank = models.CharField(max_length=250, null = True, blank=True)
    auftraggeber_aufnahmedatum = models.CharField(max_length=250, null = True, blank=True)
    auftraggeber_filiale = models.CharField(max_length=250, null = True, blank=True)

    #Verstrobener Table
    verstorbener_titel = models.CharField(max_length=17,  null= True, blank=True)
    verstorbener_anrede = models.CharField(max_length=17,  null= True, blank=True)
    verstorbener_vorname = models.CharField(max_length= 200, null = True, blank=True)
    verstorbener_nachname = models.CharField(max_length= 200,null = True, blank=True)
    verstorbener_familienstand= models.CharField(max_length=19,  null= True, blank=True)
    verstorbener_konfession = models.CharField(max_length= 200,  null = True, blank=True)
    verstorbener_geburtsdatum = models.DateField(max_length= 250, null = True, blank=True)
    verstorbener_geschlecht = models.CharField(max_length=17,  null= True, blank=True)
    verstorbener_geburtsname = models.CharField(max_length= 200,null = True, blank=True)
    verstorbener_standesamt = models.CharField(max_length= 250, null = True, blank=True)
    verstorbener_stattsangehörigkeit = models.CharField(default='deutsch', max_length= 250, null = True, blank=True)
    verstorbener_beziehungzumauftraggeber = models.CharField(max_length=17,  null= True, blank=True)
    verstorbener_geburtsort = models.CharField(max_length= 250, null = True, blank=True)
    verstorbener_strasse = models.CharField(max_length= 250, null = True, blank=True)
    verstorbener_plz = models.CharField(max_length= 250, null = True, blank=True)
    verstorbener_stadt = models.CharField(max_length= 250, null = True, blank=True)
    verstorbener_land = models.CharField( default='Deutschland', max_length= 250, null = True, blank=True)
    verstorbener_krankenkasse = models.CharField(max_length= 250, null = True, blank=True)
    verstorbener_versicherungsnummer = models.CharField(max_length= 250, null = True, blank=True)
    verstorbener_rentenversicherung = models.CharField(max_length= 250, null = True, blank=True)
    verstorbener_kanppschaftsnummer = models.CharField(max_length= 250, null = True, blank=True)
    verstorbener_betriebsrente = models.CharField(max_length= 250, null = True, blank=True)
    verstorbener_witwenrente = models.CharField(max_length= 250, null = True, blank=True)

    #Besttattungsort
    bestattung_institution = models.CharField(max_length= 250, null = True, blank=True)
    bestattungsort_strasse = models.CharField(max_length= 250, null = True, blank=True)
    bestattungsort_plz = models.CharField(max_length= 250, null = True, blank=True)
    bestattungsort_ort = models.CharField(max_length= 250, null = True, blank=True)
    bestattungsort_telefon = models.CharField(max_length= 250, null = True, blank=True)
    bestattungsort_garbart = models.CharField(max_length= 250, null = True, blank=True)
    
    #Grablage
    bestattungsart = models.CharField(max_length= 250, null = True, blank=True)
    ruhestätte = models.CharField(max_length= 250, null = True, blank=True)
    grabbezeichung1 = models.CharField(max_length= 250, null = True, blank=True)
    grabbezeichung2 = models.CharField(max_length= 250, null = True, blank=True)
    grabbezeichung3 = models.CharField(max_length= 250, null = True, blank=True)
    grabbezeichung4 = models.CharField(max_length= 250, null = True, blank=True)

    grablage1 = models.CharField(max_length= 250, null = True, blank=True)
    grablage2 = models.CharField(max_length= 250, null = True, blank=True)
    grablage3 = models.CharField(max_length= 250, null = True, blank=True)
    grablage4 = models.CharField(max_length= 250, null = True, blank=True)

    #Sterbedaten
    sterbedaten_institution = models.CharField(max_length= 250, null = True, blank=True)
    sterbedaten_strasse= models.CharField(max_length= 250, null = True, blank=True)
    sterbedaten_plz= models.CharField(max_length= 250, null = True, blank=True)
    sterbedaten_ort= models.CharField(max_length= 250, null = True, blank=True)
    sterbedaten_telefon = models.CharField(max_length= 250, null = True, blank=True)
    sterbedaten_standesamt = models.CharField(max_length= 250, null = True, blank=True)
    #sterbedaten_todeszeitpunkt
    sterbedaten_todeszeitpunkt = models.DateField(max_length= 250, null = True, blank=True)
    sterbedaten_zuletztlebendgesehen = models.DateField(max_length= 250, null = True, blank=True)
    sterbedaten_fundzeitpunkt = models.DateField(max_length= 250, null = True, blank=True)
    #sterbedaten_angaben zum tod
    sterbedaten_arzt = models.CharField(max_length= 250, null = True, blank=True)
    sterbedaten_aktenzeichen = models.CharField(max_length= 250, null = True, blank=True)
    sterbedaten_todesart = models.CharField(max_length= 250,  null = True, blank=True)
    sterbedaten_opduktion = models.CharField(max_length= 250, null = True, blank=True)
    abfahrt1= models.DateTimeField(max_length= 250, null = True, blank=True)
    von1 = models.CharField(max_length= 250, null = True, blank=True)
    nach1 = models.CharField(max_length= 250, null = True, blank=True)
    abfahrt2= models.DateTimeField(max_length= 250, null = True, blank=True)
    von2 = models.CharField(max_length= 250, null = True, blank=True)
    nach2 = models.CharField(max_length= 250, null = True, blank=True)

    #EhePartner
    partner_anrede= models.CharField(max_length=17,  null= True, blank=True)
    partner_titel= models.CharField(max_length=17,  null= True, blank=True)
    partner_vorname= models.CharField(max_length= 250, null = True, blank=True)
    partner_nachname= models.CharField(max_length= 250, null = True, blank=True)
    partner_geburtsname= models.CharField(max_length= 250, null = True, blank=True)
    partner_strasse= models.CharField(max_length= 250, null = True, blank=True)
    partner_plz= models.CharField(max_length= 250, null = True, blank=True)
    partner_ort= models.CharField(max_length= 250, null = True, blank=True)
    partner_land= models.CharField(max_length= 250, null = True, blank=True)
    partner_geschlecht= models.CharField(max_length=17,  null= True, blank=True)
    partner_telefon= models.CharField(max_length= 250, null = True, blank=True)
    partner_konfession= models.CharField(max_length= 250, null = True, blank=True)
    partner_mobil= models.CharField(max_length= 250, null = True, blank=True)
    partner_email= models.CharField(max_length= 250, null = True, blank=True)
    partner_geburtsdatum= models.DateField(max_length= 250, null = True, blank=True)
    partner_geburtsort= models.CharField(max_length= 250, null = True, blank=True)
    partner_geburtsstandesamt= models.CharField(max_length= 250, null = True, blank=True)
    partner_heiratsdatum= models.DateField(max_length= 250, null = True, blank=True)
    partner_heiratsort= models.CharField(max_length= 250, null = True, blank=True)
    partner_heistandesamt= models.CharField(max_length= 250, null = True, blank=True)
    partner_familienbuch= models.CharField(max_length= 250, null = True, blank=True)

    partner_sterbedatum= models.DateField(max_length= 250, null = True, blank=True)
    partner_sterbeort= models.CharField(max_length= 250, null = True, blank=True)
    partner_sterbestandesamt= models.CharField(max_length= 250, null = True, blank=True)

    # New field to trigger address synchronization
    synchronize_addresses = models.BooleanField(default=False, verbose_name="Synchronize Auftraggeber's address with Partner's address")
    synchronize_adresse = models.BooleanField(default=False, verbose_name="Synchronize Verstorbener mit Auftraggeber address")
    
    # Existing fields and methods continue...
    def save(self, *args, **kwargs):
        if self._state.adding:  # Nur beim ersten Speichern einer neuen Instanz
            current_year = datetime.now().year % 100  # z.B. 2024 -> 24
            last_order = Sterbefall.objects.filter(auftragsnummer__startswith=current_year).order_by('-auftragsnummer').first()

            if last_order:
                last_number = int(str(last_order.auftragsnummer)[2:])  # Extrahiere laufende Nummer
                new_number = last_number + 1
            else:
                new_number = 1  # Beginne jedes Jahr mit 001

            self.auftragsnummer = int(f"{current_year}{new_number:03d}")  # Format: YYNNN (24XXX)

        if self.synchronize_adresse:
            self.auftraggeber_strasse = self.verstorbener_strasse
            self.auftraggeber_plz = self.verstorbener_plz
            self.auftraggeber_stadt = self.verstorbener_stadt
            self.auftraggeber_land = self.verstorbener_land
        # Check if addresses should be synchronized
        if self.synchronize_addresses:
            self.partner_strasse = self.auftraggeber_strasse
            self.partner_plz = self.auftraggeber_plz
            self.partner_ort = self.auftraggeber_stadt
            self.partner_land = self.auftraggeber_land
        
        super().save(*args, **kwargs)

class SterbefallDokument(models.Model):
    sterbefall = models.ForeignKey(Sterbefall, on_delete=models.CASCADE, related_name='dokumente')
    name = models.CharField(max_length=250, null=True, blank=True)
    dokument = models.FileField(upload_to='sterbefall_dokumente/')
    hochgeladen_am = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'sterbefall'