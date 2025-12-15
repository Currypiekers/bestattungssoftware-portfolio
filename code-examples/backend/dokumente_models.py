from django.db import models
from platzhalter.models import Platzhalter



class Vorlage(models.Model):
    class Meta:
        app_label = 'dokumente'
    
    name = models.CharField(max_length=100)
    kategorie = models.CharField(max_length=100,  null= True, blank=True)
    vorlage_datei = models.FileField(upload_to='dokumente/')
    is_vorlage = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

    
class PlatzhalterInstance(models.Model):
    pdf_template = models.ForeignKey(Vorlage, on_delete=models.CASCADE)
    platzhalter = models.ForeignKey(Platzhalter, on_delete=models.CASCADE)
    page_number = models.IntegerField()
    x_position = models.FloatField()
    y_position = models.FloatField()
    name = models.CharField(max_length=255, null=True, blank=True)
    font_size = models.IntegerField(default=11)
    font_color = models.CharField(max_length=50, default='black')
    bold = models.BooleanField(default=False)
    chain_id = models.CharField(max_length=50, null=True, blank=True)  # Verkettungsfeld
    chain_position = models.IntegerField(null=True, blank=True)  # Position in der Kette
    # Add a method to update positions of chained placeholders
    def update_chained_positions(self):
        if not self.chain_id:
            return
        placeholders_in_chain = PlatzhalterInstance.objects.filter(chain_id=self.chain_id).order_by('chain_position')
        for index, placeholder in enumerate(placeholders_in_chain):
            if index == 0:
                continue  # Skip the first placeholder
            previous_placeholder = placeholders_in_chain[index - 1]
            placeholder.x_position = previous_placeholder.x_position + previous_placeholder.width + 10  # Adjust 10 for space
            placeholder.save()  

    def __str__(self):
        return f"{self.pdf_template.name} - {self.platzhalter.platzhalter_key}"


class EmailLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    recipient = models.EmailField()
    document_name = models.CharField(max_length=255)
    sterbefall = models.ForeignKey('sterbefall.Sterbefall', on_delete=models.CASCADE, null=True, blank=True)  # Assuming you want to link to Sterbefall
    vorlage = models.ForeignKey(Vorlage, on_delete=models.SET_NULL, null=True, blank=True)  # Link to the Vorlage
    success = models.BooleanField(default=True)  # Track if the email was successfully sent

    def __str__(self):
        return f"Email sent to {self.recipient} on {self.timestamp}"



